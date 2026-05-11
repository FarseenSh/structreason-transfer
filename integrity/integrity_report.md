# Integrity Report
**Paper:** Do Structured Data Comprehension Skills Transfer Across Representation Types? A Systematic Study with Frontier LLMs
**Date audited:** 2026-05-11
**Auditor:** Independent integrity-check sub-agent (cold read)
**Verdict:** BLOCKED

---

## Citation Audit

All 19 bib entries were verified using CrossRef, OpenAlex, Semantic Scholar, and Exa MCP (for recent preprints). Layer 3 (claim attribution) was checked against retrieved abstracts.

| Citation Key | Status | Issues |
|---|---|---|
| `pasupat2015compositional` | ✅ VERIFIED | Title, authors (Pasupat, Percy Liang), venue (ACL 2015) match. |
| `chen2020tabfact` | ✅ VERIFIED | Full author list (Wenhu Chen et al.) matches bib exactly. Venue ICLR 2020 confirmed via official site. |
| `masry2022chartqa` | ✅ VERIFIED | Title, authors (Masry et al.), venue (ACL Findings 2022) confirmed. |
| `chartqapro2025` | ❌ WRONG AUTHOR + PARTIAL TITLE | Bib says `Ibrahim, Mohanad`. Actual first author is **Ahmed Masry**. Bib title: "A More Challenging Benchmark"; actual title: "A More **Diverse and** Challenging Benchmark." Venue ACL Findings 2025 correct. |
| `graphomni2026` | ❌ WRONG AUTHOR | Bib says `Li, Hao`. Actual first author is **Hao Xu** (CUHK-Shenzhen). Venue ICLR 2026 confirmed. |
| `gracore2025` | ❌ WRONG AUTHOR | Bib says `Ma, Yuhan`. Actual first author is **Zike Yuan** (COLING 2025, verified on ACL Anthology). |
| `tsaqa2026` | ❌ WRONG AUTHOR + CLAIM MISMATCH | Bib says `Wang, Xin`. Actual lead authors are **Baoyu Jing and Sanhorn Chen** (UIUC). See claim analysis below. |
| `mmtsbench2026` | ❌ WRONG AUTHOR | Bib says `Zhang, Wei`. Actual first author is **Yao Yin**. |
| `hearts2026` | ❌ WRONG AUTHOR + WRONG TITLE | Bib title: "HeaRTS: Heart Rate Time Series Analysis with LLMs". Actual title: **"HeaRTS: Benchmarking LLM Reasoning on Health Time Series"** (arXiv 2603.06638). Bib says `Kim, Soomin`; actual first author is **Sirui Li** (UCLA). |
| `zhang2026samecontent` | ❌ WRONG AUTHOR + WRONG TITLE | Bib says `Zhang, Yilun`. Actual first author is **Yue Zhang**. Bib subtitle: "Evaluating LLM Sensitivity to Table Formats"; actual: "A Controlled Study for Table QA" (ICLR 2026, confirmed). |
| `liu2026formatprior` | ❌ WRONG AUTHOR + WRONG TITLE + WRONG YEAR | The matching paper is arXiv:2508.15793 "Format as a Prior: **Quantifying and Analyzing Bias in LLMs for Heterogeneous Data**" by **Jiacheng Liu** and Mayi Xu. Bib says `Liu, Chen`, subtitle completely different, year listed as 2026 but paper submitted August 2025. |
| `ho2025formatmatters` | ❌ WRONG AUTHOR + WRONG TITLE | Bib says `Ho, Thanh`. Actual first author is **Xanh Ho** (arXiv:2511.10075). Bib title subtitle: "Claim Verification Across Data Representations"; actual: "The Robustness of Multimodal LLMs in Reviewing Evidence from Tables and Charts." |
| `epoch2026` | ⚠️ PARTIAL | Paper exists at epoch.ai/data-insights/benchmark-correlations. It is a **blog/data insight**, not an arXiv preprint. No single author, attributed to "Epoch AI." Bib lists `journal = arXiv preprint` which is incorrect — this is a web post. Claim verification: paper does find cross-benchmark correlations. |
| `ilic2023gfactor` | ❌ WRONG AUTHOR + WRONG TITLE | Bib says `Ilic, Igor`. Actual first author is **David Ilić** with co-author Gilles Gignac (arXiv:2310.11616). Bib title: "A General Intelligence Factor in Large Language Models"; actual: "Evidence of interrelated cognitive-like capabilities in large language models: Indications of artificial general intelligence or achievement?" |
| `mmtu2025` | ❌ WRONG AUTHOR + WRONG TITLE | Bib says `Li, Zheng` and title: "A Multi-Modal Table Understanding Benchmark." Actual first author: **Junjie Xing** (Microsoft Research). Actual title: "MMTU: A **Massive Multi-Task** Table Understanding and Reasoning Benchmark" (NeurIPS 2025). Modal → Task is a content-level error. |
| `charxiv2026` | ❌ NOT A SEPARATE 2026 PAPER | CharXiv-R is the **reasoning subset of CharXiv**, a NeurIPS 2024 paper by **Zirui Wang et al.** Bib cites it as a separate 2026 arXiv paper by `Wang, Yi` — the first name is wrong (Zirui not Yi), the year is wrong (2024 not 2026), and no distinct "CharXiv-R: Chart Reasoning in the Wild" 2026 paper exists. This entry is a **hallucinated citation**. |
| `chartmuseum2025` | ❌ WRONG AUTHOR | Bib says `Park, Jin`. Actual first author is **Liyan Tang** (UT Austin; confirmed via OpenReview NeurIPS 2025). |
| `torr2026` | ❌ WRONG AUTHOR + WRONG TITLE + WRONG YEAR | Bib says `Ashury-Tahan, Mahsa` and title "ToRR: Table Format Robustness for Multi-Format Evaluation," year 2026. Actual first author is **Shir Ashury-Tahan**; actual title is "**The Mighty ToRR: A Benchmark for Table Reasoning and Robustness**" (arXiv 2025, confirmed on OpenReview). |
| `wikimixqa2025` | ⚠️ WRONG TITLE | Bib says `Foroutan, Negar` (correct). But bib subtitle: "Cross-Modal Question Answering over Tables and Charts"; actual subtitle: "A Multimodal Benchmark for Question Answering over Tables and Charts" (ACL Findings 2025, confirmed). |
| `datacross2026` | ❌ WRONG AUTHOR + WRONG TITLE | Bib says `Qi, Zheng`. Actual first author is **Ruyi Qi** (arXiv:2601.21403). Bib title: "A Cross-Modal Benchmark for Structured Data Understanding"; actual: "A Unified Benchmark and Agent Framework for Cross-Modal Heterogeneous Data Analysis." |
| `divgi1979calculation` | ✅ VERIFIED | Title, author (D.R. Divgi), journal (Psychometrika), year (1979) confirmed via CrossRef. |

**Summary:** 2 verified / 1 partial / 0 not-found / 15 wrong-author-or-title / 1 hallucinated (charxiv2026) out of 19 total entries.

### High-Risk Claim Analysis

1. **Orchestra ">75.3% EM on WikiTableQuestions"** — The paper prose implies Orchestra achieves >75.3%. The actual Orchestra paper (arXiv:2601.03137) explicitly states Orchestra *approaches* the best prior result of 75.3% (achieved with GPT-4), not that it achieves or exceeds it. Orchestra itself reaches 72.1% with small models; with larger Qwen/Llama/DeepSeek it beats all prior baselines — but 75.3% belongs to a prior GPT-4 system, NOT Orchestra. **CLAIM MISMATCH**: the prose says "Orchestra achieving >75.3%" when the paper says it approaches/surpasses 75.3% with different model configurations. The ">" in the prose is misleading.

2. **TabTracer "92.5% on TabFact"** — TabTracer abstract says "outperforms state-of-the-art baselines by up to 6.7%." No specific 92.5% figure was locatable in the abstract. The actual TabFact performance number cannot be confirmed as 92.5% from available sources. **PARTIAL**: exists, but specific number unverifiable from abstract.

3. **ChartQA ">95% accuracy"** — Current frontier models (Gemini, Qwen) do reach >90% on ChartQA; >95% is plausible for top models by early 2026. Claude Sonnet 3.5 scores 90.5% (confirmed by ChartQAPro paper). The >95% claim is broadly consistent with known leaderboard trends but is not directly sourced. **PARTIAL**: plausible but unsourced.

4. **ChartQAPro "Claude 3.5 with CoT reaches only 55.8%"** — ✅ VERIFIED. The actual ChartQAPro paper (arXiv:2504.05506) reports Claude Sonnet 3.5 scores 55.81% on ChartQAPro. The bib says this is the "current best" but the actual paper reports the best closed-source was Claude at 55.81%; with CoT is implied by the benchmark design. Number correct.

5. **TSAQA "fine-tuned LLMs can achieve 67.68%"** — The TSAQA paper (arXiv:2601.23204) shows the 67.68 figure is the score of **LLaMA 3.1-8B with instruction tuning on a single sub-task (Temporal Relation)**. It is NOT the overall average accuracy of fine-tuned LLMs on TSAQA. The best overall instruction-tuned model achieves ~85% average. The prose presents this as a headline accuracy for fine-tuned LLMs on "time series QA," which is **CLAIM MISMATCH** — the number is cherry-picked from one sub-task of one small model.

6. **MMTS-Bench "general LLMs with CoT can outperform specialized time-series models"** — MMTS-Bench (arXiv:2602.08588) finding (1): "TS-LLMs significantly lag behind general-purpose LLMs in cross-domain generalization" and finding (3): "CoT reasoning substantially improves performance." The combined claim is a fair paraphrase. **✅ SUPPORTED** (though it merges two separate findings).

7. **HeaRTS "temporal complexity degrades LLM performance"** — ✅ VERIFIED. HeaRTS abstract explicitly states "performance declines with increasing temporal complexity" (arXiv:2603.06638v2). Claim is correct.

8. **GraphOmni "serialization format dramatically affects LLM graph reasoning"** — ✅ VERIFIED. GraphOmni abstract confirms "critical interactions among dimensions" including serialization formats with "decisive impact on model performance."

9. **Epoch AI "cross-benchmark correlations"** — ✅ PARTIALLY SUPPORTED. The Epoch AI data insight does report cross-benchmark correlations (median Spearman r=0.68–0.79). However, the paper cites it as `arXiv preprint` when it is a web post/blog, not an arXiv paper. The claim that it supports "cross-benchmark correlations" is accurate but the citation type is wrong.

---

## Data Audit

All numerical values cross-checked against `analysis_output.json` and per-model `summary.json`.

### Table 2 (Overall Accuracy)

| Claim | Value in Paper | Value in Data | Status |
|---|---|---|---|
| DeepSeek V3.2 Table | 97.4% | 97.36% | ✅ MATCHES |
| DeepSeek V3.2 Chart Text | 88.2% | 88.16% | ✅ MATCHES |
| DeepSeek V3.2 Graph | 97.9% | 97.89% | ✅ MATCHES |
| DeepSeek V3.2 Time Series | 96.9% | 96.92% | ✅ MATCHES |
| MiniMax M2.5 Table | 95.8% | 95.76% | ✅ MATCHES |
| MiniMax M2.5 Chart Text | 87.2% | 87.22% | ✅ MATCHES |
| MiniMax M2.5 Graph | 96.3% | 96.29% | ✅ MATCHES |
| MiniMax M2.5 Time Series | 94.8% | 94.78% | ✅ MATCHES |
| Kimi K2.5 Table | 89.1% | 89.10% | ✅ MATCHES |
| Kimi K2.5 Chart Text | 81.6% | 81.61% | ✅ MATCHES |
| Kimi K2.5 Graph | 88.8% | 88.75% | ✅ MATCHES |
| Kimi K2.5 Time Series | 87.8% | 87.82% | ✅ MATCHES |
| Kimi K2.5 Chart Image | 31.9% | 31.90% | ✅ MATCHES |
| GLM-5 Table | 88.8% | 88.81% | ✅ MATCHES |
| GLM-5 Chart Text | 81.3% | 81.26% | ✅ MATCHES |
| GLM-5 Graph | 88.9% | 88.92% | ✅ MATCHES |
| GLM-5 Time Series | 88.8% | 88.75% | ✅ MATCHES |
| Qwen 3.5 Plus Table | 99.2% | 99.25% | ✅ MATCHES |
| Qwen 3.5 Plus Chart Text | 90.1% | 90.08% | ✅ MATCHES |
| Qwen 3.5 Plus Graph | 99.2% | 99.25% | ✅ MATCHES |
| Qwen 3.5 Plus Time Series | 99.4% | 99.36% | ✅ MATCHES |
| Qwen 3.5 Plus Chart Image | 58.9% | 58.87% | ✅ MATCHES |
| Gemini 3.1 Pro Table | 99.4% | 99.36% | ✅ MATCHES |
| Gemini 3.1 Pro Chart Text | 90.1% | 90.14% | ✅ MATCHES |
| Gemini 3.1 Pro Graph | 99.2% | 99.25% | ✅ MATCHES |
| Gemini 3.1 Pro Time Series | 99.3% | 99.30% | ✅ MATCHES |
| Gemini 3.1 Pro Chart Image | 70.6% | 70.59% | ✅ MATCHES |

### Abstract and Key Correlation Claims

| Claim | Value in Paper | Computed from Data | Status |
|---|---|---|---|
| Mean tetrachoric r for table/graph/timeseries | 0.84 | **0.87** (mean of 3 pairs, _averaged matrix) | ❌ MISMATCH |
| r=0.85 overall | 0.85 | **0.76** (all 6 pairs) or **0.87** (table/graph/ts only) — neither equals 0.85 | ❌ AMBIGUOUS / CANNOT REPRODUCE |
| r=0.84 for non-ceiling models (table/graph/ts) | 0.84 | **0.84** (mean of 3 pairs for Kimi/GLM/MiniMax) | ✅ MATCHES |
| Chart text pairs r=0.65 | 0.65 | **0.648** (mean of 3 chart-text pairs) | ✅ MATCHES |
| Chart text pairs r=0.64–0.65 (Section 4.2) | 0.64–0.65 | 0.645–0.651 | ✅ MATCHES |
| High-transfer r=0.85–0.88 (Section 4.2) | 0.85–0.88 | 0.855–0.878 | ✅ MATCHES |
| Basic questions r=0.89 | 0.89 | **0.81** (table/graph/ts mean) or **0.70** (all pairs) | ❌ MISMATCH |
| Hard questions r=0.78 | 0.78 | **0.85** (table/graph/ts mean) or **0.77** (all pairs) | ❌ MISMATCH |
| Hard r < Basic r (transfer decreases for hard) | Hard < Basic | **Data shows Hard > Basic** (0.85 vs 0.81 for tgt pairs) | ❌ DIRECTIONAL MISMATCH |

### Reasoning Ablation (Section 5.1)

| Claim | Paper | Data | Status |
|---|---|---|---|
| DeepSeek Table no-reasoning | 65.3% | 65.26% | ✅ MATCHES |
| DeepSeek Graph no-reasoning | 60.8% | 60.82% | ✅ MATCHES |
| DeepSeek TS no-reasoning | 59.3% | 59.28% | ✅ MATCHES |
| DeepSeek Table +32.1% with reasoning | +32.1pp | +32.1pp | ✅ MATCHES |
| DeepSeek Graph +37.1% with reasoning | +37.1pp | +37.1pp | ✅ MATCHES |
| DeepSeek gains 24–38% range | 24–38% | 24.2–37.6pp (chart_text to ts) | ✅ MATCHES |
| Gemini gain ≤0.5% | <1% | 0.0–0.5pp | ✅ MATCHES |

### Chart B vs B' Gaps

| Claim | Paper | Data | Status |
|---|---|---|---|
| Kimi K2.5 gap | 49.7% | 49.71% | ✅ MATCHES |
| Qwen 3.5 Plus gap | 31.2% | 31.21% | ✅ MATCHES |
| Gemini 3.1 Pro gap | 19.6% | 19.55% | ✅ MATCHES |
| 20–50% accuracy gap (abstract) | 20–50% | 19.6–49.7% | ✅ MATCHES |

### Question Type Accuracy (Table 3 / Appendix Table A.1)

| Claim | Paper | Data | Status |
|---|---|---|---|
| Q4 Trend overall 97.6% | 97.6% | 97.6% | ✅ MATCHES |
| Q1 Lookup overall 92.5% | 92.5% | 92.5% | ✅ MATCHES |
| Q2 Comparison overall 94.3% | 94.3% | 94.3% | ✅ MATCHES |
| Q5 Extremum overall 91.3% | 91.3% | 91.3% | ✅ MATCHES |
| Q6 Multi-hop overall 91.7% | 91.7% | 91.7% | ✅ MATCHES |
| Q3 Aggregation overall 85.8% | 85.8% | 85.8% | ✅ MATCHES |
| Q7 Cond. Aggregation overall 68.0% | 68.0% | 68.0% | ✅ MATCHES |
| Kimi K2.5 Q7 only 29.7% | 29.7% | 29.68% | ✅ MATCHES |
| Appendix Table A.1 all cells | All match | All match | ✅ MATCHES |

### Tier Accuracy (Section 5.3)

| Claim | Paper | Computed | Status |
|---|---|---|---|
| Small (5×3) tier average | 94.2% | **97.6%** | ❌ MISMATCH |
| Medium (10×5) tier average | 91.8% | **92.2%** | ❌ MISMATCH |
| Large (20×8) tier average | 88.5% | **87.7%** | ❌ MISMATCH |

Note: the paper's small-tier value (94.2%) matches DeepSeek's own medium-tier value, suggesting a possible row-copy error in producing the tier table.

### Error Agreement (Table 4)

| Claim | Paper (DeepSeek) | Computed from raw_results.jsonl | Status |
|---|---|---|---|
| All right | 87.3% | **82.6%** | ❌ MISMATCH (4.7pp) |
| All wrong | 0.3% | **0.9%** | ❌ MISMATCH (3×) |
| 1-format fail | 10.2% | **11.4%** | ❌ MISMATCH |

Other models' Table 4 values were not independently verified but the DeepSeek discrepancy indicates Table 4 was computed from a different source or methodology than what is archived in the results files.

---

## Figure Audit

| Figure | File Exists | Label in Paper | Referenced in Text | Caption Claim Check |
|---|---|---|---|---|
| fig1_correlation_heatmap.pdf | ✅ | fig:heatmap | ✅ | "averaged over six models" — 6 models confirmed. ✅ |
| fig4_reasoning_ablation.pdf | ✅ | fig:reasoning | ✅ | "24–38% / <1%" — confirmed against data. ✅ |
| fig5_modality_comparison.pdf | ✅ | fig:modality | ✅ | "19.6% (Gemini) to 49.7% (Kimi)" — confirmed. ✅ |
| fig6_per_model_heatmaps.pdf | ✅ | fig:permodel | ✅ (Appendix) | "per-model matrices for six models" — 6 confirmed. ✅ |
| fig2_radar_plots.pdf | ✅ (file exists) | — | ❌ NOT REFERENCED | Orphaned file — not in paper. |
| fig3_qtype_accuracy.pdf | ✅ (file exists) | — | ❌ NOT REFERENCED | Orphaned file — not in paper. |

No broken `??` cross-references found. All figures referenced in text have matching labels and the files exist.

---

## Claim Audit (Dangerous Phrases)

| Claim | Category | Verdict |
|---|---|---|
| "the first study measuring cross-format transfer across five fundamentally different representation types" | "first study" | ⚠️ WEAK. Related work (ToRR, WikiMixQA, DataCross, zhang2026samecontent) is cited. The qualification "identical data and questions" is what makes this claim; prior work never tests the same questions across 5 type-distinct formats. Defensible but depends on the "identical" qualifier holding up under reviewer scrutiny. |
| "first to span five fundamentally different representation types with identical content" (Conclusion) | "first to" | Same as above. Defensible with the qualifier. |
| "significantly" | Significance | Not found in paper body — authors appropriately avoided it. ✅ |
| "outperforms" | Comparison | Used only to paraphrase MMTS-Bench findings, not as a primary claim of this paper. ✅ |
| DeepSeek gains "30+" in Discussion | Magnitude claim | Accurate; Table accuracy +32.1%, Graph +37.1%. ✅ |

---

## Completeness Audit

| Item | Status |
|---|---|
| Abstract within 250 words | ✅ (225 words) |
| All required sections present | ✅ (Introduction, Related Work, Methodology, Results, Ablations, Discussion, Conclusion, Limitations as a paragraph in Discussion) |
| Limitations section | ✅ (paragraph in §6 Discussion) |
| Code/data availability statement | ✅ ("All code, data, and prompts will be released upon publication") |
| No broken `??` references | ✅ |
| All included figures exist | ✅ |
| Author block | ⚠️ STILL ANONYMOUS (`\author{Anonymous}`) — paper is going to camera-ready; author block must be de-anonymized before submission |
| Anonymization otherwise | N/A (non-archival) |

---

## Data Integrity Issues

### Issue D1: DeepSeek V3.2 results file contains 1,000 duplicate rows

The file `deepseek-v3.2/raw_results.jsonl` has 7,896 rows instead of the expected 6,896 (1,724 questions × 4 formats). Exactly 1,000 rows are duplicates of existing (sub_id, type, format) triples. Of these, 39 pairs have inconsistent scores (model gave different answers on re-run). The analysis was computed on the full 7,896-row file, inflating per-format N to ~1,935 instead of 1,724. This means DeepSeek V3.2's accuracy values in analysis_output.json are computed on a slightly inflated N. The effect is small (~tenths of a percent) but is a methodology inconsistency.

### Issue D2: Table 4 (error agreement) cannot be reproduced

The error agreement numbers in Table 4 for DeepSeek V3.2 (all_right=87.3%, all_wrong=0.3%, 1-format-fail=10.2%) cannot be reproduced from the archived raw data. The raw data gives all_right=82.6%, all_wrong=0.9%, 1-format-fail=11.4%. The discrepancy is consistent across all three metrics, suggesting Table 4 was derived from a different (possibly earlier or differently-processed) version of results.

### Issue D3: Basic vs. hard question correlations are directionally inverted

Paper Section 5.2 states: "r=0.89 for basic questions vs r=0.78 for hard questions, confirming format-dependent difficulty." The data shows the opposite: **hard questions (Q6+Q7) produce HIGHER average tetrachoric correlations than basic questions** across all 6 models (hard tgt mean: 0.847; basic tgt mean: 0.809). The numbers 0.89 and 0.78 also cannot be reproduced. This finding is directionally inverted and both numerical values are wrong.

---

## Verdict Details

**Verdict: BLOCKED**

### Blocking Issues (must fix before submission)

**B1 — Hallucinated citation: `charxiv2026`**
The bib entry `charxiv2026` cites "CharXiv-R: Chart Reasoning in the Wild" as a 2026 arXiv paper by "Wang, Yi." This paper does not exist as a separate 2026 publication. CharXiv-R is the reasoning subset of CharXiv (NeurIPS 2024) by **Zirui Wang et al.** The bib must be corrected to cite the actual CharXiv paper (arXiv:2406.18521, NeurIPS 2024, first author Zirui Wang) or removed.

**B2 — 15 bib entries have wrong lead author or significantly wrong title**
This violates ACL/SURGeLLM's three-layer citation policy. The following entries need correction:
- `chartqapro2025`: Ibrahim, Mohanad → **Ahmed Masry**; title missing "Diverse and"
- `graphomni2026`: Li, Hao → **Hao Xu**
- `gracore2025`: Ma, Yuhan → **Zike Yuan**
- `tsaqa2026`: Wang, Xin → **Baoyu Jing** (co-first with Sanhorn Chen)
- `mmtsbench2026`: Zhang, Wei → **Yao Yin**
- `hearts2026`: Kim, Soomin → **Sirui Li**; title wrong
- `zhang2026samecontent`: Zhang, Yilun → **Yue Zhang**; subtitle wrong
- `liu2026formatprior`: Liu, Chen → **Jiacheng Liu**; subtitle wrong; year 2026 → **2025**
- `ho2025formatmatters`: Ho, Thanh → **Xanh Ho**; subtitle wrong
- `ilic2023gfactor`: Ilic, Igor → **David Ilić** (+ co-author Gignac); title completely wrong
- `mmtu2025`: Li, Zheng → **Junjie Xing**; "Multi-Modal" → **"Multi-Task"** (content error)
- `chartmuseum2025`: Park, Jin → **Liyan Tang**
- `torr2026`: Ashury-Tahan, Mahsa → **Shir Ashury-Tahan**; title wrong; year 2026 → **2025**
- `wikimixqa2025`: subtitle wrong
- `datacross2026`: Qi, Zheng → **Ruyi Qi**; title subtitle wrong

**B3 — Correlation values in abstract are wrong**
Abstract states "mean tetrachoric r=0.84 between table, graph, and time series representations." The actual mean across all 6 models from the _averaged matrix is **r=0.87**, not 0.84. The parenthetical "r=0.85 overall" also cannot be reproduced from any straightforward computation. Only "r=0.84 for non-ceiling models" is correct. The abstract's headline correlation values will be trivially fact-checked by any reader inspecting the heatmap.

**B4 — Basic vs. hard correlation claim is directionally inverted (Section 5.2)**
Paper claims basic r=0.89 > hard r=0.78, stating this "confirms format-dependent difficulty." The data shows **hard questions have HIGHER correlations than basic questions** across all models (hard tgt mean 0.847 > basic tgt mean 0.809). The 0.89 and 0.78 values cannot be reproduced. This is a central analytical claim that is factually incorrect.

**B5 — Tier accuracy numbers are wrong (Section 5.3)**
All three tier values are wrong: small 94.2% (data: 97.6%), medium 91.8% (data: 92.2%), large 88.5% (data: 87.7%). The small-tier value matches DeepSeek's medium-tier value, suggesting a table-construction error. The tier direction (decreasing with size) is correct, but all three numbers are wrong.

**B6 — Table 4 error agreement cannot be reproduced from archived data**
The all-right percentage for DeepSeek (87.3%) differs from what raw_results.jsonl computes (82.6%). The source of Table 4 values is unclear. Either the archived data is not the data used in analysis, or there is a computation error. This needs to be resolved and Table 4 regenerated from the canonical data.

**B7 — TSAQA 67.68% claim is misleading (Section 2)**
The 67.68% figure is from LLaMA 3.1-8B (instruction-tuned) on a single sub-task (Temporal Relation comparison). The paper presents it as "fine-tuned LLMs can achieve 67.68% on time series QA," which implies it is a headline overall accuracy. The actual best fine-tuned model in TSAQA achieves ~85% overall. The prose must be corrected to accurately describe what 67.68% represents.

**B8 — Orchestra "achieving >75.3% EM" is inaccurate (Section 2)**
The Orchestra paper states it achieves 72.1% on WikiTQ with small models and "approaches" 75.3% (a prior GPT-4 result). The prose "Orchestra achieving >75.3% EM" misrepresents the paper — 75.3% is not Orchestra's own result, and Orchestra only reaches it (or higher) with larger models in specific configurations. Must be reworded.

**B9 — Author block still anonymous**
`\author{Anonymous}` must be replaced with real author information before camera-ready submission.

### Non-Blocking Issues (should be fixed but not critical)

- `epoch2026`: cited as `arXiv preprint` but is actually a web blog post. Change to `@misc` with URL.
- Fig2 and Fig3 exist as PDF files but are not referenced in the paper (orphaned files; harmless but suggests planned content was cut).
- `charxiv2026` is cited in the Related Work but the underlying CharXiv reasoning component (NeurIPS 2024) is actually relevant and should be properly cited.
- DeepSeek raw data has 1,000 duplicate rows — should be cleaned and analysis re-run for reproducibility.
- The prose claim "DeepSeek gains 24–38%" is accurate. The Discussion paragraph summarizing it as "+30%" is a reasonable approximation but the actual range is 24.2–37.6pp; this phrasing in Section 6 should be checked for accuracy.

---

*Report generated by independent integrity audit sub-agent, 2026-05-11.*
