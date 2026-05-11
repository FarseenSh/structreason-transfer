"""
Step 2: Generate publication-quality figures and tables.
Reads analysis_output.json and produces PDF figures.
"""

import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
RESULTS_DIR = BASE_DIR / "experiments" / "results"
FIG_DIR = RESULTS_DIR / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

# Colorblind-friendly palette
COLORS = ['#0072B2', '#E69F00', '#009E73', '#CC79A7', '#D55E00', '#56B4E9']
FORMAT_COLORS = {
    'table': '#0072B2',
    'chart_text': '#E69F00',
    'graph': '#009E73',
    'timeseries': '#CC79A7',
    'chart_image': '#D55E00',
}

MODEL_ORDER = [
    "DeepSeek V3.2", "MiniMax M2.5", "Kimi K2.5",
    "GLM-5", "Qwen 3.5 Plus", "Gemini 3.1 Pro"
]
FORMAT_LABELS = {
    'table': 'Table',
    'chart_text': 'Chart Text',
    'graph': 'Graph',
    'timeseries': 'Time Series',
    'chart_image': 'Chart Image',
}
TEXT_FORMATS = ['table', 'chart_text', 'graph', 'timeseries']
ALL_FORMATS = ['table', 'chart_text', 'graph', 'timeseries', 'chart_image']


def load_analysis():
    with open(RESULTS_DIR / "analysis_output.json") as f:
        return json.load(f)


def fig1_correlation_heatmap(data):
    """Figure 1: Averaged tetrachoric correlation heatmap (4x4 text formats)."""
    avg = data.get("_averaged", {})
    matrix = np.array(avg["tetrachoric"])
    formats = [FORMAT_LABELS[f] for f in avg["formats"]]

    fig, ax = plt.subplots(figsize=(5, 4.5))
    cmap = plt.cm.RdYlBu_r
    im = ax.imshow(matrix, cmap=cmap, vmin=0.4, vmax=1.0, aspect='equal')

    ax.set_xticks(range(len(formats)))
    ax.set_yticks(range(len(formats)))
    ax.set_xticklabels(formats, fontsize=9, rotation=45, ha='right')
    ax.set_yticklabels(formats, fontsize=9)

    # Annotate cells
    for i in range(len(formats)):
        for j in range(len(formats)):
            val = matrix[i][j]
            color = 'white' if val > 0.8 or val < 0.5 else 'black'
            ax.text(j, i, f'{val:.2f}', ha='center', va='center',
                   fontsize=11, fontweight='bold', color=color)

    cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label('Tetrachoric Correlation', fontsize=9)

    ax.set_title('Cross-Format Comprehension Transfer\n(Averaged Across 6 Models)', fontsize=11)
    plt.tight_layout()
    plt.savefig(FIG_DIR / 'fig1_correlation_heatmap.pdf', dpi=300, bbox_inches='tight')
    plt.close()
    print("  Fig 1: correlation heatmap saved")


def fig2_radar_plots(data):
    """Figure 2: Per-model radar plots showing accuracy across formats."""
    fig, axes = plt.subplots(2, 3, figsize=(12, 8), subplot_kw=dict(polar=True))
    axes = axes.flatten()

    for idx, model_name in enumerate(MODEL_ORDER):
        ax = axes[idx]
        model_data = data.get(model_name, {})
        acc = model_data.get("accuracy", {}).get("by_format", {})

        has_vision = model_data.get("has_vision", False)
        formats = ALL_FORMATS if has_vision else TEXT_FORMATS
        labels = [FORMAT_LABELS[f] for f in formats]
        values = [acc.get(f, {}).get("accuracy", 0) for f in formats]

        # Close the polygon
        angles = np.linspace(0, 2 * np.pi, len(formats), endpoint=False).tolist()
        values_closed = values + [values[0]]
        angles_closed = angles + [angles[0]]

        ax.fill(angles_closed, values_closed, alpha=0.25, color=COLORS[idx])
        ax.plot(angles_closed, values_closed, 'o-', linewidth=2, color=COLORS[idx], markersize=4)

        ax.set_xticks(angles)
        ax.set_xticklabels(labels, fontsize=7)
        ax.set_ylim(0, 1.05)
        ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
        ax.set_yticklabels(['20%', '40%', '60%', '80%', '100%'], fontsize=6)
        ax.set_title(model_name, fontsize=10, fontweight='bold', pad=15)

    plt.suptitle('Accuracy Profiles Across Data Formats', fontsize=13, y=1.02)
    plt.tight_layout()
    plt.savefig(FIG_DIR / 'fig2_radar_plots.pdf', dpi=300, bbox_inches='tight')
    plt.close()
    print("  Fig 2: radar plots saved")


def fig3_qtype_accuracy(data):
    """Figure 3: Accuracy by question type × format (grouped bar chart)."""
    qtypes = ['Q1_lookup', 'Q2_comparison', 'Q3_aggregation', 'Q4_trend',
              'Q5_extremum', 'Q6_multi_hop', 'Q7_conditional_aggregation']
    qtype_labels = ['Q1\nLookup', 'Q2\nCompare', 'Q3\nAggreg.', 'Q4\nTrend',
                    'Q5\nExtrem.', 'Q6\nMulti-hop', 'Q7\nCond.Agg.']

    # Average across all 6 models per format × qtype
    avg_scores = {}
    for fmt in TEXT_FORMATS:
        for qt in qtypes:
            key = f"{fmt}_{qt}"
            vals = []
            for model_name in MODEL_ORDER:
                model_data = data.get(model_name, {})
                fq = model_data.get("accuracy", {}).get("by_format_qtype", {})
                if key in fq:
                    vals.append(fq[key])
            avg_scores[key] = np.mean(vals) if vals else 0

    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.arange(len(qtypes))
    width = 0.18

    for i, fmt in enumerate(TEXT_FORMATS):
        values = [avg_scores.get(f"{fmt}_{qt}", 0) for qt in qtypes]
        offset = (i - len(TEXT_FORMATS)/2 + 0.5) * width
        bars = ax.bar(x + offset, values, width, label=FORMAT_LABELS[fmt],
                     color=FORMAT_COLORS[fmt], alpha=0.85)

    ax.set_xlabel('Question Type', fontsize=11)
    ax.set_ylabel('Accuracy', fontsize=11)
    ax.set_title('Accuracy by Question Type and Format\n(Averaged Across 6 Models)', fontsize=12)
    ax.set_xticks(x)
    ax.set_xticklabels(qtype_labels, fontsize=9)
    ax.set_ylim(0, 1.05)
    ax.legend(fontsize=9, loc='lower left')
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(FIG_DIR / 'fig3_qtype_accuracy.pdf', dpi=300, bbox_inches='tight')
    plt.close()
    print("  Fig 3: question type accuracy saved")


def fig4_reasoning_ablation(data):
    """Figure 4: Reasoning/thinking ablation (DeepSeek + Gemini)."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5))

    formats = TEXT_FORMATS
    labels = [FORMAT_LABELS[f] for f in formats]
    x = np.arange(len(formats))
    width = 0.35

    # DeepSeek
    ds_main = data.get("DeepSeek V3.2", {}).get("accuracy", {}).get("by_format", {})
    ds_abl = data.get("DeepSeek V3.2 (no reasoning)", {}).get("accuracy", {}).get("by_format", {})

    ds_with = [ds_main.get(f, {}).get("accuracy", 0) for f in formats]
    ds_without = [ds_abl.get(f, {}).get("accuracy", 0) for f in formats]

    ax1.bar(x - width/2, ds_without, width, label='Without Reasoning', color='#D55E00', alpha=0.8)
    ax1.bar(x + width/2, ds_with, width, label='With Reasoning', color='#0072B2', alpha=0.8)
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels, fontsize=9, rotation=30, ha='right')
    ax1.set_ylabel('Accuracy', fontsize=11)
    ax1.set_title('DeepSeek V3.2', fontsize=11, fontweight='bold')
    ax1.set_ylim(0, 1.05)
    ax1.legend(fontsize=8)
    ax1.grid(axis='y', alpha=0.3)

    # Add delta annotations
    for i in range(len(formats)):
        delta = ds_with[i] - ds_without[i]
        ax1.annotate(f'+{delta:.0%}', xy=(x[i] + width/2, ds_with[i] + 0.01),
                    ha='center', fontsize=7, color='#0072B2', fontweight='bold')

    # Gemini
    gm_main = data.get("Gemini 3.1 Pro", {}).get("accuracy", {}).get("by_format", {})
    gm_abl = data.get("Gemini 3.1 Pro (no thinking)", {}).get("accuracy", {}).get("by_format", {})

    gm_with = [gm_main.get(f, {}).get("accuracy", 0) for f in formats]
    gm_without = [gm_abl.get(f, {}).get("accuracy", 0) for f in formats]

    ax2.bar(x - width/2, gm_without, width, label='Without Thinking', color='#D55E00', alpha=0.8)
    ax2.bar(x + width/2, gm_with, width, label='With Thinking', color='#0072B2', alpha=0.8)
    ax2.set_xticks(x)
    ax2.set_xticklabels(labels, fontsize=9, rotation=30, ha='right')
    ax2.set_title('Gemini 3.1 Pro', fontsize=11, fontweight='bold')
    ax2.set_ylim(0.85, 1.02)  # Zoomed y-axis to show small differences
    ax2.legend(fontsize=8)
    ax2.grid(axis='y', alpha=0.3)

    for i in range(len(formats)):
        delta = gm_with[i] - gm_without[i]
        ax2.annotate(f'+{delta:.1%}', xy=(x[i] + width/2, gm_with[i] + 0.01),
                    ha='center', fontsize=7, color='#0072B2', fontweight='bold')

    plt.suptitle('Effect of Reasoning/Thinking on Cross-Format Comprehension', fontsize=12, y=1.02)
    plt.tight_layout()
    plt.savefig(FIG_DIR / 'fig4_reasoning_ablation.pdf', dpi=300, bbox_inches='tight')
    plt.close()
    print("  Fig 4: reasoning ablation saved")


def fig5_bvsbp_modality(data):
    """Figure 5: Chart Image (B) vs Chart Text (B') comparison."""
    vision_models = ["Kimi K2.5", "Qwen 3.5 Plus", "Gemini 3.1 Pro"]

    fig, ax = plt.subplots(figsize=(6, 4))
    x = np.arange(len(vision_models))
    width = 0.35

    b_acc = []
    bp_acc = []
    for m in vision_models:
        acc = data.get(m, {}).get("accuracy", {}).get("by_format", {})
        b_acc.append(acc.get("chart_image", {}).get("accuracy", 0))
        bp_acc.append(acc.get("chart_text", {}).get("accuracy", 0))

    ax.bar(x - width/2, b_acc, width, label='Chart Image (B)', color='#D55E00', alpha=0.85)
    ax.bar(x + width/2, bp_acc, width, label='Chart Text (B\')', color='#0072B2', alpha=0.85)

    for i in range(len(vision_models)):
        gap = bp_acc[i] - b_acc[i]
        ax.annotate(f'Gap: {gap:.0%}', xy=(x[i], max(b_acc[i], bp_acc[i]) + 0.03),
                   ha='center', fontsize=9, fontweight='bold', color='#CC0000')

    ax.set_xticks(x)
    ax.set_xticklabels(vision_models, fontsize=10)
    ax.set_ylabel('Accuracy', fontsize=11)
    ax.set_title('Modality Isolation: Chart Image vs Chart Text', fontsize=12)
    ax.set_ylim(0, 1.1)
    ax.legend(fontsize=9)
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(FIG_DIR / 'fig5_modality_comparison.pdf', dpi=300, bbox_inches='tight')
    plt.close()
    print("  Fig 5: modality comparison saved")


def fig6_per_model_heatmaps(data):
    """Appendix: Per-model correlation heatmaps."""
    fig, axes = plt.subplots(2, 3, figsize=(14, 9))
    axes = axes.flatten()

    for idx, model_name in enumerate(MODEL_ORDER):
        ax = axes[idx]
        model_data = data.get(model_name, {})
        corr = model_data.get("correlation_all", {})

        if not corr:
            ax.set_visible(False)
            continue

        formats = corr.get("formats", TEXT_FORMATS)
        matrix = np.array(corr["tetrachoric"])
        labels = [FORMAT_LABELS.get(f, f) for f in formats]

        # For non-vision models, pad to 5x5 for visual consistency
        cmap = plt.cm.RdYlBu_r
        im = ax.imshow(matrix, cmap=cmap, vmin=0.2, vmax=1.0, aspect='equal')

        ax.set_xticks(range(len(labels)))
        ax.set_yticks(range(len(labels)))
        ax.set_xticklabels(labels, fontsize=7, rotation=45, ha='right')
        ax.set_yticklabels(labels, fontsize=7)

        for i in range(len(labels)):
            for j in range(len(labels)):
                val = matrix[i][j]
                color = 'white' if val > 0.8 or val < 0.4 else 'black'
                ax.text(j, i, f'{val:.2f}', ha='center', va='center',
                       fontsize=8, color=color)

        ax.set_title(model_name, fontsize=10, fontweight='bold')

    plt.suptitle('Per-Model Tetrachoric Correlation Matrices', fontsize=13)
    plt.tight_layout()
    plt.savefig(FIG_DIR / 'fig6_per_model_heatmaps.pdf', dpi=300, bbox_inches='tight')
    plt.close()
    print("  Fig 6: per-model heatmaps saved")


def table1_accuracy(data):
    """Generate Table 1 data: 6 models × 5 formats with CIs."""
    print("\n  === TABLE 1: Raw Accuracy (%) ===")
    header = f"{'Model':<20}" + "".join(f"{FORMAT_LABELS[f]:>15}" for f in ALL_FORMATS)
    print(f"  {header}")
    print(f"  {'-'*95}")

    for model_name in MODEL_ORDER:
        model_data = data.get(model_name, {})
        acc = model_data.get("accuracy", {}).get("by_format", {})
        row = f"  {model_name:<20}"
        for fmt in ALL_FORMATS:
            if fmt in acc:
                a = acc[fmt]["accuracy"]
                lo = acc[fmt]["ci_lo"]
                hi = acc[fmt]["ci_hi"]
                row += f"{a*100:>7.1f} [{lo*100:.0f}-{hi*100:.0f}]"
            else:
                row += f"{'—':>15}"
        print(row)


def table2_qtype(data):
    """Generate Table 2: Per-question-type accuracy."""
    qtypes = ['Q1_lookup', 'Q2_comparison', 'Q3_aggregation', 'Q4_trend',
              'Q5_extremum', 'Q6_multi_hop', 'Q7_conditional_aggregation']

    print("\n  === TABLE 2: Accuracy by Question Type (%) ===")
    header = f"{'Model':<20}" + "".join(f"{qt.split('_',1)[1][:8]:>10}" for qt in qtypes)
    print(f"  {header}")
    print(f"  {'-'*90}")

    for model_name in MODEL_ORDER:
        model_data = data.get(model_name, {})
        qacc = model_data.get("accuracy", {}).get("by_qtype", {})
        row = f"  {model_name:<20}"
        for qt in qtypes:
            if qt in qacc:
                row += f"{qacc[qt]['accuracy']*100:>10.1f}"
            else:
                row += f"{'—':>10}"
        print(row)


def main():
    print("=" * 70)
    print("Generating Figures and Tables")
    print("=" * 70)

    data = load_analysis()
    print(f"Loaded analysis for {len([k for k in data if not k.startswith('_')])} models\n")

    # Figures
    print("Generating figures...")
    fig1_correlation_heatmap(data)
    fig2_radar_plots(data)
    fig3_qtype_accuracy(data)
    fig4_reasoning_ablation(data)
    fig5_bvsbp_modality(data)
    fig6_per_model_heatmaps(data)

    # Tables (printed to console)
    table1_accuracy(data)
    table2_qtype(data)

    print(f"\nAll figures saved to: {FIG_DIR}")
    print("=" * 70)
    print("FIGURES COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
