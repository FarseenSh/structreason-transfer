# SURGeLLM 2026 — Camera-Ready Quality Plan

**Paper:** Do Structured Data Comprehension Skills Transfer Across Representation Types?
**Submission #:** 81 (OpenReview)
**Decision:** Accept (3 reviewers, mean rating 6.33)
**Archival choice:** Non-archival (presentation only) — preserves the work for re-submission to EMNLP / NAACL / ACL

This file is a **quality plan**, not a deadline schedule. Every item below improves the paper artifact: the workshop talk, the poster, the v2 paper for a top conference, the public release, and the public record on the user's CV. Time considerations are intentionally omitted — work is ordered by dependency and importance.

---

## Required Actions From The Acceptance Email (Paraphrased)

The acceptance email instructed authors to:

1. Run **ACL PubCheck** for ACL formatting compliance (https://github.com/acl-org/aclpubcheck)
2. **Incorporate reviewer suggestions** — code/data release commitments, requested revisions, clarifications
3. **Verify all citations are real** — ACL applies a zero-tolerance policy on hallucinated references
4. **Reconfirm the archival choice** in OpenReview — locked once the camera-ready upload completes
5. **Submit the ACL copyright form** (only meaningful for archival papers)

Upload path: OpenReview → Tasks → SURGeLLM "Camera Ready Revision" form. The form accepts the final PDF, the signed copyright form, and the archival selection.

Format: official ACL 2026 LaTeX style, long papers up to 8 pages of content, references and appendices unlimited, de-anonymized author list.

The original email is preserved in the user's inbox for reference.

---

## How non-archival changes the picture

Of the 5 email actions, only **#4 (reconfirm archival choice)** is strictly required for non-archival papers:

| Action | Required for non-archival | Reason to do it anyway |
|---|---|---|
| 1. PubCheck | No (paper not in Anthology) | Catches real formatting bugs that show up in the talk PDF and the v2 conference submission. Worth running. |
| 2. Reviewer revisions | No (no proceedings paper to update) | The reviewer-driven changes improve the artifact. Every change here carries forward into the v2 paper. **Do them.** |
| 3. Citation verification | No strictly (zero-tolerance is for proceedings) | EMNLP / NAACL / ACL all apply equivalent or stricter rules. Any hallucinated cite found by a v2 reviewer is a desk-rejection trigger and a multi-year ineligibility trigger at EMNLP. **Do this.** |
| 4. Confirm archival choice | **Yes — strictly required** | Locks the non-archival status. |
| 5. Copyright form | No (no copyright transfer needed) | Skip. |

The principle: this is the version of the paper that gets a workshop talk and a poster, and it is the foundation of the v2 conference submission. Treat it as a quality artifact regardless of whether it lands in the Anthology.

---

## Step 1 — Apply reviewer-driven revisions to `paper/paper.tex`

Every revision below makes the paper stronger for both the SURGeLLM presentation and the eventual v2 conference submission.

### From Reviewer 5243 (rating 6, "Clear Setup, Limited Novelty")

- ☐ **Soften graph reasoning transfer claims.** The graph format is a constructed serialization of tabular data, not a natural graph representation. §3.2 already has a one-sentence acknowledgment ("this is a constructed serialization of tabular data into graph-like text, not a natural graph structure"). Extend that hedging into the Introduction (claims), the Discussion (Implications for benchmark design), and the Conclusion. Replace any uses of "graph reasoning" with "graph-like serialization" where the claim is about the constructed format.
- ☐ **Tighten writing and framing.** Rewrite the Introduction and Discussion in a more polished narrative voice. Trim the mechanical "Finding 1 / Finding 2 / Finding 3" structure in §4.1 — replace with a flowing paragraph that integrates the findings. The opening of each section currently reads like an experimental report; rewrite the topic sentences to lead with the conceptual contribution, not the table number.
- ☐ **Clarify scope of conclusions.** Add an explicit "scope of claims" passage in the Discussion, distinguishing between (a) what the controlled benchmark establishes, (b) what is suggestive evidence requiring future validation, and (c) what is speculative.
- ☐ **Strengthen positioning relative to prior work.** The Related Work section names Zhang 2026 (table-only same-content), Liu 2026 (format-as-prior), Ho 2025 (claim verification format), ToRR 2026 (multi-format table robustness), WikiMixQA, DataCross. Reorganize this section so the reader sees a clear gap-and-contribution narrative rather than a list. Each cited prior work should be followed by an explicit "we differ by…" sentence.

### From Reviewer NRrg (rating 5, "accept with changes")

- ☐ **Add statistical significance tests to the main results.** Table 2 currently shows accuracy with Wilson 95% CIs. Add per-format-pair paired McNemar tests (or bootstrap p-values from the 2,000 resamples already used for tetrachoric CIs) for the cross-format accuracy differences within each model. Surface the bootstrap CI methodology near Table 2, not just in §3.6 (Metrics).
- ☐ **Address the edge-description confound in the graph format.** The paper notes graph representations are roughly 2× longer due to edges. Run an ablation: graph-without-edges (node attributes only) vs. graph-with-edges. Report the marginal contribution of edges to graph accuracy. If the edge contribution is small, the result strengthens. If it is large, position it carefully and discuss what that implies for the constructed-vs-natural-graph framing. This ablation can be computed entirely from the existing question set against a re-rendered Format C variant.
- ☐ **Justify synthetic sub-tables vs. real-world data.** Extend the Limitations passage: explicitly motivate why controlled synthesis was chosen (counterfactual control: same content across formats, deterministic ground truth, no contamination), and acknowledge the distributional-bias trade-off NRrg flagged. Mention specific real-world datasets (WikiTQ, CharXiv-R, ChartQA-Pro) as concrete future-work targets rather than vague "real-world data."
- ☐ **Address the N=6 model concern.** Add a paragraph stating that the six models are March 2026 frontier models from six distinct organizations / training pipelines (Google, Anthropic via AWS Bedrock, Moonshot, Zhipu, Alibaba, DeepSeek, MiniMax — note that two of the seven listed in CLAUDE.md were combined). Note total compute budget. Frame N=6 as deliberate frontier coverage rather than convenience sampling. Add a forward pointer to scaling the panel for the v2 paper.
- ☐ **Answer NRrg's three technical questions** in a footnote at the end of the Discussion or in a brief Appendix B:
  - Real-world dataset transfer: "the controlled synthesis isolates representation effects from content variation; real-world transfer is a deliberate next step in the v2 study." 
  - Prompt variations for Chart Text: "the gap likely reflects structural sequentiality (entity-value pairs in flowing prose vs. row-column indexing). Prompt-engineering interventions are out of scope here but a candidate intervention would be to ask the model to reconstruct an intermediate table before answering."
  - Semantic graph construction: "edges via metric cosine similarity were chosen for reproducibility; semantic-relation edges (e.g., is-a, part-of) would require domain-specific schema and are appropriate for a future study targeting natural graph datasets."

### From Reviewer HZuL (rating 8, clear accept)

- ☐ No specific revisions requested.

### Author-driven revisions

- ☐ **De-anonymize:** change `\author{Anonymous}` (line 17 of `paper.tex`) to real name, affiliation, email. ACL camera-ready papers always show authors.
- ☐ **Acknowledgments:** the current §"Acknowledgments" thanks the credit pools (Google Cloud, AWS Bedrock, OpenRouter) and the `ordinalcorr` library. Add anyone else who deserves thanks.
- ☐ **Code and data release.** The paper text currently states "All code, data, and prompts will be released upon publication." Replace this with a concrete URL (a public GitHub repo) before camera-ready. See Step 4.

---

## Step 2 — Verify every citation exists

The bib file has 21 entries. Several have venue/year combinations that warrant explicit verification:

| Bib key | Year | Risk |
|---|---|---|
| `pasupat2015compositional`, `chen2020tabfact`, `masry2022chartqa`, `divgi1979calculation`, `ilic2023gfactor` | Older, well-known | Low |
| `mmtu2025`, `chartqapro2025`, `chartmuseum2025`, `gracore2025`, `wikimixqa2025`, `ho2025formatmatters` | 2025 | Medium — verify titles + venues + arXiv IDs |
| `graphomni2026`, `tsaqa2026`, `mmtsbench2026`, `hearts2026`, `charxiv2026`, `torr2026`, `datacross2026`, `zhang2026samecontent`, `liu2026formatprior`, `epoch2026` | 2026 | High — every entry needs verification |

**Verification process for each entry:**
1. Search the title verbatim in Google Scholar, Semantic Scholar, and the ACL Anthology
2. Cross-check authors, venue, and year against the actual paper page
3. If the entry is on arXiv, confirm the arXiv ID resolves and the title matches
4. If the cite is for a 2026 paper, confirm the paper exists at the time of writing (not a hallucinated future citation)
5. Any unverifiable entry: either correct the entry against the real paper, or remove the entry and rewrite the citing prose to reference a verifiable paper instead

The `ai-research-integrity-check` skill automates much of this. Recommended invocation:

```
Skill ai-research-integrity-check on paper/paper.tex with bibliography paper/references.bib
```

The integrity check returns CLEARED or BLOCKED with specific issues per entry.

This step is non-negotiable. ACL workshops, EMNLP, NAACL, ACL, ICLR, NeurIPS — every venue the v2 paper could target — applies a hallucinated-reference policy. The cost of a single fabricated citation is paper removal at minimum and multi-year author ineligibility at EMNLP.

---

## Step 3 — Run ACL PubCheck

Even though PubCheck enforcement is for archival proceedings, the tool is the single best automated check for ACL-style formatting bugs. Bugs it catches show up in the talk PDF, the poster, and any v2 submission that reuses the same template.

**One-shot via `uvx`:**

```bash
cd /Users/farseenshaikh/surgellm-2026-structreason/paper
tectonic paper.tex
uvx --from git+https://github.com/acl-org/aclpubcheck aclpubcheck --paper_type long paper.pdf
```

**Or via pip:**

```bash
pip3 install git+https://github.com/acl-org/aclpubcheck
aclpubcheck --paper_type long paper.pdf
```

**Pre-emptive PubCheck-related items in `paper.tex`:**

- ☐ `\usepackage{acl}` is present without the `[review]` option (currently correct — line 2 uses final mode)
- ☐ Author block is de-anonymized (Step 1)
- ☐ Page count: ≤ 8 pages of content (refs + appendix don't count)
- ☐ A4 paper format (acl.sty handles this; verify tectonic isn't downgrading to letter)
- ☐ Title block has no images, no inline LaTeX glyphs that won't render in OpenReview metadata
- ☐ Figures fit within margins (use `adjustbox` if any overflow)
- ☐ All cross-references resolve (no `??` placeholders)

---

## Step 4 — Code and data release

The paper commits to a release. Delivering on that commitment is part of the artifact.

- ☐ Create or claim a public GitHub repository for the project (e.g. `farseen/structreason-transfer`)
- ☐ Audit the repo for secrets — `.env` is in `.gitignore`, but verify that no API keys, OpenRouter tokens, AWS keys, or Google credentials are committed historically
- ☐ Choose licenses: code (MIT, Apache-2.0, or BSD-3-Clause), data (CC-BY-4.0)
- ☐ Write a top-level `README.md` covering: install (Python 3.11, requirements.txt), data download / regeneration, runner commands per provider, how to reproduce the figures, license
- ☐ Decide where data lives. Two reasonable paths:
  - Lightweight: ship the 250 sub-tables + question set + format renderings inside the repo (~ tens of MB, fine for git)
  - Long-term: archive the dataset on Zenodo or Hugging Face Datasets for a stable DOI / handle
- ☐ Replace "All code, data, and prompts will be released upon publication" in the paper with a concrete repo URL (and a Zenodo DOI if used)
- ☐ Tag a release (e.g. `v1.0-surgellm`) so the SURGeLLM-version artifacts are pinned even after the v2 work begins

**Note on git state:** at present, only `experiments/experiment-plan.md` and `sota/sota-report.md` are committed. Everything else (experiment code, data, results, figures, paper) is untracked. The repo cleanup is a substantive task on its own.

---

## Step 5 — ACL copyright form (skip for non-archival)

Non-archival papers do not transfer copyright because the work is not being archived. Confirm this by either reading the OpenReview Camera Ready Revision form (it should mark the copyright upload as not-required when archival is set to "Do not include in proceedings") or by asking the organizers directly.

If in doubt, draft a clarification email to organizers (see template at the end of this file).

---

## Step 6 — Pre-submit final audit

Before the OpenReview upload:

- ☐ Recompile `paper.tex` after all revisions: `tectonic paper.tex`
- ☐ Verify page count is ≤ 8 pages of content
- ☐ Spell-check (`aspell -t < paper.tex`, or a LaTeX-aware tool)
- ☐ Run PubCheck one more time on the final PDF
- ☐ Visually open the final PDF: confirm figures render, captions intact, table widths fit, no overflow, no `??` placeholders, no anonymized stragglers
- ☐ Run `ai-research-pre-submit` skill on the paper for a structured audit (anonymization, page limit, abstract length, figure / reference cross-checks, TODO markers, BibTeX hygiene)
- ☐ Run `ai-research-integrity-check` skill one final time
- ☐ Run `ai-research-fig-check` skill to verify figure DPI, vector vs. raster, and colorblind accessibility

---

## Step 7 — Upload to OpenReview

- ☐ Log in to OpenReview
- ☐ Tasks → SURGeLLM "Camera Ready Revision"
- ☐ Upload final `paper.pdf`
- ☐ Confirm "Do not include in proceedings"
- ☐ Skip copyright form (or follow the form's lead if it requires one)
- ☐ Submit
- ☐ Save the revision confirmation (PDF / screenshot)

---

## Critical risks (ranked by severity, not urgency)

1. **Hallucinated citations.** 13 of 21 references are 2025–2026 and have not been integrity-checked. A single hallucinated cite carries forward into the v2 paper and is a desk-rejection trigger at every top venue. **Run `ai-research-integrity-check` first; treat any BLOCKED entry as required-fix.**
2. **Untracked git state.** Paper, code, results, figures all sit outside git. The release commitment in the paper text cannot be honored until this is cleaned up. The repo also serves as the foundation for the v2 paper.
3. **Archival decision is locked at upload.** Non-archival is the right call here (preserves freedom for EMNLP / NAACL / ACL). The lock is a one-way door — make sure the OpenReview form really shows "Do not include in proceedings" before submitting.
4. **De-anonymization.** Easy to forget, and PubCheck does not always catch it. Verify by visual inspection of the PDF.
5. **Code / data release commitment in the paper text.** The paper currently promises release. Delivering means a public, clean, documented repo with at minimum a working README. Anything less is a credibility cost.

---

## Reviewer-summary cross-reference

For full review text, see [`reviews/reviews.md`](reviews/reviews.md).

| Reviewer | Rating | Action burden |
|---|---|---|
| HZuL | 8 (clear accept) | Minimal — no specific asks |
| 5243 | 6 (marginal accept) | Medium — writing/framing pass, soften graph claims, position vs. prior work |
| NRrg | 5 (marginal reject) | Heavy — significance tests, edge ablation, justify synthetic + N=6, answer 3 technical questions |

---

## Strategic context: this is v1, EMNLP / NAACL / ACL is v2

Going non-archival on SURGeLLM preserves the right to submit a stronger version to a top conference. The reviewer-driven revisions in Step 1 are not throwaway work — every fix carries forward. The integrity check in Step 2 is mandatory at every venue. The repo cleanup in Step 4 is the foundation of the v2 paper's reproducibility section. PubCheck in Step 3 catches formatting bugs that recur in v2.

The v2 upgrade levers (separate file recommended once camera-ready is uploaded):
- Add ≥1 real-world data source (CharXiv-R, ChartQA-Pro, WikiTQ) alongside the synthetic benchmark
- Expand reasoning ablation from 2 models to all 6+
- Add the planned within-subjects human study (20 participants, Latin-square, 50 questions)
- Add prompt-sensitivity analysis
- Run an additional graph format using semantic edges for direct comparison with the cosine-similarity edges
- Expand the model panel beyond N=6 (open-weights additions are cheap once infrastructure is set)
- Replace any unverifiable 2026-dated citations with real, verifiable references

---

## Clarification email to organizers (template, send if helpful)

> **Subject:** Camera-ready requirements for non-archival paper — Submission #81
>
> Dear SURGeLLM Organizers,
>
> Thank you again for accepting our paper "Do Structured Data Comprehension Skills Transfer Across Representation Types? A Systematic Study with Frontier LLMs" (Submission #81).
>
> I am confirming the **non-archival** option (presentation only, not included in proceedings). I would like to clarify what is required for the camera-ready submission given this choice:
>
> 1. Do non-archival papers still need to upload a de-anonymized final PDF via the OpenReview "Camera Ready Revision" form, or only confirm the archival selection?
> 2. Is the ACL PubCheck step required for non-archival papers, since the paper will not appear in the ACL Anthology?
> 3. Is the ACL copyright transfer form required for non-archival papers, or does it only apply to archival submissions?
> 4. Will I receive separate instructions about the poster / oral presentation logistics later, or are those tied to the camera-ready submission?
>
> Best regards,
> Farseen Shaikh
