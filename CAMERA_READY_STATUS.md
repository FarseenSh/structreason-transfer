# Camera-Ready Status (2026-05-11)

**Paper:** Do Structured Data Comprehension Skills Transfer Across Representation Types?
**Compiled PDF:** `paper/paper.pdf` (8 pages of content, ACL-compliant)
**Bib file:** `paper/references.bib` (25 entries, all integrity-verified)
**Git state:** committed and tagged `v1.0-camera-ready-2026-05-11`

---

## Phase summary

| Phase | Status | Notes |
|---|---|---|
| 0. Data integrity cleanup | **DONE** | DeepSeek deduplicated (7896→6896 rows), analyze.py re-run, canonical numbers in `integrity/canonical_numbers_post_cleanup.json` |
| A. Foundation (git + repo) | **DONE** | Initial commit + camera-ready tag. `.gitignore` configured. Local git only — user to push to GitHub when ready. |
| B. Paper number corrections | **DONE** | All 7 substantive numerical errors fixed. Verified 46/46 internal checks. |
| C. Citation + claim overhaul | **DONE** | 17 bib fixes + 2 new entries (Orchestra, TabTracer) + 2 concurrent works (InfoChartQA, Bhandari). 7 prose-claim fixes applied. Final Ilić title corrected post-recheck. |
| D. Reviewer-driven writing | **DONE** | De-anonymized, Findings 1/2/3→flowing, "first study" softened, reasoning hedged, Scope of Claims subsection added, Limitations expanded, Conclusion updated. |
| E. Re-analyses on existing data | **DEFERRED to v2** | Per master punchlist: phi-primary metric, McNemar tests, per-format-tier table, chart-image error modes. These improve the paper but are not required for camera-ready. |
| F. Small ablations | **DEFERRED to v2** | Graph-without-edges, per-chart-type, token-controlled graph. v2 work. |
| G. Pre-submission audit | **PARTIAL** | aclpubcheck: All Clear. Integrity re-check: CLEARED_WITH_CAVEATS → resolved Phase 2. Remaining: `ai-research-fig-check` (optional). |
| H. Upload | **PENDING USER ACTION** | Upload `paper/paper.pdf` to OpenReview, confirm non-archival, skip copyright form. |

---

## What was changed in the paper

### Numerical fixes (Phase B)

| Location | Before | After | Source |
|---|---|---|---|
| Abstract | r=0.84 (presented as headline) | r=0.87 across 6 models, r=0.84 mid-range subset | post-cleanup `_averaged` matrix |
| §5.2 basic-vs-hard | basic r=0.89 > hard r=0.78 | basic r=0.81, hard r=0.85 (HARD > BASIC) | recomputed per-model means |
| §5.2 model count | "five of six" | "four of six (MiniMax, Kimi, GLM-5, Qwen)" | per-model breakdown |
| §5.3 tier accuracy | small 94.2 / med 91.8 / large 88.5 | small 97.6 / med 92.3 / large 87.7 | post-cleanup tier_accuracy |
| §4.2 high-transfer range | r=0.85-0.88 | r=0.86-0.88 | post-cleanup values 0.856-0.880 |
| §4.2 ceiling within-group | DeepSeek r=0.72 vs Qwen r=0.99 | DeepSeek r=0.73 vs Qwen r=0.99 | rounding precision |
| Table 4 DeepSeek row | 87.3% / 0.3% / 10.2% | 82.5% / 0.9% / 11.3% | recomputed error agreement |
| Table 2 DeepSeek Chart Text | 88.2 [87-90] | 88.7 [87-90] | post-cleanup accuracy |

### Citation overhaul (Phase C)

- **17 bib metadata corrections** applied (each verified against arXiv / ACL Anthology / OpenReview)
- **2 new bib entries** added: Orchestra (Jiang et al. 2026), TabTracer (Luo et al. 2026) — both referenced by name in §2 but missing from v1 bib
- **2 concurrent works** added per novelty scan: InfoChartQA (NeurIPS 2025), Bhandari et al. (Apr 2026)
- **Critical fix**: removed hallucinated `charxiv2026` ("CharXiv-R: Chart Reasoning in the Wild" does not exist) → replaced with actual `charxiv2024` (CharXiv, NeurIPS 2024)
- **Prose claim fixes**:
  - Orchestra "75.3% on WikiTQ" was misattribution of GPT-4 baseline → now correctly attributed
  - TabTracer "92.5% on TabFact" was unverified specific number → replaced with verified relative claim
  - MMTU "multi-modal" → "multi-task" (the actual scope of the benchmark)
  - ChartQA ">95% accuracy" unsupported → replaced with verified Claude 3.5 at 90.5%
  - TSAQA "67.68%" presented as headline → now correctly described as best PZ-format score
  - Epoch AI "cross-benchmark correlations" → "benchmark-stitching analysis" (what the paper actually does)
  - CharXiv-R → CharXiv (paper name in prose)

### Writing/framing edits (Phase D)

- De-anonymized author block
- "We present the first study..." → "We extend prior controlled-content methodology..."
- Replaced Findings 1/2/3 with flowing prose argument
- Hedged reasoning ablation conclusions (explicit N=2 disclosure)
- Added new §Scope-of-Claims subsection explicitly listing what paper does/does not claim
- Expanded Limitations: tetrachoric bivariate-normal assumption, single language, single tokenizer, single prompt, constructed graph format
- Replaced "graph reasoning" with "graph-like serialization" throughout when referring to Format C
- Updated Conclusion to reflect corrected basic-vs-hard finding

### Infrastructure

- `.gitignore` configured to ignore venvs and backup files, allow research artifacts
- Two commits + one annotated tag `v1.0-camera-ready-2026-05-11`
- 1582 tracked files (paper, code, data, results, audit artifacts)

---

## Verification status

| Check | Result |
|---|---|
| 46-point internal verification | 46/46 PASS |
| aclpubcheck on corrected PDF | **All Clear** |
| Independent integrity sub-agent (cold-read) | CLEARED_WITH_CAVEATS → all caveats resolved in Phase 2 |
| Compile (tectonic) | OK, no errors |
| Page count | 11 total (8 content + 2 refs + 1 appendix), within ACL long-paper limit |
| `??` broken references | 0 |
| Citation key resolution | all resolve |
| De-anonymization | confirmed (author = Farseen Shaikh) |
| Repo URL in Acknowledgments | filled in |
| Secrets in committed files | none |

---

## What's NOT in this work (deferred to v2)

The following Phase E and F items are quality upgrades that the master punchlist
classifies as "improve the paper" but are not blockers for camera-ready. Each
is described in `v2_master_plan.md` for the EMNLP / NAACL / ACL submission:

- Phi-as-primary correlation metric (with tetrachoric supplementary)
- Bootstrap CIs surfaced for every reported correlation point estimate
- Paired McNemar tests for accuracy comparisons
- Per-format-tier accuracy table (chart-text size effect explicitly surfaced)
- Quantitative 1-format-fail breakdown
- Chart-image error mode analysis
- Reasoning ablation transfer-correlation panel
- Graph-without-edges ablation (NRrg W2)
- Per-chart-type analysis
- Real-world data extension (WikiTQ, ChartQA-Pro)
- Human baseline study
- Prompt sensitivity analysis
- Expanded model panel (Claude Sonnet 4.6, N≥10)

These are v2 work, not camera-ready work.

---

## What's needed from you to submit

1. Read the compiled PDF (`paper/paper.pdf`) end-to-end one more time.
2. Decide if you want to push the local git repo to GitHub now (for the URL in the
   Acknowledgments to resolve) or after camera-ready submission.
3. Upload to OpenReview:
   - Tasks → SURGeLLM "Camera Ready Revision"
   - Upload `paper/paper.pdf`
   - Confirm "Do not include in proceedings"
   - Skip copyright form (non-archival)
   - Submit
4. Save the OpenReview revision confirmation.

The paper is ready for upload.
