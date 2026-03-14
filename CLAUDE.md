# SURGeLLM 2026 — Paper 2: StructReason-Transfer

## Project Info
- **Paper title:** "Do Structured Data Comprehension Skills Transfer Across Representation Types? A Systematic Study with Frontier LLMs"
- **Target venue:** SURGeLLM 2026 Workshop @ ACL 2026 (San Diego, Jul 2-3)
- **Paper format:** Long paper, 8 pages ACL format (excl. references/appendices)
- **Submission:** Direct to OpenReview, deadline 2026-03-22 AoE
- **Notification:** 2026-04-28 | **Camera-ready:** 2026-05-12
- **Budget:** $0 cash (~$170 total credits)
  - Google: $300 available → ~$67 used → $233 remaining
  - AWS Bedrock: $100 available → ~$65 used → $35 remaining
  - OpenRouter: $60 available → ~$38 used → $22 remaining
- **Pipeline version:** Sovereign AI Scientist v1.4
- **Created:** 2026-03-14
- **Predicted acceptance:** 80-85% (after 2 rounds of adversarial review)

## IMPORTANT: Dual Paper Setup
- **Paper 1** (self-correction): `/Users/farseenshaikh/surgellm-2026/`
- **Paper 2** (this one): `/Users/farseenshaikh/surgellm-2026-structreason/`
- DO NOT modify Paper 1 files. Shared credit pool — don't overspend.

## Core Idea
Present identical underlying data in 5 formats (table, chart image, chart text-description, graph, time series). Ask identical programmatic questions (7 types). Measure cross-format comprehension correlation via tetrachoric correlation on 7 frontier March 2026 models. Key question: are skills siloed by format, or do they transfer?

## Models (March 2026 SOTA)
| Model | Platform | Vision? |
|-------|----------|---------|
| Gemini 3.1 Pro | Google credits | Yes |
| Claude Sonnet 4.6 | AWS Bedrock credits | Yes |
| Kimi K2.5 | OpenRouter credits | Yes |
| GLM-5 | OpenRouter | Yes |
| Qwen 3.5 397B MoE | OpenRouter | Check |
| DeepSeek V3.2 | OpenRouter | Check |
| MiniMax M2.5 | OpenRouter | Check |

## Final 5 Ideas (All Novelty-Verified)
1. **StructReason-Transfer** (NOVEL) ← SELECTED
2. ProcessDiagramBench (PARTIALLY NOVEL)
3. StructScale (PARTIALLY NOVEL)
4. StructEdit (PARTIALLY NOVEL)
5. AgentAnalyst-Bench (PARTIALLY NOVEL)

13 ideas generated, 8 rejected during novelty checking across 4 rounds.

## Scooping Risk (From SOTA Scan)
- "Same Content, Different Representations" (ICLR 2026) — HIGH risk but table-only. MUST CITE.
- "Format as a Prior" (arXiv Jan 2026) — MED-HIGH, bias study not transfer. MUST CITE.
- "Format Matters" (arXiv Nov 2025) — MED, claim verification only. CITE.
- **Verdict: Not scooped.** Our 5-format cross-type study is unique.

## Key Technical Decisions
- **Metrics:** Tetrachoric correlation (primary, via `ordinalcorr` 0.6.1), phi (secondary), Kendall tau-b
- **NOT scipy** for tetrachoric — function doesn't exist in scipy
- **NOT semopy** for IRT — dormant. Use `py-irt` 0.6.6
- **Python 3.11** required (py-irt needs <3.12)
- **Questions:** 100% programmatic, zero LLM involvement, deterministic ground truth
- **Judging:** Cross-judging (Gemini↔Claude), 100-question overlap for inter-judge kappa
- **Human study:** 20 participants, within-subjects, Latin-square, 50 questions

## Pipeline State
| Skill | Status | Notes |
|-------|--------|-------|
| 1. Ideation | DONE | 13 ideas, 5 selected |
| 2. Novelty Check | DONE | 4 rounds, all verified |
| 3. Literature Review | DONE (during ideation) | 60+ papers surveyed |
| 4. SOTA Scanner | DONE | Libraries, baselines, scooping risk all verified |
| 5. Experiment Design | DONE | v3 plan, 2 adversarial review rounds |
| 6. Experiment Runner | NEXT | Awaiting plan approval |

## Key Files
- `experiments/experiment-plan.md` — v3 experiment plan (post-review, SOTA-verified)
- `sota/sota-report.md` — SOTA report with library stack, baselines, scooping risk

## Decisions Log
- 2026-03-14: Generated 13 ideas targeting SURGeLLM 2026 CFP
- 2026-03-14: Novelty checked all — rejected 8 (ConstrainedReason, SerializeOrDie, BiasLens, ChartGenEval, CrossLingualTableQA, StructCoT, StructSynth, StructAdv, StructProvenance, DashboardQA, StructDelta all scooped)
- 2026-03-14: Dropped StructHalluce and StructFail — bet against model progress
- 2026-03-14: Final 5 locked: StructReason-Transfer, ProcessDiagramBench, StructScale, StructEdit, AgentAnalyst-Bench
- 2026-03-14: Selected Idea 1 (StructReason-Transfer) — only NOVEL-rated idea
- 2026-03-14: Experiment plan v1 → adversarial review → v2 (7 fixes) → re-review → v3 (6 more fixes)
- 2026-03-14: SOTA scan completed — scipy tetrachoric doesn't exist (use ordinalcorr), semopy dormant (use py-irt), scooping risk assessed (safe)
- 2026-03-14: Separated into own directory (was conflicting with Paper 1's files)
