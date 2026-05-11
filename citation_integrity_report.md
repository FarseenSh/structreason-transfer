# Citation Integrity Report — StructReason-Transfer paper

**Method:** Every one of the 21 bib entries in `paper/references.bib` was verified against the actual paper (arXiv abstract page, ACL Anthology page, OpenReview record, conference proceedings, or author homepage), located via `mcp__exa__web_search_advanced_exa` (category: research paper) and confirmed by `mcp__exa__crawling_exa` of the source page.

**Verdict:** **17 of 21 entries (81%) contain errors.** 14 of those have MAJOR errors (wrong lead author, wrong title, wrong venue, or wrong year — sometimes all four). Of the remaining, only 4 entries are clean (the well-known classics).

This is exactly the kind of failure that ACL's zero-tolerance hallucinated-references policy targets and that EMNLP's expanded paper-integrity policy threatens with multi-year ineligibility for all authors. Submitting the paper to a top venue with this bib is unacceptable.

---

## Summary table

| # | Bib key | Real paper exists? | Status |
|---|---|---|---|
| 1 | `pasupat2015compositional` | Yes | **CLEAN** |
| 2 | `chen2020tabfact` | Yes | **CLEAN** |
| 3 | `masry2022chartqa` | Yes | **CLEAN** |
| 4 | `divgi1979calculation` | Yes | **CLEAN** |
| 5 | `torr2026` | Yes | **MAJOR errors** — wrong title, wrong author |
| 6 | `wikimixqa2025` | Yes | **MEDIUM errors** — title subtitle wrong; lead author OK |
| 7 | `datacross2026` | Yes | **MAJOR errors** — wrong title, wrong author first name |
| 8 | `chartqapro2025` | Yes | **MAJOR errors** — wrong author entirely (Ibrahim is not on the paper); title subtitle slightly wrong |
| 9 | `graphomni2026` | Yes | **MAJOR errors** — wrong author (Hao Li → Hao Xu), wrong title |
| 10 | `gracore2025` | Yes | **MAJOR errors** — wrong author (Ma Yuhan → Zike Yuan), wrong entry type |
| 11 | `tsaqa2026` | Yes | **MAJOR errors** — wrong author (Wang Xin → Baoyu Jing), wrong title |
| 12 | `mmtsbench2026` | Yes | **MAJOR errors** — wrong author (Zhang Wei → Yao Yin), wrong title |
| 13 | `hearts2026` | Yes | **MAJOR errors** — wrong author (Soomin Kim → Sirui Li), title wrong (Heart Rate → Health) |
| 14 | `zhang2026samecontent` | Yes | **MAJOR errors** — wrong first name (Yilun → Yue), wrong subtitle |
| 15 | `liu2026formatprior` | Yes | **MAJOR errors** — wrong author (Liu Chen → Jiacheng Liu), wrong title, wrong year (2026 → 2025) |
| 16 | `ho2025formatmatters` | Yes | **MAJOR errors** — wrong first name (Thanh → Xanh), wrong title |
| 17 | `epoch2026` | Yes | **MAJOR errors** — subtitle hallucinated; citation misuse in paper §5 (the source paper does not study cross-benchmark correlations the way the citation implies) |
| 18 | `ilic2023gfactor` | Yes | **MAJOR errors** — wrong first name (Igor → David Ilić), wrong title |
| 19 | `mmtu2025` | Yes | **MAJOR errors** — wrong author (Li Zheng → Junjie Xing), wrong title (Multi-Modal → Massive Multi-Task) |
| 20 | `charxiv2026` | Yes | **CRITICAL errors** — paper name wrong (CharXiv, not CharXiv-R; "CharXiv-R" does not exist), wrong author (Yi Wang → Zirui Wang), wrong year (2026 → 2024), wrong venue (NeurIPS 2024 not arXiv 2026) |
| 21 | `chartmuseum2025` | Yes | **MAJOR errors** — wrong author (Park Jin → Liyan Tang), wrong title, venue questionable (not confirmed NeurIPS) |

**Tally:** 4 clean. 17 need fixes. Of the 17, 14 are major / 3 are medium. Of the 14 major, 1 is critical (CharXiv-R doesn't exist as a paper at all).

---

## Detailed entry-by-entry findings

### Clean entries (4)

#### 1. `pasupat2015compositional` ✓
- Bib: "Compositional Semantic Parsing on Semi-Structured Tables", Pasupat & Liang, ACL 2015
- Verified: matches exactly. Classic, well-cited paper.

#### 2. `chen2020tabfact` ✓
- Bib: "TabFact: A Large-scale Dataset for Table-Based Fact Verification", Chen et al., ICLR 2020
- Verified: matches exactly. Real paper, real authors, real venue.

#### 3. `masry2022chartqa` ✓
- Bib: "ChartQA: A Benchmark for Question Answering about Charts with Visual and Logical Reasoning", Masry et al., ACL Findings 2022
- Verified: matches exactly. Real, well-cited.

#### 4. `divgi1979calculation` ✓
- Bib: "Calculation of the Tetrachoric Correlation Coefficient", Divgi, Psychometrika 1979
- Verified: real, classic statistical paper. Volume 44, pages 169-172 — matches.

---

### Entries needing correction (17)

#### 5. `torr2026` — MAJOR
- **Bib title:** "ToRR: Table Format Robustness for Multi-Format Evaluation"
- **Actual title:** "The Mighty ToRR: A Benchmark for Table Reasoning and Robustness"
- **Bib author:** "Ashury-Tahan, Mahsa and others"
- **Actual lead author:** Shir Ashury-Tahan (not Mahsa)
- **Co-authors:** Yifan Mai, Rajmohan C, Ariel Gera, Yotam Perlitz, Asaf Yehudai, Elron Bandel, Leshem Choshen, Eyal Shnarch, Percy Liang, Michal Shmueli-Scheuer
- **arXiv:** 2502.19412 (correct)
- **Year:** First v1 submitted Feb 2025; latest revision Feb 2026

**Corrected bib entry:**
```bibtex
@article{torr2026,
  title={The Mighty {ToRR}: A Benchmark for Table Reasoning and Robustness},
  author={Ashury-Tahan, Shir and Mai, Yifan and C, Rajmohan and Gera, Ariel and Perlitz, Yotam and Yehudai, Asaf and Bandel, Elron and Choshen, Leshem and Shnarch, Eyal and Liang, Percy and Shmueli-Scheuer, Michal},
  journal={arXiv preprint arXiv:2502.19412},
  year={2026}
}
```

---

#### 6. `wikimixqa2025` — MEDIUM
- **Bib title:** "WikiMixQA: Cross-Modal Question Answering over Tables and Charts"
- **Actual title:** "WikiMixQA: A Multimodal Benchmark for Question Answering over Tables and Charts"
- **Bib author:** "Foroutan, Negar and others" — lead author correct
- **Actual authors:** Negar Foroutan, Angelika Romanou, Matin Ansaripour, Julian Martin Eisenschlos, Karl Aberer, Rémi Lebret
- **Venue:** Findings of ACL 2025, pages 24941-24958 (correct)

**Corrected bib entry:**
```bibtex
@inproceedings{wikimixqa2025,
  title={{WikiMixQA}: A Multimodal Benchmark for Question Answering over Tables and Charts},
  author={Foroutan, Negar and Romanou, Angelika and Ansaripour, Matin and Eisenschlos, Julian Martin and Aberer, Karl and Lebret, R{\'e}mi},
  booktitle={Findings of the Association for Computational Linguistics: ACL 2025},
  pages={24941--24958},
  year={2025}
}
```

---

#### 7. `datacross2026` — MAJOR
- **Bib title:** "DataCross: A Cross-Modal Benchmark for Structured Data Understanding"
- **Actual title:** "DataCross: A Unified Benchmark and Agent Framework for Cross-Modal Heterogeneous Data Analysis"
- **Bib author:** "Qi, Zheng and others"
- **Actual lead author:** Ruyi Qi (not Zheng)
- **Co-authors:** Zhou Liu, Wentao Zhang (only 3 authors total — "and others" is misleading)
- **arXiv:** 2601.21403 (correct)

**Corrected bib entry:**
```bibtex
@article{datacross2026,
  title={{DataCross}: A Unified Benchmark and Agent Framework for Cross-Modal Heterogeneous Data Analysis},
  author={Qi, Ruyi and Liu, Zhou and Zhang, Wentao},
  journal={arXiv preprint arXiv:2601.21403},
  year={2026}
}
```

---

#### 8. `chartqapro2025` — MAJOR
- **Bib title:** "ChartQAPro: A More Challenging Benchmark for Chart Question Answering"
- **Actual title:** "ChartQAPro: A More Diverse and Challenging Benchmark for Chart Question Answering"
- **Bib author:** "Ibrahim, Mohanad and others" — **Mohanad Ibrahim is not on the paper at all.**
- **Actual lead author:** Ahmed Masry (the same Masry who wrote the original ChartQA, `masry2022chartqa`)
- **Actual full author list:** Ahmed Masry, Mohammed Saidul Islam, Mahir Ahmed, Aayush Bajaj, Firoz Kabir, Aaryaman Kartha, Md Tahmid Rahman Laskar, Mizanur Rahman, Shadikur Rahman, Mehrad Shahmohammadi, Megh Thakkar, Md Rizwan Parvez, Enamul Hoque, Shafiq Joty
- **Venue:** Findings of ACL 2025, pages 19123-19151

**Corrected bib entry:**
```bibtex
@inproceedings{chartqapro2025,
  title={{ChartQAPro}: A More Diverse and Challenging Benchmark for Chart Question Answering},
  author={Masry, Ahmed and Islam, Mohammed Saidul and Ahmed, Mahir and Bajaj, Aayush and Kabir, Firoz and Kartha, Aaryaman and Laskar, Md Tahmid Rahman and Rahman, Mizanur and Rahman, Shadikur and Shahmohammadi, Mehrad and Thakkar, Megh and Parvez, Md Rizwan and Hoque, Enamul and Joty, Shafiq},
  booktitle={Findings of the Association for Computational Linguistics: ACL 2025},
  pages={19123--19151},
  year={2025}
}
```

---

#### 9. `graphomni2026` — MAJOR
- **Bib title:** "GraphOmni: A Comprehensive Benchmark for Graph Understanding"
- **Actual title:** "GraphOmni: A Comprehensive and Extendable Benchmark Framework for Large Language Models on Graph-theoretic Tasks"
- **Bib author:** "Li, Hao and others"
- **Actual lead author:** Hao Xu (not Hao Li)
- **Actual full author list:** Hao Xu, Xiangru Jian, Xinjian Zhao, Wei Pang, Chao Zhang, Suyuchen Wang, Qixin Zhang, Zhengyuan Dong, Joao Monteiro, Bang Liu, Qiuzhuang Sun, Tianshu Yu
- **Venue:** ICLR 2026 (correct)
- **arXiv:** 2504.12764

**Corrected bib entry:**
```bibtex
@inproceedings{graphomni2026,
  title={{GraphOmni}: A Comprehensive and Extendable Benchmark Framework for Large Language Models on Graph-theoretic Tasks},
  author={Xu, Hao and Jian, Xiangru and Zhao, Xinjian and Pang, Wei and Zhang, Chao and Wang, Suyuchen and Zhang, Qixin and Dong, Zhengyuan and Monteiro, Joao and Liu, Bang and Sun, Qiuzhuang and Yu, Tianshu},
  booktitle={The Thirteenth International Conference on Learning Representations},
  year={2026}
}
```

---

#### 10. `gracore2025` — MAJOR
- **Bib title:** "GraCoRe: Benchmarking Graph Comprehension and Complex Reasoning in Large Language Models"
- **Actual title:** matches exactly ✓
- **Bib author:** "Ma, Yuhan and others"
- **Actual lead author:** Zike Yuan (not Yuhan Ma; the GitHub handle is ZIKEYUAN)
- **Actual full author list:** Zike Yuan, Ming Liu, Hui Wang, Bing Qin
- **Bib entry type:** `@article` with `journal={COLING}` — wrong, COLING is a conference; should be `@inproceedings`
- **Venue:** COLING 2025 ✓
- **arXiv:** 2407.02936

**Corrected bib entry:**
```bibtex
@inproceedings{gracore2025,
  title={{GraCoRe}: Benchmarking Graph Comprehension and Complex Reasoning in Large Language Models},
  author={Yuan, Zike and Liu, Ming and Wang, Hui and Qin, Bing},
  booktitle={Proceedings of the 31st International Conference on Computational Linguistics (COLING 2025)},
  year={2025}
}
```

---

#### 11. `tsaqa2026` — MAJOR
- **Bib title:** "Time Series Analysis Question Answering with LLMs"
- **Actual title:** "TSAQA: Time Series Analysis Question And Answering Benchmark"
- **Bib author:** "Wang, Xin and others"
- **Actual lead author:** Baoyu Jing (not Xin Wang)
- **Actual full author list:** Baoyu Jing, Sanhorn Chen, Lecheng Zheng, Boyu Liu, Zihao Li, Jiaru Zou, Tianxin Wei, Zhining Liu, Zhichen Zeng, Ruizhong Qiu, Xiao Lin, Yuchen Yan, Dongqi Fu, Jingchao Ni, Jingrui He, Hanghang Tong
- **arXiv:** 2601.23204

**Corrected bib entry:**
```bibtex
@article{tsaqa2026,
  title={{TSAQA}: Time Series Analysis Question And Answering Benchmark},
  author={Jing, Baoyu and Chen, Sanhorn and Zheng, Lecheng and Liu, Boyu and Li, Zihao and Zou, Jiaru and Wei, Tianxin and Liu, Zhining and Zeng, Zhichen and Qiu, Ruizhong and Lin, Xiao and Yan, Yuchen and Fu, Dongqi and Ni, Jingchao and He, Jingrui and Tong, Hanghang},
  journal={arXiv preprint arXiv:2601.23204},
  year={2026}
}
```

**Note:** the paper text claims "TSAQA showed that fine-tuned LLMs can achieve 67.68% on time series QA" — this specific number must also be re-verified against the actual TSAQA paper. The original citation source has been wrong; the figure may also be wrong.

---

#### 12. `mmtsbench2026` — MAJOR
- **Bib title:** "MMTS-Bench: Multi-Modal Time Series Benchmarking"
- **Actual title:** "MMTS-Bench: A Comprehensive Benchmark for Time Series Understanding and Reasoning"
- **Bib author:** "Zhang, Wei and others"
- **Actual lead author:** Yao Yin (Tsinghua)
- **Actual full author list:** Yao Yin, Zhenyu Xiao (equal first), Musheng Li, Yiwen Liu, Sutong Nan, Yiting He, Ruiqi Wang, Zhenwei Zhang, Qingmin Liao, Yuantao Gu (corresponding) — all Tsinghua
- **arXiv:** 2602.08588

**Corrected bib entry:**
```bibtex
@article{mmtsbench2026,
  title={{MMTS-Bench}: A Comprehensive Benchmark for Time Series Understanding and Reasoning},
  author={Yin, Yao and Xiao, Zhenyu and Li, Musheng and Liu, Yiwen and Nan, Sutong and He, Yiting and Wang, Ruiqi and Zhang, Zhenwei and Liao, Qingmin and Gu, Yuantao},
  journal={arXiv preprint arXiv:2602.08588},
  year={2026}
}
```

**Note:** the paper text claims "MMTS-Bench found that general LLMs with CoT can outperform specialized time-series models" — this claim must also be re-verified against the actual paper.

---

#### 13. `hearts2026` — MAJOR
- **Bib title:** "HeaRTS: Heart Rate Time Series Analysis with LLMs"
- **Actual title:** "HeaRTS: Benchmarking LLM Reasoning on Health Time Series" (note: **Health**, not Heart Rate)
- **Bib author:** "Kim, Soomin and others"
- **Actual lead authors:** Sirui Li, Shuhan Xiao, Mihir Joshi (UCLA — equal first); Ahmed Metwally, Daniel McDuff (Google Research); Wei Wang (UCLA), Yuzhe Yang (UCLA, corresponding)
- **arXiv:** 2603.06638
- HuggingFace: `yang-ai-lab/HEARTS`

**Corrected bib entry:**
```bibtex
@article{hearts2026,
  title={{HeaRTS}: Benchmarking {LLM} Reasoning on Health Time Series},
  author={Li, Sirui and Xiao, Shuhan and Joshi, Mihir and Metwally, Ahmed and McDuff, Daniel and Wang, Wei and Yang, Yuzhe},
  journal={arXiv preprint arXiv:2603.06638},
  year={2026}
}
```

**Note:** the paper text claims "HeaRTS demonstrated that temporal complexity degrades LLM performance" — verify against the actual abstract finding ("performance declines with increasing temporal complexity").

---

#### 14. `zhang2026samecontent` — MAJOR (already flagged in deep_paper_analysis.md)
- **Bib title:** "Same Content, Different Representations: Evaluating LLM Sensitivity to Table Formats"
- **Actual title:** "Same Content, Different Representations: A Controlled Study for Table QA"
- **Bib author:** "Zhang, Yilun and others"
- **Actual lead author:** Yue Zhang (not Yilun)
- **Actual full author list:** Yue Zhang, Seiji Maekawa, Nikita Bhutani (only 3 authors)
- **Venue:** ICLR 2026
- **arXiv:** 2509.22983

**Corrected bib entry:**
```bibtex
@inproceedings{zhang2026samecontent,
  title={Same Content, Different Representations: A Controlled Study for Table {QA}},
  author={Zhang, Yue and Maekawa, Seiji and Bhutani, Nikita},
  booktitle={The Thirteenth International Conference on Learning Representations},
  year={2026}
}
```

This is the closest related work in the entire bib. The paper cites it as the centerpiece of the "we differ from prior work" argument. A reviewer who looks up the citation will see the title/author mismatch immediately.

---

#### 15. `liu2026formatprior` — MAJOR
- **Bib title:** "Format as a Prior: How Representation Shapes LLM Reasoning"
- **Actual title:** "Format as a Prior: Quantifying and Analyzing Bias in LLMs for Heterogeneous Data"
- **Bib author:** "Liu, Chen and others"
- **Actual lead authors:** Jiacheng Liu, Mayi Xu (equal first); Qiankun Pi, Wenli Li, Ming Zhong, Yuanyuan Zhu, Mengchi Liu, Tieyun Qian (corresponding)
- **Bib year:** 2026
- **Actual year:** arXiv 2508.15793, submitted Aug 2025 — should be **2025** not 2026

**Corrected bib entry:**
```bibtex
@article{liu2025formatprior,
  title={Format as a Prior: Quantifying and Analyzing Bias in {LLMs} for Heterogeneous Data},
  author={Liu, Jiacheng and Xu, Mayi and Pi, Qiankun and Li, Wenli and Zhong, Ming and Zhu, Yuanyuan and Liu, Mengchi and Qian, Tieyun},
  journal={arXiv preprint arXiv:2508.15793},
  year={2025}
}
```

(Note bib key change `liu2026formatprior` → `liu2025formatprior` to reflect actual year. The paper's `\cite{liu2026formatprior}` calls in `paper.tex` need to be updated.)

---

#### 16. `ho2025formatmatters` — MAJOR
- **Bib title:** "Format Matters: Claim Verification Across Data Representations"
- **Actual title:** "Format Matters: The Robustness of Multimodal LLMs in Reviewing Evidence from Tables and Charts"
- **Bib author:** "Ho, Thanh and others"
- **Actual lead author:** Xanh Ho (not Thanh Ho)
- **Actual full author list:** Xanh Ho, Yun-Ang Wu, Sunisth Kumar, Florian Boudin, Atsuhiro Takasu, Akiko Aizawa
- **arXiv:** 2511.10075 (Nov 2025) ✓ year correct

**Corrected bib entry:**
```bibtex
@article{ho2025formatmatters,
  title={Format Matters: The Robustness of Multimodal {LLMs} in Reviewing Evidence from Tables and Charts},
  author={Ho, Xanh and Wu, Yun-Ang and Kumar, Sunisth and Boudin, Florian and Takasu, Atsuhiro and Aizawa, Akiko},
  journal={arXiv preprint arXiv:2511.10075},
  year={2025}
}
```

---

#### 17. `epoch2026` — MAJOR (citation misuse, not just metadata)
- **Bib title:** "A Rosetta Stone for AI Benchmarks: Cross-Benchmark Correlation Analysis"
- **Actual title:** "A Rosetta Stone for AI Benchmarks" (no subtitle)
- **Bib author:** `{Epoch AI}` (a corporate-author hack)
- **Actual:** the paper has individual authors at Epoch AI (collaboration with Google DeepMind AGI Safety & Alignment team)
- **arXiv:** 2512.00193 (Nov 2025)

**Citation misuse:** The paper §5 says: "aligning with the cross-benchmark correlations reported by Epoch AI." But the Epoch paper does not "report cross-benchmark correlations" — it builds an item-response-theory-style framework that "stitches" benchmarks together onto a single capability scale (the Epoch Capabilities Index, ECI). The citation should be reframed in the paper text to accurately describe what the Epoch paper does, or removed.

**Corrected bib entry:**
```bibtex
@article{epoch2026,
  title={A {Rosetta Stone} for {AI} Benchmarks},
  author={{Epoch AI}},
  journal={arXiv preprint arXiv:2512.00193},
  year={2025}
}
```

(Note: year should be 2025, not 2026. The arXiv ID 2512 = Dec 2025.)

**Action item:** also revise the §5 sentence in `paper.tex` to accurately describe what the Epoch paper contributes, OR remove the citation.

---

#### 18. `ilic2023gfactor` — MAJOR
- **Bib title:** "A General Intelligence Factor in Large Language Models"
- **Actual title:** "Unveiling the General Intelligence Factor in Language Models: A Psychometric Approach"
- **Bib author:** "Ilic, Igor"
- **Actual author:** David Ilić (single author; not "Igor"; note diacritic)
- **arXiv:** 2310.11616 (Oct 2023) ✓ year correct

**Corrected bib entry:**
```bibtex
@article{ilic2023gfactor,
  title={Unveiling the General Intelligence Factor in Language Models: A Psychometric Approach},
  author={Ili{\'c}, David},
  journal={arXiv preprint arXiv:2310.11616},
  year={2023}
}
```

---

#### 19. `mmtu2025` — MAJOR
- **Bib title:** "MMTU: A Multi-Modal Table Understanding Benchmark"
- **Actual title:** "MMTU: A Massive Multi-Task Table Understanding and Reasoning Benchmark" (note: **Massive Multi-Task**, NOT Multi-Modal)
- **Bib author:** "Li, Zheng and others"
- **Actual lead author:** Junjie Xing
- **Actual full author list:** Junjie Xing, Yeye He, Mengyu Zhou, Haoyu Dong, Shi Han, Lingjiao Chen, Dongmei Zhang, Surajit Chaudhuri, H. V. Jagadish
- **Venue:** NeurIPS 2025 Datasets and Benchmarks Track ✓

**Corrected bib entry:**
```bibtex
@inproceedings{mmtu2025,
  title={{MMTU}: A Massive Multi-Task Table Understanding and Reasoning Benchmark},
  author={Xing, Junjie and He, Yeye and Zhou, Mengyu and Dong, Haoyu and Han, Shi and Chen, Lingjiao and Zhang, Dongmei and Chaudhuri, Surajit and Jagadish, H. V.},
  booktitle={Advances in Neural Information Processing Systems 38: Datasets and Benchmarks Track},
  year={2025}
}
```

**Note:** the bib title's "Multi-Modal" framing is consistent with how the paper's §2 cites MMTU ("MMTU extends evaluation to multi-modal table understanding across diverse domains"). But the actual MMTU paper is **NOT a multi-modal benchmark** — it's a multi-task table benchmark over 25 task types. The paper's claim about MMTU is therefore wrong. This is another citation-misuse case (in addition to the metadata error).

---

#### 20. `charxiv2026` — CRITICAL
- **Bib title:** "CharXiv-R: Chart Reasoning in the Wild"
- **CharXiv-R does not exist as a paper.** The actual paper is just **CharXiv** (no "-R" suffix), and its full title is "CharXiv: Charting Gaps in Realistic Chart Understanding in Multimodal LLMs."
- **Bib author:** "Wang, Yi and others"
- **Actual lead author:** Zirui Wang (Princeton)
- **Actual full author list:** Zirui Wang, Mengzhou Xia, Luxi He, Howard Chen, Yitao Liu, Richard Zhu, Kaiqu Liang, Xindi Wu, Haotian Liu, Sadhika Malladi, Alexis Chevalier, Sanjeev Arora, Danqi Chen
- **Bib year:** 2026
- **Actual year:** **NeurIPS 2024**, not 2026 (arXiv 2406.18521, June 2024)

**Corrected bib entry:**
```bibtex
@inproceedings{charxiv2024,
  title={{CharXiv}: Charting Gaps in Realistic Chart Understanding in Multimodal {LLMs}},
  author={Wang, Zirui and Xia, Mengzhou and He, Luxi and Chen, Howard and Liu, Yitao and Zhu, Richard and Liang, Kaiqu and Wu, Xindi and Liu, Haotian and Malladi, Sadhika and Chevalier, Alexis and Arora, Sanjeev and Chen, Danqi},
  booktitle={Advances in Neural Information Processing Systems 37: Datasets and Benchmarks Track},
  year={2024}
}
```

(Bib key change `charxiv2026` → `charxiv2024`. The paper's `\cite{charxiv2026}` calls in `paper.tex` need to be updated.)

**Action item:** §2 of the paper says "CharXiv-R [charxiv2026] and ChartMuseum [chartmuseum2025] further challenge models on real-world scientific charts." Change "CharXiv-R" to "CharXiv" in the prose.

This is the most severe error in the bib because the paper invents a paper that doesn't exist (CharXiv-R) and cites it in the Related Work section.

---

#### 21. `chartmuseum2025` — MAJOR
- **Bib title:** "ChartMuseum: A Comprehensive Chart Understanding Benchmark"
- **Actual title:** "ChartMuseum: Testing Visual Reasoning Capabilities of Large Vision-Language Models"
- **Bib author:** "Park, Jin and others"
- **Actual lead author:** Liyan Tang (UT Austin) — **Park Jin is not on the paper**
- **Actual full author list:** Liyan Tang, Grace Kim, Xinyu Zhao, Thom Lake, Wenxuan Ding, Fangcong Yin, Prasann Singhal, Manya Wadhwa, Zeyu Leo Liu, Zayne Sprague, Ramya Namuduri, Bodun Hu, Juan Diego Rodriguez, Puyuan Peng, Greg Durrett
- **arXiv:** 2505.13444 (May 2025, last revised Feb 2026)
- **Bib venue:** NeurIPS 2025 — **could not confirm**; the source pages found via Exa show only the arXiv listing. The paper may be unpublished outside arXiv, or published at a different venue.

**Corrected bib entry (conservative — defaults to arXiv preprint until venue verified):**
```bibtex
@article{chartmuseum2025,
  title={{ChartMuseum}: Testing Visual Reasoning Capabilities of Large Vision-Language Models},
  author={Tang, Liyan and Kim, Grace and Zhao, Xinyu and Lake, Thom and Ding, Wenxuan and Yin, Fangcong and Singhal, Prasann and Wadhwa, Manya and Liu, Zeyu Leo and Sprague, Zayne and Namuduri, Ramya and Hu, Bodun and Rodriguez, Juan Diego and Peng, Puyuan and Durrett, Greg},
  journal={arXiv preprint arXiv:2505.13444},
  year={2025}
}
```

**Action item:** verify whether ChartMuseum was accepted to a venue. If yes, update to the correct booktitle.

---

## What this means for the paper

### Risk if submitted to a top venue with current bib

- **ACL workshops (including SURGeLLM):** Zero-tolerance hallucinated-references policy — paper would be removed from proceedings if discovered. Since the user is going non-archival on SURGeLLM, this is moot for the workshop submission.
- **EMNLP / NAACL / ACL main:** explicit "actions against unethical paper submissions, including hallucinated citations" with **multi-year ineligibility** for all authors of the paper if the paper is desk-rejected for fabricated citations. With **17 of 21 entries containing errors**, this rises far above the threshold for desk rejection. A single reviewer who follows two or three citations will notice.
- **arXiv preprint:** no formal review, but reputational damage — peers reading the paper will notice the "CharXiv-R" entry that doesn't exist, the wrong author names, etc.

### What likely happened

This is a textbook LLM-generated bib pattern. The errors are not random:
- **First-name flips** (Yilun→Yue, Igor→David, Zheng→Ruyi, Mahsa→Shir, Soomin→Sirui, Wang Xin→Baoyu Jing, Zhang Wei→Yao Yin, Chen Liu→Jiacheng Liu, Thanh→Xanh, Yi Wang→Zirui Wang) — consistent with an LLM guessing common author names that "sound right" for a given paper topic.
- **Subtitle hallucinations** (CharXiv-R; "Cross-Benchmark Correlation Analysis"; "Heart Rate Time Series" instead of "Health Time Series"; "Multi-Modal" instead of "Massive Multi-Task") — consistent with an LLM writing a "more descriptive" subtitle that aligns with how the paper *cites* the work, not how the work was actually titled.
- **"and others"** as a default coauthor — consistent with an LLM not having access to the actual coauthor list.
- **Wrong @article vs. @inproceedings**, **journal=COLING** — consistent with an LLM not understanding citation typing.

The bib was almost certainly drafted by an LLM (or by a human who relied heavily on LLM suggestions) and not verified against actual sources before this report. None of the reviewers caught it because reviewers rarely check citations.

### Why no reviewer caught this

The 3 SURGeLLM reviewers focused on methodology, framing, and limitations. None of them clicked through citations. This is normal — peer reviewers check ~0-2 citations per paper. The defenses against hallucinated citations are (a) author due diligence, (b) automated tooling like aclpubcheck, and (c) post-acceptance integrity checks. All three failed in this paper's pipeline.

### Recommendation

Treat the entire bib as untrusted until each entry is fixed. Do not submit any version of this paper to a venue (including arXiv preprint) until:

1. **All 17 errored entries are corrected** using the `Corrected bib entry` blocks above.
2. **All `\cite{}` calls in `paper.tex` are reviewed** — some bib keys change (`liu2026formatprior` → `liu2025formatprior`; `charxiv2026` → `charxiv2024`).
3. **The paper text is re-checked for citation misuse:**
   - §2 "MMTU extends evaluation to multi-modal table understanding" — MMTU is *multi-task*, not multi-modal. Rewrite.
   - §2 "CharXiv-R and ChartMuseum further challenge models on real-world scientific charts" — change "CharXiv-R" to "CharXiv".
   - §5 "aligning with the cross-benchmark correlations reported by [Epoch AI]" — the Epoch paper does not report cross-benchmark correlations; rewrite or remove the citation.
   - §2 "TSAQA showed that fine-tuned LLMs can achieve 67.68%" — verify this number against the actual TSAQA paper since the rest of the citation was wrong.
   - §2 "MMTS-Bench found that general LLMs with CoT can outperform specialized time-series models" — verify against actual paper.
   - §2 "HeaRTS demonstrated that temporal complexity degrades LLM performance" — verify.
4. **Re-run aclpubcheck** on the corrected paper.
5. **Sanity-check the full bib once more** against the ACL Anthology, arXiv, and OpenReview sources cited above. (The corrected entries above were generated from those sources.)

### One-line bottom line

The bib has a 81% error rate (17 of 21 entries). Of those, 14 are major (wrong author or wrong title or wrong year or wrong venue). One is critical (CharXiv-R is invented — the paper cites a paper that does not exist). Until every entry is corrected and the paper text re-audited for citation misuse, the paper cannot be safely submitted to any top venue.
