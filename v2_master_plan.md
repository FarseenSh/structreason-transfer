# v2 Paper Master Plan — StructReason-Transfer (post-SURGeLLM)

**Paper:** Do Structured Data Comprehension Skills Transfer Across Representation Types?
**v1 outcome:** Accepted at SURGeLLM 2026 (mean rating 6.33), going non-archival.
**v2 target:** EMNLP / NAACL / ACL main (ARR pipeline) — venue chosen by depth of upgrade.
**Author voice in this plan:** I am writing this as the lead author who has read every paper in the space, knows where the methodology is brittle, and is committed to making this paper the canonical reference for cross-format structured data evaluation. No shortcuts. The plan is ordered by dependency, not by calendar.

---

## Section 0 — Sanity check & framing

Before the experimental plan, the question worth answering precisely:

**What is the paper actually trying to claim?**
Three claims:
1. There exists a *general* structured-data comprehension capability in frontier LLMs that transfers across text-based representations.
2. Visual-modality structured data (chart images) sits outside this general capability.
3. The paper provides the methodological tools (a controlled 5-format benchmark + transfer metric) to measure this in any future study.

**What kind of evidence does each claim need to be defensible at a top venue?**

For claim 1 (transfer):
- A correlation metric whose statistical assumptions are stated and respected.
- Measured at sample sizes where the metric is informative (not at ceiling).
- Robust across multiple model families, multiple data domains, multiple prompt templates.
- Held against a real-world data baseline, not just synthetic.
- Statistically significant with multiple-comparison corrections.

For claim 2 (siloed vision):
- Measured on more than 3 vision models.
- Decomposed into perception vs. reasoning failure modes.
- Held across multiple chart types (bar/line/scatter), not aggregated.

For claim 3 (methodology contribution):
- Released as a public benchmark with stable identifiers.
- Reproducible end-to-end from raw datasets.
- Has a human upper bound.
- Has prompt-sensitivity bounds.

The v1 paper supports each claim partially. The v2 paper needs to deliver on each.

**What would a top-conference reviewer demand?** The v1 SURGeLLM reviewers were generous on methodology because the topic is interesting and the writing is clear. An EMNLP / NAACL / ACL reviewer would push harder on:
- Why tetrachoric and not phi or Cohen's kappa
- Significance tests for accuracy comparisons
- Real-world generalization
- The graph format being constructed
- The reasoning ablation being N=2

Every one of these points is addressed in the plan below.

---

## Section 1 — Inheritance audit: what carries over from v1

### 1.1 Methodological assets to keep

- The 250 sub-tables across 10 datasets / 7 domains. Real provenance, programmatic extraction, deterministic ground truth.
- The 1,724 question generation pipeline (7 question types × 250 sub-tables minus 26 Q6 ties). Already battle-tested, already deterministic.
- The 5-format rendering pipeline (table / chart-image / chart-text / graph / timeseries). Format B' (chart-text) length-matching at ±20% with 100% compliance is an engineering contribution worth highlighting.
- The 6 frontier-model evaluation runs (DeepSeek V3.2, MiniMax M2.5, Kimi K2.5, GLM-5, Qwen 3.5 Plus, Gemini 3.1 Pro) — 8,620 judgments per model for the full panel. This data is reusable wholesale.
- The reasoning-ablation runs for DeepSeek V3.2 and Gemini 3.1 Pro. Reusable.
- The bootstrap CI machinery (2,000 resamples, already implemented).
- The codebase: `experiments/code/` runners, generators, analyzers — all reusable.

### 1.2 Methodological liabilities to fix

- Tetrachoric correlation is unreliable at >97% accuracy (Qwen, Gemini). v2 must report phi as primary with tetrachoric supplementary, OR exclude near-ceiling models from the headline correlation analysis, OR both.
- The `_averaged` correlation matrix in the v1 analysis simple-averages per-model tetrachoric values. With per-model r ranging from 0.716 (DeepSeek) to 0.990 (Qwen), the mean masks substantial heterogeneity.
- No paired statistical tests for the within-model accuracy differences (e.g., Table-vs-Chart-Text gap). McNemar on the 1700+ paired questions is what's needed.
- Bootstrap CIs are computed but not reported alongside point estimates.
- The basic-vs-hard split for DeepSeek has CIs of [-0.789, 0.919] — uninformative. The split needs to be re-thought.
- No graph-without-edges ablation despite the 2× token confound.

### 1.2a Data integrity issues discovered in cold-read integrity audit (2026-05-11)

A subsequent independent integrity audit (see `integrity/integrity_report.md`) found additional data-side issues that must be resolved before v2 work begins:

- **DeepSeek `raw_results.jsonl` has 1,000 duplicate rows**, 44 of which have inconsistent scores (the model returned different answers on re-runs). The analysis was computed on inflated N=7,896 instead of expected N=6,896. Every DeepSeek number in `analysis_output.json` is affected. The cleanup is documented in `camera_ready_master_punchlist.md` Phase 0.
- **Basic-vs-hard correlation direction in v1 is inverted.** Paper claims basic r=0.89 > hard r=0.78. Actual data: basic r=0.809, hard r=0.847. Hard transfer is *higher*. This is a substantive scientific claim that needs to be re-written, not just corrected. If the inversion holds after the DeepSeek cleanup (likely, since this involves all 6 models not just DeepSeek), the v2 paper's headline becomes stronger: "transfer holds or even strengthens on hard questions."
- **Tier accuracy numbers in v1 are all wrong** (small 94.2% should be 97.6%, etc.). The direction is preserved but magnitudes are off by 3-5pp.
- **Table 4 (error agreement) values cannot be reproduced** from archived raw data. The computation pipeline that produced the paper's numbers is unaccounted for.
- **Abstract correlation r=0.84 vs data r=0.87** — the abstract presents the mid-range-only mean as if it were the all-6-model headline. Conflation that needs to be resolved.

These v1 fixes are the *foundation* for the v2 paper. The v2 analysis pipeline must inherit clean data and the corrected direction of findings. Specifically:

- v2 Section 3.1.3 (mixed-effects regression as headline statistic) should be run on the post-cleanup raw data.
- v2 Section 3.1.8 (reasoning ablation transfer-correlation panel) values should be recomputed from post-cleanup DeepSeek data.
- v2 Section 3.4 (real-world data extension) should be evaluated against the corrected v1 baselines, not the pre-cleanup ones.
- v2 Discussion should adopt the corrected basic-vs-hard direction as the framing.

### 1.3 Reviewer concern → v2 section mapping

Every weakness, detailed comment, and technical question raised in the three SURGeLLM reviews is mapped explicitly to the v2 sections that address it. Source: `reviews/reviews.md`.

#### Reviewer 5243 (rating 6, "Clear Setup, Limited Novelty")

| # | Reviewer 5243 ask | v2 section that addresses it |
|---|---|---|
| W1 | Graph format is constructed from tabular data, not naturally occurring; graph reasoning claims should be stated more carefully | §1.4 (independent finding overlap), §3.2.1 (graph-without-edges ablation), §3.2.2 (semantic-edge variant), §5.1 (soften "graph reasoning" framing in abstract + intro + conclusion), §5.5 (Scope of Claims subsection) |
| W2 | Highly controlled/programmatic supports internal validity, but unclear how findings transfer to noisier real-world settings | §3.4 (real-world data extension: WikiTQ, ChartQA-Pro, optional CharXiv pilot), §5.5 (Scope of Claims), §10.1 (explicit risk that real-world transfer may diverge from synthetic, with a mitigation that re-frames the central claim if needed) |
| W3 | Some broader conclusions based on limited coverage, especially for chart-image evaluation and reasoning ablation | §3.3.1-3 (expand vision-capable models from 3 to ≥5 by adding Claude Sonnet 4.6 + frontier additions), §3.3.4 (full reasoning ablation across all models, not just 2), §3.1.6 (chart-image error mode analysis) |
| W4 | Writing reads like experimental report, not polished paper; contribution would benefit from more careful positioning relative to prior work | §5.2 (soften "first study" claim with explicit Zhang 2026 differentiation), §5.4 (replace mechanical Findings 1/2/3 with flowing argument), §6.4 (add InfoChartQA + Bhandari 2026 to Related Work), §8 (restructured outline) |
| D | "Tighten the claims, improve the framing, and clarify the intended scope of the conclusions" | §5.3 (hedge reasoning ablation conclusions), §5.5 (Scope of Claims subsection — explicit list of what the paper does and does not claim), §5.6 (Limitations expansion: tetrachoric assumption, single language, single tokenizer, single prompt template) |

#### Reviewer NRrg (rating 5, "accept with changes")

| # | Reviewer NRrg ask | v2 section that addresses it |
|---|---|---|
| W1 | Table 2 quantitative results insufficient; needs more granular data including CIs and statistical significance tests | §3.1.2 (bootstrap CIs surfaced for every reported correlation point estimate), §4.1 (phi as primary metric, base-rate-robust), §4.2 (paired McNemar tests for every accuracy comparison), §4.3 (mixed-effects regression as headline statistic), §4.4 (Bonferroni / Holm multiple-comparison correction), §4.6 (Cohen's h and Cohen's q effect sizes) |
| W2 | Edge-descriptions confound in graph format is important but not fully explored or mitigated | §3.2.1 (graph-without-edges ablation: re-render Format C with edges removed, re-evaluate on Kimi K2.5 + DeepSeek V3.2, ~13,792 new judgments), §3.2.4 (token-count-controlled graph variant) |
| W3 | Reliance on synthetic sub-tables introduces potential bias; real-world data may exhibit different difficulty distributions | §3.4 (real-world extension across WikiTQ + ChartQA-Pro + optional CharXiv), §5.5 (Scope of Claims), §10.1 (risk + mitigation) |
| W4 | Evaluating only six LLMs is a relatively small sample size, limiting generalizability | §3.3.1 (Claude Sonnet 4.6 first), §3.3.2 (2 frontier reasoning additions), §3.3.3 (2-3 open-weights additions, target N≥10), §10.3 (risk that expanded panel shows heterogeneous patterns + mixed-effects mitigation) |
| Q1 | How would the results change if evaluated with real-world datasets with varying difficulty levels and data distribution? | §3.4.1 (WikiTQ subset, 100-200 questions, all 5 formats), §3.4.2 (ChartQA-Pro subset, real-world chart distribution), §3.4.3 (optional CharXiv pilot for "wild" chart-image evaluation) |
| Q2 | What prompt variations of phrasing and constraints would improve Chart Text performance? | §3.6 (prompt sensitivity analysis on Kimi K2.5: Template A current, Template B chain-of-thought, Template C decompose-first, Template D cite-evidence; 4 templates × 5 formats × 1724 questions = 34,480 judgments per model) |
| Q3 | Could alternative graph construction methods like those based on semantic relationships yield more meaningful representations? | §3.2.2 (semantic-edge graph variant: edges = domain-meaningful relations such as neighboring countries / same metropolitan area / industry sector / taxonomic class; re-evaluated on the same 2 models as the cosine variant for direct comparison) |

#### Reviewer HZuL (rating 8, "clear accept")

No weaknesses listed. The substantive observation — "Questions involving aggregation or conditional aggregation show the largest format-dependence variance" — is preserved and developed in v2 §3.1.4 (per-format-tier breakdown surfaces the chart-text-at-medium-size effect that v1 buried) and §4.7 (robustness checks per-domain / per-tier / per-chart-type).

#### Three honest interpretive choices

A few places where the v2 plan does not literally do what a reviewer asked, and the rationale:

1. **NRrg said "Originality: the core concept ... is not entirely novel."** The v2 plan does not change the contribution claim. Instead, it strengthens the differentiation (§2.2 four-pillar framing: five-format scope, strict same-content control, question-level transfer metric, frontier-model panel) and adds InfoChartQA + Bhandari 2026 + Zhang 2026 with explicit "we differ by..." sentences (§6.4). The paper's contribution is real; the issue is positioning, not novelty. The plan pushes back on NRrg's framing rather than capitulating to it.

2. **5243 said "tighten the claims."** Interpreted in two directions: *softer hedging* (§5.1, §5.3) where the v1 overclaims (graph reasoning, reasoning ablation generalizability), and *more rigorous evidence* (§4 statistical upgrades) where the v1 underclaims (mixed-effects regression instead of per-model-then-average). In some places the v2 paper hedges more; in others it builds stronger evidence for the same finding. Both directions are "tightening."

3. **HZuL's rating 8 was generous given the methodological gaps the audit found.** The v2 plan does not optimize for "keep HZuL happy" — v1 already satisfies HZuL. It optimizes for converting NRrg-style critical reviewers into supporters, which is the binding constraint at EMNLP / NAACL / ACL where the median reviewer is harsher than HZuL.

#### Items beyond the reviews

These v2 changes were not requested by any reviewer but emerged from the deep audit (`deep_paper_analysis.md`) and citation integrity scan (`citation_integrity_report.md`):

- Phi-as-primary metric (no reviewer noticed the tetrachoric base-rate inflation; addressed in §4.1).
- Within-ceiling-group variance reporting (no reviewer noticed DeepSeek r=0.716 vs. Qwen r=0.990 inside the same group; addressed in §3.1.7).
- Reasoning-ablation transfer-correlation panel (no reviewer noticed that DeepSeek transfer-r is flat while Gemini transfer-r increases with thinking; addressed in §3.1.8).
- Chart-text size effect (no reviewer noticed chart-text dropping to 81% at medium tier; addressed in §3.1.4).
- Chart-image error mode analysis (no reviewer noticed Kimi at 25% on Q1-lookup vs. 68% on Q4-trend; addressed in §3.1.6).
- 1-format-fail quantification (v1 had "manual inspection" prose; addressed in §3.1.5).
- Citation integrity (no reviewer checked citations; 17 of 21 entries had errors; addressed in §6.1-6.3).
- Three citation-misuse passages in prose (MMTU multi-modal, CharXiv-R, Epoch claim; addressed in §6.2).

These additions are what move the paper from "SURGeLLM workshop accept" to "EMNLP / NAACL / ACL main defensible."

### 1.4 Independent findings to incorporate

These are what I found in the deep audit (`deep_paper_analysis.md`) that were not in any reviewer's report:

- Chart Text has a buried *size effect*: at medium tier (10×5), DeepSeek Chart Text drops to 81.3% while other formats stay >98%. The v1 paper reports tier accuracy averaged across formats and aggregates this away. v2 needs a per-format-tier table.
- Reasoning ablation has a non-obvious finding: DeepSeek's transfer correlation is roughly *flat* with vs. without reasoning (0.74 vs. 0.72) despite +33 accuracy points; Gemini's transfer correlation *increases* with thinking (0.93 → 0.98) despite <1 accuracy point. v2 should foreground this as a counterintuitive finding.
- Chart-image error modes show a clear pattern: vision-capable models read shape (Q4 trend at 68% for Kimi) but cannot extract values (Q1 lookup at 25%, Q3 aggregation at 3%). v2 should develop this as a publishable sub-finding.
- The "1-format fail" 9-13% rate is probably worth a quantitative breakdown rather than the v1 prose ("manual inspection reveals predominantly Q3 and Q7 in Chart Text").
- Within-ceiling-group variance: DeepSeek r=0.716, Qwen r=0.990, Gemini r=0.983. Reporting only the mean (0.90) hides this structure.

### 1.5 Citation overhaul (from `citation_integrity_report.md`)

17 of 21 bib entries have errors. Of those, 14 are major. One (`charxiv2026` citing "CharXiv-R") is critical — it cites a paper that does not exist. Plus three citation-misuse cases in the prose:
- §2 "MMTU extends evaluation to multi-modal table understanding" — MMTU is multi-task, not multi-modal.
- §2 "CharXiv-R" — name does not exist; real paper is "CharXiv".
- §5 "aligning with the cross-benchmark correlations reported by Epoch AI" — Epoch's paper is about benchmark stitching (item-response-theory style), not cross-benchmark correlations.

Fix all 17 entries (templates already in `citation_integrity_report.md`) and rewrite the three misuse passages.

### 1.6 What's missing that should not be missing

- Claude Sonnet 4.6 was in the original 7-model plan (per `CLAUDE.md`) and was dropped without explanation. v2 must run Claude or document why.
- The human baseline study was promised in the v1 paper text ("planned for the camera-ready version") and never delivered. v2 must deliver it.
- Code/data release was promised ("All code, data, and prompts will be released upon publication") and not delivered. v2 must deliver before any submission.

---

## Section 2 — Novelty assessment (May 2026 snapshot)

I ran live searches across 2025–2026 for adjacent work. The 5-format same-content design with tetrachoric/phi transfer measurement remains uncontested. Two adjacent works have appeared since v1's bib was finalized and need to be engaged.

### 2.1 New related work to cite (not in v1's bib)

**InfoChartQA (Xie et al., NeurIPS 2025).** *"InfoChartQA: A Benchmark for Multimodal Question Answering on Infographic Charts"* — 5,948 paired infographic + plain charts sharing the same underlying data but differing in visual presentation. Evaluates 20 MLLMs and finds a substantial performance decline on infographic vs. plain charts. This is the paired-modality-control idea applied to infographic vs. plain chart pairs — directly adjacent to the paper's B-vs-B' (chart-image-vs-chart-text) finding. v2 must:
- Cite InfoChartQA in the related-work chart section.
- Differentiate: InfoChartQA pairs *two visual* representations of the same data (infographic vs. plain). The paper pairs *visual* (chart-image) with *text* (chart-text) of the same data — a fundamentally different control.

**Bhandari et al., Apr 2026 (arXiv 2604.24040).** *"Improving Robustness of Tabular Retrieval via Representational Stability"* — shows that semantically equivalent serializations (csv, tsv, html, markdown, ddl) produce substantially different embeddings and retrieval results. Proposes centroid averaging across serializations to suppress format-specific variation. This is the format-sensitivity problem applied to retrieval, while we apply it to QA. v2 must:
- Cite as concurrent evidence that format effects are pervasive.
- Differentiate: Bhandari operates on *embeddings* (encoder-side); we operate on *task accuracy* (decoder-side). Bhandari proposes a *fix* (centroid averaging); we *characterize* the gap and ask whether it transfers across radically different formats.

### 2.2 Differentiation strategy for v2

The v2 contribution rests on four pillars, none of which are individually unique but whose combination is:

1. **Five fundamentally different representation types.** Most prior work operates within one modality (table-only: Zhang 2026, ToRR, Bhandari) or two (table-and-chart: WikiMixQA, InfoChartQA, DataCross). The paper spans table / chart-image / chart-text / graph-like-serialization / time-series — a wider scope than any single prior work.

2. **Identical content and identical questions across all formats.** Strict same-content control. WikiMixQA, DataCross, and InfoChartQA all maintain same-content but vary across two formats; Zhang 2026 maintains same-content but varies *within* tables (structured vs. semi-structured); the paper extends the strict control to five formats.

3. **Transfer measured at the question level, not the model level.** Most prior work asks "does this model do better on format X or Y." The paper asks "does the *same question* succeed or fail across formats" — a question-paired metric, not a per-format-mean metric. Tetrachoric / phi correlation is the natural metric for this and has not been used at scale in this literature.

4. **Frontier-model panel (March 2026 SOTA).** The paper evaluates Claude / Gemini / Qwen / Kimi / GLM / DeepSeek / MiniMax — a representative slice of March 2026 frontier models from 6+ organizations. v2 expands to 10+ to make model-level claims defensible.

### 2.3 Scooping risk audit

No publication or arXiv preprint as of May 2026 directly subsumes the v2 contribution. The closest scooping risks are:

- **InfoChartQA** has the modality-control idea but for two visual formats only. Differentiation is clean.
- **Zhang 2026** has the same-content controlled-study idea but for table-only. Already cited; differentiation is clean.
- **Bhandari 2026** has the format-sensitivity finding for retrieval. Differentiation is task-level.
- **GraphOmni (ICLR 2026)** evaluates LLMs on graphs across 7 serialization formats. Does not span out to tables or charts. No direct scoop.

The v2 paper's distinguishing claim — "across five fundamentally different format types, text-based comprehension transfers strongly while chart-image is siloed" — has no direct competitor.

---

## Section 3 — Experimental plan (the actual work)

The plan is structured by dependency: re-analyses first (zero new compute), then ablations on existing data (small re-renders + re-eval), then new runs (compute spend), then human study (longest lead time). Each subsection has an "outputs" line specifying what artifact this work produces for the v2 paper.

### 3.1 Re-analyses on existing data (no new compute)

These use the existing 8,620-judgment-per-model data already in `experiments/results/`. They produce most of the statistical-rigor improvements that NRrg asked for and that I flagged in the deep analysis.

**3.1.1 Phi-vs-tetrachoric re-reporting.** Re-render every reported correlation table and figure in two-column format: phi on the left, tetrachoric on the right. Adopt phi as the primary metric. Justify the choice in §3.5 (Metrics) by noting that phi is base-rate-robust and does not require the bivariate-normal latent assumption.

*Outputs:* updated Table 2, Figure 1 (correlation heatmap), Figure 6 (per-model heatmaps).

**3.1.2 Bootstrap CIs on every reported correlation point estimate.** The CI machinery is already in `analyze.py` and the values are in `analysis_output.json`. Surface them in figure captions and table rows. For Table 2 of the v1 paper (accuracy table), add per-cell Wilson CIs (already there) and new column: paired-McNemar test of the *intra-model format-pair* difference.

*Outputs:* updated Table 2 with significance markers, updated Figure 1 caption with CI ranges.

**3.1.3 Mixed-effects model for question-level outcomes.** Fit a logistic mixed-effects regression: outcome = `correct`, fixed effects = `format`, `qtype`, `tier`, `domain`, `format × qtype`, random effects = `model | question_id`. This properly handles the nested structure (multiple questions per sub-table, multiple formats per question, multiple models per format) that v1 ignores. Report fixed-effect coefficients with CIs and likelihood-ratio tests.

*Outputs:* new Table 3 (mixed-effects coefficients), new appendix section on the model.

**3.1.4 Per-format-tier accuracy breakdown.** Replace the v1 §4.6 single sentence about complexity tiers with a per-format-tier table showing accuracy by (format, tier) per model. This surfaces the chart-text-at-medium-size effect that v1 buries.

*Outputs:* new Table 4 (24 cells: 4 text formats × 3 tiers × 2 = with/without ceiling models).

**3.1.5 Quantitative 1-format-fail breakdown.** From `raw_results.jsonl`, identify per-model the questions where exactly one format fails. Report the conditional distribution of `failing_format | qtype` and `failing_format | tier`. Replace the v1 prose ("manual inspection reveals") with a count table.

*Outputs:* new Table 5 in the appendix.

**3.1.6 Chart-image error mode analysis.** From the 3-vision-model data (Kimi, Qwen, Gemini), compute accuracy by `(chart_image, qtype)` and break down failure modes for Q1 (lookup), Q3 (aggregation), Q4 (trend). For each model, sample 50 random failures per qtype and tag them with manual error categories (perception failure, value-extraction failure, reasoning failure, format-misread). This is a publishable sub-finding: vision models can read chart shape but cannot extract values.

*Outputs:* new §4.7 "Chart-image error modes," new Table 6 (error category breakdown), 50-sample examples in appendix.

**3.1.7 Within-ceiling-group variance reporting.** Replace the v1 §4.2 ceiling-group r=0.90 single number with a per-model breakdown for the ceiling group (DeepSeek r=0.716, Qwen r=0.990, Gemini r=0.983) and a discussion of why DeepSeek looks different despite being in the same accuracy range.

*Outputs:* updated §4.2 paragraph, updated Figure 6 with model labels and r values.

**3.1.8 Reasoning ablation re-framing.** Add a "transfer correlation" panel to Figure 4 (currently shows accuracy only). The panel shows that DeepSeek's transfer-r is flat across reasoning on/off (0.74 vs. 0.72) while Gemini's increases (0.93 → 0.98). This makes the reasoning ablation richer than v1's "weaker model gains accuracy."

*Outputs:* updated Figure 4 (two-panel: accuracy delta + transfer-r delta).

### 3.2 Ablations on existing models (re-render + re-eval)

These require re-rendering one or more formats and re-running the evaluation on a subset of existing models. The cost is much lower than the original full panel run because (a) we already have prompts cached, (b) we can target a single model where the effect is largest.

**3.2.1 Graph-without-edges ablation.** Re-render Format C with edges removed (node attributes only). Re-evaluate on Kimi K2.5 (largest transfer effect among mid-range models) and DeepSeek V3.2 (representative ceiling-adjacent model). Compare to the existing Format-C-with-edges results. If accuracy drops, the edges contribute meaningfully and the v1 framing must change. If accuracy is stable, the edge confound is small and we can defend the v1 framing more strongly.

*Outputs:* new §4.8 "Edge contribution in graph format," 2 models × 4 question types × 1724 questions = 13,792 new judgments.

**3.2.2 Semantic-edge graph variant (NRrg's third question).** Re-render Format C with edges based on domain-meaningful relations rather than cosine similarity. For example, in the energy dataset, edges = "neighboring countries"; in transit, edges = "same metropolitan area"; etc. Where domain-meaningful relations don't apply, fall back to the cosine variant. Re-evaluate on the same 2 models. Compare to cosine-edge variant.

*Outputs:* new §4.9 "Semantic-edge graph variant," 2 models × 1724 questions = 3,448 new judgments.

**3.2.3 Per-chart-type analysis.** The v1 chart_image data is already broken down by chart type in the raw results. Re-aggregate accuracy by `(chart_image, chart_type ∈ {bar, line, scatter})` per vision model. Test whether some chart types are systematically harder. This is zero compute — pure re-analysis of existing data.

*Outputs:* new Table 7 "Chart-image accuracy by chart type."

**3.2.4 Token-count-controlled re-analysis of Graph format.** The existing Format C has 2× tokens of Format A. Re-run with token-trimmed Format C (truncate to match Table token count by reducing K in `K=max(3, ⌊N/2⌋)` to K=1). Evaluate on Kimi only. Test whether the high-transfer cluster Table-Graph correlation persists when token counts are matched.

*Outputs:* new appendix subsection "Token-controlled graph variant," 1 model × 1724 questions = 1,724 new judgments.

### 3.3 New model runs (expanded panel)

This is where the budget question matters most. Cost depends on which models we add and how. Per the existing memory feedback, *test 1 call first, measure actual billing, multiply, +50% buffer*.

**3.3.1 Add Claude Sonnet 4.6.** AWS Bedrock credits already in place (per `CLAUDE.md`: $35 remaining out of $100). Run all 4 text formats (1724 × 4 = 6,896 questions) plus chart_image (1724 questions) = 8,620 judgments. Test 10 calls first to measure actual cost. Run resumable per `feedback_api_credits.md`.

*Outputs:* Claude row in Table 2, Claude column in transfer correlation analyses.

**3.3.2 Add 2 frontier reasoning models if accessible.** Candidates: GPT-5 (if released), Claude Opus 4 (premium, expensive), DeepSeek R2 (reasoning-specialized successor to V3.2). Pick based on availability, cost, and architectural diversity. Each adds 8,620 judgments.

*Outputs:* additional rows in Table 2.

**3.3.3 Add 2-3 open-weights models for breadth.** Candidates: Llama 4 (when available), Qwen 3.5 Max, GLM-5 Flash, Mistral Large 3. Adds open-weights coverage and addresses the N=6 reviewer concern.

*Outputs:* additional rows in Table 2.

**3.3.4 Full reasoning ablation across all models.** Currently only DeepSeek V3.2 and Gemini 3.1 Pro have on/off reasoning runs. Extend to every model that supports a reasoning toggle (Claude extended thinking, Kimi K2.5 reasoning mode, Qwen 3.5 thinking, GLM-5 reasoning). Each ablation adds ~6,896 judgments per model (text formats only, since chart_image reasoning is rarely useful for vision tasks).

*Outputs:* upgraded §5.1 (Reasoning Effect) with N=4–6 model pairs instead of N=2.

**Cost discipline note:** before launching any of these runs, do a 10-call test batch on each provider, check actual billing, multiply, add 50% buffer. Report a cost estimate to the user before committing to the full run. This is the rule from `feedback_cost_estimation.md` and applies without exception.

### 3.4 Real-world data extension (NRrg's primary concern)

This is the single biggest defensibility upgrade for top venues. The v1 paper uses 250 sub-tables sampled from 10 datasets. The synthetic-extraction process gives experimental control but has the distributional-bias issue NRrg flagged. v2 needs to demonstrate that the cross-format-transfer finding holds on real-world data not generated by the paper's pipeline.

**3.4.1 WikiTQ subset.** Take 100–200 questions from WikiTableQuestions where the source table is renderable in all 5 formats (numeric content with multiple entities and metrics). Render each in 5 formats using the existing pipeline. Evaluate on the v2 model panel. Compare cross-format transfer correlation against the synthetic benchmark.

*Outputs:* new §4.10 "Real-world data extension (WikiTQ)."

**3.4.2 ChartQA-Pro subset.** Take 100–200 chart-oriented questions from ChartQA-Pro where the underlying data table is recoverable. Render each in 5 formats. Evaluate. This specifically tests the chart-image siloed-modality finding on a more challenging chart distribution than the synthetic matplotlib charts.

*Outputs:* new §4.11 "Real-world chart extension (ChartQA-Pro)."

**3.4.3 CharXiv subset (optional, expensive).** CharXiv has 2,323 charts from scientific papers. A subset (100 charts where the underlying data is well-defined) could provide a "wild" chart-image evaluation. Cost is non-trivial because CharXiv charts have complex structures that may require manual data recovery. Decision: pilot with 30 charts; expand if results are clean.

*Outputs:* new §4.12 (if pilot succeeds).

### 3.5 Human baseline study

The v1 paper text promises this. v2 delivers it.

**3.5.1 Design.** Within-subjects, Latin-square randomized, 50 questions per participant, 20 participants. Each participant sees each question exactly once but in a different format than other participants (so each (question, format) pair has 4 ratings). 20 participants × 50 questions = 1,000 ratings, divided across 5 formats = 200 per format. Inter-rater agreement computed pairwise.

**3.5.2 Recruitment.** Prolific or MTurk, screened for English fluency and basic numerical literacy. Pay at minimum-wage equivalent for the expected 60-minute session. ~$10-15/hour × 20 participants × 1 hour = $200-300 total.

**3.5.3 Protocol.** Web interface presenting one question at a time with the chosen format; 90-second time cap per question; participants can mark "don't know" instead of guessing. IRB approval where required.

**3.5.4 Analysis.** Compute human accuracy per format. Compute inter-rater kappa. Establish a human upper bound and per-format human ceiling. Report whether the format ranking (Table > Graph > Time Series > Chart Text > Chart Image) is preserved in humans.

*Outputs:* new §4.13 "Human baseline study," human accuracy as horizontal line in Figure 1 / Figure 2.

This is the longest-lead-time experiment because it requires participant recruitment, scheduling, and IRB. Start the IRB and recruitment process early.

### 3.6 Prompt sensitivity analysis (5243's third question)

Pick 1 model (Gemini 3.1 Pro for high baseline; Kimi K2.5 for high variance). Run 3 alternative prompt templates per format:
- Template A (current): "Answer the question using the data below."
- Template B (chain-of-thought): "Think step by step, then answer using the data below."
- Template C (decompose-first): "For each step, identify what subset of the data you need; then compute."
- Template D (cite-evidence): "Quote the specific data values you use, then state your answer."

Each template × 1 model × 5 formats × 1724 questions = 34,480 judgments per model. Pick 1 model for v2 (Kimi to maximize variance signal); 2 if budget allows.

*Outputs:* new §5.2 "Prompt sensitivity," new Table 8 (accuracy delta by prompt template).

---

## Section 4 — Statistical analysis upgrades (rigor pass)

These complement Section 3 but are listed separately because they are statistical decisions that affect every result, not single experiments.

### 4.1 Primary metric: phi (with tetrachoric supplementary)

Phi is the appropriate base-rate-robust correlation for binary outcomes. Tetrachoric makes a bivariate-normal latent-variable assumption that is unverified for accuracy data and that systematically inflates correlations at extreme base rates. The v2 paper makes phi primary and reports tetrachoric as a supplementary check.

### 4.2 McNemar tests for paired accuracy comparisons

Every "Format A is X% better than Format B" claim in v1 is unsupported by a paired test. v2 reports a paired-McNemar p-value for every such claim, with Bonferroni correction across the family of comparisons within each model.

### 4.3 Mixed-effects regression as the headline statistical model

Per §3.1.3 above. The mixed-effects model produces fixed-effect coefficients with CIs that the v1's per-model-then-average analysis cannot. The headline finding becomes "format X has fixed-effect coefficient β = ±, p < 0.001 in the mixed-effects model."

### 4.4 Multiple-comparison correction

For every family of correlation comparisons (e.g., all 6 format pairs × 6 models = 36 correlations in Figure 1), report Bonferroni- or Holm-adjusted CIs. The v1 reports neither.

### 4.5 Sample-size justification

For each headline result, compute and report the effective sample size (questions × models) that contributed. The v1 paper claims "transfer is strong" based on what is effectively N≈3 models for the mid-range correlation. v2 makes this explicit.

### 4.6 Effect-size reporting

Cohen's h for accuracy differences between formats, Cohen's q for differences between correlations. Surfaces magnitude alongside significance.

### 4.7 Robustness checks

- Per-domain transfer correlations: does the cross-format finding hold within each of 7 domains?
- Per-tier transfer correlations: does it hold for small / medium / large sub-tables?
- Per-chart-type transfer (where applicable): does it hold for bar vs. line vs. scatter charts?

These all use existing data (no new compute) and can be added to the appendix.

---

## Section 5 — Writing & framing changes

### 5.1 Soften "graph reasoning" framing

Replace "graph reasoning" with "graph-like serialization" or "node-attribute representation" throughout. Move the "constructed serialization" disclosure from §3.2 to the abstract and the contribution list. The Discussion explicitly addresses what the constructed-vs-natural-graph distinction means for the transfer claim.

### 5.2 Soften "first study" claim

Replace "We present the first study measuring cross-format transfer across five fundamentally different representation types" with something like:

> "We extend prior controlled-content methodology — most notably Zhang et al. (2026), who isolate representation effects within table-only variations — to span five fundamentally different representation types, enabling cross-modality transfer measurement."

This positions Zhang 2026 as a precursor and makes the differentiation specific to what we add (five formats spanning text and visual modalities).

### 5.3 Hedge reasoning ablation conclusions

The v1 abstract already says "based on two models and requires further validation." The Discussion should match. Replace the v1 §5 paragraph "Models with strong base inference (Gemini, Qwen) may already internalize the reasoning steps that weaker models must perform explicitly" with a tighter claim: "In our 2-model ablation, the gain from explicit reasoning correlates with the model's no-reasoning baseline. Whether this generalizes across the broader model panel is examined in §5.1.2 [the new full-panel ablation]."

### 5.4 Tighten the Findings/Results structure

The v1 §4.1 has "Finding 1 / Finding 2 / Finding 3" headings and reads like an experimental report. v2 replaces this with a flowing argument:

> "Three patterns emerge consistently. First, accuracy on the table, graph, and time-series formats is within 1–3 percentage points for every model — suggesting the underlying comprehension skill is shared. Second, despite length-matching, chart-text descriptions consistently lag tables by 7–9 percent. Third, chart images are the outlier: vision models read trends but fail at value extraction, producing accuracy gaps of 20–50 percent compared to chart-text on identical data. We develop each pattern in turn."

### 5.5 Add a "Scope of Claims" subsection in the Discussion

Explicit list of what the paper does and does not claim:
- *Does claim:* Strong text-format transfer in mid-range frontier models, consistent across domain and tier.
- *Does not claim:* That the synthetic benchmark generalizes to all real-world structured-data tasks (motivates §3.4).
- *Does not claim:* That chart image is universally siloed (motivates expanded vision-model panel and per-chart-type analysis).
- *Does not claim:* That CoT helps all models equally (motivates full reasoning ablation).

### 5.6 Limitations expansion

Explicit acknowledgment of:
- Tetrachoric correlation's bivariate-normal assumption (now reported as supplementary).
- The constructed nature of Format C (graph).
- The single language (English) in all questions and data.
- The single tokenizer family (cl100k_base) used for length matching.
- The synthetic-extraction pipeline producing sub-tables with potentially different difficulty distributions than wild data (addressed in §3.4 but never fully closed).

---

## Section 6 — Citation & integrity overhaul

### 6.1 Apply all 17 corrected bib entries

From `citation_integrity_report.md`. Templates already written. Two bib keys change: `liu2026formatprior` → `liu2025formatprior`, `charxiv2026` → `charxiv2024`. Update all `\cite{}` calls in `paper.tex` accordingly.

### 6.2 Fix the three citation-misuse passages in prose

- §2 "MMTU extends evaluation to multi-modal table understanding" → "MMTU extends evaluation to a multi-task table understanding suite covering 25 task types over diverse domains."
- §2 "CharXiv-R" → "CharXiv".
- §5 "aligning with the cross-benchmark correlations reported by Epoch AI" → either remove, or rewrite as "consistent with the unidimensional capability factor reported by Epoch AI's benchmark-stitching analysis (Epoch AI, 2025) and by Ilić's (2023) factor-analytic study."

### 6.3 Re-verify cited numbers from corrected sources

Three claims in v1 came from now-corrected citations and need re-verification:
- "TSAQA showed that fine-tuned LLMs can achieve 67.68%" — verify against the actual TSAQA paper (arXiv 2601.23204, Jing et al.).
- "MMTS-Bench found that general LLMs with CoT can outperform specialized time-series models" — verify against the actual MMTS-Bench paper (arXiv 2602.08588, Yin et al.).
- "HeaRTS demonstrated that temporal complexity degrades LLM performance" — verify against the actual HeaRTS paper (arXiv 2603.06638, Li et al.). Also: change "Heart Rate" to "Health" wherever the paper text references the HeaRTS paper.

### 6.4 Add new related work

- Cite InfoChartQA (Xie et al., NeurIPS 2025) in the chart-comprehension paragraph. Differentiate as B-vs-B' modality control vs. their infographic-vs-plain.
- Cite Bhandari et al. (Apr 2026, arXiv 2604.24040) in the format-sensitivity discussion. Differentiate as task-accuracy vs. their embedding-stability.

### 6.5 Run aclpubcheck and integrity check on the v2 manuscript

Pre-submission, both:
- `uvx --from git+https://github.com/acl-org/aclpubcheck aclpubcheck --paper_type long paper.pdf`
- `ai-research-integrity-check` skill on the full paper + bib

Both pass before any submission.

---

## Section 7 — Infrastructure (reproducibility commitments)

The v1 paper text promises code/data release. v2 must deliver. This is also a substantive defense against the "synthetic-data" critique: a public, reproducible benchmark is harder to dismiss than a closed pipeline.

### 7.1 Repository setup

- Public GitHub repository: `farseen/structreason-transfer` (or chosen name).
- Top-level `README.md`: install (Python 3.11, requirements.txt), data download / regenerate from raw datasets, runner commands per provider, figure regeneration, test commands, license, contact.
- License: code MIT or Apache-2.0; data CC-BY-4.0.
- `.gitignore` audited: no `.env`, no API keys committed historically.
- `requirements.txt` pinned to specific versions for reproducibility.
- `scripts/` directory with one-shot reproducibility scripts for each headline result.

### 7.2 Pre-v2 git cleanup

Currently only `experiments/experiment-plan.md` and `sota/sota-report.md` are committed. The full project state needs to be committed before any v2 work begins:

- Commit the v1 paper, all experiment code, all results, all figures.
- Tag a release `v1.0-surgellm` to pin the SURGeLLM artifact.
- All v2 work happens on a `v2/main` branch with feature branches per upgrade.

### 7.3 Dataset archive

- Archive the 250 sub-tables, 1,724 questions, and 5-format renderings on Zenodo (DOI) or Hugging Face Datasets. Stable identifier means the v2 paper can cite a specific snapshot.
- Archive raw model outputs (`raw_results.jsonl` files) so other researchers can re-score without re-running models.
- Include format generation scripts so the dataset can be regenerated from raw datasets.

### 7.4 Reproducibility testing

Before v2 submission, do a clean-room reproduction: fresh clone, follow the README, regenerate all results and figures from scratch. Document any gaps. Fix them.

---

## Section 8 — v2 paper structure (proposed 8-9 page outline)

Long paper at most ACL venues = 8 pages content + 1 reviewer-revision page + unlimited appendix.

```
Abstract (250 words)
1. Introduction
2. Related Work (1.5 pages)
   2.1 Format effects (Zhang 2026, Bhandari 2026, Liu 2025, Ho 2025)
   2.2 Single-modality benchmarks (TabFact, ChartQA, GraphOmni, TSAQA)
   2.3 Cross-modal benchmarks (WikiMixQA, DataCross, InfoChartQA)
   2.4 Cross-benchmark capability studies (Ilić 2023, Epoch AI 2025)
3. Methodology (1.5 pages)
   3.1 Data construction (250 sub-tables, 10 datasets, 7 domains)
   3.2 Five representation formats (with explicit "graph-like serialization" framing)
   3.3 Question generation (7 types, programmatic ground truth)
   3.4 Models (now N=10+, justification for frontier coverage)
   3.5 Metrics (phi primary, tetrachoric supplementary, mixed-effects regression as headline statistic)
4. Results (3 pages)
   4.1 Overall accuracy
   4.2 Cross-format transfer (phi-primary)
   4.3 Question type analysis (with format×qtype interaction)
   4.4 Modality isolation: chart image vs. chart text
   4.5 Error agreement analysis
   4.6 Domain effects (with significance tests)
   4.7 NEW: Chart-image error modes (perception vs. value extraction vs. reasoning)
   4.8 NEW: Edge contribution in graph format (graph-without-edges ablation)
   4.9 NEW: Semantic-edge graph variant
   4.10 NEW: Real-world data extension (WikiTQ + ChartQA-Pro)
5. Ablations (1.5 pages)
   5.1 Reasoning ablation (now full panel, with transfer-correlation panel)
   5.2 NEW: Prompt sensitivity (Kimi K2.5 + 4 templates)
   5.3 NEW: Human baseline study
   5.4 Question difficulty (basic vs. hard)
   5.5 Complexity tiers (with per-format breakdown)
6. Discussion (1 page)
   - Skills transfer, modality doesn't (extended with vision-error-mode finding)
   - Chart text: information-loss format
   - Reasoning is not universally necessary (now N≥4 in ablation)
   - Implications for benchmark design
   - Why does Chart Text underperform? (preserve v1 hypotheses + new evidence)
   - NEW: Scope of claims
7. Limitations (0.5 page)
8. Conclusion (0.5 page)
References
Appendix:
   A. Per-model correlation matrices (Figure 6 expanded for N≥10)
   B. Mixed-effects regression coefficients
   C. Per-format-tier accuracy
   D. Quantitative 1-format-fail breakdown
   E. Real-world data details
   F. Human study protocol
   G. Prompt templates
   H. Sample question / format examples (one per format)
   I. Cost and compute disclosure
```

---

## Section 9 — Sequencing (dependency-ordered)

The plan is ordered by what unblocks what, not by calendar.

### Phase 0 — Foundation

Before any new experiment work:
- Apply the 17 bib corrections from `citation_integrity_report.md`.
- Fix the 3 citation-misuse passages in prose.
- Verify TSAQA / MMTS-Bench / HeaRTS specific numbers cited in §2.
- Run `ai-research-integrity-check` on the corrected manuscript. Pass = clear.
- Commit current project state to git, tag `v1.0-surgellm`.
- Set up the public GitHub repo skeleton.

This phase is the smallest and produces the largest reduction in long-term risk.

### Phase 1 — Re-analyses on existing data (Section 3.1)

All eight sub-items in §3.1 use the existing 8,620-judgment-per-model data. Outputs feed directly into v2 paper figures and tables.

Dependency: Phase 0 done.

### Phase 2 — Ablations on existing models (Section 3.2)

Graph-without-edges ablation (3.2.1) and semantic-edge variant (3.2.2) need re-rendering and re-evaluating, ~5,000–13,000 new judgments each. Per-chart-type (3.2.3) and token-controlled graph (3.2.4) are re-analyses.

Dependency: Phase 1 in progress (re-analyses don't need to be complete to start ablations).

### Phase 3 — Statistical-rigor upgrades (Section 4)

Primary metric switch, McNemar tests, mixed-effects model — all rerun on Phase 1 + Phase 2 data.

Dependency: Phase 1 complete.

### Phase 4 — Expanded model panel (Section 3.3)

Add Claude Sonnet 4.6 first (already-allocated AWS Bedrock credits). Cost-test before committing. Add 2 more frontier models and 2 open-weights models contingent on budget. Full reasoning ablation across all models last.

Dependency: Phase 0 done. Cost test before each provider.

### Phase 5 — Real-world data extension (Section 3.4)

WikiTQ subset first (cheapest to render). ChartQA-Pro subset second. CharXiv pilot last (most expensive).

Dependency: Phase 1 + Phase 4 in progress.

### Phase 6 — Human baseline study (Section 3.5)

Longest lead time. Start IRB / pilot protocol design as early as possible — in parallel with Phase 1.

Dependency: protocol approval, recruitment platform setup.

### Phase 7 — Prompt sensitivity (Section 3.6)

Kimi K2.5 with 4 prompt templates × 5 formats. ~34,480 judgments.

Dependency: Phase 4 (Kimi access already in place).

### Phase 8 — Writing & assembly (Section 5 + Section 8)

Apply all framing changes. Restructure §4 per outline. Write new sections. Assemble v2 manuscript.

Dependency: All prior phases produce inputs.

### Phase 9 — Pre-submission audit

- aclpubcheck on the v2 PDF.
- ai-research-integrity-check on v2 bib.
- ai-research-pre-submit on the v2 paper.
- ai-research-fig-check on the v2 figures.
- Clean-room reproducibility test from public repo.
- Page count, anonymization (if venue is double-blind).

Dependency: Phase 8 complete.

### Phase 10 — Submission

Choose the ARR cycle that fits the work, not the other way around. May, June, August, October, December cycles all feed into ACL 2027 / NAACL 2027 / EMNLP 2027. Commit to the cycle whose timing matches the *finished work*, not the cycle whose timing pressures shortcuts.

---

## Section 10 — Risks & mitigations

### 10.1 The cross-format-transfer finding may not survive on real-world data

**Risk:** §3.4 (real-world extension) reveals that synthetic and real-world transfer correlations diverge substantially. The v1 headline claim "skills transfer across text formats" may not hold on WikiTQ or ChartQA-Pro.
**Mitigation:** Run §3.4 early. If the finding doesn't hold, the v2 paper *changes its central claim* to "synthetic data overstates transfer; real-world transfer is weaker." This is still a publishable finding and an honest correction. Better to know early.

### 10.2 Phi-primary reporting may weaken the headline

**Risk:** Switching from tetrachoric to phi reduces the headline correlation from r=0.87 to r≈0.4 in the high-transfer cluster. "r=0.4 transfer" is a much weaker headline than "r=0.85 transfer."
**Mitigation:** Reframe the claim. Phi=0.4 for binary outcomes corresponds to substantial above-chance agreement (it's not the same scale as Pearson r for continuous data). Report both metrics and explain what each means. The headline becomes "consistent above-chance cross-format agreement (phi=0.4) at the question level, robust across models" — still a publishable claim.

### 10.3 Expanded model panel may show heterogeneous patterns

**Risk:** The v1 paper reports a clean "Table ≈ Graph ≈ Time Series; Chart Text weaker; Chart Image siloed" pattern across 6 models. With N=10+, the pattern may fragment and become model-class-dependent.
**Mitigation:** Run the mixed-effects model with `model` as a random effect. If the format effect is robust across the random-effect distribution, the headline holds even with heterogeneous per-model patterns.

### 10.4 Human baseline may invalidate the ranking

**Risk:** Humans may not show Table > Graph > TimeSeries > ChartText > ChartImage. They may find Chart Image easier than Chart Text (charts are designed for human consumption).
**Mitigation:** This is interesting either way. If human ranking matches LLM ranking, the v2 paper has a strong "format effects are universal" claim. If it diverges, the v2 paper has a strong "format effects are LLM-specific, indicating a cognitive gap" claim.

### 10.5 Citation re-verification may reveal more errors

**Risk:** The 17-error finding was based on a sample of 21 entries. As we re-verify cited numbers (TSAQA 67.68%, MMTS-Bench CoT claim, HeaRTS temporal-complexity claim), more inconsistencies may emerge.
**Mitigation:** Treat any inconsistency as a hard fix. Write the paper to make minimal claims about prior work — only cite specific numbers from prior papers if we have actually verified them against the source.

### 10.6 Concurrent work may scoop part of the contribution

**Risk:** Between now and v2 submission, another paper may publish a similar 5-format same-content benchmark.
**Mitigation:** Rapid Phase 0 + Phase 1 + Phase 4 (re-analyses + Claude addition) lets us put a strong arXiv preprint out earlier as a placeholder. The full v2 paper can come later with the human study and expanded ablations.

### 10.7 Real-world data extension reveals format-specific licensing or content issues

**Risk:** WikiTQ tables don't all permit redistribution; ChartQA-Pro charts may have copyright issues for re-rendering.
**Mitigation:** Use only datasets with permissive licensing (CC-BY, MIT, public domain). Document each dataset's license in the public repo. Where re-rendering is questionable, link to the original rather than redistributing.

### 10.8 Budget exhaustion mid-experiment

**Risk:** Per `feedback_cost_estimation.md`, my historical estimates are 7–10× low for OpenRouter. The v2 plan adds substantial new compute.
**Mitigation:** 10-call test batch on each new provider. Real billing measurement. +50% buffer in every estimate. Resumable runners (per `feedback_api_credits.md`). User approval before any spend exceeding $25.

---

## Section 11 — One-page TL;DR

The v2 paper is a serious upgrade of v1:
- Phi as primary correlation metric, with mixed-effects regression as headline statistic.
- Bootstrap CIs, McNemar tests, multiple-comparison corrections everywhere.
- Graph-without-edges and semantic-edge ablations to address the constructed-graph confound.
- Expanded model panel from N=6 to N≥10 including Claude Sonnet 4.6 and 2+ frontier additions.
- Full reasoning ablation across all models, not just 2.
- Real-world data extension via WikiTQ + ChartQA-Pro to address the synthetic-data concern.
- Human baseline study (within-subjects, Latin-square, 20 participants × 50 questions).
- Prompt sensitivity analysis (4 templates × 1 model × 5 formats).
- Per-format-tier accuracy breakdown (surfaces the chart-text-at-medium effect).
- Chart-image error mode analysis (perception vs. value extraction vs. reasoning).
- Bib overhaul: 17 corrected entries + 3 prose citation-misuse fixes + 2 new citations (InfoChartQA, Bhandari 2026).
- Public repo, dataset archive, full reproducibility commitment.
- Writing pass: soften graph framing, soften "first study" claim, hedge reasoning conclusions, tighten Findings structure, add explicit Scope-of-Claims subsection, expand Limitations.

The plan is dependency-ordered. Phase 0 (citation overhaul + git cleanup + repo skeleton) is the highest-leverage starting point. Phase 6 (human study) has the longest lead time and should be initiated in parallel.

The contribution remains novel as of May 2026. Closest concurrent work (InfoChartQA, Bhandari 2026, Zhang 2026 ICLR) is differentiated. The paper's distinguishing claim — five fundamentally different format types, identical content, transfer measured at the question level — has no direct competitor.

This is what a top-conference submission needs to look like.
