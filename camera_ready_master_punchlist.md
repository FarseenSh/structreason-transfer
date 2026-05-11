# Camera-Ready Master Punch-List

**Purpose:** the single sequential list of every concrete edit, fix, addition, and audit needed to make `paper.tex` a defensible, publishable, reproducible artifact — regardless of which window is in play. This is the "make the paper as good as it can be" file.

**Scope:** everything that improves the v1 paper *without requiring new compute beyond what we already have, plus a few small targeted ablations*. Items that require substantial new compute or new experiments (expanded model panel, real-world data extension, human study, full reasoning ablation, prompt sensitivity, semantic-edge graph) live in `v2_master_plan.md` and are explicitly excluded here.

**File references:**
- `paper/paper.tex` — current v1 manuscript
- `paper/references.bib` — bib file with 17 metadata errors + 2 missing entries
- `experiments/results/analysis_output.json` — raw correlation data already computed (NOTE: this file was computed on inflated DeepSeek N — see Phase 0 below; the file must be regenerated before Layer 2 fixes)
- `reviews/reviews.md` — verbatim reviewer text
- `reviews/reference_accuracy_reminder_email.md` — SURGeLLM organizers' 2026-05-11 reminder confirming the zero-tolerance reference policy applies to ALL submissions (archival and non-archival)
- `integrity/integrity_report.md` — independent cold-read integrity audit (2026-05-11) — VERDICT: BLOCKED
- `deep_paper_analysis.md` — methodological audit
- `citation_integrity_report.md` — corrected bib entries
- `prose_claim_audit.md` — prose-claim issues beyond the bib (Orchestra misattribution, TabTracer unverified number, ChartQA ">95%", etc.)
- `v2_master_plan.md` — what's NOT in scope here

This file consolidates inputs from all of the above into a dependency-ordered punch-list with specific line references and exact text changes.

## CORRECTION TO EARLIER GUIDANCE (2026-05-11)

Two corrections to earlier guidance, both received on 2026-05-11:

1. **SURGeLLM organizers' email** confirmed that reference accuracy is **mandatory for all accepted submissions, archival or non-archival**. Any earlier informal guidance suggesting non-archival papers could skip the citation verification step was wrong. Phase C (citation overhaul, formerly Phase B) is non-optional regardless of the archival selection. The third verification check from the email — "the claim attributed to the citation in your prose matches what the source actually says" — adds prose-level scrutiny on top of bib-metadata verification.

2. **Independent integrity-check sub-agent audit** (`integrity/integrity_report.md`) found four substantive scientific errors and one data-integrity issue that no human reviewer or earlier audit caught:
   - **D1**: DeepSeek `raw_results.jsonl` has 1,000 duplicate rows; 44 of those duplicates have inconsistent scores (the model returned different answers on re-runs). Analysis was computed on inflated N=7,896 instead of the expected N=6,896.
   - **B3**: Abstract claim "r=0.84 between table, graph, and time series" doesn't match the computed value (0.869 across all 6 models). The 0.84 is actually the *mid-range-only* mean; the abstract conflates two different averagings.
   - **B4**: Section 5.2 basic-vs-hard correlation direction is **inverted**. Paper says basic r=0.89 > hard r=0.78. Actual data: basic r=0.809, hard r=**0.847**. Hard transfer is *higher* than basic, opposite of what the paper claims.
   - **B5**: Section 5.3 tier accuracy values are all wrong. Paper says small 94.2%, medium 91.8%, large 88.5%. Actual: small **97.6%**, medium **92.2%**, large **87.7%**.
   - **B6**: Table 4 (error agreement) values cannot be reproduced from archived raw data. DeepSeek all-right: paper 87.3% vs data 82.6%.

   These data and number issues require fixing *before* any prose edits, because the prose fixes depend on knowing the correct numbers. **The phase ordering is therefore: Phase 0 (data cleanup + re-analysis) → Phase A (foundation) → Phase B (paper number corrections from clean data) → Phase C (citation overhaul) → Phase D (reviewer-driven writing) → Phase E (re-analyses on existing data) → Phase F (small ablations) → Phase G (pre-submit audit) → Phase H (upload).**

---

## Phase 0 — Data integrity cleanup and re-analysis (CRITICAL, no compute except local re-analysis)

The independent integrity audit found that the raw experimental data and the analysis derived from it both contain issues that must be resolved before any paper text is edited. This is a one-time cleanup that produces a regenerated `analysis_output.json` we can trust.

### 0.1 Deduplicate DeepSeek raw results

`experiments/results/deepseek-v3.2/raw_results.jsonl` currently has 7,896 rows. Expected: 6,896 (1,724 questions × 4 text formats). Excess: 1,000 duplicate rows on `(sub_id, qtype, format)` triples, of which 44 have inconsistent scores.

- [ ] Back up the current file: `cp deepseek-v3.2/raw_results.jsonl deepseek-v3.2/raw_results.jsonl.bak-2026-05-11`
- [ ] For each duplicated `(sub_id, qtype, format)` triple, decide a policy. Recommended: keep the **first occurrence** (chronological earliest). For inconsistent-score pairs, this means whichever judgment the model produced on the first run.
- [ ] Alternative policy (if first-occurrence isn't right): for the 44 inconsistent-score pairs, mark them as "uncertain" and exclude from the analysis (treat as missing). For the 956 consistent-score duplicates, the policy is irrelevant (both rows are identical).
- [ ] Write the deduplicated file: `deepseek-v3.2/raw_results.jsonl` (or a parallel `raw_results.dedup.jsonl`).
- [ ] Verify: `wc -l` should report exactly 6,896 (or fewer if any inconsistent pairs are excluded).
- [ ] Document the policy choice in a brief `experiments/results/deepseek-v3.2/DEDUP_NOTES.md` so the v2 paper can reference it.

### 0.2 Re-run analysis on the cleaned data

- [ ] Re-run `experiments/code/analyze.py` against the deduplicated DeepSeek file (plus all other models, which are already clean) to regenerate `analysis_output.json`.
- [ ] Verify by checking DeepSeek per-format N values in the new `analysis_output.json`: should now show n=1724 per format, not n≈1935.
- [ ] Save the regenerated file. Keep the old version as `analysis_output.json.bak-2026-05-11` for traceability.

### 0.3 Audit other models for similar duplicate issues

- [ ] For each of the 8 model directories (gemini-31-pro, gemini-31-pro-nothinking, deepseek-v3.2, deepseek-v3.2-noreasoning, glm-5, kimi-k2.5, minimax-m2.5, qwen3.5-plus), count lines vs unique (sub_id, qtype, format) triples.
- [ ] Expected line counts: 8,620 for vision-enabled models (Kimi, Qwen, Gemini — 5 formats including chart_image), 6,896 for non-vision (4 text formats only). DeepSeek-no-reasoning and Gemini-no-thinking should match their main counterparts.
- [ ] If any other model has duplicates, deduplicate and re-run analysis.

### 0.4 Resolve the Table 4 (error agreement) discrepancy

The paper reports DeepSeek error-agreement values (all_right=87.3%, all_wrong=0.3%, 1-format-fail=10.2%) that cannot be reproduced from `raw_results.jsonl` (which gives 82.6%, 0.9%, 11.4%). Either there is a computation pipeline that produced the paper's numbers that isn't in the current codebase, or the paper's numbers are stale and the data is canonical.

- [ ] Search the codebase for any error-agreement-computation function: `grep -r "all_right\|all_wrong\|error_agree\|1.format" experiments/code/`
- [ ] If found, run it against the clean data and compare. The clean-data answer becomes canonical for Table 4.
- [ ] If not found, regenerate Table 4 from clean `raw_results.jsonl` using a fresh computation (per-question grouping across the 4 text formats per model; classify each question as all_right / all_wrong / 1-format-fail / 2-format-fail / 3-format-fail).
- [ ] Document the canonical computation in `experiments/code/analyze.py` so it's reproducible.

### 0.5 Record the canonical numbers for use in Phase B

After Phase 0 completes, document the canonical values that need to flow into the paper text:

- [ ] Per-model per-format accuracy (Table 2): document any change from current `analysis_output.json` (DeepSeek values likely shift by tenths of a percent).
- [ ] Mean tetrachoric r for table-graph-timeseries across all 6 models: should now be the post-cleanup value (was 0.869 pre-cleanup).
- [ ] Mid-range (Kimi, GLM-5, MiniMax) high-transfer cluster mean.
- [ ] Basic vs hard correlation values (table-graph-timeseries pairs).
- [ ] Tier accuracy values (small, medium, large) averaged across 6 models × 4 text formats.
- [ ] Table 4 error-agreement values per model.
- [ ] Reasoning ablation deltas (DeepSeek ±, Gemini ±).

These will be the source of truth for Phase B prose updates.

---

## Phase A — Foundation (zero compute, zero risk)

### A.1 Git cleanup and snapshot

Currently only `experiments/experiment-plan.md` and `sota/sota-report.md` are committed. Everything else (paper, code, results, figures) is untracked.

- [ ] `git add` the experiment code, data, results, figures, paper artifacts
- [ ] Audit for secrets before committing: `grep -r "sk-\|API_KEY\|BEARER" --include="*.py" --include="*.json" --include="*.md" .`
- [ ] Verify `.env` is in `.gitignore` and never committed historically: `git log --all --full-history -- .env`
- [ ] Commit current v1 state with descriptive message
- [ ] Tag `v1.0-surgellm` to pin the SURGeLLM artifact
- [ ] Create `v2/main` branch for v2 work — keep `main` as the SURGeLLM-stable branch

### A.2 Public GitHub repo

- [ ] Create public repo (e.g., `farseen/structreason-transfer`)
- [ ] Push `main` and the `v1.0-surgellm` tag
- [ ] Add `LICENSE` (MIT or Apache-2.0 for code; CC-BY-4.0 for data)
- [ ] Add top-level `README.md`:
 - install (Python 3.11, requirements.txt)
 - data download / regeneration
 - per-provider runner commands
 - figure regeneration commands
 - reproducibility note
 - citation block
- [ ] Pin `requirements.txt` to specific versions
- [ ] Add `scripts/reproduce_all.sh` that regenerates every figure from scratch

### A.3 Zenodo / Hugging Face dataset archive

- [ ] Bundle the 250 sub-tables, 1,724 questions, 5-format renderings as a release artifact
- [ ] Decide on archive: Zenodo (DOI) or HF Datasets (handle)
- [ ] Include format-generation scripts so the dataset is regeneratable from raw datasets
- [ ] Include `raw_results.jsonl` per model so other researchers can re-score without re-running

### A.4 Replace "released upon publication" with concrete URL

`paper.tex` line 313: `All code, data, and prompts will be released upon publication.`

- [ ] Replace with: `All code, data, prompts, and raw model outputs are released at \url{https://github.com/<user>/structreason-transfer} (archive DOI: \url{https://doi.org/...}).`

---

## Phase B — Paper number corrections from clean re-analysis (CRITICAL)

After Phase 0 produces a regenerated `analysis_output.json`, the following numbers in `paper.tex` must be updated. Each item is keyed to the integrity-report finding it addresses.

### B.0 Abstract correlation value (integrity B3)

`paper.tex` lines 23-29 (abstract):

- v1 abstract: `"with mean tetrachoric r=0.84 between table, graph, and time series representations (r=0.85 overall; r=0.84 for non-ceiling models, confirming the result is not an artifact of high accuracy)"`
- Two issues: (1) the "r=0.84 between table, graph, and time series" actually equals the **mid-range subset mean (0.841)**, not the all-6-model mean (0.869); (2) the parenthetical "r=0.85 overall" cannot be cleanly reproduced.

**Fix (option 1 — be precise about which average is which):**

```
"with mean tetrachoric r=0.87 across all six models for table-graph-timeseries pairs (mid-range subset: r=0.84, confirming the result is not an artifact of ceiling effects in the highest-accuracy models)"
```

**Fix (option 2 — drop the conflated parenthetical):**

```
"with mean tetrachoric r=0.87 between table, graph, and time series representations across all six models (r=0.84 for the three mid-range models, confirming the finding is not an artifact of near-ceiling accuracy)"
```

Choose based on what the canonical post-cleanup r value actually is.

### B.1 Section 5.2 basic-vs-hard direction inversion (integrity B4)

`paper.tex` §5.2 around line 281:

- v1: `"The averaged tetrachoric correlation for text formats on basic questions is r=0.89, compared to r=0.78 for hard questions. Transfer remains strong even on hard questions but weakens, suggesting that multi-step reasoning introduces format-dependent difficulty."`
- The data shows the **opposite direction**: hard r=0.847 > basic r=0.809 for table-graph-timeseries pairs.

**Fix (assuming the post-cleanup data preserves the inversion):**

```
"The averaged tetrachoric correlation for the table-graph-timeseries cluster is r=0.81 on basic questions (Q1-Q5) and r=0.85 on hard questions (Q6-Q7). Contrary to our initial expectation that multi-step reasoning would introduce format-dependent difficulty, transfer is at least as strong on hard questions as on basic ones — suggesting that the cross-format shared capability includes the compositional reasoning required by Q6 (multi-hop) and Q7 (conditional aggregation), not just basic data extraction."
```

This is a *stronger* claim than the v1 framing — instead of the result weakening on hard questions, it holds or strengthens. The Discussion section may need a corresponding update.

### B.2 Section 5.2 follow-up paragraph (Q7-specific correlation values)

`paper.tex` §5.2 around line 283:

- v1: `"On Q7 specifically---the hardest question type---mid-range models show r=0.60-0.72 for table-graph-timeseries pairs and r=0.35-0.56 for chart text pairs."`

These numbers were derived from the inflated DeepSeek data and the original computation. Recompute from clean data and update.

- [ ] Recompute Q7-specific tetrachoric correlations for the mid-range models (Kimi, GLM-5, MiniMax) from the deduplicated raw data
- [ ] Replace the v1 ranges with the post-cleanup ranges
- [ ] If the direction of the basic-vs-hard finding changes (B.1), reconsider whether this Q7-specific paragraph still belongs in the same place or needs to be reframed

### B.3 Section 5.3 tier accuracy values (integrity B5)

`paper.tex` §5.3 around line 287:

- v1: `"Accuracy decreases with sub-table complexity: small (5×3) averages 94.2%, medium (10×5) averages 91.8%, and large (20×8) averages 88.5% across all models and formats."`
- Actual values from clean data: small **97.6%**, medium **92.2%**, large **87.7%**.

**Fix:**

```
"Accuracy decreases with sub-table complexity: small (5×3) averages 97.6%, medium (10×5) averages 92.2%, and large (20×8) averages 87.7% across all six models and four text formats. The relative ordering of formats is preserved across tiers, confirming that our findings are not artifacts of data size."
```

Verify against the canonical post-cleanup values from Phase 0.5.

### B.4 Table 4 error agreement values (integrity B6)

`paper.tex` Table 4 (lines 236-253 in v1):

The DeepSeek row in v1 says (all_right=87.3%, all_wrong=0.3%, 1-format-fail=10.2%). Clean data says (82.6%, 0.9%, 11.4%) — a 4.7-percentage-point discrepancy on the headline number.

- [ ] After Phase 0.4 establishes the canonical Table 4 computation, regenerate the entire Table 4 from clean raw data for all six models
- [ ] Replace the v1 table values with the canonical values
- [ ] If any model's all_right or all_wrong shifts substantially, update the surrounding prose in §5.4

### B.5 DeepSeek per-format accuracy values (Table 2)

`paper.tex` Table 2 (lines 145-162):

All DeepSeek values are computed on n≈1935 (inflated by 1,000 duplicate rows) instead of n=1724. After Phase 0.1 deduplication and 0.2 re-analysis, the DeepSeek values will shift by tenths of a percent. The integrity audit found Table 2 matches the current (inflated) `analysis_output.json` exactly — so the Table 2 values themselves are consistent with the current analysis, but the analysis is computed on inflated N.

- [ ] After Phase 0 completes, re-check Table 2 DeepSeek cells against the new `analysis_output.json`
- [ ] Update each affected cell with the post-cleanup value
- [ ] The other models (MiniMax, Kimi, GLM-5, Qwen, Gemini) likely don't change unless Phase 0.3 finds duplicates in their raw data

### B.6 Reasoning ablation deltas (already verified)

`paper.tex` §5.1 (around line 275) and Figure 4 caption:

The reasoning ablation deltas (DeepSeek +24% to +38%, Gemini <1%) were verified exactly against the data by the integrity audit (`integrity_report.md` Reasoning Ablation table — all matches). However:

- [ ] After Phase 0 cleanup, re-verify the DeepSeek-with-reasoning baseline values (since DeepSeek-without-reasoning was clean and DeepSeek-with-reasoning had the duplicates).
- [ ] Confirm that the gain range "24-38%" still holds post-cleanup. If the with-reasoning numbers shift, the gain range may shift slightly too.

### B.7 Quantitative-claim audit pass

After all B.0-B.6 number updates, audit every other numerical claim in `paper.tex` against the post-cleanup `analysis_output.json`:

- [ ] Section 4.1 "1-3 percentage points" claim for Table-Graph-TimeSeries spread
- [ ] Section 4.1 "7-9% lower" claim for chart-text accuracy gap
- [ ] Section 4.1 "31.9% (Kimi K2.5) to 70.6% (Gemini 3.1 Pro)" for chart-image range
- [ ] Section 4.2 "high transfer (r=0.85-0.88)" range
- [ ] Section 4.2 "moderate transfer (r=0.64-0.65)" range
- [ ] Section 4.2 ceiling-vs-mid-range "r=0.90 and r=0.63" / "r=0.84 and r=0.67" claims
- [ ] Section 4.3 "Q7 accuracy ranging from 29.7% (Kimi K2.5) to 87.8% (Gemini 3.1 Pro)"
- [ ] Section 4.3 "Chart Text accuracy is 12-15% lower" for Q7
- [ ] Section 4.4 chart-image-vs-chart-text gap (19.6%, 31.2%, 49.7%)
- [ ] Section 4.6 domain accuracies (agriculture 95.4%, energy 94.5%, transit 90.3%, air quality 90.6%)
- [ ] Section 5.1 DeepSeek baseline (65.3% Table, 60.8% Graph, 59.3% TimeSeries) and deltas
- [ ] Abstract chart-image "20-50% accuracy gap"
- [ ] Token-count claims (Table 276, Chart Text 270, Graph 520, Time Series 380 — §3.6)
- [ ] All numbers in appendix Table A.1

Where claims still hold post-cleanup: mark verified in a tracking file. Where they shift: update prose with new values.

---

## Phase C — Citation and claim overhaul (zero compute, hard requirement)

Sources: `citation_integrity_report.md` (17 bib metadata errors) + `prose_claim_audit.md` (7 prose-claim issues, 2 missing bib entries discovered after the SURGeLLM 2026-05-11 reminder). The email's third verification check — "the claim attributed to the citation in your prose matches what the source actually says" — requires both bib accuracy AND prose-source consistency.

**Total scope:** 19 bib changes (17 corrections + 2 new entries) + 7 prose-claim fixes.

### C.1 Apply 17 corrected bib entries

For each entry below, replace the v1 stanza in `paper/references.bib` with the corrected stanza from `citation_integrity_report.md`. Note bib-key changes — `paper.tex` `\cite{}` calls must be updated:

- [ ] `torr2026` — title + lead author fix
- [ ] `wikimixqa2025` — title subtitle + author list expansion
- [ ] `datacross2026` — title + lead author + author count
- [ ] `chartqapro2025` — full author list (Mohanad Ibrahim is not on the paper)
- [ ] `graphomni2026` — Hao Li → Hao Xu, expanded title and author list
- [ ] `gracore2025` — author (Ma Yuhan → Zike Yuan), `@article` → `@inproceedings`
- [ ] `tsaqa2026` — Wang Xin → Baoyu Jing, full title
- [ ] `mmtsbench2026` — Zhang Wei → Yao Yin, full title
- [ ] `hearts2026` — Soomin Kim → Sirui Li, "Heart Rate" → "Health"
- [ ] `zhang2026samecontent` — Yilun → Yue Zhang, correct subtitle
- [ ] `liu2026formatprior` → **`liu2025formatprior`** (year change), Liu Chen → Jiacheng Liu
- [ ] `ho2025formatmatters` — Thanh → Xanh Ho, full title
- [ ] `epoch2026` — remove hallucinated subtitle, year 2026 → 2025
- [ ] `ilic2023gfactor` — Igor → David Ilić (with diacritic), full title
- [ ] `mmtu2025` — Li Zheng → Junjie Xing, "Multi-Modal" → "Massive Multi-Task"
- [ ] `charxiv2026` → **`charxiv2024`** (year change), "CharXiv-R" → "CharXiv", Yi Wang → Zirui Wang
- [ ] `chartmuseum2025` — Park Jin → Liyan Tang, full title; verify venue (likely arXiv preprint, not NeurIPS)

### C.2 Add 2 missing bib entries (Orchestra and TabTracer)

Source: `prose_claim_audit.md` Findings 1 and 2. Both papers are named in v1 §2 prose with specific accuracy claims but have no bib entries. The cited works (`pasupat2015compositional`, `chen2020tabfact`) do not describe these systems.

Add to `paper/references.bib`:

```bibtex
@article{orchestra2026,
  title={Accurate Table Question Answering with Accessible {LLMs}},
  author={Jiang, Yangfan and Wei, Fei and Bao, Ergute and Li, Yaliang and Ding, Bolin and Yang, Yin and Xiao, Xiaokui},
  journal={arXiv preprint arXiv:2601.03137},
  year={2026}
}

@article{tabtracer2026,
  title={{TabTracer}: Monte Carlo Tree Search for Complex Table Reasoning with Large Language Models},
  author={Luo, Zhizhao and Luo, Zhaojing and Zhang, Meihui and Mao, Rui},
  journal={arXiv preprint arXiv:2602.14089},
  year={2026}
}
```

### C.3 Update `\cite{}` calls in `paper.tex` for bib-key changes

- [ ] `\cite{liu2026formatprior}` → `\cite{liu2025formatprior}` (search-replace across `paper.tex`)
- [ ] `\cite{charxiv2026}` → `\cite{charxiv2024}` (search-replace across `paper.tex`)

### C.4 Fix prose claim issues

Source: `prose_claim_audit.md`. Each fix below addresses a specific prose-source mismatch.

**B.4.0 — Orchestra: misattributed 75.3% number (`paper.tex` §2 around line 52)**

- v1: `Table question answering has advanced rapidly, with Orchestra achieving $>$75.3\% EM on WikiTableQuestions \cite{pasupat2015compositional} and TabTracer reaching 92.5\% on TabFact \cite{chen2020tabfact}.`
- The 75.3% is the prior GPT-4 result that Orchestra approaches (72.1% with Qwen2.5-14B), not Orchestra's accuracy.
- The TabTracer 92.5% does not appear as an accuracy claim in the TabTracer paper; the paper reports "up to 6.7% improvement over prior state-of-the-art."
- Suggested fix: `Table question answering has advanced rapidly, with recent multi-agent systems \cite{orchestra2026} approaching GPT-4's previously reported 75.3\% EM on WikiTableQuestions \cite{pasupat2015compositional}, and MCTS-based agentic frameworks \cite{tabtracer2026} reporting 6-7\% accuracy improvements over prior state-of-the-art on TabFact \cite{chen2020tabfact} and WikiTQ.`

**B.4.1** `paper.tex` §2 paragraph "Table QA" (around line 52):
- v1 prose: `MMTU \cite{mmtu2025} extends evaluation to multi-modal table understanding across diverse domains.`
- Fix to: `MMTU \cite{mmtu2025} extends evaluation to a multi-task table understanding suite covering 25 task types over diverse domains.`
- Reason: MMTU is multi-task, not multi-modal.

**B.4.2** `paper.tex` §2 paragraph "Chart Comprehension" (around line 54): ChartQA ">95% accuracy" claim is unsupported by available data (most recent verified frontier accuracy is Claude Sonnet 3.5 at 90.5%, per the ChartQAPro paper).
- v1 prose: `ChartQA \cite{masry2022chartqa} established chart QA as a benchmark, with recent models achieving $>$95\% accuracy.`
- Fix to: `ChartQA \cite{masry2022chartqa} established chart QA as a benchmark; frontier vision-language models have approached saturation, with Claude Sonnet 3.5 scoring 90.5\% \cite{chartqapro2025}.`

**B.4.3** `paper.tex` §2 paragraph "Time Series" (around line 58): TSAQA 67.68% is verified but oversimplified. The 67.68% is specifically the best PZ (puzzling) format score by fine-tuned LLaMA-3.1-8B.
- v1 prose: `TSAQA \cite{tsaqa2026} showed that fine-tuned LLMs can achieve 67.68\% on time series QA, while MMTS-Bench \cite{mmtsbench2026} found that general LLMs with CoT can outperform specialized time-series models. HeaRTS \cite{hearts2026} demonstrated that temporal complexity degrades LLM performance.`
- Fix to: `\citet{tsaqa2026} introduced a unified time-series QA benchmark spanning six tasks; their best accuracy on the hardest (puzzling) subtask is 67.68\% with a fine-tuned LLaMA-3.1-8B. \citet{mmtsbench2026} report that general-purpose LLMs with chain-of-thought outperform specialized time-series adapted LLMs. \citet{hearts2026} show that LLM performance on health time-series tasks declines with increasing temporal complexity.`

**B.4.4** `paper.tex` §2 paragraph "Chart Comprehension" (around line 54):
- v1 prose: `CharXiv-R \cite{charxiv2026} and ChartMuseum \cite{chartmuseum2025} further challenge models on real-world scientific charts.`
- Fix to: `CharXiv \cite{charxiv2024} and ChartMuseum \cite{chartmuseum2025} further challenge models on real-world scientific charts.`
- Reason: paper name is CharXiv, not CharXiv-R; the latter does not exist.

**B.4.5** `paper.tex` §5 Discussion (around line 292): Epoch citation misuse.
- v1 prose: `...while aligning with the cross-benchmark correlations reported by \citet{epoch2026}.`
- Fix to: `...while aligning with the unidimensional capability factor reported by \citet{epoch2026}'s benchmark-stitching analysis and by \citet{ilic2023gfactor}.`
- Reason: Epoch's paper is item-response-theory-style benchmark stitching, not cross-benchmark correlations.

### C.5 Re-verification status of numerical claims (post-2026-05-11 audit)

All specific numerical claims in v1 §2 prose have been re-verified against the actual source papers via Exa crawls of arXiv abstracts and PDFs. Status:

- [x] `Orchestra 75.3%` → **WRONG**: 75.3% is GPT-4's prior result, not Orchestra. Fix applied in B.4.0.
- [x] `TabTracer 92.5% on TabFact` → **UNVERIFIED**: not found as an accuracy claim in the TabTracer paper (only appears in a token-cost table). Fix applied in B.4.0.
- [x] `TSAQA 67.68%` → **VERIFIED** but oversimplified (specifically the best PZ-format score by LLaMA-3.1-8B fine-tuned). Reframe applied in B.4.3.
- [x] `MMTS-Bench CoT outperforms specialized` → **VERIFIED**. Bib still needs metadata fix (in B.1).
- [x] `HeaRTS temporal complexity degrades` → **VERIFIED**. Bib still needs metadata fix (in B.1; Heart Rate → Health Time Series).
- [x] `ChartQAPro Claude 3.5 with CoT 55.8%` → **VERIFIED** (actual: 55.81%). Bib still needs author fix (in B.1).
- [x] `GraphOmni serialization affects` → **VERIFIED**. Bib still needs author fix (in B.1).
- [x] `GraCoRe major gaps` → **WEAKLY VERIFIED**. Bib still needs author fix (in B.1).
- [x] `ChartQA recent models >95% accuracy` → **UNSUPPORTED**: most recent verified is Claude 3.5 at 90.5%. Fix applied in B.4.2.

Full details in `prose_claim_audit.md`.

### C.6 Add two newly-discovered concurrent works

Source: novelty scan in `v2_master_plan.md` §2.

**B.6.1 InfoChartQA (Xie et al., NeurIPS 2025).**

- [ ] Add bib entry:
```bibtex
@inproceedings{infochartqa2025,
  title={{InfoChartQA}: A Benchmark for Multimodal Question Answering on Infographic Charts},
  author={Xie, Tianchi and Lin, Minzhi and Liu, Mengchen and Ye, Yilin and Chen, Changjian and Liu, Shixia},
  booktitle={Advances in Neural Information Processing Systems 38: Datasets and Benchmarks Track},
  year={2025}
}
```
- [ ] Cite in `paper.tex` §2 "Chart Comprehension" paragraph after the ChartMuseum citation:
 - "InfoChartQA \cite{infochartqa2025} pairs infographic and plain charts sharing identical underlying data, finding substantial accuracy drops on the infographic variant. Our work differs in pairing visual (Format B) with text (Format B') of the same data, isolating visual processing rather than visual style."

**B.6.2 Bhandari et al. (Apr 2026, arXiv 2604.24040).**

- [ ] Add bib entry:
```bibtex
@article{bhandari2026tabular,
  title={Improving Robustness of Tabular Retrieval via Representational Stability},
  author={Bhandari, Kushal Raj and Singh, Adarsh and Gao, Jianxi and Dan, Soham and Gupta, Vivek},
  journal={arXiv preprint arXiv:2604.24040},
  year={2026}
}
```
- [ ] Cite in `paper.tex` §2 "Cross-Format Studies" paragraph:
 - "\citet{bhandari2026tabular} show that semantically equivalent table serializations (csv, tsv, html, markdown, ddl) produce substantially different retrieval embeddings, addressing format sensitivity at the encoder level. Our work addresses format sensitivity at the task-accuracy level across a wider modality span (table, chart, graph, time series)."

---

## Phase D — Reviewer-driven writing edits (zero compute)

Source: `reviews/reviews.md` cross-referenced in `v2_master_plan.md` §1.3.

### D.1 De-anonymize

`paper.tex` line 17:
- v1: `\author{Anonymous}`
- Fix to: `\author{Farseen Shaikh \\ <affiliation> \\ <email>}` (real name, affiliation, email per ACL 2026 style)

### D.2 Soften "graph reasoning" framing throughout (Reviewer 5243 W1)

Replace "graph reasoning" / "graph reasoning transfer" / similar phrases with "graph-like serialization" / "node-attribute representation" where the claim is about the constructed Format C.

- [ ] `paper.tex` line 28 (abstract): Reword "transfer strongly across text-based formats, with mean tetrachoric r=0.84 between table, graph, and time series representations" — keep but add a brief disclosure that "graph" denotes a constructed graph-like serialization of tabular data (single sentence).
- [ ] `paper.tex` line 40 (intro): "We present the first study measuring cross-format transfer across five fundamentally different representation types" — soften per C.4 below.
- [ ] `paper.tex` line 81 (§3.2 Format C description): the existing disclosure is good; promote this to the abstract and §1 contribution list.
- [ ] `paper.tex` lines 56, 164, 178, 183, 184, 217, 287, 292, 309, 322 — every "graph" mention: audit and clarify whether this is constructed-graph-serialization (most) or natural-graph (none in this paper). Use "graph-like serialization" or "Format C" in technical claims; reserve "graph reasoning" for related-work discussion of natural graphs.
- [ ] `paper.tex` Conclusion (line 309): explicit acknowledgment in 1-2 sentences that the graph-like serialization is constructed and that conclusions about graph reasoning capabilities should be read in that context.

### D.3 Replace mechanical Findings 1/2/3 with flowing argument (Reviewer 5243 W4)

`paper.tex` §4.1 "Overall Accuracy" lines 164-168 currently has "Finding 1 / Finding 2 / Finding 3" bold-headed structure.

- [ ] Rewrite as flowing prose. Suggested draft:

> Three patterns emerge consistently. First, accuracy on table, graph, and time-series formats is within 1-3 percentage points for every model, suggesting a shared underlying comprehension skill. Second, despite length-matching to ±20% tokens, chart-text descriptions consistently lag tables by 7-9% across all six models, indicating a systematic information-loss penalty for prose-formatted structured data. Third, chart images are the outlier: among the three vision-capable models, chart-image accuracy ranges from 31.9% (Kimi K2.5) to 70.6% (Gemini 3.1 Pro) — dramatically lower than the 81-99% achieved on text formats with identical data. We develop each pattern in §4.2 (transfer correlation), §4.4 (modality isolation), and §4.7 (chart-image error modes).

### D.4 Soften "first study" claim (Reviewer 5243 W4)

`paper.tex` line 40:
- v1: `We present the first study measuring cross-format transfer across five fundamentally different representation types---table, chart image, chart text, graph, and time series---using identical content and programmatic ground truth.`
- Fix to: `We extend prior controlled-content methodology --- most notably \citet{zhang2026samecontent}, who isolate representation effects within table-only variations --- to span five fundamentally different representation types (table, chart image, chart text, graph-like serialization, time series), enabling cross-modality transfer measurement under identical content and programmatic ground truth.`

### D.5 Hedge reasoning ablation conclusions (Reviewer 5243 W3)

`paper.tex` §5 Discussion paragraph "Reasoning is not universally necessary" (around line 298):
- v1: `The dramatic model-dependent effect of reasoning (DeepSeek: +30\%, Gemini: <1\%) challenges the assumption that chain-of-thought uniformly improves structured data tasks. Models with strong base inference (Gemini, Qwen) may already internalize the reasoning steps that weaker models must perform explicitly.`
- Fix to: `In our two-model ablation, the gain from explicit reasoning correlates with the model's no-reasoning baseline accuracy: DeepSeek V3.2 (62% baseline) gains +33\%; Gemini 3.1 Pro (97% baseline) gains <1\%. We caution that this pattern is observed in N=2 models. Whether it generalizes — for example, whether stronger base inference systematically reduces reasoning's marginal benefit — is a hypothesis that requires testing across a broader model panel and is reserved for future work.`

### D.6 Add Scope of Claims subsection (Reviewer 5243 detailed comments)

Insert a new subsection in `paper.tex` §5 Discussion (before Limitations, around line 302), explicitly listing what the paper does and does not claim:

```latex
\paragraph{Scope of claims.} Our results support the following claims:
\begin{itemize}
 \item Question-level accuracy on table, graph-like, and time-series formats is highly correlated within each frontier LLM evaluated, robust across domain and complexity tier.
 \item Chart-text accuracy systematically lags table accuracy by 7--9\% across all evaluated models, with the largest gap on aggregation-style questions (Q3, Q7).
 \item Among vision-capable models, chart-image accuracy is substantially lower than chart-text accuracy on identical data, with the gap largest for value-extraction tasks.
\end{itemize}
We do \emph{not} claim:
\begin{itemize}
 \item That the synthetic sub-tables generalize to all real-world structured-data tasks --- distributional bias is a known limitation (see \S5.4).
 \item That chart-image performance is universally siloed across all vision models --- our claim is supported by N=3 vision models and warrants validation on a broader panel.
 \item That chain-of-thought reasoning's model-dependent effect generalizes beyond the two-model ablation studied here.
 \item That ``graph reasoning'' transfers --- our Format C is a constructed graph-like serialization of tabular data, not a natural graph; conclusions are about LLM reasoning over node-attribute serializations.
\end{itemize}
```

### D.7 Expand Limitations (Reviewer 5243 detailed comments + my audit)

`paper.tex` §5 Limitations paragraph (line 304). Add the following items:

- [ ] Tetrachoric correlation assumes a bivariate-normal latent variable; this assumption is unverified for binary correctness data, and tetrachoric is base-rate-sensitive at extreme accuracy levels. We report phi as a robustness check.
- [ ] Single language (English) in all questions and data.
- [ ] Single tokenizer family (cl100k_base) for length matching; may not generalize to other tokenizer families.
- [ ] Single prompt template per format; prompt sensitivity is reserved for future work.
- [ ] Format C ("graph") is a constructed serialization of tabular data with cosine-similarity edges; the high transfer between Table and Graph is partially confounded by the 2× token length of Format C. We address this with the graph-without-edges ablation in §4.8.
- [ ] Format B (chart image) evaluation is conducted on N=3 vision-capable models; the chart-image-as-siloed claim warrants replication on a broader vision-model panel.

---

## Phase E — Re-analyses on existing data (zero compute)

Source: `deep_paper_analysis.md` §3 + `v2_master_plan.md` §3.1. All items below use existing `analysis_output.json` and `raw_results.jsonl` data — no new model runs needed.

### E.1 Switch headline metric to phi, with tetrachoric supplementary

- [ ] `experiments/code/analyze.py`: ensure phi is computed alongside tetrachoric (already there per the JSON inspection)
- [ ] `experiments/code/plot_figures.py`: re-render `fig1_correlation_heatmap.pdf` with phi as the primary heatmap, tetrachoric as a smaller inset or right-panel
- [ ] `paper.tex` §3.5 Metrics (line 130-132): rewrite to make phi primary
- [ ] `paper.tex` Table 2 / Figure 1: report phi values; tetrachoric values move to appendix
- [ ] `paper.tex` §4.2 (lines 170-188): rewrite to use phi correlations; mention that tetrachoric inflates the apparent magnitude due to base-rate sensitivity, and that phi is the assumption-light alternative

### E.2 Surface bootstrap CIs for every reported correlation

- [ ] `analysis_output.json` already has `bootstrap_ci` for every correlation pair
- [ ] `paper.tex` Figure 1 caption: append CI ranges
- [ ] `paper.tex` Table 2 (around line 145): add CIs as `r=0.85 [0.78, 0.91]` style for every correlation cell
- [ ] `paper.tex` Figure 6 (per-model heatmaps, line 327): regenerate with CI overlays

### E.3 Add paired McNemar tests for accuracy comparisons

- [ ] Add to `analyze.py`: function that computes paired McNemar p-values for every (format_A, format_B) pair within each model, using the per-question outcome data in `raw_results.jsonl`
- [ ] Apply Bonferroni correction across the family of comparisons within each model
- [ ] `paper.tex` Table 2 (line 145): annotate format-pair differences with significance markers (* p<.05 / ** p<.01 / *** p<.001 after correction)
- [ ] `paper.tex` Table 2 caption: add brief note on the test (paired McNemar across n=1700+ questions per model, Bonferroni-corrected)

### E.4 Per-format-tier breakdown (chart-text size effect)

Existing v1 §4.6 (line 287) reports tier accuracy averaged across formats. The chart-text-at-medium-size effect (DeepSeek drops to 81.3% at medium tier on chart_text, while other formats stay >98%) is buried.

- [ ] `analyze.py`: extract per-(model, format, tier) accuracy from existing `raw_results.jsonl`
- [ ] Add new Table 4 to `paper.tex` after current §4.6 — 4 text formats × 3 tiers grid, averaged across the mid-range model group (where the effect is visible without ceiling artifacts)
- [ ] `paper.tex` §4.6: add 1-2 sentences highlighting the chart-text size effect — specifically that chart-text accuracy degrades faster with tier than other formats, supporting the "structural information loss" hypothesis in §5

### E.5 Quantitative 1-format-fail breakdown

`paper.tex` §4.4 Error Agreement Analysis (line 255) currently says "Manual inspection reveals these are predominantly Q3 (aggregation) and Q7 (conditional aggregation) questions presented in Chart Text format." This is unquantified.

- [ ] `analyze.py`: from `raw_results.jsonl`, identify per-model the questions where exactly one of the four text formats fails. Group by `(failing_format, qtype, tier)`.
- [ ] Replace the "manual inspection" sentence with an explicit count table (or appendix table referenced from main text).
- [ ] Suggested table format: 4 failing-formats × 7 qtypes = 28 cells, summed across the 6 main models; show the dominant cells (Chart Text × Q3, Chart Text × Q7) explicitly.

### E.6 Chart-image error mode analysis

This is the most publishable independent finding. v1 reports only the chart-image accuracy gap; v2 should decompose the failure modes.

- [ ] `analyze.py`: for each vision-capable model (Kimi K2.5, Qwen 3.5 Plus, Gemini 3.1 Pro), compute per-qtype chart-image accuracy
- [ ] Construct a comparison table: chart-text accuracy vs. chart-image accuracy, per qtype, per model. Highlight the ratio.
- [ ] Sample 50 random chart-image failures per model from Q1 (lookup) and Q3 (aggregation) — these are the value-extraction tasks where vision fails hardest.
- [ ] Manually tag each failure as: (a) perception failure (model misread the chart), (b) value-extraction failure (model read the chart but extracted wrong numbers), (c) reasoning failure (model extracted right values but computed wrong), (d) format-misread (model thought it was looking at a different chart type).
- [ ] Add new §4.7 "Chart-image error modes" with the breakdown table and error-mode distribution chart.

Estimated manual annotation: 50 failures × 3 models = 150 questions, ~5-10 minutes each = 1-2 hours.

### E.7 Within-ceiling-group variance reporting

`paper.tex` §4.2 ceiling effect robustness check (line 187) reports ceiling group r=0.90 as a single number. Inside the ceiling group, DeepSeek V3.2 has r=0.716 (table-graph-timeseries) while Qwen has r=0.990 and Gemini has r=0.983 — wide variance hidden by the mean.

- [ ] `paper.tex` §4.2 (around line 187): add a paragraph explicitly reporting the within-ceiling-group spread. Suggested wording:

> "Within the ceiling group, however, the per-model correlations vary substantially: Qwen 3.5 Plus and Gemini 3.1 Pro both show r > 0.98 across the high-transfer cluster, while DeepSeek V3.2 shows r = 0.72. The gap likely reflects tetrachoric correlation's known instability at extreme base rates: at >97% accuracy, only ~14 errors per format remain, and whether those errors coincide drives the metric. We treat this as evidence that the ceiling-group correlations should be interpreted as upper-bound estimates rather than precise measurements; the mid-range group (r = 0.84) provides the more trustworthy point estimate."

### E.8 Reasoning ablation transfer-correlation panel

v1 Figure 4 shows reasoning-on/off accuracy delta. The interesting result that DeepSeek's transfer-r is flat while Gemini's increases is buried.

- [ ] `experiments/code/plot_figures.py`: add a second panel to `fig4_reasoning_ablation.pdf` showing transfer-r delta (high-transfer cluster) for DeepSeek and Gemini in both reasoning conditions
- [ ] `paper.tex` Figure 4 caption: extend to describe both panels
- [ ] `paper.tex` §5.1 Reasoning Effect (around line 277): add a paragraph on the transfer-r finding. Suggested:

> "An additional pattern emerges in the transfer correlations themselves. DeepSeek V3.2's table-graph-timeseries correlation is stable across reasoning conditions (r = 0.74 without, r = 0.72 with), suggesting that explicit reasoning improves accuracy uniformly across formats without reorganizing how questions transfer. Gemini 3.1 Pro shows the opposite pattern: r = 0.93 without thinking, r = 0.98 with thinking — explicit reasoning tightens cross-format consistency despite a negligible accuracy delta. We caution that this is N = 2; whether it reflects an architectural distinction or a sampling artifact is a question for the broader reasoning-ablation extension reserved for future work."

---

## Phase F — Targeted small-compute ablations (optional)

These are small-compute experiments that produce paper-quality findings. Each is justified by a specific reviewer concern. Listed in priority order.

### F.1 Graph-without-edges ablation (NRrg W2 + my §3.4)

The single highest-leverage compute item. Re-renders Format C with edges removed (node attributes only) and re-evaluates on the model where the effect is largest.

- [ ] `experiments/code/data/generate_formats.py`: add a `--no-edges` flag for Format C
- [ ] Re-render Format C without edges for all 250 sub-tables
- [ ] Pick 1 model: Kimi K2.5 is recommended (mid-range accuracy, largest transfer signal)
- [ ] **Cost test first:** run 10 questions through Kimi on the no-edges format, measure billing, multiply
- [ ] Run resumable evaluation per `feedback_api_credits.md`: 1,724 questions × 1 model = 1,724 calls
- [ ] Compare to existing Format C with edges
- [ ] Add new §4.8 "Edge contribution in graph format" with results
- [ ] If the no-edges variant shows similar accuracy, the edge confound is small and the v1 framing strengthens. If it differs substantially, the framing must be hedged further.

### F.2 Per-chart-type analysis (zero compute)

The v1 chart_image data is already broken down by chart type. Re-aggregate.

- [ ] `analyze.py`: group existing chart_image results by `(chart_type ∈ {bar, line, scatter}, model)`
- [ ] Add Table 7: per-chart-type accuracy for the 3 vision models
- [ ] Test whether chart-type difficulty interacts with model
- [ ] Add 1-2 sentences in §4.4 "Modality Isolation" referencing this finding

### F.3 Token-controlled graph variant (small compute, for completeness)

Not strictly required if E.1 shows edges contribute little, but useful for the appendix.

- [ ] Re-render Format C with K = 1 (single edge, similar token count to Table)
- [ ] Re-evaluate on Kimi K2.5: 1,724 questions
- [ ] Add to appendix

---

## Phase G — Pre-submission audit

### G.1 Run aclpubcheck

- [ ] Recompile `paper/paper.tex`: `cd paper && tectonic paper.tex`
- [ ] Run: `uvx --from git+https://github.com/acl-org/aclpubcheck aclpubcheck --paper_type long paper/paper.pdf`
- [ ] Fix any flagged issues (margins, fonts, page count, etc.)
- [ ] Re-run until clean

### G.2 Run ai-research-integrity-check

- [ ] Invoke the skill on the corrected `paper.tex` + `references.bib`
- [ ] Pass = clear. Any flagged entry must be re-fixed.

### G.3 Run ai-research-pre-submit

- [ ] Invoke the skill — checks anonymization, page limit, abstract length, figure cross-refs, TODO markers, BibTeX hygiene
- [ ] Note: anonymization is now intentionally OFF (de-anonymized for camera-ready); the skill should handle this

### G.4 Run ai-research-fig-check

- [ ] Invoke the skill — DPI, vector vs. raster, colorblind accessibility, all figure references in text

### G.5 Clean-room reproducibility test

- [ ] Fresh clone of the public GitHub repo to a clean directory
- [ ] Follow `README.md` from scratch
- [ ] Regenerate all results and figures
- [ ] Document any gaps; fix them in the repo

### G.6 Final visual inspection

- [ ] Open the final PDF. Read end-to-end at least once.
- [ ] Verify: figures render, captions intact, table widths fit, no `??` cross-references, no leftover anonymization, page count ≤ 8 content pages.
- [ ] Spot-check 3 random citations: do they actually exist? (sanity check on top of B.1)

---

## Phase H — Upload

### H.1 OpenReview submission

- [ ] Log in to OpenReview
- [ ] Tasks → SURGeLLM "Camera Ready Revision"
- [ ] Upload final `paper.pdf`
- [ ] Confirm "Do not include in proceedings" (non-archival)
- [ ] Skip copyright form (non-archival)
- [ ] Submit
- [ ] Save the revision confirmation page / receipt as a PDF in `submission_records/`

### H.2 Public arXiv preprint (optional but strongly recommended)

A clean, integrity-checked v1 preprint on arXiv establishes authorship date and prevents anyone from claiming priority on the contribution while v2 is in flight.

- [ ] Strip ACL formatting (or keep it — arXiv accepts)
- [ ] Submit to arXiv with clear "v1, presented at SURGeLLM 2026, non-archival" note in the abstract
- [ ] Update the GitHub repo `README.md` with the arXiv ID

---

## Out of scope (reserved for v2)

These are the v2-only items from `v2_master_plan.md` that are deliberately excluded from the camera-ready punch-list:

- Expanded model panel (Claude Sonnet 4.6, frontier additions, open-weights additions to N≥10)
- Real-world data extension (WikiTQ, ChartQA-Pro, optional CharXiv)
- Human baseline study
- Prompt sensitivity analysis (Kimi × 4 templates)
- Full reasoning ablation across all models (currently N=2)
- Semantic-edge graph variant
- Mixed-effects regression as headline statistic (paired McNemar in §D.3 is the camera-ready upgrade; full mixed-effects is v2)
- Additional vision-model evaluations beyond the existing 3

These are all listed and sequenced in `v2_master_plan.md` Section 9. They go into the EMNLP / NAACL / ACL submission, not the SURGeLLM camera-ready.

---

## Sequencing note

Phase **0 → A → B** is the dependency chain that gates everything else, and the order is non-negotiable.

- **Phase 0** (data cleanup + re-analysis) must come first because the paper currently contains numbers computed on a contaminated DeepSeek raw file (1,000 duplicate rows, 44 inconsistent-score pairs). Every downstream phase that touches paper numbers depends on a regenerated `analysis_output.json`. Touching paper prose before this is rework — the numbers will move.
- **Phase A** (git cleanup + public repo skeleton) runs in parallel with Phase 0 — git work doesn't depend on data cleanup.
- **Phase B** (paper number corrections) cannot start until Phase 0 produces the regenerated analysis. Once Phase 0 outputs the canonical numbers, Phase B updates every affected paper-text number in one pass.
- **Phase C** (citation overhaul) can run in parallel with Phase B — bib metadata fixes don't depend on data numbers. Some prose-citation fixes do interact with Phase B (e.g., the basic-vs-hard sentence in §5.2 needs both the number fix from B.1 and the framing soften from C.4); coordinate those.
- **Phase D** (reviewer-driven writing edits) starts after Phase B and Phase C settle, because writing changes need the canonical numbers and the fixed bib in place.
- **Phase E** (re-analyses on existing data) runs in parallel with Phase D — they touch different sections of `paper.tex`.
- **Phase F** (small ablations) is optional but high-value; if budget and time permit, do at least F.1 (graph-without-edges) because it directly answers NRrg W2 and is cheap. Independent of Phases B/C/D/E.
- **Phase G** (audit) gates submission. All preceding phases must be complete.
- **Phase H** (upload) is the last action.

The biggest risk is starting at Phase C or Phase D and discovering mid-edit that a number changes. The discipline is: clean data first, fix numbers second, fix citations and prose third.

The order is dependency-driven. No deadlines surfaced anywhere in this file because deadlines should not influence what to do — only when to do it.
