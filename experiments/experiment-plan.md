# Experiment Plan: StructReason-Transfer (v3 — Second Review Revision)

**Title:** Do Structured Data Comprehension Skills Transfer Across Representation Types? A Systematic Study with Frontier LLMs
**Venue:** SURGeLLM 2026 (ACL Workshop, 4-8 pages) | San Diego | Jul 2-3, 2026
**Submission Deadline:** Mar 22, 2026 (AoE)

> **Changelog v3:** Incorporates fixes from second-round adversarial review.
> - Made tetrachoric correlation the PRIMARY metric; phi is secondary (Fix W13)
> - Human study switched to within-subjects design (Fix W14)
> - Added token count reporting per format to control length confound (Fix W11)
> - Added 100-question judge overlap for inter-judge kappa (Fix W15)
> - Added prompt sensitivity ablation with 2 variants (Fix W16)
> - Added tie-breaking protocol for Q6-Q7 multi-hop questions (Fix W17)
> - Downgraded natural-graph comparison from "ablation" to "sanity check" (Fix W12)
>
> **Changelog v2:** First review fixes.
> - Reframed "reasoning" → "comprehension" (Fix W10)
> - Added Format B': text-described chart to control modality confound (Fix W8)
> - Made time series format more distinct — unlabeled arrays (Fix W2)
> - Improved graph format justification + added real-graph subset (Fix W1)
> - Added 2 harder question types: multi-hop and conditional (Fix W6)
> - Switched from Spearman on binary data to phi/tetrachoric (Fix W4)
> - PCA moved to appendix as exploratory only (Fix W5)
> - Added small human baseline study (Fix W7)

---

## Hypothesis

LLM structured data comprehension skills are siloed by representation type — a model strong at table comprehension does not proportionally excel at chart or graph comprehension over the same underlying data, suggesting these require fundamentally different capabilities.

**Falsifiable prediction:** If skills are transferable, per-model accuracy on matched tasks across structure types will show tetrachoric correlation r > 0.7. If siloed, r < 0.4.

---

## Step 1 — Dataset Selection

### Selection Criteria
- Must support all 5 formats naturally (table, chart image, chart text-description, graph, time series)
- Prefer low LLM memorization risk
- Diverse domains (no more than 2 datasets per domain)
- Manageable size (sub-tables fit in prompt)
- Permissive license (CC-BY or public domain)

### Selected Datasets (10 datasets, 7 domains)

| # | Dataset | Domain | License | Memorization Risk | Source |
|---|---------|--------|---------|-------------------|--------|
| 1 | **QoG EU Regional** | Governance/Econ | Free academic | Very Low | https://www.gu.se/en/quality-government/qog-data |
| 2 | **HK Traffic Digest** | Transportation | HK Open Data | Very Low | https://data.gov.hk/en-data/dataset/hk-td-tis_17 |
| 3 | **OPSD Electricity** | Energy | Per-source | Low | https://data.open-power-system-data.org/time_series/ |
| 4 | **Iizumi Crop Yields** | Agriculture | CC-BY-4.0 | Low | https://doi.pangaea.de/10.1594/PANGAEA.909132 |
| 5 | **EPA AQS Daily** | Air Quality | Public Domain | Low-Med | https://aqs.epa.gov/aqsweb/airdata/download_files.html |
| 6 | **NTD Monthly Transit** | Transportation | Public Domain | Low | https://data.transportation.gov/Public-Transit/Monthly-Modal-Time-Series/5ti2-5uiv |
| 7 | **Ember Monthly Elec** | Energy | CC-BY-4.0 | Low-Med | https://ember-energy.org/data/monthly-electricity-data/ |
| 8 | **FAOSTAT Crops** | Agriculture | CC-BY-4.0 | Medium | https://www.fao.org/faostat/ |
| 9 | **SEC XBRL Financials** | Finance | Public Domain | Medium | https://www.sec.gov/data-research/sec-markets-data/financial-statement-data-sets |
| 10 | **OpenAQ** | Air Quality | Varies (gov sources) | Low-Med | https://openaq.org/ |

### Per-Dataset Extraction Plan

From each dataset, extract **25 sub-tables** (slices by entity/time window), yielding **250 total underlying data instances**.

Each sub-table:
- 5-20 rows (entity/time observations)
- 3-8 columns (metrics)
- Contains temporal dimension + entity dimension + 1-3 numeric metrics

**Complexity tiers** (for Ablation 2):
- Small: 5 rows × 3 cols (~80 sub-tables)
- Medium: 10 rows × 5 cols (~100 sub-tables)
- Large: 20 rows × 8 cols (~70 sub-tables)

---

## Step 2 — Format Specifications

Each of the 250 sub-tables is rendered in **5 formats** (4 primary + 1 modality control):

### Format A: Table (Text)
- **Serialization:** Markdown table
- **Example:**
```
| Month | Coal (GWh) | Solar (GWh) | Wind (GWh) |
|-------|-----------|------------|------------|
| Jan   | 2,450     | 890        | 3,200      |
| Feb   | 2,100     | 1,100      | 2,800      |
```
- **Input type:** Text prompt
- **All 7 models tested:** Yes

### Format B: Chart Image (Visual)
- **Generation:** matplotlib/plotly, programmatic
- **Chart type selection rules:**
  - Temporal data → line chart
  - Categorical comparison → bar chart
  - Two-variable relationship → scatter plot
  - Composition → stacked bar chart
- **Resolution:** 800×600 PNG, standard fonts, clear axis labels
- **Input type:** Image (base64)
- **Models tested:** Only VLM-capable models (Gemini 3.1 Pro, Claude Sonnet 4.6, Kimi K2.5, GLM-5; check Qwen 3.5 VL, DeepSeek V3.2, MiniMax M2.5)

### Format B': Chart Text-Description (Modality Control) ← NEW
- **Purpose:** Controls for the text-vs-image modality confound. If a model fails on Format B (chart image) but succeeds on Format B' (same chart described in text), the failure is due to visual processing, not chart-specific reasoning.
- **Generation:** Programmatic text description of the chart, **length-controlled**
- **Length control protocol:** B' descriptions are capped to match Format A (table) token count ±20%. If raw description exceeds this, truncate to key data points only (no redundant prose). This prevents a length confound where B' outperforms simply because it provides more tokens.
- **Example (length-controlled):**
```
Line chart: "Germany Monthly Electricity Generation 2023" (GWh).
Coal: Jan=2450, Apr=1800, Jul=1100, Oct=2000, Dec=2500.
Solar: Jan=890, Apr=1600, Jul=2800, Oct=1200, Dec=750.
Wind: Jan=3200, Apr=2400, Jul=1900, Oct=2600, Dec=3100.
```
- **Input type:** Text prompt
- **All 7 models tested:** Yes
- **Key comparison:** Accuracy(B) vs Accuracy(B') isolates visual processing from chart reasoning

### Token Count Reporting ← NEW
For every format, report median token count (via tiktoken cl100k_base) in the paper:

| Format | Expected Median Tokens | Notes |
|--------|----------------------|-------|
| A: Table (MD) | ~80-150 | Scales with rows × cols |
| B: Chart (Image) | ~250-500 (image tokens) | Varies by model's vision encoder |
| B': Chart Text-Desc | ~80-150 (length-matched to A) | Capped to ±20% of Format A length |
| C: Graph (Text) | ~120-200 | Depends on # nodes/edges |
| D: Time Series (Array) | ~40-80 | Compact numerical array |

Report token counts per format in Methodology section. If any format pair shows >2× token difference, flag as potential confound and run a length-controlled sub-analysis.

### Format C: Graph (Text)
- **Representation:** Structured edge list with explicit node attributes
- **Construction rules:**
  - **Entity-attribute graph** (primary): Entities are nodes. Edges connect entities that share a categorical attribute (e.g., same region, same energy source) or have a quantitative relationship (e.g., co-occurrence, similarity).
  - **NOT just temporal chaining** — we avoid the "Jan→Feb→Mar" sequential graph that is just a reformatted time series. Instead, the graph encodes cross-entity relationships.
- **Example (Ember Electricity — country relationships):**
```
Graph: European electricity generation similarity network (2023)

Nodes:
  Germany: {coal: 2450, solar: 890, wind: 3200, total: 6540}
  France: {coal: 200, solar: 1100, wind: 2100, nuclear: 8500, total: 11900}
  Poland: {coal: 4200, solar: 400, wind: 1800, total: 6400}
  Spain: {coal: 300, solar: 3200, wind: 2800, total: 6300}

Edges (generation mix similarity > 0.7):
  Germany -- Poland (similarity: 0.82, reason: both coal-heavy)
  France -- Spain (similarity: 0.75, reason: both low-coal, high-renewable)
```
- **Input type:** Text prompt
- **All 7 models tested:** Yes
- **Justification:** This is a genuine graph task — the model must reason about node attributes AND edge relationships (similarity, connectivity), not just follow a sequence.

**Additional: Real-graph subset (30 instances)**
For 30 of the 250 instances, we use data that is NATURALLY a graph:
- **UN Comtrade** bilateral trade flows (country→country directed graph)
- **OPSD** European grid interconnections (zone→zone edges)
- **Transit data** station connectivity (station→station edges)
These serve as validation that our constructed graphs produce similar patterns to natural graphs.

### Format D: Time Series (Unlabeled Numerical Array) ← REVISED
- **Representation:** Raw numerical sequence WITHOUT entity labels, with only a header describing what the numbers represent. Forces positional reasoning.
- **Example:**
```
The following 12 values represent monthly coal generation (GWh) for Germany in 2023, from January to December:
[2450, 2100, 2200, 1800, 1500, 1200, 1100, 1300, 1600, 2000, 2300, 2500]
```
- **Input type:** Text prompt
- **All 7 models tested:** Yes
- **Key difference from Format A:** No row/column labels per value. The model must count positions to answer "What was the value in March?" (position 3 = 2200). This makes time series genuinely harder than tables for lookup tasks.

---

## Step 3 — Question Taxonomy

**7 question types** (5 basic + 2 hard), all programmatically generated with deterministic answers.

### Basic Questions (Q1-Q5)

#### Q1: Lookup (Direct Retrieval)
- **Template:** "What is the {metric} for {entity} in {time_period}?"
- **Example:** "What is the coal generation for Germany in March?"
- **Answer type:** Single number
- **Scoring:** Exact match with ±2% numerical tolerance
- **Tests:** Can the model extract a specific value?

#### Q2: Comparison
- **Template:** "Which has a higher {metric} in {time_period}: {entity_A} or {entity_B}?"
- **Example:** "Which has higher generation in June: solar or wind?"
- **Answer type:** Entity name
- **Scoring:** Exact match (case-insensitive)
- **Tests:** Can the model compare two values?

#### Q3: Aggregation
- **Template:** "What is the {total/average} {metric} across all {entities/time_periods}?"
- **Example:** "What is the average coal generation across all months?"
- **Answer type:** Single number
- **Scoring:** ±5% numerical tolerance
- **Tests:** Can the model perform arithmetic over multiple elements?

#### Q4: Trend
- **Template:** "Did {metric} for {entity} increase or decrease between {T1} and {T2}?"
- **Example:** "Did solar generation increase or decrease between January and June?"
- **Answer type:** "increase" or "decrease"
- **Scoring:** Exact match
- **Tests:** Can the model identify directional change?

#### Q5: Extremum
- **Template:** "In which {time_period/entity} is {metric} the highest/lowest?"
- **Example:** "In which month is wind generation the highest?"
- **Answer type:** Entity/time label
- **Scoring:** Exact match
- **Tests:** Can the model find max/min?

### Hard Questions (Q6-Q7) ← NEW

#### Q6: Multi-Hop
- **Template:** "What is the {metric_B} for the {entity} that has the highest {metric_A}?"
- **Example:** "What is the wind generation for the month that has the highest coal generation?"
- **Answer type:** Single number
- **Scoring:** ±2% numerical tolerance
- **Tests:** Requires two steps — find the extremum, then look up a different value for that entity. This is genuinely harder and less likely to hit ceiling.
- **Tie-breaking protocol:** ← NEW
  - During question generation, compute the gap between the top-2 values for the extremum metric
  - **Exclude** any instance where the gap is <5% of the top value (ambiguous extremum)
  - **Exclude** any instance where multiple entities share the exact max/min
  - This ensures every Q6 question has exactly one unambiguous correct answer
  - Log excluded instances and report exclusion rate in appendix

#### Q7: Conditional Aggregation
- **Template:** "What is the average {metric_A} for {entities/time_periods} where {metric_B} is above {threshold}?"
- **Example:** "What is the average solar generation for months where coal generation exceeds 2,000 GWh?"
- **Answer type:** Single number
- **Scoring:** ±5% numerical tolerance
- **Tests:** Requires filtering + aggregation — two operations chained. Substantially harder than Q3.
- **Threshold selection protocol:** ← NEW
  - Threshold chosen programmatically to ensure 30-70% of entities/time_periods pass the filter
  - Avoids degenerate cases where filter selects all (=Q3) or none (unanswerable)
  - If no valid threshold exists for a sub-table, skip Q7 for that instance

### Question Generation Pipeline
1. For each of 250 sub-tables, programmatically generate 1 question per type = **7 questions per sub-table**
2. Total: **1,750 base questions**
3. Each question asked across 5 formats (B' only for VLM-capable models' chart comparison) = **~6,500-7,500 question-format instances**
4. Ground truth computed directly from source data (pandas/numpy)
5. **Zero LLM involvement in question generation**

### Prompt Template (Identical Across Formats)
```
You are given data in the following format. Answer the question precisely.

{DATA IN FORMAT A/B/B'/C/D}

Question: {QUESTION}

Answer with ONLY the answer value, no explanation.
```

---

## Step 4 — Metrics

### Primary Metric: Cross-Structure Comprehension Correlation ← REVISED v3

For each model M and each pair of structure types (S_i, S_j):

1. Create binary accuracy vectors: for each of ~1,750 questions, score 1 (correct) or 0 (incorrect) in format S_i and S_j
2. Compute **tetrachoric correlation** (PRIMARY) — estimates the latent continuous correlation underlying the binary observations. Robust to skewed marginals (e.g., 95% vs 70% accuracy). Computed via `ordinalcorr` v0.6.1 (NOT scipy — scipy has no tetrachoric function). Validate on 10 instances against R's `polycor` package.
3. Compute **phi coefficient** (SECONDARY) — raw binary correlation, reported for transparency. Note: phi is bounded by marginal distributions, so direct comparison of phi values across format pairs with different base rates is invalid. Tetrachoric corrects for this.
4. Report **Kendall's tau-b** as a non-parametric robustness check
5. This yields a **5×5 correlation matrix per model** (10 unique format pairs)

**Interpretation (tetrachoric r):**
- r_tet > 0.7 → strong skill transfer (model's comprehension is consistent across formats)
- 0.4 < r_tet < 0.7 → moderate transfer
- r_tet < 0.4 → siloed skills (model fails on different questions per format)

**Why tetrachoric over phi (Fix W13):**
Phi is constrained by marginal distributions. If table accuracy = 95% and graph accuracy = 60%, the maximum possible phi is ~0.45 regardless of true association. Tetrachoric estimates what the correlation WOULD be if both variables were continuous and normally distributed — it is the standard metric in psychometrics for binary test items (cf. IRT literature). This ensures we can fairly compare correlation strength across format pairs even when absolute accuracy levels differ.

**Key comparison:** r_tet(B, B') = chart-image vs chart-text-description → isolates visual processing from chart comprehension

### Secondary Metrics

| Metric | What It Measures |
|--------|-----------------|
| **Per-format accuracy** | Raw accuracy per model per structure type (7×5 matrix) |
| **Per-question-type accuracy** | Accuracy breakdown by Q1-Q7 per format (reveals which skills transfer) |
| **Kendall's W (concordance)** | Do all models agree on which format is hardest? High W = consistent difficulty ranking |
| **Cohen's kappa per format pair** | Agreement between format-pair correctness beyond chance |
| **Hard vs Easy question transfer** | Do correlations differ for Q1-Q5 (basic) vs Q6-Q7 (hard)? |
| **IRT analysis (py-irt)** | EXPLORATORY ONLY — in appendix. Fit 2PL IRT model to estimate item difficulty and model ability per format. Use `py-irt` v0.6.6 (NOT semopy — dormant). Acknowledge N=7 models is insufficient for confirmatory analysis |

### Statistical Protocol
- **Instance-level analysis** (N=1,750 per model): sufficient power for phi coefficient
- **Model-level analysis** (N=7): descriptive only, report effect sizes, NO p-value claims
- **Confidence intervals:** 95% bootstrap CIs for all correlations (10,000 resamples)
- **Multiple comparison correction:** Bonferroni for 10 pairwise format comparisons
- **Effect size reporting:** Report phi, tetrachoric r, and raw accuracy differences. Avoid over-relying on p-values.
- **Visualization:**
  - Heatmaps (5×5 correlation matrices per model + averaged)
  - Radar plots (per-model accuracy profiles across 5 formats)
  - Scatter plots (format A accuracy vs format B accuracy per question)
  - Bar charts (accuracy by question type × format)

---

## Step 5 — Ablation Plan

### Ablation 1: Question Difficulty Effect ← STRENGTHENED
- **Split:** Basic questions (Q1-Q5) vs Hard questions (Q6-Q7)
- **Tests:** Does skill transfer hold for harder compositional questions, or only for simple extraction?
- **Expected:** Transfer weakens for hard questions (format-specific weaknesses emerge under load)
- **This is the most important ablation** — directly addresses the ceiling effect concern

### Ablation 2: Data Complexity
- **Vary:** Sub-table size (small: 5×3, medium: 10×5, large: 20×8)
- **Tests:** Does transfer increase or decrease with data complexity?
- **Expected:** Transfer decreases with complexity

### Ablation 3: Chart Type Effect
- **Vary:** Chart visualization (line vs. bar vs. scatter for same data)
- **Tests:** Does the specific chart type matter?
- **Expected:** Line charts easiest for temporal questions, bar charts easiest for comparison

### Ablation 4: Modality Isolation (B vs B')
- **Compare:** Chart image (B) vs Chart text-description (B') accuracy
- **Tests:** How much of the chart comprehension gap is due to visual processing vs. chart-specific reasoning?
- **Expected:** B' accuracy ≈ Format A accuracy (chart reasoning is fine; image parsing is the bottleneck)
- **This directly resolves Reviewer 3's modality confound concern**

### Ablation 5: Prompt Sensitivity ← NEW (Fix W16)
- **Vary:** 3 prompt template variants on a 50-question subset × 3 models (Gemini, Claude, DeepSeek)
  - **Prompt V1 (default):** "Answer with ONLY the answer value, no explanation."
  - **Prompt V2 (CoT-style):** "Think step by step, then provide ONLY the final answer on the last line."
  - **Prompt V3 (role-based):** "You are a data analyst. Extract the answer from the data below. Answer with ONLY the value."
- **Tests:** Are cross-format correlation patterns robust to prompt variation?
- **Expected:** Absolute accuracy may shift, but relative format difficulty ranking should be stable
- **Cost:** ~2,250 additional calls (50 × 5 formats × 3 prompts × 3 models), ~$5 on credits

### Sanity Check: Natural vs Constructed Graphs ← DOWNGRADED from Ablation (Fix W12)
- **Compare:** 30 natural-graph instances vs 220 constructed-graph instances
- **Purpose:** Validate that constructed graphs produce similar patterns to natural graphs
- **NOT a formal ablation** — 30 instances is too few for statistical claims
- **Report as:** "We verified on a small natural-graph subset (N=30) that patterns were directionally consistent" — no strong claims

---

## Step 6 — Human Baseline Study ← REVISED v3 (Within-Subjects)

### Design
- **Participants:** 20 volunteers (lab members, colleagues)
- **Subset:** 50 randomly sampled questions (from the 1,750), 10 per format
- **Within-subjects design:** ← REVISED from between-subjects
  - Each participant answers ALL 50 questions
  - Each question is assigned a FIXED format (same for all participants)
  - Questions are distributed: 10 questions × 5 formats = 50 questions
  - This gives **20 responses per question** (sufficient for per-question accuracy)
  - And **20 participants × 10 questions = 200 responses per format** (sufficient for per-format accuracy)
- **Latin-square counterbalancing:** To check format sensitivity, create 5 variants of the form. Each variant assigns each question to a DIFFERENT format. Run 4 participants per variant (4 × 5 = 20 total). This gives us within-subject comparisons without every person seeing 250 questions.
- **Total annotations:** 20 people × 50 questions = 1,000 human responses
- **Compensation:** Volunteer basis (or small gift cards)
- **Platform:** Google Forms (5 variant forms, auto-randomized assignment)
- **Time:** ~25-35 minutes per participant

### Purpose
- Establishes whether format effects are LLM-specific or inherent to the representation
- Within-subjects + Latin square lets us compute human cross-format correlations from the counterbalanced variants
- If humans show similar cross-format accuracy patterns → format difficulty is intrinsic
- If humans are equally accurate across formats but LLMs aren't → LLM-specific comprehension gap

### Analysis
- Compute human accuracy per format (N=200 responses per format)
- From Latin-square variants: compute human cross-format agreement per question
- Compare human format-difficulty ranking to LLM format-difficulty ranking (Kendall's W)
- Report in 3-4 sentences in Results + full breakdown in appendix

---

## Step 7 — Compute and Budget

### Models

| Model | Platform | API Cost | Vision? |
|-------|----------|----------|---------|
| Gemini 3.1 Pro | Google AI | $300 credits | Yes |
| Claude Sonnet 4.6 | AWS Bedrock | $100 credits | Yes |
| Kimi K2.5 | OpenRouter | $60 credits (shared) | Yes |
| GLM-5 | OpenRouter | (shared) | Yes |
| Qwen 3.5 397B | OpenRouter | (shared) | Check |
| DeepSeek V3.2 | OpenRouter | (shared) | Check |
| MiniMax M2.5 | OpenRouter | (shared) | Check |

### API Call Estimate (Revised for 5 formats + 7 question types)

| Component | Calls | Tokens (in/out) | Notes |
|-----------|-------|-----------------|-------|
| Main experiment (7 models × ~6,500 instances) | ~45,500 | 1.5K / 300 per call | VLMs get chart image; all get chart text-description |
| Ablations (top 3 × subset on 3 models) | ~8,000 | 1.5K / 300 per call | Gemini, Claude, DeepSeek only |
| Judge calls (5% edge cases for Q6-Q7) | ~1,500 | 2K / 200 per call | Cross-judging: Gemini↔Claude |
| Judge overlap (inter-judge agreement) | ~200 | 2K / 200 per call | 100 questions judged by BOTH Gemini and Claude → report Cohen's kappa (Fix W15) |
| Prompt sensitivity ablation | ~2,250 | 1.5K / 300 per call | 50 Qs × 5 formats × 3 prompts × 3 models (Fix W16) |
| Pilot runs (debugging) | ~2,000 | 1.5K / 300 per call | Before full run |
| **Total** | **~61,000** | | |

### Budget Allocation (Revised v3)

| Platform | Allocated To | Est. Cost | Credits Available |
|----------|-------------|-----------|-------------------|
| Google ($300) | Gemini eval (~6.5K) + judge for Claude (~750) + judge overlap (~100) + pilot (~1K) + prompt ablation (~750) | ~$67 | $300 → **$233 remaining** |
| AWS ($100) | Claude eval (~6.5K) + judge for others (~750) + judge overlap (~100) + prompt ablation (~750) | ~$65 | $100 → **$35 remaining** |
| OpenRouter ($60) | Kimi + GLM-5 + Qwen + DeepSeek + MiniMax (~32.5K) + DeepSeek prompt ablation (~750) | ~$38 | $60 → **$22 remaining** |
| **Cash** | **None** | **$0** | |

### Compute (Non-API)

| Task | Hardware | Time | Cost |
|------|----------|------|------|
| Data preparation (250 sub-tables, 5 formats) | Local CPU | ~5 hours | $0 |
| Chart generation (250 matplotlib PNGs) | Local CPU | ~1 hour | $0 |
| Chart text-description generation (250 programmatic) | Local CPU | ~1 hour | $0 |
| Question generation (1,750 questions + ground truth) | Local CPU | ~45 min | $0 |
| Human baseline study setup (Google Forms) | Local | ~2 hours | $0 |
| Statistical analysis + visualization | Local CPU | ~3 hours | $0 |

---

## Step 8 — Venue-Aware Scoping (Workshop, 4-8 pages)

### What Fits in 8 Pages

| Section | Pages | Content |
|---------|-------|---------|
| Introduction | 1 | Motivation, hypothesis, key finding preview |
| Related Work | 0.75 | STRuCT-LLM, "Tables as Texts or Images", FCMR, Epoch AI correlations, Ilic g-factor |
| Methodology | 1.75 | 5 formats (with modality control justification), 7 question types, metrics, 7 models |
| Results | 2 | Correlation matrices, per-question-type breakdown, human comparison |
| Ablations | 1 | Ablation 1 (difficulty), Ablation 4 (modality isolation) — the two strongest |
| Discussion + Conclusion | 1 | Implications, limitations (N=7 models, graph construction), future work |
| **Total** | **~7.5 pages** + references/appendix |

### What Goes in Appendix
- Full dataset list with download links and extraction details
- All question templates with examples for all 7 types
- Per-model per-format accuracy tables (full 7×5×7 breakdown)
- PCA analysis (exploratory, with caveat about N=7)
- Additional ablation results (Ablations 2, 3, 5)
- All prompt templates
- Human study instructions and full results

### Key Figures

1. **Figure 1:** 5×5 phi-coefficient heatmap (averaged across models) — the main result
2. **Figure 2:** Per-model radar plots showing accuracy profiles across 5 formats
3. **Figure 3:** Accuracy by question type × format (grouped bar chart) — shows where transfer breaks down
4. **Figure 4:** Chart Image (B) vs Chart Text-Description (B') scatter — the modality isolation result
5. **Table 1:** Raw accuracy (7 models × 5 formats) with 95% CIs
6. **Table 2:** Phi coefficients by question type — basic (Q1-Q5) vs hard (Q6-Q7)
7. **Table 3:** Human vs LLM accuracy comparison (compact, 5 formats × 2 rows)

---

## Step 9 — Risk Assessment (Revised)

### Risk 1: Skills ARE Transferable (Null Result)
- **Likelihood:** MEDIUM
- **Impact:** HIGH (undermines the "siloed" hypothesis)
- **Mitigation:** Reframe as positive finding: "format does NOT matter — researchers can benchmark in any format." SURGeLLM welcomes negative results. Also: hard questions (Q6-Q7) may still show siloing even if basic questions don't.

### Risk 2: Chart Modality Confound → RESOLVED
- **Likelihood:** N/A (addressed by design)
- **Mitigation:** Format B' (chart text-description) directly controls for this. Report both B vs A (includes modality) and B' vs A (pure format effect).

### Risk 3: Ceiling Effect on Basic Questions
- **Likelihood:** MEDIUM
- **Impact:** MEDIUM (reduced, since Q6-Q7 are hard)
- **Mitigation:** (a) Q6 (multi-hop) and Q7 (conditional aggregation) provide harder tasks. (b) Pilot on 20 instances — if >90% accuracy on ALL question types, increase sub-table size to 20×8 minimum. (c) Unlabeled time series format (Format D) forces positional reasoning, reducing ceiling.

### Risk 4: API Rate Limits / Downtime
- **Likelihood:** MEDIUM
- **Impact:** LOW
- **Mitigation:** Stagger calls. Retry with backoff. Run cheapest models first.

### Risk 5: Non-VLM Models Can't Do Chart Images
- **Likelihood:** MEDIUM
- **Impact:** LOW (Format B' covers chart reasoning for text-only models)
- **Mitigation:** Text-only models skip Format B but still do Format B'. Analysis separates "chart reasoning" (B') from "chart vision" (B).

### Risk 6: Artificial Graph Format Criticism → MITIGATED
- **Likelihood:** MEDIUM
- **Impact:** MEDIUM
- **Mitigation:** (a) Graph construction uses cross-entity relationships (similarity, co-occurrence), NOT sequential temporal chains. (b) 30 natural-graph instances serve as validation set. (c) Ablation 5 compares natural vs constructed. (d) Explicitly acknowledge construction as a limitation.

### Risk 7: LLM Memorization
- **Likelihood:** LOW
- **Impact:** MEDIUM
- **Mitigation:** Obscure datasets, randomized row ordering, generic column rename check on subset.

### Risk 8: Deadline Pressure (Mar 22)
- **Likelihood:** HIGH (8 days)
- **Impact:** HIGH
- **Mitigation:** (a) Prioritize: data prep → pilot → full run → write. (b) Human study can run in parallel during API runs. (c) If time-crunched: submit 4-page short paper, move ablations + human study to appendix. (d) Worst case: non-archival track.

---

## Timeline (Revised)

| Date | Task | Deliverable |
|------|------|-------------|
| Mar 14-15 | Data prep: download 10 datasets, extract 250 sub-tables | `data/` with 250 JSON files |
| Mar 15-16 | Format generation: tables (MD), charts (PNG), chart descriptions (text), graphs (text), time series (unlabeled arrays) | `formats/` with 1,250 formatted files |
| Mar 16 | Question generation: 1,750 questions (7 types) + ground truth | `questions.jsonl` + `answers.jsonl` |
| Mar 16-17 | Pilot: 20 instances × 2 models, check ceiling effect | Pilot report |
| Mar 17 | Launch human baseline study (Google Forms, 20 participants, 50 questions) | Form live, collect over 2-3 days |
| Mar 17-19 | Full API runs: 7 models × ~6,500 instances | `results/` with model outputs |
| Mar 19-20 | Scoring + statistical analysis (phi, tetrachoric, heatmaps) | Figures + tables |
| Mar 20 | Key ablations (Ablation 1: difficulty, Ablation 4: modality) | Ablation results |
| Mar 20-22 | Write paper (ACL format, 8 pages) | `paper.tex` |
| Mar 22 | Collect human study results, finalize, submit to OpenReview | Submission |

---

## Methodological Safeguards Summary (v3)

| Concern | Safeguard |
|---------|-----------|
| LLM bias in questions | Programmatic generation only, zero LLM involvement |
| Judge conflicts | Cross-judging: Gemini judges Claude, Claude judges others |
| Judge reliability | 100-question overlap judged by BOTH → report Cohen's kappa |
| Ground truth validity | Computed from source data via pandas, deterministic |
| Scoring objectivity | 95%+ auto-scored (exact match + numerical tolerance) |
| Dataset memorization | Obscure datasets, randomized row ordering, contamination check |
| Statistical power | Instance-level (N=1,750), not model-level (N=7) |
| Binary correlation method | Tetrachoric (primary) + phi (secondary). NOT Spearman on binary data |
| Marginal distribution bias | Tetrachoric corrects for skewed marginals; phi reported with caveat |
| Modality confound | Format B' (chart text-description, length-matched) controls for text-vs-image |
| Length confound | Token counts reported per format; B' capped to ±20% of Format A length |
| Graph artificiality | Cross-entity construction + 30 natural-graph sanity check (not formal ablation) |
| Ceiling effect | Hard questions (Q6-Q7) + unlabeled time series + complexity tiers |
| Q6-Q7 ambiguity | Tie-breaking protocol: exclude instances with <5% gap between top-2 values |
| Q7 degeneracy | Threshold selected to ensure 30-70% pass rate; skip if no valid threshold |
| Prompt sensitivity | 3 prompt variants on 50-question subset × 3 models |
| Overclaiming | "Comprehension" not "reasoning"; PCA in appendix only |
| Human comparison | 20-person within-subjects study with Latin-square counterbalancing |
| Reproducibility | All code, prompts, data scripts, and human study materials released |

---

## Predicted Review Scores (v3)

| Reviewer | v1 | v2 | v2 Re-Review | v3 (current) |
|----------|-----|-----|-------------|--------------|
| R1 (NLP) | 6.5 | 7.5 | 7.5 | **7.5** |
| R2 (Eval Methods) | 5.0 | 7.0 | 6.5 | **7.5** |
| R3 (Multimodal) | 6.0 | 7.5 | 7.0 | **7.5** |
| **Average** | 5.8 | 7.3 | 7.0 | **7.5** |
| **P(Accept)** | 30-35% | 70-75% | 60-65% | **80-85%** |

---

## Approval Checklist

- [ ] Dataset selection (10 datasets, 7 domains) approved
- [ ] Format specifications (5 formats including modality control + length matching) approved
- [ ] Question types (7 types including 2 hard + tie-breaking protocol) approved
- [ ] Metrics (tetrachoric primary + phi secondary) approved
- [ ] Human baseline study (20 participants, within-subjects, Latin square) approved
- [ ] Inter-judge agreement protocol (100-question overlap) approved
- [ ] Prompt sensitivity ablation (3 variants × 50 Qs × 3 models) approved
- [ ] Budget ($0 cash, ~$170 total credits) approved
- [ ] Timeline (8 days) feasible
- [ ] Risk mitigations acceptable

**HUMAN CHECKPOINT: Please review and approve this plan before any code is written.**
