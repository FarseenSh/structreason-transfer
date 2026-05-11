# Deep Paper Analysis — StructReason-Transfer

**Paper:** Do Structured Data Comprehension Skills Transfer Across Representation Types?
**Status at SURGeLLM 2026:** Accept (mean rating 6.33). Going non-archival to allow EMNLP / NAACL / ACL v2 submission.
**Purpose of this report:** Independent technical review by reading the paper line-by-line, auditing claims against the underlying data, and comparing with each reviewer's verdict. Output is a ranked issue list and a v2 plan.

This is **my own analysis** of the paper, formed by reading the LaTeX source, the analysis_output.json, the bib file, and verifying claims against the raw correlation matrices. The reviewer comparison comes after, so I am not anchored on what they wrote.

---

## Section 1 — Independent technical review (my own read)

### 1.1 What the paper claims

The paper makes four headline claims:

1. Structured data comprehension transfers strongly across text-based formats (table, graph, time series) with mean tetrachoric r=0.85.
2. Chart-text descriptions show consistently lower transfer (r=0.65) despite length-matching.
3. Chart-image comprehension is siloed: 20-50% accuracy gap vs. equivalent chart-text.
4. Chain-of-thought reasoning helps DeepSeek (+24-38%) but not Gemini (<1%), suggesting reasoning benefits are model-dependent.

The contribution claim: this is the *first study* measuring cross-format transfer across five fundamentally different representation types (table, chart-image, chart-text, graph, time-series) with identical content and programmatic ground truth.

### 1.2 What is genuinely novel and well-executed

- **The five-format same-content design is a real contribution.** Prior cross-format work either varies content alongside format (WikiMixQA, DataCross) or stays within one modality (Zhang 2026 ICLR — table-only). Holding content fixed across five formats is a meaningful methodological step that lets the paper isolate format effects from content effects.
- **Programmatic question generation with deterministic ground truth.** The pandas-computed answers eliminate LLM-judge bias, which is a clean experimental choice and avoids the well-known judge contamination issues in LLM evaluation.
- **The B vs. B' (chart-image vs. chart-text) modality control is genuinely informative.** When you length-match the chart-text to the table and still see a 20-50% accuracy gap on chart-image, the conclusion that "vision is the bottleneck, not chart comprehension" is well-supported.
- **The reasoning ablation is useful** — even though it is on only 2 models, the contrast between DeepSeek (+30%) and Gemini (<1%) is striking and challenges the "CoT always helps" assumption.
- **The decision to release questions, formats, and code is good open-science practice** (subject to actually doing it, which has not happened yet).

### 1.3 Paper-internal issues I noticed before looking at the data

**1.3.1 The "graph" framing is overstated.**
Format C is described as an "entity-relationship graph" with "top-K edges by metric cosine similarity." The paper acknowledges this in §3.2 ("constructed serialization of tabular data into graph-like text, not a natural graph structure") but then uses "graph reasoning transfer" throughout the abstract, intro, results, and conclusion. A reader who doesn't reach §3.2 carries away a false claim. The whole "graph reasoning" framing is a marketing choice that the experiment does not support — what is actually measured is whether models can answer questions about node-attribute serializations augmented with cosine-similarity edges.

**1.3.2 The "first study" claim is strong but defensible.**
Zhang 2026 ICLR ("Same Content, Different Representations: A Controlled Study for Table QA") explicitly claims to be "the first controlled study that isolates the role of table representation by holding content constant." Their scope is table-only (structured vs. semi-structured). The paper's claim of "first across five fundamentally different representation types" is differentiated from theirs but the framing should acknowledge Zhang as the closest prior work in spirit.

**1.3.3 The reasoning ablation section overclaims from N=2.**
"DeepSeek V3.2 gains 24-38%; Gemini 3.1 Pro gains <1%" → "reasoning benefits may vary substantially across models." The abstract does hedge with "though this observation is based on two models and requires further validation," which is good. But the Discussion (§5) makes broader claims like "Gemini and Qwen may already internalize the reasoning steps that weaker models must perform explicitly" — extrapolation from 2 models to a model-class-level claim.

**1.3.4 The `Findings 1/2/3` structure (§4.1) reads as an experimental report, not a polished paper.**
This is an aesthetic issue but it accumulates with the mechanical "Per-model variation" / "Interaction between question type and format" paragraphs. Papers at top venues read more like arguments; this one reads like a dump of separately-completed analyses.

**1.3.5 The "Domain Effects" section (§4.6) is too thin.**
It claims agriculture (95.4%) and energy (94.5%) are easiest, transit (90.3%) and air quality (90.6%) are hardest. The 5-point spread is small relative to the 95% Wilson CIs reported elsewhere. Without significance tests, this could be noise. The interpretation ("metric naming transparency, numerical range distributions") is post-hoc.

**1.3.6 Token counts and format fairness.**
§3.6 reports median tokens per format: Table 276, Chart Text 270 (length-matched), Graph 520, Time Series 380. Graph is 2× longer. The paper says "we note this as a potential confound." It does not actually run a length-controlled ablation on graph. If graph-without-edges performed similarly to graph-with-edges, the edge-length confound would be partially addressed. Without that ablation, the high-transfer cluster (Table-Graph-TimeSeries r=0.85+) is entangled with the fact that Graph carries 2× the information density of Table.

**1.3.7 The Appendix is sparse.**
Two figures + two tables + correlation matrices in the analysis JSON. For a paper that hangs on tetrachoric correlations, I'd expect: per-pair bootstrap CIs, McNemar tests for accuracy differences, scatter plots of Format A vs. Format C accuracy with point sizes, prompt templates, dataset card with full domain/source/license info, sample question + answer + format pair illustrations. The paper underspends the page-unlimited appendix budget.

**1.3.8 The Limitations paragraph (§5) is honest but minimal.**
It names: N=6, constructed graphs, synthetic sub-tables, single prompt template, missing human baseline. What is missing from the limitations: (a) tetrachoric correlation's known instability at extreme base rates, (b) the gap between phi and tetrachoric being interpretable, (c) the fact that "chart_image" is evaluated on only 3 of 6 models (sample size for that finding is N=3 models × 1724 questions, not N=6), (d) what happens when the underlying table has non-numeric or mixed-type columns (the experiment seems to assume numeric metrics throughout).

---

## Section 2 — Data audit: claim-versus-data verification

I verified the paper's headline numbers against the raw correlation matrices in `experiments/results/analysis_output.json`. Conclusions:

### 2.1 The headline r=0.85 number checks out — but not in the way the paper implies

The paper says "averaged tetrachoric r=0.84 between table, graph, and time series representations (r=0.85 overall)." The `_averaged` matrix in the analysis JSON gives:

| Format pair | Averaged r (across 6 models) |
|---|---|
| table-graph | 0.855 |
| table-timeseries | 0.873 |
| graph-timeseries | 0.878 |
| **High-transfer cluster mean** | **0.869** |
| table-chart_text | 0.647 |
| chart_text-graph | 0.651 |
| chart_text-timeseries | 0.645 |
| **Chart-text-pairs mean** | **0.648** |

So the headline r=0.85/0.65 numbers check out as **across-model means of per-model tetrachoric r**. However, this masks enormous between-model variance:

| Model | Mean text-format accuracy | High-transfer cluster r | Chart-text-pair r |
|---|---|---|---|
| DeepSeek V3.2 | 95.1% | 0.716 | 0.507 |
| MiniMax M2.5 | 93.5% | 0.745 | 0.562 |
| Kimi K2.5 | 86.8% | 0.906 | 0.715 |
| GLM-5 | 86.9% | 0.872 | 0.722 |
| Qwen 3.5 Plus | 97.0% | 0.990 | 0.680 |
| Gemini 3.1 Pro | 97.0% | 0.983 | 0.700 |

The high-transfer cluster r ranges from **0.716 (DeepSeek)** to **0.990 (Qwen)**. That is not a small range. Reporting only the mean (0.869) buries this.

### 2.2 The "ceiling effect robustness check" arithmetic is correct but the conclusion is misleading

§4.2 splits models into "ceiling group (>95% acc; n=3)" and "mid-range group (<95%; n=3)." It reports ceiling r=0.90, mid-range r=0.84 for table-graph-timeseries pairs.

I verified:
- **Ceiling group** (DeepSeek, Qwen, Gemini): high-transfer r = (0.716 + 0.990 + 0.983) / 3 = **0.896**. ✓ Paper claim r=0.90 matches.
- **Mid-range group** (MiniMax, Kimi, GLM-5): high-transfer r = (0.745 + 0.906 + 0.872) / 3 = **0.841**. ✓ Paper claim r=0.84 matches.

So the arithmetic is honest. But the **conclusion** ("the strong-transfer finding is not an artifact of ceiling effects") is misleading for two reasons:

1. **Within the ceiling group, Qwen (r=0.990) and Gemini (r=0.983) versus DeepSeek (r=0.716) tells a different story.** Qwen and Gemini sit at 99%+ accuracy on Table, Graph, and Timeseries — they make ~14 errors out of 1700+ questions per format. With sparse errors, **tetrachoric correlation is essentially uninformative**: it depends on whether those few errors happen to coincide. That's a base-rate artifact, not a transfer signal.

2. **DeepSeek at 95% accuracy, also in the ceiling group, shows r=0.716** — much closer to the mid-range MiniMax (0.745) than to Qwen/Gemini. The "ceiling group" label hides that DeepSeek is statistically more like MiniMax than like Qwen/Gemini.

The right framing: tetrachoric correlation at >97% accuracy is an unstable estimator that should not anchor a paper's headline number. The robust comparison would use mid-range models, where r=0.84.

### 2.3 Bootstrap confidence intervals are very wide — paper presents point estimates without CIs in headline

Looking at DeepSeek V3.2's bootstrap CIs (full-question text-format pairs):

| Pair | Point r | 95% CI |
|---|---|---|
| table-chart_text | 0.398 | [0.207, 0.547] |
| table-graph | 0.638 | [0.393, 0.781] |
| table-timeseries | 0.749 | [0.587, 0.855] |
| chart_text-graph | 0.592 | [0.427, 0.730] |
| chart_text-timeseries | 0.532 | [0.367, 0.660] |
| graph-timeseries | 0.759 | [0.599, 0.865] |

The CIs span ~0.2-0.4 width. The paper's table 2 reports accuracy with Wilson CIs but the **correlation point estimates have no CIs at all**. Reviewer NRrg correctly flagged this — it is a more serious issue than even NRrg realized, because the CIs are wide enough to make the point estimates meaningfully uncertain.

The "basic questions" CIs are even wider — for DeepSeek, table_vs_graph on basic Q has CI of [-0.789, 0.919], which is essentially "could be anything from large negative to large positive." That CI should have killed the basic-vs-hard split as a meaningful comparison for DeepSeek.

### 2.4 Phi vs. tetrachoric show very different stories, and the paper picks the friendlier one

For DeepSeek V3.2 table-graph:
- Tetrachoric r = 0.638
- Phi = 0.242
- (Paper-reported value: tetrachoric, contributing to r=0.86 average)

Tetrachoric correlation assumes that the dichotomous outcomes are derived from an underlying bivariate-normal latent variable. When that assumption is violated — for example, when one or both formats are at >95% accuracy — tetrachoric **systematically inflates the apparent correlation** relative to phi. The paper's own data shows this: across all 6 main models, mean phi for the high-transfer cluster is roughly **0.4** while tetrachoric is **0.87**. That is a 2× difference.

The paper says it reports phi as a secondary metric (§3.5) but does not actually report a phi-based version of the headline finding. The equivalent phi-based statement would be "mean phi r=0.4 between text formats" — which is not "strong transfer," it's "moderate transfer." This is a meaningful framing choice the paper does not justify.

### 2.5 The "all-wrong rate confirms transfer" argument confuses base rates with correlation

§4.4 (Error Agreement Analysis) reports:

| Model | All right | All wrong | 1-format fail |
|---|---|---|---|
| DeepSeek V3.2 | 87.3% | 0.3% | 10.2% |
| Qwen 3.5 Plus | 89.7% | 0.5% | 9.6% |
| Gemini 3.1 Pro | 89.8% | 0.5% | 9.5% |
| Kimi K2.5 | 75.1% | 4.6% | 11.3% |

The paper says high "all right" + low "all wrong" "confirms strong cross-format transfer." This conflates **success agreement** (which is mostly base-rate-driven for high-accuracy models) with **error agreement** (which is the actual transfer signal). For Kimi K2.5 at 89% mean accuracy, independent errors would predict an all-wrong rate of (0.11)^4 = 0.015%. Observed is **4.6%** — 300× higher than independence predicts. That is the strong transfer signal. Conversely, Qwen at 99% accuracy would predict all-wrong rate of (0.01)^4 ≈ 0%; observed 0.5% is also far above that, also a strong signal. But the paper's framing of "high all-right rate" is mostly redundant with "high accuracy" and adds little.

### 2.6 The reasoning ablation is more interesting than the paper says

DeepSeek V3.2 with vs. without reasoning, plus Gemini with vs. without thinking:

| Model variant | Mean text-format acc | High-transfer r | Chart-text-pair r |
|---|---|---|---|
| DeepSeek V3.2 (with reasoning) | 95.1% | 0.716 | 0.507 |
| DeepSeek V3.2 (no reasoning) | 62.3% | 0.739 | 0.658 |
| Gemini 3.1 Pro (thinking on) | 97.0% | 0.983 | 0.700 |
| Gemini 3.1 Pro (no thinking) | 96.8% | 0.933 | 0.626 |

Three observations the paper does not make:

1. **DeepSeek's transfer correlation is essentially flat with vs. without reasoning** (0.74 vs. 0.72). Reasoning adds ~33 accuracy points but does not reconfigure how it solves the questions across formats. The paper's claim that "the relative format ranking is preserved" is true but understates the finding: it is not just the *ranking* that's preserved, the *correlation structure* is preserved.

2. **Gemini's transfer correlation actually increases with thinking** (0.93 → 0.98). Thinking adds <1 accuracy point but tightens the cross-format coupling. This is the opposite pattern from accuracy.

3. **DeepSeek without reasoning has higher transfer than DeepSeek with reasoning on chart_text pairs** (0.658 vs. 0.507). This contradicts the paper's narrative that reasoning helps. For chart-text specifically, reasoning may hurt cross-format consistency.

These observations would deepen the reasoning section.

### 2.7 Sub-table tier accuracy reveals a Chart-Text size effect

Looking at DeepSeek:
- small (5×3): table 98.8%, chart_text 98.6%, graph 99.0%, timeseries 98.6%
- medium (10×5): table 98.6%, chart_text 81.3%, graph 98.9%, timeseries 98.1%
- large (20×8): table 93.6%, chart_text 84.6%, graph 95.0%, timeseries 92.9%

**Chart Text falls off a cliff at medium size and stays low at large size, while the other three formats stay above 90% even at large.** The paper reports complexity-tier accuracy aggregated across formats (§4.6) but does not break it out by format-tier. The aggregated 88.5% large-tier number masks that Chart Text drops to 81% at medium, which is 17 points below table at medium.

This is a substantive finding the paper buried.

### 2.8 The chart_image data is reported only for 3 models — sample size is smaller than implied

The paper's headline #3 claim ("chart image comprehension is largely siloed, with a 20-50% accuracy gap") is based on Kimi (31.9%), Qwen (58.9%), and Gemini (70.6%). Three data points. The 20-50% range comes from Gemini's 19.6 to Kimi's 49.7. This is a real finding but the inference is weaker than "siloed" — it could just as easily be "vision is hard for some models and we have 3 models so we cannot tell why."

The DeepSeek-MiniMax-GLM-5 group is non-vision and contributes nothing to this finding. The "siloed across modality" claim is supported by 3 model evaluations.

---

## Section 3 — Critical methodological issues none of the reviewers caught

These are the issues I think are most important and that no reviewer flagged.

### 3.1 Tetrachoric base-rate instability at high accuracy (CRITICAL)

The headline transfer finding is anchored on Qwen (r=0.99) and Gemini (r=0.98), which sit at 99%+ accuracy on table/graph/timeseries. At those base rates, tetrachoric correlation is dominated by whether the few errors happen to coincide rather than by genuine transfer. The mid-range estimate (r=0.84) is more trustworthy and should be the headline number, with ceiling models reported as a separate (and statistically less informative) row.

This is the single biggest methodological issue. None of the reviewers noticed.

### 3.2 The phi-vs-tetrachoric ratio is a 2× framing choice (CRITICAL)

For the same underlying data, phi r ≈ 0.4 and tetrachoric r ≈ 0.87 in the high-transfer cluster. The paper picks tetrachoric as primary. Tetrachoric assumes bivariate normality of latent variables, which is a strong and unverified assumption for binary correctness data. A defensible reporting strategy would be:

- Report both phi and tetrachoric in the main table.
- Justify the bivariate-normal assumption (or flag that it is untested).
- Use phi as the primary in robust readings.

Saying "r=0.85 transfer" when the alternative metric on the same data says "r=0.4" without explaining why is a one-sided framing choice.

### 3.3 The "first study" claim does not hold up cleanly against Zhang 2026 (MEDIUM)

Zhang 2026 ICLR explicitly claims "the first controlled study that isolates the role of table representation by holding content constant." Their study is table-only (structured vs. semi-structured). The paper's "first across five fundamentally different representation types" claim is differentiated, but Zhang's framing of "first controlled study" is structurally identical and predates this paper at ICLR 2026.

The honest framing: "We extend Zhang et al.'s controlled-content methodology from table-only to five formats spanning text and image modalities."

Reviewer 5243 hinted at this ("contribution would benefit from more careful positioning relative to prior work") but did not name Zhang 2026 specifically.

### 3.4 The Graph format's 2× token confound is acknowledged but not addressed (MEDIUM)

§3.6 says "Graph representations are approximately 2× longer due to edge descriptions; we note this as a potential confound." The paper does not run a graph-without-edges ablation. Without it, the "Table ≈ Graph ≈ Time Series" finding is partially driven by the fact that Graph carries 2× the surface information.

The simplest fix: re-render Format C without edges, re-evaluate at least Kimi (where transfer effects are most visible), and report whether edge-free Graph performs the same as edge-included Graph. If yes, the edge confound is small. If no, the framing must change.

NRrg flagged this concern but did not specify the ablation needed.

### 3.5 The "1-format fail" interpretation is unquantified (MEDIUM)

§4.4 says these are "predominantly Q3 (aggregation) and Q7 (conditional aggregation) questions presented in Chart Text format" via "manual inspection." With ~10% of 1700 questions being 1-format fails, this is ~150-200 questions per model. That should be a quantitative breakdown table, not a manual-inspection sentence.

### 3.6 Chart-text size-effect is real and buried (MEDIUM)

Per §2.7 above. Chart Text at medium size drops to 81% accuracy for DeepSeek while other formats stay >98%. The paper aggregates this away by reporting tier accuracy averaged across formats.

### 3.7 No analysis of chart-image error modes (LOW-MEDIUM)

For Kimi K2.5, Q1 (lookup) on chart_image is 24.8% — barely better than random for a 4-class numerical lookup. Q4 (trend) on chart_image is 68% — much better. Q3 (aggregation) on chart_image is 3.2% — essentially zero. There's a clear pattern: vision-capable models can read chart shape (trend) but cannot extract precise values. This is a publishable finding the paper does not develop.

### 3.8 Missing Claude (LOW)

CLAUDE.md indicates the original lineup was 7 models including Claude Sonnet 4.6 via AWS Bedrock. The paper has 6, no Claude. Was Claude run and dropped, or never run? The paper does not say. For a frontier-model evaluation in March 2026, omitting Claude without explanation is conspicuous.

### 3.9 "Identical content" is slightly looser than claimed (LOW)

Format B (chart image) is described as "bar, line, or scatter, selected by data properties." This means different sub-tables get different chart types. The "identical content" claim strictly holds at the data level, but the *visual format* of Format B varies sub-table by sub-table. That is fine, but the paper does not analyze whether some chart types are easier than others. Bar chart accuracy vs. line chart accuracy vs. scatter accuracy would be a useful finer-grained analysis.

### 3.10 No prompt-sensitivity analysis (FLAGGED IN PAPER, BUT GAP REMAINS)

The paper acknowledges this in Limitations. For a paper whose results hinge on format effects, prompt effects are a co-equal concern: a slightly different prompt template could produce a different ranking. Without a sensitivity analysis on at least one model, the "Chart Text underperforms" finding could be partly a prompt artifact.

---

## Section 4 — Citation integrity preliminary scan (FOUND ERRORS)

I sampled three high-risk 2026 entries and verified them against the actual papers. **All three have errors.**

### 4.1 `graphomni2026` — AUTHOR WRONG

| Field | Bib value | Actual value (verified via ICLR 2026 + arXiv 2504.12764) |
|---|---|---|
| Title | "GraphOmni: A Comprehensive Benchmark for Graph Understanding" | "GraphOmni: A Comprehensive and Extendable Benchmark Framework for Large Language Models on Graph-theoretic Tasks" |
| Author (lead) | "Li, Hao and others" | **Hao Xu** (and Xiangru Jian, Xinjian Zhao, Wei Pang, Chao Zhang, Suyuchen Wang, Qixin Zhang, Zhengyuan Dong, Joao Monteiro, Bang Liu, Qiuzhuang Sun, Tianshu Yu) |
| Venue | ICLR 2026 | ICLR 2026 ✓ |

The lead author is Hao **Xu**, not Hao **Li**. The title is shortened. This is a hard hallucination on the author name.

### 4.2 `zhang2026samecontent` — AUTHOR WRONG **AND** TITLE WRONG

| Field | Bib value | Actual value (verified via ICLR 2026 + arXiv 2509.22983) |
|---|---|---|
| Title | "Same Content, Different Representations: Evaluating LLM Sensitivity to Table Formats" | "Same Content, Different Representations: A Controlled Study for Table QA" |
| Author (lead) | "Zhang, Yilun and others" | **Yue Zhang** (and Seiji Maekawa, Nikita Bhutani) |
| Venue | ICLR 2026 | ICLR 2026 ✓ |

Wrong subtitle (the bib hallucinates "Evaluating LLM Sensitivity to Table Formats" when the actual paper says "A Controlled Study for Table QA"). Wrong author first name (Yilun vs. Yue). The actual paper has 3 authors total, not "and others."

This is the closest related work in the entire bib, cited multiple times in the paper as the centerpiece of the related-work positioning. A reviewer who follows the citation will notice the title mismatch immediately.

### 4.3 `epoch2026` — TITLE PARTIALLY HALLUCINATED

| Field | Bib value | Actual value (verified via arXiv 2512.00193) |
|---|---|---|
| Title | "A Rosetta Stone for AI Benchmarks: Cross-Benchmark Correlation Analysis" | "A Rosetta Stone for AI Benchmarks" |
| Author | "Epoch AI" | The paper is published by Epoch AI but the actual author block on arXiv lists individual researchers (collaboration with Google DeepMind AGI Safety & Alignment) |

The "Cross-Benchmark Correlation Analysis" subtitle is hallucinated. The Epoch paper is about *benchmark stitching* (translating heterogeneous benchmark scores onto a single capability scale via item-response-theory-style modeling), **not** cross-benchmark correlation. The paper's Discussion (§5) misuses this citation: "aligning with the cross-benchmark correlations reported by Epoch AI" — the Epoch paper does not report cross-benchmark correlations in the way the paper's claim implies.

### 4.4 What this implies

I sampled 3 of 13 high-risk entries. **3 of 3 had errors.** Extrapolating, the bib likely has multiple author/title/venue errors and at least one outright misuse-of-citation case. This is exactly the failure mode that ACL's zero-tolerance policy targets and that EMNLP's expanded paper-integrity policy threatens with multi-year ineligibility.

The full bib needs every entry checked. Specifically:

| Bib key | Likely action |
|---|---|
| `torr2026` | Verify arXiv 2502.19412 — title/author/year |
| `wikimixqa2025` | Verify ACL Findings 2025 + author list |
| `datacross2026` | Verify arXiv 2601.21403 (suspicious arXiv ID format) |
| `chartqapro2025` | Verify ACL 2025 + Ibrahim et al. |
| **`graphomni2026`** | **FIX: change author to Hao Xu et al., expand title** |
| `gracore2025` | Verify COLING + Ma et al. |
| `tsaqa2026` | Verify exists, get arXiv ID, verify authors (currently "Wang, Xin and others" — too vague) |
| `mmtsbench2026` | Verify exists, get arXiv ID |
| `hearts2026` | Suspicious — "Heart Rate Time Series Analysis with LLMs" sounds medical, not relevant; check if this paper actually exists |
| **`zhang2026samecontent`** | **FIX: change author to Yue Zhang, Seiji Maekawa, Nikita Bhutani; correct title to "A Controlled Study for Table QA"** |
| `liu2026formatprior` | Verify exists |
| `ho2025formatmatters` | Verify exists |
| **`epoch2026`** | **FIX: remove subtitle, fix author block, and reconsider whether the paper actually supports the claim it's cited for** |
| `mmtu2025` | Verify NeurIPS 2025 |
| `charxiv2026` | Verify exists |
| `chartmuseum2025` | Verify NeurIPS 2025 |
| `divgi1979calculation` | Real, classic — likely fine |
| `pasupat2015compositional` | Real |
| `chen2020tabfact` | Real |
| `masry2022chartqa` | Real |
| `ilic2023gfactor` | Verify arXiv |

Recommendation: run `ai-research-integrity-check` on the full bib before any further venue submission.

---

## Section 5 — Comparison with each reviewer

### 5.1 Reviewer HZuL (rating 8, "clear accept")

**Verdict on the review:** Generous. The review summarizes the paper accurately but does not engage with methodology. Saying "clear accept" given the tetrachoric base-rate issues, the citation errors, and the phi-vs-tetrachoric framing choice is, in my view, undermerited rigor. HZuL's review reads as the kind of review a busy reviewer writes when the paper is well-written and the topic is interesting — they did not run the numbers.

**Things HZuL got right:**
- The benchmark structure (1724 questions × 5 formats) is a real contribution.
- "Questions involving aggregation or conditional aggregation show the largest format-dependence variance" — this is correct and consistent with my §2.7 finding.

**Things HZuL missed:**
- All of §3.1-3.10 above.
- The graph format is constructed, not natural.
- Citation integrity has not been verified.

I would have given this paper around a 5-6 with the methodological concerns. Rating 8 implies a review pass that did not pressure-test the analysis.

### 5.2 Reviewer 5243 (rating 6, "Clear Setup, Limited Novelty")

**Verdict on the review:** Mostly correct, mildly underweights the contribution. 5243 caught:

- The graph format being "constructed from tabular data" rather than natural. **I agree, this is a real concern (§3.4).**
- Real-world transfer is unclear. **I agree, this is a real limitation.**
- "Some broader conclusions are based on limited coverage" — chart-image (3 models) and reasoning ablation (2 models). **I agree (§2.8, §3.8).**
- "Writing reads like an experimental report" and "contribution could benefit from more careful positioning relative to prior work." **I agree (§1.3.4, §3.3).**

**Things 5243 missed:**
- Tetrachoric base-rate issue (§3.1).
- Phi-vs-tetrachoric framing (§3.2).
- The Zhang 2026 specific framing concern (§3.3).
- Citation errors.

**Things 5243 may have over-discounted:**
- "Limited novelty." The five-format same-content design is real novelty over Zhang 2026 (table-only). The novelty is methodological scope, not theoretical.

5243's rating of 6 ("marginally above acceptance threshold") is in line with my read. If the methodological issues were addressed, this would deserve closer to a 7.

### 5.3 Reviewer NRrg (rating 5, "accept with changes")

**Verdict on the review:** Most rigorous reviewer. Caught:

- Table 2 needs more granular data with CIs and significance tests. **I agree, with stronger force — see §2.3.**
- Edge-description confound in graph format is acknowledged but not mitigated. **I agree, this is the §3.4 issue and needs an ablation.**
- Synthetic sub-tables vs. real-world data. **Agreed limitation; the v2 paper should add real-world data.**
- N=6 model concern. **Valid, though I'd reframe — the issue isn't just N=6, it's that the N=6 spans both ceiling and mid-range models, and ceiling model correlations are unreliable.**

NRrg also asked three technical questions that the paper does not address:
1. Real-world dataset transfer — legitimate v2 question.
2. Prompt variations for Chart Text — legitimate v2 question.
3. Semantic graph construction — legitimate v2 question.

**Things NRrg missed:**
- The phi-vs-tetrachoric framing choice (§3.2). NRrg asked for more granular stats but didn't notice that the choice of tetrachoric over phi is itself doing heavy lifting.
- The DeepSeek-vs-Qwen-vs-Gemini split *within* the ceiling group (§2.1). NRrg accepted "ceiling group r=0.90" as one number rather than three.
- Citation errors.
- The chart-text size effect (§2.7).

**Things NRrg may have over-weighted:**
- "Originality is not entirely novel" — somewhat unfair given the five-format scope.

NRrg's rating of 5 was the harshest. With the methodological issues unaddressed, I'd give a similar rating.

### 5.4 What the reviewer mix tells us

- **HZuL (8):** "I read the paper, it's coherent, the topic is interesting, accept."
- **5243 (6):** "Clear setup, but I'm uneasy about novelty and framing."
- **NRrg (5):** "Methodologically I'm skeptical, the synthetic data and small N concern me."

Mean rating 6.33, decision Accept. This was a reasonable ACL workshop decision: accept-with-revisions for a paper that has clear value but real issues. For EMNLP main, the same paper would likely get rejected, because EMNLP applies tighter methodological standards and the citation-integrity/zero-tolerance policy.

---

## Section 6 — Synthesis: ranked issue list

Severity is "how much this hurts paper credibility" not "how hard to fix."

### Tier 1 — must fix before any venue submission

1. **Citation errors** (§4). Three errors found in a 3-entry sample. Run integrity check on full bib. Fix every entry to actual title/author/venue/year. ETA: a few hours.

2. **Tetrachoric base-rate framing** (§3.1, §3.2). Either:
   - Make mid-range r=0.84 the headline and demote ceiling r=0.90 to a separate row with caveats; OR
   - Report phi as the primary metric, with tetrachoric as supplementary.
   - Acknowledge the bivariate-normal assumption explicitly.
   ETA: writing change + re-table.

3. **Add bootstrap CIs to all reported correlation point estimates** (§2.3). The data is already there in the JSON. ETA: a few hours of figure/table re-rendering.

4. **Statistical significance tests for accuracy differences** (NRrg's ask). Pairwise McNemar on within-model format pairs. Already computable from raw_results.jsonl. ETA: a few hours.

### Tier 2 — strongly recommended

5. **Run the graph-without-edges ablation** (§3.4). Re-render Format C without edges, re-evaluate at least Kimi K2.5 (largest-effect model). If transfer holds, the edge confound is small; if not, the framing must change. ETA: a re-render + re-run on one model.

6. **Soften the "graph reasoning" framing** (§1.3.1). Use "graph-like serialization" or "node-attribute representation" throughout, with one explicit acknowledgment that this is not natural-graph data. Already partly done in §3.2; extend to abstract / intro / conclusion.

7. **Soften the "first study" claim** (§3.3). Frame as "extending Zhang et al.'s controlled-content methodology from table-only to five formats."

8. **Quantify the 1-format-fail breakdown** (§3.5). Replace "manual inspection reveals" with a count table.

9. **Break out chart-text size effect** (§2.7). Add a per-format-tier accuracy table to the appendix or main text.

10. **Tighten Discussion writing** (5243's ask). Replace "Findings 1/2/3" structure in §4.1 with prose. Replace mechanical paragraph headers in §4.3 ("Per-model variation," "Interaction between question type and format") with topic sentences that make the contribution argument.

### Tier 3 — v2 paper additions (not required for current submission but unlock a higher tier of venue)

11. **Add ≥1 real-world data source.** WikiTQ, CharXiv-R, or ChartQA-Pro. Run the same five formats and compare transfer correlations to synthetic. If the cross-format finding holds, the paper becomes much stronger.

12. **Expand the model panel** (NRrg's N=6 concern). Add Claude Sonnet 4.6 (already in the original plan, abandoned). Add 2-3 more frontier models. Aim for N=10+ with at least 5 vision-capable.

13. **Run the full reasoning ablation** on all 6 (or 10+) models, not just 2.

14. **Add the human baseline study** that the paper text explicitly promises ("planned for the camera-ready version" — never delivered). Within-subjects, Latin-square, ~50 questions, 20 participants. The paper plan is already in `experiments/experiment-plan.md`.

15. **Prompt sensitivity analysis.** Re-run at least 1 model with 3 different prompt templates. Report whether the format ranking is stable.

16. **Add a chart-image error-mode analysis** (§3.7). The Q1/Q3/Q4 breakdown by chart_image is publishable on its own.

17. **Address the missing Claude question** (§3.8). Either run Claude Sonnet 4.6 or document why it was excluded.

18. **Add a semantic-edge graph variant** (NRrg's third question). If the data has natural relationships (geographic proximity, taxonomic class), use those instead of cosine-similarity. Compare to current graph.

---

## Section 7 — v2 paper plan (high level)

Title: probably keeps "Do Structured Data Comprehension Skills Transfer Across Representation Types?" — strong working title.

Target venue: **EMNLP 2026** if Tier 1 + Tier 2 + items 11, 13, 15 from Tier 3 can be done. **NAACL 2027 / ACL 2027** if items 12 and 14 are also wanted (more time for human study + 10-model panel).

Story arc revision:
- v1 (current): "Are skills siloed or do they transfer?" → "Mostly transfer for text formats; chart image is siloed; reasoning is model-dependent."
- v2: "How does the 5-format/N-model controlled benchmark generalize?" → "(1) Mid-range models show strong text-format transfer (phi r=0.4, tetrachoric r=0.84) on synthetic data, with results corroborated by real-world WikiTQ/CharXiv-R splits; (2) Chart image gap is consistent across N=10+ vision models; (3) Reasoning ablation across all models reveals a model-class-level pattern; (4) Human baseline establishes upper bound; (5) Prompt sensitivity confirms the ranking is robust."

Key narrative addition for v2: **the paper becomes a study of "what stays constant across format and model" rather than "models can all do tables."** That re-framing leverages the methodological strength while making the contribution defensible at top venues.

---

## Section 8 — One-line summary

The paper has a real and methodologically clean contribution (5-format same-content controlled benchmark, programmatic ground truth) but the headline tetrachoric-r=0.85 finding leans on at-ceiling models where the metric is unreliable, the graph framing overreaches what the experiment supports, and the bib contains hard citation errors that would trigger desk rejection at any top venue. SURGeLLM's accept is reasonable; the same paper is not yet ready for EMNLP. The v2 plan above turns it into a paper that is.
