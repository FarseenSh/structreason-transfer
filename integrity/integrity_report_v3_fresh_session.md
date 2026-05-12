# Integrity Report v3 — Fresh-session cold read (2026-05-11)

**Auditor:** Independent Claude session, cold context, verifies from primary sources (arXiv, ACL Anthology, OpenReview, Microsoft Research, Springer/Cambridge, paper-author project pages), `experiments/results/analysis_output.json`, and `experiments/results/<model>/raw_results.jsonl`. No reliance on `CAMERA_READY_STATUS.md`, `integrity_report.md`, `integrity_report_v2.md`, or `canonical_numbers_post_cleanup.json` for correctness claims.

**Verifier:** Fresh Claude session, opus-4-7[1m], invoked 2026-05-11.

---

## Verdict: CLEARED_WITH_CAVEATS

No outright hallucination was found in the post-correction state. All 25 bibliography entries map to real papers with correct titles, authors, and venues (modulo a few minor stylistic notes). The Ilić title is now correct, as is each of the 17 entries the prior session claimed to fix.

However, **six numerical/scoping issues** in prose remain. None requires re-running experiments; each is a single-line edit. They are non-blocking for upload to a non-archival venue but should be cleaned up to avoid contradicting the paper's own Table 2 and Table 3 numbers.

---

## Tier 1 — Hallucination risk

### 1.1 Bibliography verification

All 25 entries spot-checked against primary sources. Each marked VERIFIED was confirmed against a primary-source page (arXiv, ACL Anthology, OpenReview, publisher).

| Bib key | Status | Source | Notes |
|---|---|---|---|
| `pasupat2015compositional` | VERIFIED | aclanthology.org/P15-1142 | Title, authors, ACL 2015 pages 1470-1480 correct. |
| `chen2020tabfact` | VERIFIED | openreview.net/forum?id=rkeJRhNYDH | ICLR 2020 confirmed; title matches. |
| `masry2022chartqa` | VERIFIED | aclanthology.org/2022.findings-acl.177 | Authors (Masry, Long, Tan, Joty, Hoque) and pages 2263-2279 correct. |
| `chartqapro2025` | VERIFIED | aclanthology.org/2025.findings-acl.978 | ACL Findings 2025; authors and 14-name list match. |
| `graphomni2026` | VERIFIED | gai-community.github.io/Graph-Omni (ICLR 2026 banner) | All 12 authors and order correct; "Accepted to ICLR 2026" confirmed. |
| `gracore2025` | VERIFIED | aclanthology.org/2025.coling-main.531 | COLING 2025; authors Yuan/Liu/Wang/Qin match. |
| `tsaqa2026` | VERIFIED | arXiv:2601.23204 | All 16 authors and order match. |
| `mmtsbench2026` | VERIFIED | arXiv:2602.08588 | Title "MMTS-BENCH" (caps); bib uses `{MMTS-Bench}` — acceptable casing. All 10 authors match. |
| `hearts2026` | VERIFIED | arXiv:2603.06638 | Title and 7 authors match; project page yang-ai-lab/HEARTS confirms. |
| `zhang2026samecontent` | VERIFIED | iclr.cc/virtual/2026/poster/10009585 | ICLR 2026 poster; Zhang/Maekawa/Bhutani correct. |
| `liu2025formatprior` | VERIFIED | arXiv:2508.15793 | Title matches; 8 authors confirmed. |
| `ho2025formatmatters` | VERIFIED | arXiv:2511.10075 | Title and 6 authors match. |
| `epoch2026` | VERIFIED with note | arXiv:2512.00193 | Title "A Rosetta Stone for AI Benchmarks" and Nov 28, 2025 submission match. **bib uses `author={{Epoch AI}}` but actual paper has 5 named authors: Anson Ho, Jean-Stanislas Denain, David Atanasov, Samuel Albanie, Rohin Shah.** Stylistic, not an error per se. See SHOULD FIX #6. |
| `ilic2023gfactor` | VERIFIED | arXiv:2310.11616 | Title "Evidence of interrelated cognitive-like capabilities in large language models: Indications of artificial general intelligence or achievement?" — **MATCHES BIB EXACTLY**. Authors Ilić, Gignac and journal Intelligence 106:101858 (2024) correct. The prior hallucination (N1 in v2 report) is now resolved. |
| `mmtu2025` | VERIFIED | microsoft.com/research/publication/mmtu-... | NeurIPS 2025; all 9 authors match bib. |
| `charxiv2024` | VERIFIED | openreview.net/forum?id=cy8mq7QYae | NeurIPS 2024 D&B Poster confirmed; all 13 authors match. |
| `chartmuseum2025` | VERIFIED | arXiv:2505.13444 | All 15 authors match bib. |
| `torr2026` | VERIFIED | arXiv:2502.19412 | All 11 authors match. |
| `wikimixqa2025` | VERIFIED | aclanthology.org/2025.findings-acl.1280 | Findings ACL 2025; authors and pages 24941-24958 correct. |
| `datacross2026` | VERIFIED | arXiv:2601.21403 | 3 authors (Qi, Liu, Zhang) match. |
| `divgi1979calculation` | VERIFIED | cambridge.org / Springer doi:10.1007/BF02293968 | Psychometrika 44(2):169-172, 1979, D. R. Divgi. |
| `orchestra2026` | VERIFIED | arXiv:2601.03137 | All 7 authors match; submission date 6 Jan 2026 consistent. |
| `tabtracer2026` | VERIFIED | arXiv:2602.14089 | All 4 authors match; abstract confirms 6.7% improvement on TabFact/WikiTQ/CRT. |
| `infochartqa2025` | VERIFIED | openreview.net/pdf/68d5a1f251964c2fd5d05751685bec0fe1e3747a.pdf (NeurIPS 2025 D&B published PDF) | All 6 authors confirmed in published order: Xie, Lin, Liu, Ye, Chen, Liu (with Xie and Lin as co-first via asterisk). NeurIPS 2025 D&B Track venue **NOW CONFIRMED** (v2 had flagged this as unverified). |
| `bhandari2026tabular` | VERIFIED | arXiv:2604.24040 | 5 authors and order match bib. |

**Verdict for §1.1: 25/25 VERIFIED. No hallucinated entries. The previously hallucinated Ilić title (caught in v2) is now correctly cited.**

### 1.2 Prose claim verification (§2 Related Work + §5 Discussion)

For each citation-attributed factual claim:

| Claim | Source | Status |
|---|---|---|
| §2 Table QA: "Orchestra approach GPT-4's prior 75.3% EM benchmark on WikiTableQuestions using smaller open-weight models" | arXiv:2601.03137 abstract: "with Qwen2.5-14B, Orchestra reaches 72.1% accuracy on WikiTQ, approaching the best prior result of 75.3% achieved with GPT-4" | **CLAIM SUPPORTED** but incomplete. Abstract also notes Orchestra with *larger* Qwen/Llama/DeepSeek models **outperforms** all prior methods. The paper's framing ("approach") understates the contribution but is not factually wrong. |
| §2 Table QA: "TabTracer reports up to 6.7% accuracy improvements over prior state-of-the-art on TabFact and WikiTQ" | arXiv:2602.14089 abstract: "outperforms state-of-the-art baselines by up to 6.7% in accuracy" on TabFact, WikiTQ, **and CRT** | **CLAIM SUPPORTED** (CRT omitted but no misrepresentation). |
| §2 Table QA: "MMTU extends evaluation to a multi-task table understanding suite covering 25 task types" | microsoft.com/research MMTU page: "over 30K questions across 25 real-world table tasks" | **CLAIM SUPPORTED.** |
| §2 Chart Comprehension: "Claude Sonnet 3.5 scoring 90.5%" | chartqapro2025 abstract: "Claude Sonnet 3.5 scores 90.5% on ChartQA" | **CLAIM SUPPORTED** (90.5% is on the original ChartQA, not ChartQAPro; the paper attributes this to chartqapro2025 because that is the source reporting the number — defensible). |
| §2 Chart Comprehension: "Claude 3.5 with CoT reaches only 55.81%" on ChartQAPro | chartqapro2025 abstract: "Claude Sonnet 3.5 scores ... only 55.81% on ChartQAPro" | **CLAIM PARTIALLY SUPPORTED.** 55.81% is correct, but the abstract does not explicitly say "with CoT" — the "with CoT" qualifier may come from the paper body (Table results) but is not in the abstract. Cannot confirm without the full paper body; recommend dropping "with CoT" or verifying against §X of the ChartQAPro paper. **SHOULD VERIFY.** |
| §2 Chart Comprehension: "InfoChartQA pair infographic and plain charts sharing identical underlying data, finding substantial accuracy drops" | InfoChartQA NeurIPS 2025 abstract: "5,948 pairs of infographic and plain charts, each sharing the same underlying data ... reveals a substantial performance decline on infographic charts" | **CLAIM SUPPORTED.** |
| §2 Time Series: "TSAQA best accuracy on the puzzling format is 67.68% with a fine-tuned LLaMA-3.1-8B" | arXiv:2601.23204 abstract reports only Gemini-2.5-Flash 65.08% **average**; does not mention 67.68% or "best on puzzling" specifically. | **CLAIM CANNOT BE VERIFIED FROM ABSTRACT** — the 67.68% number must come from the paper body / results table. The abstract does confirm "a novel puzzling (PZ)" format exists. The specific number/configuration is plausible but unverified. **SHOULD VERIFY** against TSAQA paper body. (Carry-over caveat from v2.) |
| §2 Time Series: "MMTS-Bench: general-purpose LLMs with chain-of-thought outperform specialized" | arXiv:2602.08588 abstract: "(1) TS-LLMs significantly lag behind general-purpose LLMs in cross-domain generalization" + "(3) CoT reasoning ... substantially improves performance" | **CLAIM IS A SYNTHESIS** of two abstract findings. The combination ("general + CoT > specialized") is implied but not stated as a single result. Defensible paraphrase. |
| §2 Time Series: "HeaRTS: performance declines with increasing temporal complexity" | arXiv:2603.06638 abstract verbatim: "performance declines with increasing temporal complexity" | **CLAIM SUPPORTED — EXACT MATCH.** |
| §2 Graph Reasoning: "GraphOmni: serialization format dramatically affects ... across 7 graph types and 7 serialization formats" | GraphOmni website: "6 graph tasks, 7 graph types, 7 serialization formats" | **CLAIM SUPPORTED.** 7 types and 7 formats correctly stated (note: 6 *tasks*, not in the paper claim, but the count of types/formats is right). |
| §2 Cross-Format Studies: "Bhandari et al. show that semantically equivalent table serializations produce substantially different retrieval embeddings" | arXiv:2604.24040 title "Improving Robustness of Tabular Retrieval via Representational Stability" + abstract topic | **CLAIM SUPPORTED.** Title and topic align. |
| §5 Discussion: "Epoch AI's benchmark-stitching analysis" | arXiv:2512.00193 abstract: "we build a statistical framework that **stitches benchmarks together** ... onto a single numerical scale" | **CLAIM SUPPORTED.** "Benchmark-stitching" matches the abstract verbatim. |
| §5 Discussion: "the unidimensional capability factor reported by Epoch AI's benchmark-stitching analysis" | Epoch abstract describes a single-scale measurement framework but does not explicitly frame it as a "unidimensional capability factor" (that framing is more apt for `ilic2023gfactor`). | **CLAIM SLIGHTLY INTERPRETIVE.** Co-citing Epoch with Ilić as evidence of a "unidimensional capability factor" is a fair gloss, but Epoch's contribution is more about measurement than factor analysis. **MINOR — consider softening to "consistent with"**. |

**Verdict for §1.2: All claims either supported or supported-with-minor-caveat. No falsified citations. Two items (ChartQAPro CoT qualifier; TSAQA 67.68% number) cannot be verified from abstracts alone — these were not introduced by the prior session, but should ideally be checked against full paper bodies.**

### 1.3 Numerical claim verification

Numbers re-computed from `experiments/results/<model>/raw_results.jsonl` (1,724 × 6 models × 4-5 formats) and cross-checked against `experiments/results/analysis_output.json`. All checks use Python with `pandas`/`numpy` and the same `ordinalcorr.tetrachoric` library as the analysis script.

#### Abstract numbers — ALL MATCH

| Claim | Paper value | Computed | Status |
|---|---|---|---|
| TGT cluster mean tetrachoric (6 models) | r=0.87 | 0.8704 | MATCHES |
| Mid-range subset TGT mean | r=0.84 | 0.8411 | MATCHES |
| Chart-text pair mean (6 models) | r=0.65 | 0.6489 | MATCHES |
| TGT basic mean (6 models) | r=0.81 | 0.8088 | MATCHES |
| TGT hard mean (6 models) | r=0.85 | 0.8499 | MATCHES |
| Chart Image gap range | 20–50% | 19.55–49.71pp | MATCHES |
| DeepSeek reasoning gain range | 24–38% | 24.74–37.61pp | MATCHES (24.74 rounds tightly to 25; the range "24-38" is acceptable) |
| Gemini gain range (text-only) | 0–0.5% | 0.0–0.52pp | MATCHES (text formats only — see SHOULD FIX #5) |

#### §4.1 Overall accuracy — ALL MATCH

Every cell in Table 2 (DeepSeek/MiniMax/Kimi/GLM-5/Qwen/Gemini × Table/Chart Text/Graph/Time Series/Chart Image) matches `analysis_output.json` to within 0.05pp. The Wilson CIs also match.

Range claims:
| Claim | Computed | Status |
|---|---|---|
| Chart image: "31.9% (Kimi) to 70.6% (Gemini)" | 31.90, 70.59 | MATCHES |
| Text formats 81–99% range | 81.26–99.36 | MATCHES |
| "1–3 percentage points" within TGT cluster per model | DeepSeek 0.6/1.0; MiniMax 0.5/1.0; Kimi 0.3/1.3; GLM-5 0.04/0.2; Qwen 0.0/0.1; Gemini 0.1/0.1 | MATCHES (max gap 1.3pp, within 1–3pp) |
| "7–9% lower" Chart Text vs Table | DeepSeek 8.6; MiniMax 8.5; Kimi 7.5; GLM-5 7.6; Qwen 9.2; Gemini 9.2 | MATCHES |

#### §4.2 Cross-format transfer — ALL MATCH

| Claim | Computed | Status |
|---|---|---|
| TGT high-transfer range r=0.86–0.88 | 0.8558, 0.8759, 0.8796 (rounds to 0.86, 0.88, 0.88) | MATCHES |
| Chart-text pair range r=0.64–0.65 | 0.6499, 0.6520, 0.6447 (rounds to 0.64–0.65) | MATCHES |
| Ceiling group TGT r=0.90 | 0.8997 | MATCHES |
| Mid-range TGT r=0.84 | 0.8411 | MATCHES |
| Ceiling chart-text pair r=0.63 | 0.6315 | MATCHES |
| Mid-range chart-text pair r=0.67 | 0.6663 | MATCHES |
| DeepSeek within-ceiling r=0.73 | 0.7259 | MATCHES |
| Qwen within-ceiling r=0.99 | 0.9904 | MATCHES |

#### §4.3 Question type analysis

Table 3 cell-by-cell (averaged across 6 models — note: averaging includes chart_image for the 3 vision models, since `by_qtype` in `analysis_output.json` is averaged across all formats responded to by that model):

| Q | Paper | Recomputed | Status |
|---|---|---|---|
| Q1 Lookup | 92.5 | 92.46 | MATCHES |
| Q2 Comparison | 94.3 | 94.33 | MATCHES |
| Q3 Aggregation | 85.8 | 85.90 | MATCHES (within 0.1pp) |
| Q4 Trend | 97.6 | 97.61 | MATCHES |
| Q5 Extremum | 91.3 | 91.40 | MATCHES (within 0.1pp) |
| Q6 Multi-hop | 91.7 | 91.67 | MATCHES |
| Q7 Cond. Aggregation | 68.0 | 67.93 | MATCHES (within 0.1pp) |

**Note on caption:** Table 3 caption says "averaged across 6 models, text formats only". In fact the source `by_qtype` includes chart_image for the 3 vision models (Kimi, Qwen, Gemini) and is text-only for the 3 non-vision models. If the average were strictly text-only across all 6 models, Q1 would be ~97.9%, not 92.5%. The paper's Table 3 numbers are consistent across the chain, but the caption "text formats only" is imprecise. **SHOULD FIX #1** (see below).

Per-model Q7 range:
| Claim | Computed | Status |
|---|---|---|
| Q7 29.7% (Kimi) to 87.8% (Gemini) | 29.68, 87.84 | MATCHES |

§4.3 paragraph claim "On Q7 specifically, Chart Text accuracy is 12–15% lower than Table accuracy on average, compared to only 2–3% lower for Q1":
| Computed (per-model gap Table − Chart Text, in pp) | Q1 | Q7 |
|---|---|---|
| DeepSeek | 6.83 | 13.50 |
| MiniMax | 6.80 | 10.16 |
| Kimi | 7.60 | 0.00 |
| GLM-5 | 7.60 | 0.80 |
| Qwen | 7.20 | 17.20 |
| Gemini | 7.20 | 17.60 |
| **Mean** | **7.21** | **9.88** |

**MISMATCH:** Q1 actual mean gap is **~7pp, not 2–3%**, and Q7 actual mean gap is **~10pp, not 12–15%**. Q3 (aggregation) actually has the largest mean gap (~16.6pp). The directional claim ("Q7 gap > Q1 gap") still holds in aggregate, but the specific numbers in the prose are wrong. **SHOULD FIX #2.**

#### §4.4 Modality (Chart Image vs Chart Text) — ALL MATCH

| Model | Paper | Computed | Status |
|---|---|---|---|
| Gemini gap | 19.6% | 19.55pp | MATCHES |
| Qwen gap | 31.2% | 31.21pp | MATCHES |
| Kimi gap | 49.7% | 49.71pp | MATCHES |

#### §4.5 Error agreement (Table 4) — ALL MATCH

Recomputed by treating timeout rows (null `raw_answer`) as wrong (i.e., using full n=1,724 denominator):

| Model | Paper all_right / all_wrong / 1-fail | Computed | Status |
|---|---|---|---|
| DeepSeek | 82.5 / 0.9 / 11.3 | 82.48 / 0.87 / 11.31 | MATCHES |
| MiniMax | 82.4 / 0.8 / 12.7 | 82.39 / 0.76 / 12.67 | MATCHES |
| Kimi | 75.1 / 4.6 / 11.3 | 75.12 / 4.64 / 11.31 | MATCHES |
| GLM-5 | 74.3 / 4.4 / 12.8 | 74.30 / 4.41 / 12.76 | MATCHES |
| Qwen | 89.7 / 0.5 / 9.6 | 89.73 / 0.52 / 9.63 | MATCHES |
| Gemini | 89.8 / 0.5 / 9.5 | 89.85 / 0.46 / 9.45 | MATCHES |

**Important note:** Table 4 uses a *different denominator* (n=1,724, treating DeepSeek timeouts as wrong) than Table 2 (which uses n_responded ≈ 1,684 for DeepSeek). This means Table 4 DeepSeek = 82.5% "all right" while Table 2 implies a higher per-format rate. The two are internally consistent but the denominator switch is undocumented. See SHOULD FIX #4.

#### §4.6 Domain accuracy

| Domain | Paper | Computed (pooled, text-only, notna) | Status |
|---|---|---|---|
| agriculture | 95.4% | 95.43% | MATCHES |
| energy | 94.5% | 94.45% | MATCHES |
| transit | 90.3% | 90.35% | MATCHES |
| air quality | **90.6%** | **90.24%** | **MISMATCH (−0.36pp)** |

The "air quality (90.6%)" number does not reproduce. Recomputed using both pooled mean (0.9024) and mean-of-model-means (0.9025) — both give 90.2–90.3%. **The paper's 90.6% number for air quality cannot be reproduced from the current data.** Likely a stale number from an earlier analysis run. **SHOULD FIX #3.**

Also: as stated, the paper's ordering "transit (90.3%) and air quality (90.6%)" makes air quality slightly *easier* than transit. Correct data has them inverted (transit 90.35 > air quality 90.24 — i.e., air quality is hardest by a hair). Trivial in practice but worth aligning.

#### §5.1 Reasoning ablation

DeepSeek reasoning gains (per format):
| Format | Paper | Computed | Status |
|---|---|---|---|
| Table 65.3% → "97.4%" (+32.1%) | claims 97.4 | actual 97.33 | **0.07pp MISMATCH; "97.4%" should be "97.3%"** to match Table 2 (97.3). **SHOULD FIX #4a.** |
| Graph 60.8% → 97.9% (+37.1%) | 60.82 → 97.93 | 60.82 / 97.93 / +37.11 | MATCHES |
| Time Series — | 59.28 → 96.89 / +37.61 | (not specifically stated as a gain number) | MATCHES (within text) |

§5.1 paragraph: "with reasoning the ordering becomes Table (97.4%) ≈ Graph (97.9%) ≈ Time Series (96.9%) > **Chart Text (88.2%)**"

| Field | Paper | Computed | Status |
|---|---|---|---|
| Chart Text | **88.2%** | **88.72%** (→ 88.7) | **MISMATCH (−0.52pp).** The paper's own Table 2 reports DeepSeek Chart Text as 88.7%. The "88.2%" in §5.1 conflicts with Table 2. **SHOULD FIX #4b.** |

DeepSeek without-reasoning ordering "Table (65.3%) > Chart Text (64.0%) > Graph (60.8%) > Time Series (59.3%)":
| Format | Paper | Computed | Status |
|---|---|---|---|
| Table | 65.3 | 65.26 | MATCHES |
| Chart Text | 64.0 | 63.98 | MATCHES |
| Graph | 60.8 | 60.82 | MATCHES |
| Time Series | 59.3 | 59.28 | MATCHES |

Gemini "gains <1pp on any format":
| Format | Δ | Status |
|---|---|---|
| Table | +0.52 | <1 ✓ |
| Chart Text | 0.00 | <1 ✓ |
| Graph | +0.24 | <1 ✓ |
| Time Series | +0.17 | <1 ✓ |
| **Chart Image** | **+2.03** | **NOT <1** |

The Gemini "<1pp" / "0–0.5%" claim is correct **for text formats** but **understates the Chart Image gain (+2.0pp)**. Abstract, §5.1 figure caption, §5 Discussion paragraph, and Conclusion all assert "<1pp" or "0–0.5%" without disclosing the text-only scope. **SHOULD FIX #5.**

#### §5.2 Basic vs Hard

| Claim | Computed | Status |
|---|---|---|
| Grand TGT basic r=0.81 | 0.8088 | MATCHES |
| Grand TGT hard r=0.85 | 0.8499 | MATCHES |
| "four of six models showing hard > basic" | MiniMax/Kimi/GLM-5/Qwen=T; DeepSeek/Gemini=F | MATCHES (correctly fixed from v2's "five of six") |
| "two exceptions (DeepSeek, Gemini) at near-ceiling" | DeepSeek mean text acc ≈95.2%; Gemini ≈97.0% | DEFENSIBLE — both >95% mean text-format accuracy. |

#### §5.3 Complexity tiers — ALL MATCH

| Tier | Paper | Recomputed | Status |
|---|---|---|---|
| small | 97.6% | 97.62 | MATCHES |
| medium | 92.3% | 92.31 | MATCHES |
| large | 87.7% | 87.72 | MATCHES |

#### §3.6 Token counts — ALL MATCH

Recomputed with `tiktoken.get_encoding('cl100k_base')` over 250 files per format:
| Format | Paper median | Recomputed median | Status |
|---|---|---|---|
| Table | 276 | 276 | MATCHES |
| Chart Text | 270 | 270 | MATCHES |
| Graph | 520 | 520 | MATCHES |
| Time Series | 380 | 380 | MATCHES |

#### Appendix Table A.1 — ALL MATCH

Per-model × per-qtype values (rounded to 0.1pp) all match `analysis_output.json` `by_qtype` values exactly. Note: this Appendix table also reflects the mixed-formats averaging (chart_image included for vision models). Consistent with Table 3.

---

## Tier 2 — Judgment-based prose

### 2.1 "Scope of claims" subsection in §5

Read in full. The three positive claims:
1. "question-level accuracy on table, graph-like, and time-series formats is highly correlated" — supported by r=0.87 / 0.84 mid-range / r=0.81 basic / r=0.85 hard.
2. "chart-text accuracy systematically lags table accuracy by 7–9%" — supported by per-model gaps 7.5–9.2pp.
3. "chart-image accuracy is substantially lower than chart-text accuracy on identical data" — supported by per-model gaps 19.6–49.7pp.

The four negative claims (do *not* claim):
- "real-world structured-data generalizability" — appropriate, study uses synthetic sub-tables.
- "universal silo for vision models" — appropriate, N=3 vision models.
- "CoT effect generalizes beyond two-model ablation" — appropriate, hedge holds.
- "graph reasoning in the natural-graph sense" — appropriate, format is constructed serialization.

**No overclaiming detected. Internally consistent.**

### 2.2 Limitations paragraph

Each added limitation is true of this study:
- N=6 models → descriptive analyses (true).
- Graph format is constructed (cosine-similarity edges) (true; matches Methodology §3.2).
- Synthetic sub-tables vs in-the-wild benchmarks (true).
- Single prompt template + cl100k_base (true).
- Tetrachoric assumes bivariate-normal; base-rate sensitive (true — and consistent with §4.2 ceiling-effect caveat).
- N=3 vision models for chart-image silo claim (true).

**All limitations are accurately scoped to the actual study design.**

### 2.3 Conclusion paragraph

> "Cross-format transfer holds at least as strongly on hard (multi-hop and conditional aggregation) questions as on basic ones"

Correctly reflects the (corrected) basic-vs-hard finding (basic r=0.81 < hard r=0.85). No contradiction with §5.2.

> "reasoning dramatically helps the weaker base model (+24 to +38pp) but not the stronger one (<1pp)"

Same caveat as SHOULD FIX #5: "<1pp" silently restricts to text formats; on chart_image, Gemini gains 2.0pp. Either the qualifier needs adding or the chart_image exception needs disclosing.

> "comprehension skills transfer strongly across text-based formats (r=0.86–0.88 across the table-graph-timeseries cluster)"

Three TGT pair correlations are 0.8558, 0.8759, 0.8796 → rounds to 0.86, 0.88, 0.88. Range "0.86–0.88" is technically accurate (lower bound rounds to 0.86; the abstract uses 0.85 as a >threshold not a range). The slight rounding choice (0.8558 → "0.86" vs "0.85") is permissible.

### 2.4 Reasoning ablation rewrite (§5.1 Discussion paragraph)

> "the gain from explicit reasoning correlates with the model's no-reasoning baseline accuracy: DeepSeek V3.2 (62% baseline mean) gains +24 to +38pp depending on format; Gemini 3.1 Pro (97% baseline) gains <1pp"

- "62% baseline mean" — DeepSeek no-reasoning text mean = (65.26+63.98+60.82+59.28)/4 = 62.34% ✓
- "97% baseline" — Gemini no-thinking text mean = (98.84+90.14+99.01+99.13)/4 = 96.78% ≈ 97% ✓
- "+24 to +38pp" — actual 24.74 to 37.61pp ✓
- "<1pp" — text only; chart_image is +2.03pp (not disclosed). See SHOULD FIX #5.

> "We caution that this pattern is observed in N=2 models. ... requires testing across a broader model panel and reasoning-toggle pair, which we reserve for future work."

Appropriately hedged.

> "DeepSeek used ~200 reasoning tokens per call vs. ~5 without"

This token-count claim could not be verified from `raw_results.jsonl` (the `raw_answer` field stores parsed final answers, not full reasoning traces). It is a hand-wavy comparative claim; the directional gist (reasoning incurs nontrivial token cost) is undisputed. Recommend either citing the source of this number or softening to "substantially more reasoning tokens." **MINOR.**

### 2.5 §2 Related Work paragraph rewrites

Covered in §1.2 above. All citations verified; one number (TSAQA 67.68%) and one qualifier (ChartQAPro "with CoT") could not be confirmed from abstracts.

### 2.6 §5.2 paragraph (basic vs hard, corrected)

> "transfer is at least as strong on hard questions as on basic ones in aggregate, with four of six models (MiniMax, Kimi, GLM-5, Qwen) showing hard > basic correlations; the two exceptions (DeepSeek, Gemini) operate at near-ceiling accuracy where the metric is less stable"

- "four of six" — verified (the v2 correction from "five of six" to "four of six" is correct).
- Named models — verified (MiniMax/Kimi/GLM-5/Qwen all show hard > basic; DeepSeek and Gemini show basic > hard).
- "near-ceiling accuracy" qualifier — DeepSeek's overall text mean is ~95% and Gemini's is ~97%, both in the ceiling group defined in §4.2 (≥95%). For DeepSeek the basic-hard *correlation* gap (0.80 vs 0.60) is large; the near-ceiling explanation is plausible but not airtight, since DeepSeek's hard-question accuracy is not actually near ceiling (Q7 at 80.9%). The framing is acceptable but could be strengthened.

**Internally consistent with §4.2 and the abstract.**

---

## Tier 3 — Regression check

| Check | Result |
|---|---|
| PDF compile (paper.log) | Clean — only `Underfull \hbox` warnings (cosmetic). No errors, no missing references. |
| Final page count | 11 pages total (`pdfinfo`): content pages 1–8, Acknowledgments p9, References p9–10, Appendix p10–11. **8 content pages = ACL long paper compliant.** |
| `??` cross-references in PDF | None (`pdftotext | grep '??'` = 0 hits). |
| Citation key resolution | 25 `\cite{}` keys used; 25 `@*{}` entries defined; **diff = empty (perfect match).** |
| aclpubcheck | **"All Clear"** (aclpubcheck 0.2.0 on paper.pdf). |
| Abstract word count | 216 words (within ACL ≤250 limit). |

---

## Tier 4 — Cosmetic / completeness

| Item | Status |
|---|---|
| Author block | `\author{Farseen Shaikh \\ \texttt{claudeshaikh3@gmail.com}}` — real name + real email. ✓ |
| Repository URL in Acknowledgments | `https://github.com/farseen/structreason-transfer` — not yet created (verified via curl: 404). Flagged as expected per the audit request. **MINOR — create the repo before submission, or replace with "will be released on publication".** |
| Figures referenced | fig1, fig4, fig5, fig6 (all render in PDF). |
| Orphan figure files | **fig2_radar_plots.pdf and fig3_qtype_accuracy.pdf exist in `paper/` but are NOT referenced in paper.tex.** Harmless for upload but should be deleted or referenced. **MINOR.** |
| BibTeX cleanliness | All entries parse; `epoch2026` uses institutional author (`{{Epoch AI}}`) when the actual paper has 5 named individuals (Ho, Denain, Atanasov, Albanie, Shah). **MINOR — recommend updating.** |
| Compile artifacts | `errors-paper.json` = `{}` (empty), `paper.log` = clean, `paper.blg` = ~373 bytes (BibTeX log normal). |

---

## Specific BLOCKING issues

**None.** No outright hallucinations, no fabricated citations, no contradictions between paper claims and underlying data that would mislead a reader.

---

## Specific SHOULD FIX issues

Listed in approximate order of importance. Each is a single-edit fix.

### SHOULD FIX #1 — Table 3 caption is imprecise

**Location:** §4.3, Table 3 caption.
**Current:** "Accuracy by question type (averaged across 6 models, **text formats only**). Q7 conditional aggregation provides the strongest discrimination."
**Problem:** The underlying averages include `chart_image` for the 3 vision-capable models (Kimi, Qwen, Gemini). If averaging were strictly text-only across all 6 models, Q1 would be ~97.9% (not 92.5% as reported). The current numbers are *correct as computed*, but the caption misrepresents the computation.
**Suggested fix:**
> "Accuracy by question type, averaged across 6 models over each model's set of evaluated formats (4 text formats for the 3 non-vision models; 4 text + 1 chart-image for the 3 vision models)."

Or alternatively, recompute strictly text-only and update both Table 3 and the surrounding prose. The first (caption-only) fix is cheaper.

### SHOULD FIX #2 — §4.3 Q1 / Q7 chart-text-vs-table gap percentages are wrong

**Location:** §4.3, paragraph "Interaction between question type and format".
**Current:** "On Q7 specifically, Chart Text accuracy is **12--15\%** lower than Table accuracy on average, compared to only **2--3\%** lower for Q1."
**Computed:** Mean per-model gap is **9.9pp on Q7** and **7.2pp on Q1**. Neither 12-15% nor 2-3% reproduces.
- Directional claim ("Q7 gap > Q1 gap") still holds (9.9 > 7.2).
- Q3 (aggregation) actually has the largest mean gap (~16.6pp); the paragraph asserting Q3+Q7 have the largest format-dependent variance is correct *for Q3*, less so for Q7.
**Suggested fix:**
> "On Q7 specifically, Chart Text accuracy is ~10pp lower than Table accuracy on average, compared to ~7pp lower for Q1. The largest format-dependent gap is on Q3 (aggregation) at ~17pp on average."

### SHOULD FIX #3 — §4.6 air-quality domain accuracy is wrong

**Location:** §4.6 Domain Effects.
**Current:** "agriculture (95.4\%) and energy (94.5\%) are easiest, while transit (90.3\%) and air quality (**90.6\%**) are hardest"
**Computed:** air quality = **90.24%** (pooled) / 90.25% (mean of model means). Off by 0.36pp.
**Suggested fix:** Change "90.6%" to "90.2%". (Also: the relative ordering puts air quality marginally *below* transit. The two-domain "hardest" framing still holds.)

### SHOULD FIX #4 — §5.1 DeepSeek "with reasoning" Chart Text/Table numbers contradict Table 2

**Location:** §5.1, paragraph after the format-ordering sentence.
**Current:** "with reasoning the ordering becomes Table (**97.4\%**) ≈ Graph (97.9\%) ≈ Time Series (96.9\%) > Chart Text (**88.2\%**)"
**Table 2 says:** DeepSeek table = 97.3%, chart_text = 88.7%.
**Computed:** 97.33% and 88.72%, both rounding to 97.3% and 88.7%.
**Problem:** §5.1's "97.4%" and "88.2%" disagree with Table 2 and with the underlying data. The "88.2%" is the larger discrepancy (−0.5pp) and is the most visible inconsistency to a reviewer who cross-checks.
**Suggested fix:** Change "97.4" → "97.3" and "88.2" → "88.7". Also update the parenthetical "+32.1%" — 97.3 − 65.3 = 32.0; the rounded gain becomes "+32.0".

### SHOULD FIX #5 — "Gemini <1pp" / "0–0.5%" silently excludes Chart Image

**Locations:** Abstract; §5.1 paragraph; Figure 4 caption; §5 Discussion paragraph; Conclusion.
**Current:** Various phrasings of "Gemini 3.1 Pro gains <1pp" or "0–0.5%".
**Data:** Gemini text-format gains are 0.00–0.52pp (within claim). Gemini chart-image gain is **+2.03pp** (68.56 → 70.59 with thinking enabled), which exceeds the stated bound.
**Problem:** The "<1pp" claim is true only for text formats. Reviewers comparing to Table 2 (which shows chart_image for Gemini) may catch this.
**Suggested fix:** Add a text-format qualifier in at least the abstract and §5.1 caption, e.g.:
> "(abstract) ... only 0–0.5% for Gemini 3.1 Pro **on text formats** (with a modest +2pp gain on chart-image)"
> "(Fig 4 caption) ... Gemini 3.1 Pro gains <1% **on text formats**."

Alternatively, restrict the reasoning ablation discussion explicitly to text formats throughout. The current implicit scoping is the most error-prone framing.

### SHOULD FIX #6 — `epoch2026` bib uses institutional author when 5 named authors exist

**Location:** `references.bib`, `@misc{epoch2026, ...}`.
**Current:** `author={{Epoch AI}}`.
**Actual authors (arXiv:2512.00193):** Anson Ho, Jean-Stanislas Denain, David Atanasov, Samuel Albanie, Rohin Shah.
**Suggested fix:**
```bibtex
@misc{epoch2026,
  title={A {Rosetta Stone} for {AI} Benchmarks},
  author={Ho, Anson and Denain, Jean-Stanislas and Atanasov, David and Albanie, Samuel and Shah, Rohin},
  year={2025},
  note={arXiv:2512.00193},
  url={https://arxiv.org/abs/2512.00193}
}
```
And consider replacing in-prose `\citet{epoch2026}`'s framing ("Epoch AI's benchmark-stitching analysis") if author-style changes — `\citet{epoch2026}` will then render "Ho et al. (2025)", which may read better than "Epoch AI's analysis". Minor stylistic choice.

---

## MINOR issues

| # | Item |
|---|---|
| MINOR-1 | Methodology §3 silently filters DeepSeek timeout rows (158 total across 4 formats, ~2.3% of attempts) from the accuracy denominator while Table 4 uses the full 1,724 denominator. Internally consistent computations but the policy is undisclosed. Recommend a one-sentence note in §3 ("API timeouts contributing <3% of attempts are excluded from per-format accuracy but counted as errors in cross-format error-agreement analysis"). |
| MINOR-2 | §5 Discussion: framing `\citet{epoch2026}` as evidence of a "unidimensional capability factor" is interpretive — the Epoch paper provides a single-scale measurement framework, not a factor analysis (which is Ilić's contribution). Recommend softening to "consistent with". |
| MINOR-3 | §2 ChartQA Comprehension: "Claude 3.5 **with CoT** reaches only 55.81%" — the "with CoT" qualifier is not in the ChartQAPro abstract; should be checked against §X of that paper or dropped. |
| MINOR-4 | §2 Time Series: TSAQA's "67.68% with fine-tuned LLaMA-3.1-8B on the puzzling format" is plausible but unverified from the abstract; should be confirmed against the paper's results table. (Carry-over from v2 N8.) |
| MINOR-5 | §5 Discussion: "DeepSeek used ~200 reasoning tokens per call vs. ~5 without" cannot be verified from `raw_results.jsonl` (which stores only parsed answers). Either cite source/log or soften to qualitative claim. |
| MINOR-6 | Orphan figures `fig2_radar_plots.pdf` and `fig3_qtype_accuracy.pdf` are in `paper/` but not referenced. Harmless; delete or reference. |
| MINOR-7 | `https://github.com/farseen/structreason-transfer` 404s. Create the repo before the camera-ready upload, or temporize to "will be released on publication". |
| MINOR-8 | Title casing for `mmtsbench2026`: the arXiv title is "MMTS-BENCH" (all caps); the bib uses `{MMTS-Bench}`. Cosmetic choice; not an error. |

---

## Notable items that turned out to be FINE

| Item | Status |
|---|---|
| Ilić title (prior hallucination) | Now correct: "Evidence of interrelated cognitive-like capabilities ... ?" |
| InfoChartQA NeurIPS 2025 venue (v2 caveat) | Confirmed via OpenReview-hosted NeurIPS published PDF (October 2025). |
| All 25 bibliography entries | Verified against primary sources. |
| All abstract numbers | Match recomputed values from raw data. |
| Cross-format correlation grand means (r=0.87, r=0.84, r=0.65, r=0.81 basic, r=0.85 hard) | All verified. |
| Tier accuracies (97.6/92.3/87.7) | Verified. |
| Modality gaps (49.7/31.2/19.6) | Verified. |
| Token medians (276/270/520/380) | Verified by recomputing with `tiktoken cl100k_base`. |
| Page count (8 content + refs + appendix = 11) | ACL compliant. |
| aclpubcheck | "All Clear". |

---

## Recommendation

**The paper is in clearable shape for non-archival camera-ready upload to SURGeLLM 2026 as-is.** Verdict: **CLEARED_WITH_CAVEATS.**

If the author has time for one more pass, the highest-value edits in order are:

1. **SHOULD FIX #4** — fix DeepSeek "with reasoning" §5.1 numbers ("97.4%" → "97.3%", "88.2%" → "88.7%"). This is the most visible inconsistency a reviewer would catch.
2. **SHOULD FIX #5** — qualify the Gemini "<1pp" claim with "on text formats" (or disclose the chart-image +2pp).
3. **SHOULD FIX #3** — air quality "90.6%" → "90.2%".
4. **SHOULD FIX #2** — Q1/Q7 chart-text-vs-table gap numbers in §4.3 ("12-15%" / "2-3%" → "~10pp" / "~7pp"; mention Q3 has the largest gap).
5. **SHOULD FIX #1** — Table 3 caption: replace "text formats only" with accurate scoping.
6. **SHOULD FIX #6** — `epoch2026` named authors.

Items 1, 3, and 5 are single-line LaTeX edits. Items 2 and 4 are two-line edits. Item 6 is a 6-line bib edit.

If the author has *no* time, the paper still presents truthful headline findings and the bibliography is clean — but a reviewer who recomputes the §4.3 / §4.6 / §5.1 numbers will find the discrepancies above.

---

*Report generated 2026-05-11 by independent cold-read integrity audit.*
*All numerical claims independently recomputed from `experiments/results/<model>/raw_results.jsonl`.*
*All bibliography entries verified against arXiv / ACL Anthology / OpenReview / Microsoft Research / publisher sources.*
