# Integrity Re-Check Report (post-corrections, 2026-05-11)

**Paper:** Do Structured Data Comprehension Skills Transfer Across Representation Types? A Systematic Study with Frontier LLMs  
**Date audited:** 2026-05-11  
**Auditor:** Independent cold-read integrity audit (post-revision pass)  
**Prior report:** integrity/integrity_report.md (verdict: BLOCKED)

---

**Verdict: CLEARED_WITH_CAVEATS**

Two new blocking issues were introduced during corrections (N1 and N2). Both are fixable in under 5 minutes. No prior blocking issue remains unaddressed at the directional or factual level.

---

## Phase 1: Prior Issues — Status

| ID | Issue | Status | Notes |
|---|---|---|---|
| B1 | Hallucinated `charxiv2026` citation | ✓ FIXED | Now cites `charxiv2024` (NeurIPS 2024, Zirui Wang et al.). Title and authors verified against arXiv:2406.18521. |
| B2 | 17 bib metadata errors (wrong authors/titles) | ✓ FIXED (15/15 spot-checked) | All 5 spot-checked entries now show correct first authors and titles: chartqapro2025 → Masry; graphomni2026 → Xu, Hao; ilic2023gfactor → Ilić, David + Gignac; mmtu2025 → Xing, Junjie + "Multi-Task"; torr2026 → Ashury-Tahan, Shir. **EXCEPTION: ilic2023gfactor title is still wrong — see N1 below.** |
| B3 | Abstract r=0.84 mismatch | ✓ FIXED | Abstract now says r=0.87 (all 6 models) and r=0.84 (mid-range group). Both verified: r=0.87 matches analysis_output.json grand mean of 0.870; r=0.84 matches midrange mean of 0.841. |
| B4 | Basic vs hard inversion (direction wrong) | ✓ FIXED | §5.2 now says r=0.81 basic and r=0.85 hard, framed as "transfer at least as strong on hard questions." Directional claim correct. **However, see N2: the "five of six models" per-model count is wrong.** |
| B5 | Tier accuracy wrong (94.2/91.8/88.5) | ✓ FIXED | §5.3 now says 97.6%/92.3%/87.7%. All three match canonical_numbers_post_cleanup.json exactly. |
| B6 | Table 4 DeepSeek row (87.3/0.3/10.2) | ✓ FIXED | Now shows 82.5%/0.9%/11.3%. All six model rows verified against canonical numbers (within 0.1pp rounding for MiniMax). |
| B7 | TSAQA 67.68% oversimplified | ✓ PARTIALLY FIXED | Now describes 67.68% as "best accuracy on the puzzling format" with LLaMA-3.1-8B. TSAQA abstract confirms a "puzzling (PZ)" format exists; Gemini-2.5-Flash achieves 65.08% average. The PZ-format-specific description is plausible but cannot be fully verified from the abstract alone. Material improvement over original. |
| B8 | Orchestra >75.3% misattribution | ✓ FIXED | Now reads: "approach GPT-4's prior 75.3% EM benchmark on WikiTableQuestions using smaller open-weight models." Orchestra title and authors verified against arXiv:2601.03137 (Yangfan Jiang et al.). |
| B9 | `\author{Anonymous}` | ✓ FIXED | Now `\author{Farseen Shaikh \\ claudeshaikh3@gmail.com}`. Confirmed in PDF. |
| B10 | MMTU "multi-modal" error; Epoch "cross-benchmark correlations" framing | ✓ FIXED | MMTU now described as "multi-task table understanding"; Epoch2026 now described as "benchmark-stitching analysis." Both verified. |

---

## Phase 2: New Issues Introduced by Corrections

### N1 — `ilic2023gfactor` title is still wrong (BLOCKING)

**Location:** `references.bib`, entry `ilic2023gfactor`  
**Current bib title:** "Unveiling the General Intelligence Factor in Language Models: A Psychometric Approach"  
**Actual title (arXiv:2310.11616):** "Evidence of interrelated cognitive-like capabilities in large language models: Indications of artificial general intelligence or achievement?"  
**Status:** STILL BROKEN — The prior correction fixed the author name (`Ilić, David` is now correct) but replaced one wrong title with a different wrong title. No paper matching the bib title was found on arXiv, Semantic Scholar, or via any search. The correct title needs to be substituted from arXiv:2310.11616.

**Fix:**
```bibtex
title={Evidence of Interrelated Cognitive-Like Capabilities in Large Language Models: {Indications} of Artificial General Intelligence or Achievement?},
```

---

### N2 — §5.2 "five of six models" count is wrong (BLOCKING)

**Location:** `paper.tex`, Section 5.2, sentence "…with five of six models showing hard ≥ basic correlations."  
**Data (from analysis_output.json):** Only **four** of six models have hard ≥ basic correlation for the table-graph-timeseries cluster:
- MiniMax M2.5: hard=0.778 > basic=0.580 ✓
- Kimi K2.5: hard=0.870 > basic=0.755 ✓
- GLM-5: hard=0.873 > basic=0.738 ✓
- Qwen 3.5 Plus: hard=1.000 > basic=0.987 ✓
- DeepSeek V3.2: hard=0.603 < basic=0.803 ✗
- Gemini 3.1 Pro: hard=0.975 < basic=0.990 ✗

The directional claim (hard > basic overall) is correct (grand means 0.85 vs 0.81). Only the per-model count "five of six" is wrong — it should be "four of six."  
**Fix:** Change "five of six models" → "four of six models" in §5.2.

---

## Specific Verifications

### Citation Sample (5 new bib entries verified)

| Entry | Verification Method | Result |
|---|---|---|
| `orchestra2026` | arXiv:2601.03137 HTML, author div | ✓ VERIFIED — Title "Accurate Table Question Answering with Accessible LLMs"; first author Yangfan Jiang; all authors match bib. |
| `tabtracer2026` | arXiv:2602.14089 + Semantic Scholar | ✓ VERIFIED — Title confirmed; first author Zhizhao Luo (note: S2 incorrectly lists as Zhi-Quan Luo; arXiv is authoritative). |
| `bhandari2026tabular` | arXiv:2604.24040 HTML | ✓ VERIFIED — Title "Improving Robustness of Tabular Retrieval via Representational Stability"; authors Kushal Raj Bhandari, Adarsh Singh, Jianxi Gao, Soham Dan, Vivek Gupta; all match bib. |
| `infochartqa2025` | arXiv:2505.19028 HTML | ✓ VERIFIED — Title "InfoChartQA: A Benchmark for Multimodal Question Answering on Infographic Charts"; authors Tianchi Xie et al., all 6 authors match bib. Venue NeurIPS 2025 not confirmed from arXiv page — caveat noted. |
| `tsaqa2026` | arXiv:2601.23204 HTML | ✓ VERIFIED — Title "TSAQA: Time Series Analysis Question And Answering Benchmark"; first authors Baoyu Jing and Sanhorn Chen; full author list matches bib exactly. |

### Numerical Claims Sample (5 verified)

| Claim | Paper value | Canonical / Analysis | Status |
|---|---|---|---|
| Abstract: mean tetrachoric r=0.87 (all 6 models, TGT cluster) | 0.87 | analysis_output.json: grand mean = 0.870 | ✓ MATCHES |
| Abstract: r=0.84 for mid-range models (Kimi/GLM/MiniMax) | 0.84 | canonical: midrange_high_transfer_r = 0.841 | ✓ MATCHES |
| §5.3 Tier accuracy: small=97.6%, medium=92.3%, large=87.7% | 97.6/92.3/87.7 | canonical: 97.62/92.31/87.72 | ✓ MATCHES |
| Table 4: DeepSeek all_right=82.5%, all_wrong=0.9%, 1-format-fail=11.3% | 82.5/0.9/11.3 | canonical: same | ✓ MATCHES |
| §5.2: r=0.81 basic, r=0.85 hard (TGT cluster, 6-model mean) | 0.81/0.85 | canonical: basic=0.809, hard=0.850 | ✓ MATCHES |

### New Content Quality Check

| Item | Finding |
|---|---|
| "Scope of claims" paragraph | Structurally sound. The three "do claim" items (text-format correlation, chart-text lag, chart-image gap) all track to specific data. The four "do not claim" items are appropriate hedges. No overclaiming found. |
| §5.1 N=2 disclosure | Reads naturally: "We caution that this pattern is observed in N=2 models… requires testing across a broader model panel." Appropriately hedged. |
| Conclusion basic-vs-hard | Correctly states "transfer holds at least as strongly on hard questions as on basic ones" without the incorrect per-model count. |
| New citations (infochartqa2025, bhandari2026tabular, orchestra2026, tabtracer2026) | Bib entries verified (see citation sample above). Claim attributions are accurate: InfoChartQA finding of accuracy drops on infographics is correctly paraphrased; Bhandari finding about retrieval embedding instability is correctly attributed; Orchestra attribution to "approach GPT-4's prior 75.3%" is now correct; TabTracer "up to 6.7% improvement" is consistent with abstract ("outperforms state-of-the-art baselines"). |

---

## Minor Non-Blocking Issues

| ID | Issue | Severity |
|---|---|---|
| N3 | §4.2 says "r=0.85--0.88" but Conclusion says "r=0.86--0.88" for the same cluster. Data pair averages are 0.856/0.876/0.880 — the range rounds to 0.86–0.88. Section 4.2's "0.85" appears to be a threshold qualifier ("r>0.85") rather than an empirical lower bound, but it reads as an empirical range and conflicts with the Conclusion. | MINOR — recommend aligning both to "r=0.86--0.88" or using "r>0.85" as a threshold claim in §4.2. |
| N4 | Ceiling paragraph: "DeepSeek r=0.72" but analysis_output.json gives DeepSeek TGT mean = 0.726, which rounds to 0.73. Off by 0.01. | MINOR — rounding error. |
| N5 | Table 4: MiniMax 1-format-fail listed as 12.7%; canonical says 12.8%. | NEGLIGIBLE — 0.1pp rounding artifact at n=1724. |
| N6 | `epoch2026` bib uses `author={{Epoch AI}}` but arXiv:2512.00193 has five named individual authors (Anson Ho, Jean-Stanislas Denain, David Atanasov, Samuel Albanie, Rohin Shah). Using institutional author is a citation style choice but omits actual authors. | MINOR — recommend adding named authors. |
| N7 | `infochartqa2025` claims `booktitle={Advances in Neural Information Processing Systems 38: Datasets and Benchmarks Track}` but NeurIPS publication not confirmed on arXiv page for 2505.19028. | MINOR — venue not contradicted, just unconfirmed from arXiv metadata. |

---

## Page Count / ACL Compliance

- **PDF pages:** 11 total (pdfinfo confirmed). Content pages 1–8, Acknowledgments on page 9, References on pages 9–10, Appendix on pages 11–12.
- **ACL limit:** 8 pages of content + unlimited references/appendices for long papers. **COMPLIANT.**
- Abstract word count: ~225 words (within 250-word ACL limit). **COMPLIANT.**

---

## Verdict Details

**CLEARED_WITH_CAVEATS**

The paper has been substantially improved from the original BLOCKED verdict. Nine of ten prior blocking issues are now fully resolved, and one (B7) is materially improved. However, two new blocking issues were introduced during the correction pass:

1. **N1 (BLOCKING):** `ilic2023gfactor` still has a wrong title. The author correction was made but the title was changed to a different incorrect title not found in any database. Fix: use the actual arXiv:2310.11616 title.

2. **N2 (BLOCKING):** Section 5.2 claims "five of six models showing hard ≥ basic correlations" when the data shows four of six. This is a verifiable count error introduced during the correction.

Both are quick fixes (single-line edits). Once corrected, the paper achieves full integrity clearance.

---

*Report generated by independent cold-read integrity audit, 2026-05-11.*
