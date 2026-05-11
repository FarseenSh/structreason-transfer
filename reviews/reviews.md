# SURGeLLM 2026 — Paper Reviews

**Paper:** Do Structured Data Comprehension Skills Transfer Across Representation Types? A Systematic Study with Frontier LLMs.
**Author:** Farseen Shaikh
**Submission Number:** 81
**Venue:** SURGeLLM
**Published:** 30 Apr 2026 (Last Modified: 30 Apr 2026)
**License:** CC BY 4.0

**Keywords:** structured data, cross-format transfer, tetrachoric correlation, table QA, chart comprehension, graph reasoning, time series, LLM evaluation, benchmark

**TL;DR:** We test identical questions on identical data across 5 formats (table, chart, graph, time series) on 6 frontier LLMs and find comprehension skills transfer strongly across text formats (r=0.84) but chart image processing is siloed.

**Abstract:**
Large language models (LLMs) are increasingly evaluated on structured data tasks—table question answering, chart comprehension, graph reasoning, and time series analysis—yet these benchmarks operate in isolation. We ask: does competence in one structured data format predict competence in another when the underlying data and questions are identical? We construct a controlled benchmark of 1,724 programmatically generated questions over 250 sub-tables drawn from 10 datasets spanning 7 domains. Each sub-table is rendered in five formats: Markdown table, chart image, chart text-description, entity-relationship graph, and unlabeled time series. We evaluate six frontier March 2026 LLMs and measure cross-format transfer via tetrachoric correlation on binary (correct/incorrect) outcomes. Our key findings: (1) structured data comprehension skills transfer strongly across text-based formats, with mean tetrachoric r=0.84 between table, graph, and time series representations (r=0.85 overall; r=0.84 for non-ceiling models, confirming the result is not an artifact of high accuracy); (2) chart text-descriptions show consistently lower transfer (r=0.65) despite being length-matched to tables; (3) chart image comprehension is largely siloed, with a 20-50% accuracy gap compared to equivalent text descriptions; and (4) enabling chain-of-thought reasoning improves accuracy by 24-38% for DeepSeek V3.2 but only 0-0.5% for Gemini 3.1 Pro, suggesting reasoning benefits may vary substantially across models. On hard questions (multi-hop and conditional aggregation), transfer remains substantial at r=0.78.

**Proceedings Inclusion:** Do not include in proceedings

---

## Paper Decision

**Decision:** Accept
**By:** Program Chairs
**Date:** 30 Apr 2026, 22:35 (modified: 30 Apr 2026, 23:09)

---

## Official Review — Reviewer 5243

**Title:** Clear Setup, Limited Novelty
**Date:** 23 Apr 2026, 14:38 (modified: 30 Apr 2026, 23:23)

### Summary

This paper studies whether structured data comprehension transfers across representation types when the underlying content is kept constant. The authors compare the same data and questions across table, chart, chart-text, graph, and time-series representations, and show that text-based structured formats transfer well to one another, while chart-image understanding remains noticeably weaker. Overall, the paper offers a clear and useful explanation of where current structured-data understanding appears to generalize and where it still breaks down.

### Strengths

1. The paper addresses a relevant question for structured-data evaluation.
2. The controlled same-content, same-question setup helps isolate representation effects and makes the comparisons easier to interpret.
3. The chart-image versus chart-text comparison is a useful part of the study and helps clarify the nature of the observed gap.

### Weaknesses

1. The graph format is constructed from tabular data rather than being a naturally occurring graph representation, so the claims about graph reasoning transfer should be stated more carefully.
2. The benchmark is highly controlled and programmatic, which supports internal validity, but it is less clear how strongly the findings transfer to noisier real-world settings.
3. Some broader conclusions are based on limited coverage, especially for chart-image evaluation and the reasoning ablation.
4. The writing and framing could be improved. At times, the paper reads more like an experimental report than a polished research paper, and the contribution would benefit from more careful positioning relative to prior work.

### Detailed Comments

This paper addresses a relevant question and uses a controlled setup that makes the comparisons easy to follow. The chart-image versus chart-text comparison is informative. That said, I think the paper would benefit from a more measured presentation. In several places, the writing reads more like an experimental report than a polished paper, and the contribution could be positioned more carefully relative to prior work. I would encourage the authors to tighten the claims, improve the framing, and clarify the intended scope of the conclusions.

**Rating:** 6: Marginally above acceptance threshold
**Confidence:** 4: The reviewer is confident but not absolutely certain that the evaluation is correct

---

## Official Review — Reviewer HZuL

**Title:** Well written work exploring the transfer of structured data comprehension skills across representation types
**Date:** 22 Apr 2026, 10:18 (modified: 30 Apr 2026, 23:23)

### Review

The paper explores whether the representation of how structured data is presented matters. The authors create a benchmark of 1724 questions where the same data and questions are presented in five formats namely: Table, Chart Image, Chart Text, Graph, and Time Series. The questions also vary from simple Lookup to complex questions involving aggregation, multihop, or conditional aggregation.

The authors observe that all models exhibit similar accuracy when data is presented either as a table, a graph, or a time series. When the chart is presented as text, they observe significant information loss. Chart Image performance is the lowest. The results indicate that there is a high transfer of skill between Table to graph, table to time series, and graph to time-series. Questions which involve aggregation or conditional aggregation show the largest format-dependence variance.

**Rating:** 8: Top 50% of accepted papers, clear accept
**Confidence:** 4: The reviewer is confident but not absolutely certain that the evaluation is correct

---

## Official Review — Reviewer NRrg

**Title:** This work represents an important initial step in systematically evaluating cross-format comprehension within structured data. The experimental design is well-controlled, generating valuable insights into the relative strengths and weaknesses if different LLMs across various representations. However, several limitations and areas for future investigation warrant careful consideration. My verdict is accept with changes.
**Date:** 21 Apr 2026, 01:41 (modified: 30 Apr 2026, 23:23)

### Review

**Quality and Clarity:** The paper demonstrates a reasonable level of clarity in its methodology and presentation. The use of tetrachoric correlation as a metric is justified given the nature of the data. Tables are used effectively to organize results. The inclusion of confidence intervals via bootstrapping adds robustness to the findings.

**Originality:** The core concept of exploring cross-format transfer in structured data is not entirely novel. However, the specific combination of models, formats, and the reliance on synthetic sub-tables creates a unique experimental setup. The central innovation lies in simplifying the evaluation landscape for structured data by highlighting the distinct challenges posed by chart image comprehension vs. text-based formats. The paper explicitly states, "researchers may confidently generalize from one text-based format to others, but chart image comprehension requires independent assessment". This is a crucial observation that directly addresses a significant gap in existing benchmarks.

**Significance:** This research contributes meaningfully to the AI benchmark field, especially for structured data. The finding that chart image comprehension remains significantly weaker than other formats highlights a critical gap in current LLM capabilities and provides a clear direction for future development.

The authors have clearly articulated the weaknesses of the paper:

- While the findings regarding the accuracy are noted, the level of detail in presenting the quantitative results in Table 2 is insufficient. The paper needs to provide more granular data, including confidence intervals and statistical significance tests, to fully support its claim.
- The acknowledgment of "edge-descriptions" as a potential confound in graph representation is important, but the paper doesn't fully explore or mitigate this issue. More rigorous controls would strengthen the findings.
- The reliance on synthetic sub-tables introduces a potential bias. Real-world data may exhibit different difficulty distributions that could significantly alter the results.
- Evaluating only six LLMs represents a relatively small sample size, limiting the generalizability of the findings.

*Key technical questions*

- How would the results change if evaluated with real-world datasets with varying difficulty levels and data distribution?
- What prompt variations of phrasing and constraints would improve Chart Text performance?
- Could alternative graph construction methods like those based on semantic relationships yield more meaningful representations?

The paper demonstrates a reasonable level of reproducibility through detailed metric definitions, code release plans, and the use of publicly available datasets. This research has significant merit and has contributed meaningfully to the field. However, addressing the weaknesses outlined above, especially by providing more robust quantitative evidence and a deeper exploration of key technical aspects, is crucial for achieving a stronger paper.

**Rating:** 5: Marginally below acceptance threshold
**Confidence:** 3: The reviewer is fairly confident that the evaluation is correct

---

## Summary

| Reviewer | Rating | Confidence |
|---|---|---|
| HZuL | 8: Top 50% of accepted papers, clear accept | 4 |
| 5243 | 6: Marginally above acceptance threshold | 4 |
| NRrg | 5: Marginally below acceptance threshold | 3 |

**Mean rating:** 6.33 · **Mean confidence:** 3.67 · **Final decision:** Accept (no proceedings inclusion)
