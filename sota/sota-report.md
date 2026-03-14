# SOTA Report: StructReason-Transfer

**Paper:** "Do Structured Data Comprehension Skills Transfer Across Representation Types?"
**Generated:** 2026-03-14 | **Venue:** SURGeLLM 2026 @ ACL

---

## Recommended Framework Stack

| Package | Version | Purpose | Status |
|---------|---------|---------|--------|
| **ordinalcorr** | 0.6.1 | Tetrachoric correlation (PRIMARY metric) | Active |
| **scipy** | 1.17.1 | General stats (bootstrap CIs, Kendall tau, phi) | Active |
| **py-irt** | 0.6.6 | Bayesian IRT (appendix, exploratory) | Active, Python <3.12 |
| **tiktoken** | 0.12.0 | Token counting for length confound | Active |
| **matplotlib** | 3.10.8 | Chart PNGs + paper figures | Active |

```bash
pip install ordinalcorr==0.6.1 scipy==1.17.1 py-irt==0.6.6 tiktoken==0.12.0 matplotlib==3.10.8 pandas numpy
```

**Python:** 3.11 (py-irt needs <3.12)

### Avoid
| Package | Why | Use Instead |
|---------|-----|-------------|
| semopy | Dormant | py-irt |
| scipy tetrachoric | Doesn't exist | ordinalcorr |

---

## SOTA Baselines (March 2026)

### Table QA
| Benchmark | SOTA | Score | Date |
|-----------|------|-------|------|
| WikiTQ | Orchestra | >75.3% EM | Jan 2026 |
| TabFact | TabTracer/GPT-4o | ~92.5% | Feb 2026 |
| MMTU | GPT-5 | ~69% | NeurIPS 2025 |

### Chart QA
| Benchmark | SOTA | Score | Human | Date |
|-----------|------|-------|-------|------|
| ChartQA | Qwen3-VL-8B-Masters | 95.9% | ~98% | Dec 2025 |
| ChartQAPro | Claude 3.5 (CoT) | 55.8% | -- | ACL 2025 |
| CharXiv-R | GPT-5.2 | 82.1% | 80.5% | Mar 2026 |
| ChartMuseum | GPT-5.2 | 77.0% | 93.0% | NeurIPS 2025 |

### Graph Reasoning
| Benchmark | SOTA | Key Finding | Date |
|-----------|------|-------------|------|
| GraphOmni | Claude-3.5/o4-mini | Serialization format changes results dramatically | ICLR 2026 |
| GraCoRe | GPT-4 | Major gaps on complex reasoning | COLING 2025 |

### Time Series
| Benchmark | SOTA | Key Finding | Date |
|-----------|------|-------------|------|
| TSAQA | LLaMA-3.1-8B tuned | Best PZ=67.68% | Jan 2026 |
| MMTS-Bench | General LLMs > TS-LLMs | CoT helps | Feb 2026 |
| HeaRTS | Specialists >> LLMs | Temporal complexity kills performance | Feb 2026 |

---

## Scooping Risk

| Paper | Risk | Our Differentiator |
|-------|------|-------------------|
| "Same Content, Different Representations" (ICLR 2026) | **HIGH** | Table-only. We do 5 formats. MUST CITE. |
| "Format as a Prior" (Jan 2026) | MED-HIGH | Bias study, not transfer. No same-data control. MUST CITE. |
| "Format Matters" (Nov 2025) | MED | Claim verification only. CITE. |

**Verdict: Not scooped.**

---

## Must-Cite Papers
1. Zhang et al. "Same Content, Different Representations" (ICLR 2026)
2. Liu et al. "Format as a Prior" (arXiv Jan 2026)
3. Ho et al. "Format Matters" (arXiv Nov 2025)
4. Epoch AI benchmark correlations (Jan 2026)
5. Ilic "General Intelligence Factor in LLMs" (2023)
6. GraphOmni (ICLR 2026)
7. ChartQAPro (ACL 2025)
8. TSAQA (Jan 2026)
9. MMTU (NeurIPS 2025)
10. "Rosetta Stone for AI Benchmarks" (Epoch/DeepMind 2025)

---

## Known Gotchas
| Issue | Fix |
|-------|-----|
| scipy has no tetrachoric | Use ordinalcorr 0.6.1 |
| ordinalcorr low adoption | Validate vs R's polycor on 10 instances |
| py-irt needs Python <3.12 | Use Python 3.11 |
| tiktoken = OpenAI tokenizer only | Report as proxy with caveat |
| ChartQA saturated (>95%) | Target ChartQAPro difficulty |
| GraphOmni: serialization matters | Acknowledge in limitations |
