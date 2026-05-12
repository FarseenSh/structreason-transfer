# Do Structured Data Comprehension Skills Transfer Across Representation Types?

Code, data, prompts, and raw model outputs for the paper accepted at **SURGeLLM 2026 Workshop @ ACL 2026** (San Diego, Jul 2–3, non-archival).

[[Paper PDF]](paper/paper.pdf)

## Overview

We construct a controlled benchmark of **1,724 programmatically generated questions** over **250 sub-tables** drawn from 10 public datasets spanning 7 domains. Each sub-table is rendered in **five formats** with identical underlying content: Markdown table, chart image, chart text-description, entity-relationship graph, and unlabeled time series. We evaluate **six frontier March 2026 LLMs** and measure cross-format transfer via **tetrachoric correlation** on binary (correct/incorrect) outcomes.

**Key findings:**

- Structured data comprehension skills **transfer strongly** across text-based formats: mean tetrachoric *r* = 0.87 between table, graph, and time series across all six models (*r* = 0.84 in the three mid-range models, confirming the result is not a ceiling artifact).
- Chart text-descriptions show consistently **lower transfer** (*r* = 0.65) despite being length-matched to tables.
- Chart **image** comprehension is largely **siloed**: 20–50% accuracy gap vs. equivalent text descriptions on identical data.
- Chain-of-thought reasoning improves **text-format** accuracy by 24–38% for DeepSeek V3.2 but only 0–0.5% for Gemini 3.1 Pro (with a +2% chart-image gain on Gemini), suggesting reasoning benefits vary substantially across models.
- Cross-format transfer holds at least as strongly on **hard questions** (multi-hop and conditional aggregation) as on basic ones (*r* = 0.85 vs *r* = 0.81 for the table-graph-timeseries cluster).

## Models

| Model | Provider | Vision | Reasoning |
|-------|----------|--------|-----------|
| DeepSeek V3.2 | DeepSeek | No | Enabled |
| MiniMax M2.5 | MiniMax | No | Default on |
| Kimi K2.5 | Moonshot AI | Yes | Default on |
| GLM-5 | Zhipu AI | No | Default on |
| Qwen 3.5 Plus | Alibaba | Yes | Default on |
| Gemini 3.1 Pro | Google | Yes | Thinking on |

## Repository Structure

```
.
├── paper/
│   ├── paper.pdf                  # Final camera-ready PDF
│   ├── paper.tex                  # LaTeX source
│   ├── references.bib             # Bibliography (25 entries, primary-source verified)
│   ├── fig{1,4,5,6}_*.pdf         # Figures referenced in the paper
│   └── fig{2,3}_*.pdf             # Additional plots (not referenced in final paper)
├── experiments/
│   ├── experiment-plan.md         # Pre-registered experiment design (v3)
│   ├── code/
│   │   ├── analyze.py             # Compute accuracy, tetrachoric correlations,
│   │   │                          # error agreement, tier/domain breakdowns
│   │   ├── plot_figures.py        # Generate paper figures
│   │   ├── run_openrouter.py      # OpenRouter-hosted models (Kimi, GLM-5,
│   │   │                          # Qwen, DeepSeek, MiniMax)
│   │   ├── run_gemini.py          # Vertex AI: Gemini 3.1 Pro (thinking on)
│   │   ├── run_gemini_no_thinking.py  # Reasoning ablation for Gemini
│   │   ├── run_resumable.py       # Resumable runner with checkpoint/retry
│   │   ├── pilot_runner.py        # Pilot-study driver
│   │   ├── data/                  # Data generation: sub-table sampling,
│   │   │                          # format rendering, question generation
│   │   └── requirements.txt       # Python dependencies
│   ├── data/
│   │   ├── subtables/             # 250 sampled sub-tables (JSON)
│   │   ├── formats/               # Each sub-table rendered in 5 formats
│   │   │   ├── table/             # Markdown tables (250 files)
│   │   │   ├── chart_image/       # Matplotlib PNG charts (250 files)
│   │   │   ├── chart_text/        # Chart text-descriptions, length-matched to table (250 files)
│   │   │   ├── graph/             # Entity-relationship graph serializations (250 files)
│   │   │   └── timeseries/        # Unlabeled numerical arrays (250 files)
│   │   ├── questions/             # 1,724 programmatic Q&A pairs with
│   │   │                          # deterministic ground truth (pandas)
│   │   └── raw/                   # Source datasets (Ember, OPSD, EPA AQS,
│   │                              # FAOSTAT, NTD, OpenAQ, QoG, SEC XBRL, etc.)
│   └── results/
│       ├── analysis_output.json   # Aggregated analysis (accuracy, correlations,
│       │                          # tier/domain breakdowns, basic vs. hard splits)
│       ├── <model>/raw_results.jsonl    # Per-question raw outputs and scores
│       └── figures/               # Generated figure source files
└── .gitignore
```

## Reproducing the analysis

Install dependencies (Python 3.11 required — `py-irt` constraint, even though IRT is not used in the final analysis):

```bash
python3.11 -m venv venv
source venv/bin/activate
pip install -r experiments/code/requirements.txt
```

Re-run aggregation from raw outputs:

```bash
python experiments/code/analyze.py
# Writes experiments/results/analysis_output.json
```

Regenerate paper figures:

```bash
python experiments/code/plot_figures.py
# Writes paper/fig*.pdf
```

## Reproducing the model runs

Model evaluations require API credentials. We used Google Cloud (Vertex AI for Gemini), AWS Bedrock, and OpenRouter. Each runner is **resumable** — checkpoints land in `experiments/results/<model>/` and the runner picks up where it left off:

```bash
# Set provider credentials (see code/config.yaml for env-var names)
export OPENROUTER_API_KEY=...
export GOOGLE_APPLICATION_CREDENTIALS=...

# Example: run a single OpenRouter-hosted model
python experiments/code/run_openrouter.py --model kimi-k2.5

# Reasoning ablations
python experiments/code/run_gemini_no_thinking.py
```

Total run cost (March 2026 prices, all six models + two ablations): ≈ \$170 across the three providers.

## Statistical methodology

- **Primary metric:** Tetrachoric correlation on binary correctness outcomes, computed via the [`ordinalcorr`](https://pypi.org/project/ordinalcorr/) library (v0.6.1). Tetrachoric correlation estimates the latent Pearson correlation from dichotomized observations, making it appropriate for paired correct/incorrect data across formats. `scipy` does not implement tetrachoric correlation.
- **Secondary metrics:** Phi coefficient (Pearson on binary) and Kendall's τ-b.
- **Confidence intervals:** Bootstrap (2,000 resamples) for tetrachoric; Wilson binomial for accuracy.
- **Question difficulty splits:** Basic = Q1–Q5; Hard = Q6 (multi-hop), Q7 (conditional aggregation).
- **Ceiling robustness check:** Models split into ceiling group (≥95% mean text-format accuracy: DeepSeek, Qwen, Gemini) and mid-range group (Kimi, GLM-5, MiniMax). Mid-range estimates reported as conservative point estimates.

## Datasets used

Sub-tables are sampled from publicly available sources, including:

- **Ember** electricity generation (energy)
- **OPSD** Open Power System Data (energy)
- **EPA AQS** air-quality measurements (air quality)
- **OpenAQ** air-quality network (air quality)
- **FAOSTAT** crop production (agriculture)
- **Iizumi** crop yields (agriculture)
- **NTD** transit (transit)
- **QoG** EU governance/economics (governance)
- **SEC XBRL** corporate filings (finance)
- **HK traffic** (transportation)

Raw dataset files are under `experiments/data/raw/`. Sub-table sampling logic is in `experiments/code/data/generate_questions.py`.

## Citation

If you use this benchmark or analysis, please cite:

```bibtex
@inproceedings{shaikh2026structreason,
  title={Do Structured Data Comprehension Skills Transfer Across Representation Types? A Systematic Study with Frontier LLMs},
  author={Shaikh, Farseen},
  booktitle={SURGeLLM Workshop at ACL 2026},
  year={2026},
  note={Non-archival}
}
```

## Companion paper

This is Paper 2 of a pair accepted at SURGeLLM 2026. The companion paper on table-reasoning self-correction is at [FarseenSh/table-self-correction](https://github.com/FarseenSh/table-self-correction).

## Contact

Farseen Shaikh — farseenshaikh20@gmail.com
