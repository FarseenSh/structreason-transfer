"""
Generate 5 formats for each of 250 sub-tables:
  A: Markdown table
  B: Chart image (matplotlib PNG)
  B': Chart text-description (length-matched to A ±20%)
  C: Graph (entity-relationship edge list)
  D: Time series (unlabeled numerical array)
"""

import json
import os
import random
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import tiktoken
from pathlib import Path

SEED = 42
random.seed(SEED)
np.random.seed(SEED)

BASE_DIR = Path(__file__).resolve().parent.parent.parent
SUBTABLE_DIR = BASE_DIR / "data" / "subtables"
FORMAT_DIR = BASE_DIR / "data" / "formats"
for sub in ["table", "chart_image", "chart_text", "graph", "timeseries"]:
    (FORMAT_DIR / sub).mkdir(parents=True, exist_ok=True)

ENC = tiktoken.get_encoding("cl100k_base")


def count_tokens(text):
    return len(ENC.encode(text))


def load_subtable(path):
    with open(path) as f:
        st = json.load(f)
    df = pd.DataFrame(st["data"])
    return st, df


# === FORMAT A: Markdown Table ===

def generate_table(st, df):
    """Generate Markdown table string."""
    lines = ["| " + " | ".join(str(c) for c in df.columns) + " |"]
    lines.append("|" + "|".join(["---"] * len(df.columns)) + "|")
    for _, row in df.iterrows():
        vals = []
        for v in row:
            if isinstance(v, float):
                if v == int(v):
                    vals.append(str(int(v)))
                else:
                    vals.append(f"{v:.1f}")
            else:
                vals.append(str(v))
        lines.append("| " + " | ".join(vals) + " |")
    return "\n".join(lines)


# === FORMAT B: Chart Image ===

def _select_chart_type(st, df):
    """Select appropriate chart type based on data structure."""
    index_col = st["index_col"]
    metric_cols = st["metric_cols"]
    n_rows = len(df)

    # Check if index looks temporal
    temporal_keywords = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug",
                         "Sep", "Oct", "Nov", "Dec", "Q1", "Q2", "Q3", "Q4",
                         "2005", "2006", "2007", "2008", "2009", "2010", "2011",
                         "2012", "2013", "2014", "2015", "2016", "2017", "2018",
                         "2019", "2020", "2021", "2022", "2023"]
    is_temporal = any(str(v) in temporal_keywords for v in df[index_col].values[:3])

    if is_temporal and len(metric_cols) <= 4:
        return "line"
    elif n_rows <= 8 and len(metric_cols) <= 3:
        return "bar"
    elif len(metric_cols) == 2:
        return "scatter"
    else:
        return "bar"


def generate_chart_image(st, df, out_path):
    """Generate matplotlib PNG chart."""
    chart_type = _select_chart_type(st, df)
    index_col = st["index_col"]
    metric_cols = st["metric_cols"]

    fig, ax = plt.subplots(figsize=(8, 6))
    title = f"{st['dataset']} — {st['domain'].replace('_', ' ').title()}"

    x_labels = [str(v) for v in df[index_col].values]

    if chart_type == "line":
        for m in metric_cols:
            ax.plot(x_labels, df[m].values, marker='o', label=m, linewidth=1.5)
        ax.set_xlabel(index_col)
        ax.legend(fontsize=8)

    elif chart_type == "bar":
        x = np.arange(len(x_labels))
        width = 0.8 / max(len(metric_cols), 1)
        for i, m in enumerate(metric_cols):
            offset = (i - len(metric_cols)/2 + 0.5) * width
            ax.bar(x + offset, df[m].values, width, label=m)
        ax.set_xticks(x)
        ax.set_xticklabels(x_labels, rotation=45 if len(x_labels) > 6 else 0,
                           ha='right' if len(x_labels) > 6 else 'center', fontsize=7)
        ax.legend(fontsize=8)

    elif chart_type == "scatter":
        if len(metric_cols) >= 2:
            ax.scatter(df[metric_cols[0]], df[metric_cols[1]], alpha=0.7, s=40)
            for i, label in enumerate(x_labels):
                ax.annotate(label, (df[metric_cols[0]].iloc[i], df[metric_cols[1]].iloc[i]),
                           fontsize=6, alpha=0.7)
            ax.set_xlabel(metric_cols[0])
            ax.set_ylabel(metric_cols[1])

    ax.set_title(title, fontsize=10)
    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches='tight')
    plt.close(fig)
    return chart_type


# === FORMAT B': Chart Text-Description (length-matched) ===

def generate_chart_text(st, df, chart_type, table_tokens):
    """
    Generate text description of the chart.
    Length-matched to Format A (table) ±20%.
    """
    index_col = st["index_col"]
    metric_cols = st["metric_cols"]
    x_labels = [str(v) for v in df[index_col].values]

    chart_type_name = {"line": "Line chart", "bar": "Bar chart", "scatter": "Scatter plot"}
    title = f"{st['dataset']} — {st['domain'].replace('_', ' ').title()}"

    parts = [f'{chart_type_name.get(chart_type, "Chart")}: "{title}".']

    # Add data points per metric
    for m in metric_cols:
        values = df[m].values
        pairs = []
        for label, val in zip(x_labels, values):
            if isinstance(val, float) and val == int(val):
                pairs.append(f"{label}={int(val)}")
            else:
                pairs.append(f"{label}={val:.1f}" if isinstance(val, float) else f"{label}={val}")
        parts.append(f"{m}: {', '.join(pairs)}.")

    text = "\n".join(parts)

    # Length control: cap to ±20% of table token count
    target_min = int(table_tokens * 0.8)
    target_max = int(table_tokens * 1.2)
    current_tokens = count_tokens(text)

    # Iteratively reduce data points until within ±20% of table tokens
    if current_tokens > target_max:
        for fraction in [0.75, 0.6, 0.5, 0.4, 0.33]:
            parts = [f'{chart_type_name.get(chart_type, "Chart")}: "{title}".']
            n_points = max(3, int(len(x_labels) * fraction))
            indices = np.linspace(0, len(x_labels)-1, n_points, dtype=int)
            for m in metric_cols:
                values = df[m].values
                pairs = []
                for idx in indices:
                    label = x_labels[idx]
                    val = values[idx]
                    if isinstance(val, float) and val == int(val):
                        pairs.append(f"{label}={int(val)}")
                    else:
                        pairs.append(f"{label}={val:.1f}" if isinstance(val, float) else f"{label}={val}")
                parts.append(f"{m}: {', '.join(pairs)}.")
            text = "\n".join(parts)
            if count_tokens(text) <= target_max:
                break

    return text


# === FORMAT C: Graph (Entity-Relationship) ===

def generate_graph(st, df):
    """
    Generate entity-relationship graph.
    NOT temporal chaining — cross-entity relationships based on metric similarity.
    Compact format: node attributes as comma-separated key=value pairs,
    limited to top-K edges to keep token count reasonable.
    """
    index_col = st["index_col"]
    metric_cols = st["metric_cols"]
    entities = df[index_col].values

    def fmt_val(v):
        if isinstance(v, float) and v == int(v):
            return str(int(v))
        return f"{v:.1f}" if isinstance(v, float) else str(v)

    # Build node attributes — compact key=value format
    lines = [f"Graph: {st['dataset']} entity relationship network\n"]
    lines.append("Nodes:")
    for _, row in df.iterrows():
        attrs = ", ".join(f"{m}={fmt_val(row[m])}" for m in metric_cols)
        lines.append(f"  {row[index_col]}: {{{attrs}}}")

    # Compute pairwise similarity and keep top edges
    if len(metric_cols) > 0 and len(entities) > 1:
        metric_matrix = df[metric_cols].values.astype(float)
        norms = np.linalg.norm(metric_matrix, axis=1, keepdims=True)
        norms[norms == 0] = 1
        normalized = metric_matrix / norms

        # Collect all pair similarities
        all_sims = []
        for i in range(len(entities)):
            for j in range(i+1, len(entities)):
                sim = float(np.dot(normalized[i], normalized[j]))
                all_sims.append((sim, i, j))
        all_sims.sort(reverse=True)

        # Keep top-K edges: min(N, max(3, N_entities//2)) to bound length
        max_edges = min(len(all_sims), max(3, len(entities) // 2))
        top_edges = all_sims[:max_edges]

        lines.append(f"\nEdges (top {max_edges} by metric similarity):")
        for sim, i, j in top_edges:
            diffs = np.abs(metric_matrix[i] - metric_matrix[j])
            most_similar_idx = np.argmin(diffs)
            reason = f"similar {metric_cols[most_similar_idx]}"
            lines.append(f"  {entities[i]} -- {entities[j]} (sim={sim:.2f}, {reason})")

    return "\n".join(lines)


# === FORMAT D: Time Series (Unlabeled Array) ===

def generate_timeseries(st, df):
    """
    Generate unlabeled numerical array.
    Forces positional reasoning — no per-value labels.
    """
    index_col = st["index_col"]
    metric_cols = st["metric_cols"]
    x_labels = [str(v) for v in df[index_col].values]

    parts = []
    for m in metric_cols:
        values = df[m].values
        formatted = []
        for v in values:
            if isinstance(v, float) and v == int(v):
                formatted.append(str(int(v)))
            else:
                formatted.append(f"{v:.1f}" if isinstance(v, float) else str(v))
        header = f"The following {len(values)} values represent {m} for each {index_col} ({', '.join(x_labels)}), listed in order:"
        parts.append(f"{header}\n[{', '.join(formatted)}]")

    return "\n\n".join(parts)


# === MAIN ===

def generate_all_formats():
    """Generate all 5 formats for all 250 sub-tables."""
    subtable_files = sorted(SUBTABLE_DIR.glob("*.json"))
    print(f"Found {len(subtable_files)} sub-tables")

    token_stats = {fmt: [] for fmt in ["table", "chart_text", "graph", "timeseries"]}
    format_metadata = []

    for path in subtable_files:
        st, df = load_subtable(path)
        sub_id = st["id"]

        # Format A: Table
        table_text = generate_table(st, df)
        table_tokens = count_tokens(table_text)
        (FORMAT_DIR / "table" / f"{sub_id}.txt").write_text(table_text)
        token_stats["table"].append(table_tokens)

        # Format B: Chart Image
        chart_path = FORMAT_DIR / "chart_image" / f"{sub_id}.png"
        chart_type = generate_chart_image(st, df, chart_path)

        # Format B': Chart Text-Description (length-matched to A)
        chart_text = generate_chart_text(st, df, chart_type, table_tokens)
        chart_text_tokens = count_tokens(chart_text)
        (FORMAT_DIR / "chart_text" / f"{sub_id}.txt").write_text(chart_text)
        token_stats["chart_text"].append(chart_text_tokens)

        # Format C: Graph
        graph_text = generate_graph(st, df)
        graph_tokens = count_tokens(graph_text)
        (FORMAT_DIR / "graph" / f"{sub_id}.txt").write_text(graph_text)
        token_stats["graph"].append(graph_tokens)

        # Format D: Time Series
        ts_text = generate_timeseries(st, df)
        ts_tokens = count_tokens(ts_text)
        (FORMAT_DIR / "timeseries" / f"{sub_id}.txt").write_text(ts_text)
        token_stats["timeseries"].append(ts_tokens)

        format_metadata.append({
            "id": sub_id,
            "chart_type": chart_type,
            "tokens": {
                "table": table_tokens,
                "chart_text": chart_text_tokens,
                "graph": graph_tokens,
                "timeseries": ts_tokens,
            }
        })

    # Save metadata
    with open(FORMAT_DIR / "format_metadata.json", 'w') as f:
        json.dump(format_metadata, f, indent=2)

    # Report token statistics
    print(f"\n{'='*60}")
    print("TOKEN COUNT REPORT (cl100k_base)")
    print(f"{'='*60}")
    print(f"{'Format':<20} {'Median':>8} {'Mean':>8} {'Min':>6} {'Max':>6}")
    print(f"{'-'*60}")
    for fmt, tokens in token_stats.items():
        arr = np.array(tokens)
        print(f"{fmt:<20} {np.median(arr):>8.0f} {np.mean(arr):>8.1f} {np.min(arr):>6} {np.max(arr):>6}")

    # Check length matching (B' vs A)
    table_arr = np.array(token_stats["table"])
    ct_arr = np.array(token_stats["chart_text"])
    ratios = ct_arr / table_arr
    within_20 = np.sum((ratios >= 0.8) & (ratios <= 1.2))
    print(f"\nB'/A length match: {within_20}/{len(ratios)} within ±20% ({within_20/len(ratios)*100:.1f}%)")
    print(f"B'/A ratio — median: {np.median(ratios):.2f}, mean: {np.mean(ratios):.2f}")

    # Check >2x token difference flag
    for fmt_name, fmt_tokens in token_stats.items():
        for other_name, other_tokens in token_stats.items():
            if fmt_name < other_name:
                ratio = np.median(fmt_tokens) / np.median(other_tokens)
                if ratio > 2.0 or ratio < 0.5:
                    print(f"  ⚠ {fmt_name} vs {other_name}: median ratio = {ratio:.2f} (>2x difference)")

    return format_metadata


if __name__ == "__main__":
    generate_all_formats()
