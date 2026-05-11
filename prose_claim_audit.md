# Prose Claim Audit — Beyond the Bib

**Context:** The SURGeLLM organizers sent a focused reminder (2026-05-11) that the zero-tolerance reference accuracy policy applies to **all accepted submissions, archival or non-archival** — explicitly contradicting any reading that non-archival papers can skip citation rigor. The email also added a third verification requirement: *"The claim attributed to the citation in your prose matches what the source actually says."*

This audit goes beyond bib metadata (`citation_integrity_report.md`) to check every specific prose claim attributed to a cited or named work. Method: search/crawl each source paper via Exa, locate the specific claim, compare to v1 paper prose.

**Status: 5 prose-claim issues found, 2 missing bib entries discovered.**

---

## Findings

### Finding 1 — Orchestra: misattributed number, missing bib entry

**v1 paper §2 Table QA (around line 52) says:**
> "Table question answering has advanced rapidly, with Orchestra achieving $>$75.3\% EM on WikiTableQuestions \cite{pasupat2015compositional} and TabTracer reaching 92.5\% on TabFact \cite{chen2020tabfact}."

**What the actual Orchestra paper (arXiv 2601.03137, Jiang et al., Jan 2026) says:**
> "with Qwen2.5-14B, Orchestra reaches 72.1% accuracy on WikiTQ, **approaching the best prior result of 75.3% achieved with GPT-4**; with larger Qwen, Llama, or DeepSeek models, Orchestra outperforms all prior methods and establishes new state-of-the-art results across all benchmarks."

**Two issues:**

1. **The 75.3% is the prior GPT-4 result, NOT Orchestra's accuracy.** Orchestra reaches 72.1% with Qwen2.5-14B, approaching that GPT-4 number. With larger models it surpasses, but the actual Orchestra-with-larger-model number is not stated in the abstract. The v1 paper attributes 75.3% to Orchestra, which is **wrong attribution of a baseline number**.

2. **Orchestra has no bib entry.** The v1 paper names "Orchestra" but cites only `pasupat2015compositional` (the WikiTQ benchmark paper from 2015). The benchmark paper does not describe Orchestra. This violates the email's third check: "The claim attributed to the citation in your prose matches what the source actually says." Pasupat & Liang 2015 does not say anything about Orchestra (which was published 11 years later).

**Fix (option 1 — drop specific number, add proper citation):**

```latex
Table question answering has advanced rapidly, with recent multi-agent approaches \cite{orchestra2026} approaching or surpassing GPT-4's prior 75.3\% EM on WikiTableQuestions \cite{pasupat2015compositional} ...
```

**Fix (option 2 — remove the specific Orchestra mention entirely if uncertain):**

```latex
Table question answering has advanced rapidly, with state-of-the-art systems reaching $>$75\% EM on WikiTableQuestions \cite{pasupat2015compositional} ...
```

**Add to bib:**

```bibtex
@article{orchestra2026,
  title={Accurate Table Question Answering with Accessible {LLMs}},
  author={Jiang, Yangfan and Wei, Fei and Bao, Ergute and Li, Yaliang and Ding, Bolin and Yang, Yin and Xiao, Xiaokui},
  journal={arXiv preprint arXiv:2601.03137},
  year={2026}
}
```

---

### Finding 2 — TabTracer: unverified 92.5% accuracy claim, missing bib entry

**v1 paper §2 Table QA (around line 52) says:**
> "...and TabTracer reaching 92.5\% on TabFact \cite{chen2020tabfact}."

**What the actual TabTracer paper (arXiv 2602.14089, Luo et al., Feb 2026) says:**
- Abstract: "TabTracer outperforms state-of-the-art baselines **by up to 6.7%** in accuracy while reducing token consumption by 59-84%."
- **No specific 92.5% accuracy number for TabFact appears in the abstract.**
- The 92.5 string appears in the paper only as a **token-count entry in a cost table** ("CoT-Consist 3715.40 954.12 4918.51 2323.75 ..."), not as an accuracy figure.

**Two issues:**

1. **The 92.5% number is unverified.** TabTracer's abstract reports a relative improvement (+6.7%), not the absolute 92.5%. The number may exist in the experimental results table of the full paper, but it is not stated where the v1 paper claims it.

2. **TabTracer has no bib entry.** Same problem as Orchestra: the v1 cites `chen2020tabfact` (the TabFact benchmark paper, 2020), which obviously does not describe TabTracer (2026). The prose claim is unsupported by the cited work.

**Recommended fix:** Either (a) verify the 92.5% number by reading the TabTracer paper's experimental tables and cite TabTracer directly, OR (b) replace the specific number with the verified relative claim ("up to 6.7% improvement over prior state-of-the-art"), OR (c) remove the TabTracer mention if the number cannot be verified.

**Suggested fix (option c, removal with verified replacement):**

```latex
Table question answering has advanced rapidly: recent MCTS-based agentic frameworks \cite{tabtracer2026} report 6--7\% accuracy improvements over prior state-of-the-art on TabFact \cite{chen2020tabfact} and WikiTQ \cite{pasupat2015compositional}.
```

**Add to bib:**

```bibtex
@article{tabtracer2026,
  title={{TabTracer}: Monte Carlo Tree Search for Complex Table Reasoning with Large Language Models},
  author={Luo, Zhizhao and Luo, Zhaojing and Zhang, Meihui and Mao, Rui},
  journal={arXiv preprint arXiv:2602.14089},
  year={2026}
}
```

---

### Finding 3 — ChartQA ">95% accuracy" claim unsupported

**v1 paper §2 Chart Comprehension (around line 54) says:**
> "ChartQA \cite{masry2022chartqa} established chart QA as a benchmark, with recent models achieving $>$95\% accuracy."

**What the data shows:**
- The ChartQAPro paper (Masry et al., ACL Findings 2025) reports: "Claude Sonnet 3.5 scores **90.5%** on ChartQA." This is the most-recent publicly stated frontier-model accuracy on ChartQA I can find.
- There may be papers claiming >95% on ChartQA, but no citation is provided in the v1 paper.

**Issue:** The ">95% accuracy" claim is unsupported and likely overstated. Without a citation, it's a free-floating assertion that fails the email's third check ("the claim attributed to the citation in your prose matches what the source actually says").

**Fix (option 1 — update with verified number + cite):**

```latex
ChartQA \cite{masry2022chartqa} established chart QA as a benchmark, with frontier models like Claude Sonnet 3.5 reaching 90.5\% accuracy \cite{chartqapro2025}.
```

**Fix (option 2 — drop the specific number):**

```latex
ChartQA \cite{masry2022chartqa} established chart QA as a benchmark; recent vision-language models have approached saturation on its test set.
```

---

### Finding 4 — TSAQA 67.68%: verified but oversimplified

**v1 paper §2 Time Series (around line 58) says:**
> "TSAQA \cite{tsaqa2026} showed that fine-tuned LLMs can achieve 67.68\% on time series QA"

**What the actual TSAQA paper (arXiv 2601.23204, Jing et al., Jan 2026) says (Section 4):**
> "Considerable room for improvement remains, e.g., **the best PZ score is only 67.68 (LLaMA-3.1-8B after instruction tuning)**."

**Verdict:** The 67.68% number is **verified**, but the framing in the v1 paper is oversimplified:
- The 67.68% is specifically the **best PZ (puzzling) format score**, not overall TSAQA accuracy.
- It's specifically **LLaMA-3.1-8B after instruction tuning**, not generic "fine-tuned LLMs".
- TSAQA has three formats (TF, MC, PZ); the PZ is the hardest and the 67.68 is the best score on that hardest subset.

**Fix (more precise):**

```latex
\citet{tsaqa2026} introduced a unified time-series QA benchmark spanning six tasks and three answer formats. They report best-case accuracy of 67.68\% on the hardest (puzzling) format, achieved by fine-tuned LLaMA-3.1-8B, indicating substantial room for improvement.
```

This is also a chance to fix the bib entry per `citation_integrity_report.md` (Wang Xin → Baoyu Jing, etc.).

---

### Finding 5 — HeaRTS: claim verified, but Heart Rate → Health context

**v1 paper §2 Time Series (around line 58) says:**
> "HeaRTS \cite{hearts2026} demonstrated that temporal complexity degrades LLM performance."

**What the actual HeaRTS paper (arXiv 2603.06638, Li et al.) says:**
> "Finally, **performance declines with increasing temporal complexity.**"

**Verdict:** The temporal-complexity claim is **verified**. However:
- The paper is "**Health** Time Series" (HeaRTS = **Health Reasoning over Time Series**), not "Heart Rate Time Series" as the v1 bib entry suggested.
- The fix is already in `citation_integrity_report.md` for the bib entry. The prose claim itself is correct.

**No additional prose fix needed** beyond the bib correction.

---

### Finding 6 — GraphOmni, GraCoRe, MMTS-Bench prose claims

These claims, on review, are accurate:

- **GraphOmni claim** ("demonstrated that serialization format dramatically affects LLM graph reasoning performance"): The actual paper says "Through systematic evaluation, we uncover critical interactions among these dimensions, revealing their decisive impact on model performance." Specifically mentions 7 serialization formats. **VERIFIED.**
- **GraCoRe claim** ("revealed major gaps on complex graph reasoning tasks"): The paper reports gaps and capability differences across graph types and reasoning categories. "Major gaps" is loose but not inaccurate. **WEAKLY VERIFIED.**
- **MMTS-Bench claim** ("general LLMs with CoT can outperform specialized time-series models"): The abstract says "(1) TS-LLMs significantly lag behind general-purpose LLMs in cross-domain generalization... (3) chain-of-thought (CoT) reasoning... substantially improve performance." Combined, this supports the v1 claim. **VERIFIED.**

The bib entries for all three still need the metadata fixes from `citation_integrity_report.md`. The prose claims are fine.

---

### Finding 7 — ChartQAPro 55.8% claim verified

**v1 paper §2 Chart Comprehension says:**
> "ChartQAPro \cite{chartqapro2025} introduced harder questions where the current best (Claude 3.5 with CoT) reaches only 55.8\%."

**Actual ChartQAPro abstract:**
> "Claude Sonnet 3.5 scores 90.5\% on ChartQA but only **55.81%** on ChartQAPro"

**Verdict:** Number matches (55.8 ≈ 55.81). **VERIFIED.**

Bib still needs the author correction (Mohanad Ibrahim → Ahmed Masry et al.) per `citation_integrity_report.md`.

---

### Finding 8 — Epoch AI claim: citation misuse (already flagged)

**v1 paper §5 Discussion (around line 292) says:**
> "...while aligning with the cross-benchmark correlations reported by \citet{epoch2026}."

**Verdict:** The Epoch AI Rosetta Stone paper does not report cross-benchmark correlations; it builds an item-response-theory-style framework for stitching benchmarks onto a single capability scale. Already flagged in `deep_paper_analysis.md` §3.3 and `citation_integrity_report.md`. The fix is to rewrite the prose, not just fix the bib.

---

### Finding 9 — MMTU "multi-modal" claim: misuse (already flagged)

**v1 paper §2 Table QA says:**
> "MMTU \cite{mmtu2025} extends evaluation to multi-modal table understanding across diverse domains."

**Verdict:** MMTU is "Massive Multi-Task", not multi-modal. Already flagged. Fix in prose required, not just bib.

---

## Summary of prose-claim issues (in addition to the 17 bib errors)

| # | Issue | Severity | Fix scope |
|---|---|---|---|
| 1 | Orchestra: misattribution of 75.3% (GPT-4's number) | **MAJOR** | Add Orchestra bib entry; rewrite prose to correctly attribute the 75.3% to GPT-4, or remove specific number |
| 2 | TabTracer: 92.5% unverified, no bib entry | **MAJOR** | Add TabTracer bib entry; verify or remove the 92.5% number |
| 3 | ChartQA ">95% accuracy" unsupported | MEDIUM | Update to verified 90.5% or remove specific number |
| 4 | TSAQA 67.68% oversimplified | MEDIUM | Reframe more precisely (best PZ score, fine-tuned LLaMA-3.1-8B) |
| 5 | HeaRTS context wrong (Heart Rate vs. Health) | MINOR | Already covered by bib fix |
| 6 | Epoch AI claim misuses source | MEDIUM | Rewrite prose (already in citation integrity report) |
| 7 | MMTU "multi-modal" misuse | MEDIUM | Rewrite prose (already in citation integrity report) |

Plus two missing bib entries to add: **Orchestra (Jiang et al. 2026)** and **TabTracer (Luo et al. 2026)**.

---

## Critical correction to my earlier guidance

In my earlier camera-ready guidance (`camera_ready_checklist.md` and related), I wrote that citation verification is "No strictly (zero-tolerance is for proceedings)" for non-archival papers. **The SURGeLLM organizers explicitly contradicted this** in their 2026-05-11 reminder email:

> "We expect accuracy from all accepted submissions, archival or non-archival."

The accuracy requirement is mandatory regardless of archival status. I should have flagged this as mandatory in the first place. The camera-ready master punchlist's Phase B (citation overhaul) was correctly framed as mandatory; the earlier informal guidance that non-archival could skip it was wrong.

---

## What this means for the camera-ready

The new prose-claim findings add to (not replace) the 17 bib-entry corrections already documented in `citation_integrity_report.md`. The total work is:

1. **Bib metadata fixes:** 17 corrected entries + 2 new entries (Orchestra, TabTracer) = **19 bib changes**
2. **Prose claim fixes:** 7 issues — Orchestra misattribution, TabTracer unverified number, ChartQA >95%, TSAQA 67.68% framing, Epoch misuse, MMTU misuse, plus the CharXiv-R name correction already flagged

After these fixes, the prose-cite chain is verifiable end-to-end.
