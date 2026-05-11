"""
Step 1: Statistical analysis for StructReason-Transfer.
Computes tetrachoric correlations, phi coefficients, Kendall tau-b,
bootstrap CIs, and all ablation analyses.

Uses ordinalcorr 0.6.1 (NOT scipy) for tetrachoric correlation.
"""

import json
import numpy as np
import pandas as pd
from pathlib import Path
from collections import defaultdict
from ordinalcorr import tetrachoric
from scipy import stats
import warnings
import sys

sys.stdout.reconfigure(line_buffering=True)

SEED = 42
np.random.seed(SEED)

BASE_DIR = Path(__file__).resolve().parent.parent.parent
RESULTS_DIR = BASE_DIR / "experiments" / "results"
QUESTION_FILE = BASE_DIR / "experiments" / "data" / "questions" / "questions.jsonl"
FORMAT_META = BASE_DIR / "experiments" / "data" / "formats" / "format_metadata.json"

TEXT_FORMATS = ["table", "chart_text", "graph", "timeseries"]
ALL_FORMATS = ["table", "chart_text", "graph", "timeseries", "chart_image"]

# Model registry: name → (result_dir, has_vision, is_ablation)
MODELS = {
    "DeepSeek V3.2": ("deepseek-v3.2", False, False),
    "MiniMax M2.5": ("minimax-m2.5", False, False),
    "Kimi K2.5": ("kimi-k2.5", True, False),
    "GLM-5": ("glm-5", False, False),
    "Qwen 3.5 Plus": ("qwen3.5-plus", True, False),
    "Gemini 3.1 Pro": ("gemini-31-pro", True, False),
}

ABLATIONS = {
    "DeepSeek V3.2 (no reasoning)": ("deepseek-v3.2-noreasoning", False),
    "Gemini 3.1 Pro (no thinking)": ("gemini-31-pro-nothinking", True),
}


def load_questions():
    """Load question metadata for splits."""
    questions = {}
    with open(QUESTION_FILE) as f:
        for line in f:
            q = json.loads(line)
            key = (q["sub_id"], q["type"])
            questions[key] = q
    return questions


def load_results(result_dir):
    """Load raw results into a DataFrame."""
    path = RESULTS_DIR / result_dir / "raw_results.jsonl"
    if not path.exists():
        print(f"  WARNING: {path} not found")
        return None
    results = []
    with open(path) as f:
        for line in f:
            r = json.loads(line)
            results.append(r)
    df = pd.DataFrame(results)
    # Keep only valid (non-error) results
    if "raw_answer" in df.columns:
        df = df[df["raw_answer"].notna()].copy()
    return df


def build_score_matrix(df, formats):
    """
    Build binary score matrix: rows = (sub_id, type), columns = formats.
    Returns DataFrame with question keys as index, format names as columns.
    """
    # Create question key
    df = df.copy()
    df["q_key"] = list(zip(df["sub_id"], df["type"]))

    # Pivot to get score per format
    pivot = df.pivot_table(
        values="score", index="q_key", columns="format",
        aggfunc="first"  # Should be unique per (q_key, format)
    )

    # Keep only requested formats
    available = [f for f in formats if f in pivot.columns]
    pivot = pivot[available].dropna()  # Drop questions missing any format

    return pivot.astype(int)


def compute_tetrachoric(score_matrix, fmt_a, fmt_b):
    """
    Compute tetrachoric correlation between two formats.
    Uses ordinalcorr 0.6.1 — takes two binary arrays (x, y).
    """
    if fmt_a not in score_matrix.columns or fmt_b not in score_matrix.columns:
        return None, None

    a = score_matrix[fmt_a].values.astype(int)
    b = score_matrix[fmt_b].values.astype(int)

    # Build 2x2 contingency table for reporting
    n00 = int(np.sum((a == 0) & (b == 0)))
    n01 = int(np.sum((a == 0) & (b == 1)))
    n10 = int(np.sum((a == 1) & (b == 0)))
    n11 = int(np.sum((a == 1) & (b == 1)))
    table = [[n00, n01], [n10, n11]]

    # ordinalcorr needs variance in both variables
    if np.std(a) == 0 or np.std(b) == 0:
        # One variable is constant — correlation undefined, return 1.0 if both same
        return (1.0 if np.array_equal(a, b) else None), table

    try:
        r = tetrachoric(a, b)
        return float(r), table
    except Exception as e:
        warnings.warn(f"Tetrachoric failed for {fmt_a} vs {fmt_b}: {e}")
        return None, table


def compute_phi(score_matrix, fmt_a, fmt_b):
    """Compute phi coefficient between two binary format vectors."""
    if fmt_a not in score_matrix.columns or fmt_b not in score_matrix.columns:
        return None

    a = score_matrix[fmt_a].values
    b = score_matrix[fmt_b].values

    # Phi = Pearson correlation on binary data
    if np.std(a) == 0 or np.std(b) == 0:
        return 1.0 if np.array_equal(a, b) else 0.0

    r, _ = stats.pearsonr(a, b)
    return float(r)


def compute_kendall(score_matrix, fmt_a, fmt_b):
    """Compute Kendall's tau-b between two format vectors."""
    if fmt_a not in score_matrix.columns or fmt_b not in score_matrix.columns:
        return None

    a = score_matrix[fmt_a].values
    b = score_matrix[fmt_b].values

    tau, _ = stats.kendalltau(a, b)
    return float(tau)


def bootstrap_tetrachoric(score_matrix, fmt_a, fmt_b, n_resamples=10000, ci=0.95):
    """Bootstrap CI for tetrachoric correlation."""
    if fmt_a not in score_matrix.columns or fmt_b not in score_matrix.columns:
        return None, None

    n = len(score_matrix)
    correlations = []

    for _ in range(n_resamples):
        idx = np.random.randint(0, n, size=n)
        sample = score_matrix.iloc[idx]
        r, _ = compute_tetrachoric(sample, fmt_a, fmt_b)
        if r is not None:
            correlations.append(r)

    if len(correlations) < n_resamples * 0.5:
        return None, None

    alpha = (1 - ci) / 2
    lo = np.percentile(correlations, alpha * 100)
    hi = np.percentile(correlations, (1 - alpha) * 100)
    return float(lo), float(hi)


def compute_correlation_matrix(score_matrix, formats):
    """Compute full correlation matrix for given formats."""
    n = len(formats)
    tet_matrix = np.ones((n, n))
    phi_matrix = np.ones((n, n))
    tau_matrix = np.ones((n, n))
    ci_matrix = {}

    for i in range(n):
        for j in range(i + 1, n):
            # Tetrachoric
            r_tet, _ = compute_tetrachoric(score_matrix, formats[i], formats[j])
            if r_tet is not None:
                tet_matrix[i, j] = r_tet
                tet_matrix[j, i] = r_tet

            # Phi
            r_phi = compute_phi(score_matrix, formats[i], formats[j])
            if r_phi is not None:
                phi_matrix[i, j] = r_phi
                phi_matrix[j, i] = r_phi

            # Kendall
            r_tau = compute_kendall(score_matrix, formats[i], formats[j])
            if r_tau is not None:
                tau_matrix[i, j] = r_tau
                tau_matrix[j, i] = r_tau

            # Bootstrap CI (tetrachoric)
            lo, hi = bootstrap_tetrachoric(score_matrix, formats[i], formats[j],
                                           n_resamples=2000)  # 2000 for speed
            ci_matrix[f"{formats[i]}_vs_{formats[j]}"] = {"lo": lo, "hi": hi, "r": r_tet}

    return {
        "tetrachoric": tet_matrix.tolist(),
        "phi": phi_matrix.tolist(),
        "kendall_tau": tau_matrix.tolist(),
        "bootstrap_ci": ci_matrix,
        "formats": formats,
    }


def compute_accuracy_stats(df, formats):
    """Compute per-format and per-qtype accuracy with CIs."""
    valid = df[df["raw_answer"].notna()]

    format_acc = {}
    for fmt in formats:
        d = valid[valid["format"] == fmt]
        if len(d) > 0:
            acc = d["score"].mean()
            n = len(d)
            # Wilson binomial CI
            z = 1.96
            denom = 1 + z**2 / n
            center = (acc + z**2 / (2 * n)) / denom
            margin = z * np.sqrt((acc * (1 - acc) + z**2 / (4 * n)) / n) / denom
            format_acc[fmt] = {
                "accuracy": round(float(acc), 4),
                "n": int(n),
                "correct": int(d["score"].sum()),
                "ci_lo": round(float(center - margin), 4),
                "ci_hi": round(float(center + margin), 4),
            }

    qtype_acc = {}
    for qt in sorted(valid["type"].unique()):
        d = valid[valid["type"] == qt]
        acc = d["score"].mean()
        qtype_acc[qt] = {
            "accuracy": round(float(acc), 4),
            "n": int(len(d)),
        }

    # Per format × qtype
    format_qtype = {}
    for fmt in formats:
        for qt in sorted(valid["type"].unique()):
            d = valid[(valid["format"] == fmt) & (valid["type"] == qt)]
            if len(d) > 0:
                format_qtype[f"{fmt}_{qt}"] = round(float(d["score"].mean()), 4)

    return {
        "by_format": format_acc,
        "by_qtype": qtype_acc,
        "by_format_qtype": format_qtype,
    }


def main():
    print("=" * 70)
    print("StructReason-Transfer — Statistical Analysis")
    print("=" * 70)

    # Load question metadata
    questions = load_questions()
    print(f"Loaded {len(questions)} question metadata entries")

    # Question type splits
    basic_qtypes = {"Q1_lookup", "Q2_comparison", "Q3_aggregation", "Q4_trend", "Q5_extremum"}
    hard_qtypes = {"Q6_multi_hop", "Q7_conditional_aggregation"}

    all_results = {}

    # ==========================================
    # MAIN MODELS
    # ==========================================
    print("\n--- Main Models ---")
    for model_name, (result_dir, has_vision, _) in MODELS.items():
        print(f"\n[{model_name}]")
        df = load_results(result_dir)
        if df is None:
            continue

        formats = ALL_FORMATS if has_vision else TEXT_FORMATS
        print(f"  Loaded {len(df)} valid results | Formats: {formats}")

        # Accuracy stats
        acc_stats = compute_accuracy_stats(df, formats)
        print(f"  Overall accuracy by format:")
        for fmt, stats_dict in acc_stats["by_format"].items():
            print(f"    {fmt:<15} {stats_dict['accuracy']:.3f} [{stats_dict['ci_lo']:.3f}, {stats_dict['ci_hi']:.3f}] (n={stats_dict['n']})")

        # Build score matrix
        score_matrix = build_score_matrix(df, formats)
        print(f"  Score matrix: {score_matrix.shape[0]} questions × {score_matrix.shape[1]} formats")

        # Correlation matrix (all questions)
        print(f"  Computing correlations...")
        corr = compute_correlation_matrix(score_matrix, formats)
        print(f"  Tetrachoric correlation matrix:")
        for i, fi in enumerate(formats):
            row = " ".join(f"{corr['tetrachoric'][i][j]:.3f}" for j in range(len(formats)))
            print(f"    {fi:<15} {row}")

        # Split by difficulty
        basic_keys = {k for k in score_matrix.index if k[1] in basic_qtypes}
        hard_keys = {k for k in score_matrix.index if k[1] in hard_qtypes}

        basic_matrix = score_matrix.loc[score_matrix.index.isin(basic_keys)]
        hard_matrix = score_matrix.loc[score_matrix.index.isin(hard_keys)]

        text_formats = [f for f in formats if f != "chart_image"]
        corr_basic = compute_correlation_matrix(basic_matrix, text_formats) if len(basic_matrix) > 10 else None
        corr_hard = compute_correlation_matrix(hard_matrix, text_formats) if len(hard_matrix) > 10 else None

        # Complexity tier breakdown
        tier_acc = {}
        for tier in ["small", "medium", "large"]:
            tier_keys = {k for k, q in questions.items() if q.get("tier") == tier}
            tier_df = df[df.apply(lambda r: (r["sub_id"], r["type"]) in tier_keys, axis=1)]
            if len(tier_df) > 0:
                tier_acc[tier] = {fmt: round(float(tier_df[tier_df["format"] == fmt]["score"].mean()), 4)
                                  for fmt in formats if len(tier_df[tier_df["format"] == fmt]) > 0}

        all_results[model_name] = {
            "accuracy": acc_stats,
            "correlation_all": corr,
            "correlation_basic": corr_basic,
            "correlation_hard": corr_hard,
            "tier_accuracy": tier_acc,
            "n_questions": score_matrix.shape[0],
            "has_vision": has_vision,
        }

    # ==========================================
    # ABLATION MODELS
    # ==========================================
    print("\n--- Ablation Models ---")
    for model_name, (result_dir, has_vision) in ABLATIONS.items():
        print(f"\n[{model_name}]")
        df = load_results(result_dir)
        if df is None:
            continue

        # Pilot data uses different column naming — check
        if "expected_type" not in df.columns and "answer_type" in df.columns:
            df["expected_type"] = df["answer_type"]

        formats = ALL_FORMATS if has_vision else TEXT_FORMATS
        print(f"  Loaded {len(df)} valid results")

        acc_stats = compute_accuracy_stats(df, formats)
        print(f"  Accuracy by format:")
        for fmt, stats_dict in acc_stats["by_format"].items():
            print(f"    {fmt:<15} {stats_dict['accuracy']:.3f} (n={stats_dict['n']})")

        score_matrix = build_score_matrix(df, formats)
        corr = compute_correlation_matrix(score_matrix, formats) if score_matrix.shape[0] > 10 else None

        all_results[model_name] = {
            "accuracy": acc_stats,
            "correlation_all": corr,
            "n_questions": score_matrix.shape[0],
            "has_vision": has_vision,
            "is_ablation": True,
        }

    # ==========================================
    # AVERAGED CORRELATION MATRIX (text formats only, main models)
    # ==========================================
    print("\n--- Averaged Correlation Matrix (text formats, 6 models) ---")
    all_tet_matrices = []
    for model_name, data in all_results.items():
        if data.get("is_ablation"):
            continue
        corr = data.get("correlation_all")
        if corr is None:
            continue
        # Extract text-format submatrix
        formats = corr["formats"]
        text_idx = [i for i, f in enumerate(formats) if f in TEXT_FORMATS]
        sub_matrix = np.array(corr["tetrachoric"])[np.ix_(text_idx, text_idx)]
        all_tet_matrices.append(sub_matrix)

    if all_tet_matrices:
        avg_matrix = np.mean(all_tet_matrices, axis=0)
        print(f"  Averaged tetrachoric (N={len(all_tet_matrices)} models):")
        for i, fi in enumerate(TEXT_FORMATS):
            row = " ".join(f"{avg_matrix[i][j]:.3f}" for j in range(len(TEXT_FORMATS)))
            print(f"    {fi:<15} {row}")
        all_results["_averaged"] = {
            "tetrachoric": avg_matrix.tolist(),
            "formats": TEXT_FORMATS,
            "n_models": len(all_tet_matrices),
        }

    # ==========================================
    # B vs B' MODALITY COMPARISON (vision models only)
    # ==========================================
    print("\n--- B vs B' Modality Comparison ---")
    for model_name in ["Kimi K2.5", "Qwen 3.5 Plus", "Gemini 3.1 Pro"]:
        data = all_results.get(model_name)
        if data is None:
            continue
        acc = data["accuracy"]["by_format"]
        b_acc = acc.get("chart_image", {}).get("accuracy", "N/A")
        bp_acc = acc.get("chart_text", {}).get("accuracy", "N/A")
        gap = float(bp_acc) - float(b_acc) if isinstance(b_acc, float) and isinstance(bp_acc, float) else "N/A"
        print(f"  {model_name}: chart_image={b_acc}, chart_text={bp_acc}, gap={gap:.3f}" if gap != "N/A" else f"  {model_name}: N/A")

    # ==========================================
    # REASONING ABLATION COMPARISON
    # ==========================================
    print("\n--- Reasoning Ablation ---")
    for main, ablation in [("DeepSeek V3.2", "DeepSeek V3.2 (no reasoning)"),
                            ("Gemini 3.1 Pro", "Gemini 3.1 Pro (no thinking)")]:
        main_data = all_results.get(main)
        abl_data = all_results.get(ablation)
        if main_data and abl_data:
            print(f"\n  {main} vs {ablation}:")
            for fmt in TEXT_FORMATS:
                m_acc = main_data["accuracy"]["by_format"].get(fmt, {}).get("accuracy", "N/A")
                a_acc = abl_data["accuracy"]["by_format"].get(fmt, {}).get("accuracy", "N/A")
                diff = float(m_acc) - float(a_acc) if isinstance(m_acc, float) and isinstance(a_acc, float) else "N/A"
                print(f"    {fmt:<15} {a_acc} → {m_acc} (Δ={diff:+.3f})" if diff != "N/A" else f"    {fmt:<15} N/A")

    # ==========================================
    # SAVE ALL RESULTS
    # ==========================================
    output_path = RESULTS_DIR / "analysis_output.json"
    with open(output_path, 'w') as f:
        json.dump(all_results, f, indent=2, default=str)
    print(f"\nSaved analysis to: {output_path}")

    print("\n" + "=" * 70)
    print("ANALYSIS COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
