# Thesis Reduce Prompt

Use this prompt for targeted plagiarism-reduction (降重) rewriting that preserves
all factual anchors, experiment numbers, and citation bindings.

## Objective
Reduce repetition and AI-fingerprint patterns in flagged paragraphs by genuinely
improving the writing — varying structure, sharpening word choice, and adding real
specific content — without drifting conclusions, metrics, model names, or dataset
names. The goal is prose that is actually better and more the author's own, not text
that is superficially disguised.

## Scope boundary — what this stage is NOT

This stage improves writing quality. It does **not** disguise AI-generated content to
evade integrity checks. The following are explicitly out of scope and must never be
produced by this skill:

- docx run-level / XML manipulation to fool detectors (invisible characters,
  zero-width spaces, hidden white text, character-spacing tricks)
- homoglyph substitution (swapping Latin/Cyrillic/Greek look-alike characters)
- any edit whose only purpose is to break a detector's tokenizer while leaving the
  content unchanged and undisclosed

These techniques do not improve the thesis, are increasingly flagged as artifacts in
their own right, and constitute academic-integrity evasion. If a user asks for them,
decline and offer genuine rewriting instead. A high AI-detection score is a signal to
improve the writing and add the author's own analysis — not to hide the text.

## Stage in pipeline
Runs at `/thesis-reduce` (stage 9), after `/thesis-audit` (stage 8) clears P0 items
and BEFORE `/thesis-format` (stage 10) — format must check the post-reduce text.
Never run before audit — rewriting on unverified content invalidates the evidence map.

## Inputs (mandatory)

| Path | Provider |
|---|---|
| `thesis/*.md` | `/thesis-write` — chapters to reduce |
| `thesis/notes/ai_risk_audit.md` | `/thesis-audit` — P2 "机械化" flags and locations |
| `thesis/notes/chapter_evidence_map.md` | `/thesis-write` — claim ↔ evidence bindings |
| `thesis/notes/template_requirements.md` | `/thesis-intake` — style constraints |

If the audit reports any unresolved P0, halt and return an error — do not rewrite.

## Outputs

| File | Content |
|---|---|
| `thesis/<chapter>_reduced.md` | Rewritten chapter; replaces the canonical chapter file after user approval |
| `thesis/notes/reduce_report.md` | Per-paragraph change log (see schema below) |
| `thesis/notes/chapter_evidence_map.md` | **updated in place** — see evidence-map sync rule |

### Evidence-map sync rule (mandatory)

Rewriting can merge, split, or renumber paragraphs/sections. After the rewrite:
1. For every evidence-map row whose claim lives in a changed paragraph, verify the
   claim text still appears (possibly reworded) and update its `source_loc`
   (§section / paragraph anchor) to the new location.
2. If a claim was dropped by the rewrite, mark its row `status = removed-by-reduce`
   and flag it in `reduce_report.md` — a silently vanished verified claim is a defect.
3. Do NOT ship the reduced chapter until the evidence map matches the new text.
   A stale map means format/build lose claim traceability entirely.

### Canonical-file resolution rule

After user approval, the `_reduced.md` content replaces the original chapter file
and the `_reduced.md` copy is deleted. `/thesis-format` and `/thesis-build` read
ONLY canonical chapter files; a leftover `_reduced.md` is treated as a gate FAIL.

### `reduce_report.md` schema

```md
| chapter | §section | change_type | original_first_10_words | new_first_10_words | anchor_preserved |
|---|---|---|---|---|---|
| 4 | §4.2 | sentence_restructure | 首先，本文将数据集划分为… | 数据集按 8:1:1 比例划分为… | yes |
| 2 | §2.1 | passive_to_active | 该方法被广泛应用于… | 研究者广泛将该方法用于… | yes |
```

`change_type` ∈ `sentence_restructure | passive_to_active | connector_removal |
lexical_variation | content_injection | paragraph_merge | paragraph_split | other`

`anchor_preserved`: must be `yes` for every row; if `no`, do not ship that change.

`layer` (optional column) ∈ `structure | lexicon | content` — see the three-layer
model below; useful for reporting which layer did the work.

## Fact anchor invariants (hard rules)

These must not change across any rewrite:

| Category | Examples — do not alter |
|---|---|
| Metrics | mIoU = 0.83, Recall = 0.91, FPS = 24 |
| Dataset names | Dunhuang-Mural 2023, COCO val2017 |
| Model names | U-Net, ResNet-50, YOLOv8n |
| Citation bindings | [1], [2-4], inline `(Zhang et al., 2021)` |
| Experiment claims tied to evidence | "训练集 8000 张" bound to data_inventory.md |

If a rewrite would mutate any of the above: skip it and log in `reduce_report.md`.

## Three-layer rewriting model

Apply the layers in order — cheapest and safest first. Each layer genuinely improves
the prose; none disguises unchanged content. Log which layer did the work in the
optional `layer` column of `reduce_report.md`.

### Layer 1 — structure (最先做，收益最大)
Detectors flag **low burstiness** (uniform sentence/paragraph length) and **excessive
structural regularity** far more than individual words. Fix the shape first:
- Vary sentence length: mix short (≤15 chars) and long (≥40 chars) in the same paragraph.
- Break 段段等长 / 段段总分总: alternate detailed and terse paragraphs; use single-focus
  paragraphs; interleave figures/tables to break text walls.
- Remove structural previews ("本文从 A、B、C 三个方面…", "本节将从以下几点…").
- Replace mechanical sequencing (首先/其次/再次/最后) with semantic transitions
  (cause, contrast, escalation) or no connector at all.

### Layer 2 — lexicon (词汇层)
Replace AI-signature phrases with precise, information-bearing wording.
See [`docs/AI_TRIGGER_WORDS.md`](../docs/AI_TRIGGER_WORDS.md) for the full list.
- 空洞套话 → the specific fact it was gesturing at ("具有重要意义" → 对谁、量化多少).
- 研究表明 → named citation + year + number.
- Hollow adverbs (有效地/显著地) → the actual magnitude, or delete.
- Never swap a technical term for a looser synonym — precision beats "variety".

### Layer 3 — content injection (内容层，最有效且最正当)
The one thing no detector can generate for the author: the author's own analysis.
- Add a concrete critique of a cited method ("该方法在小目标上召回偏低，本文据此…").
- Add specific project data, edge cases, or a design-decision rationale.
- Content injection must obey the fact-anchor rules — inject real, evidence-backed
  material only; append a new `chapter_evidence_map.md` row for any injected claim.

Address only paragraphs flagged as P2 in `ai_risk_audit.md` for this session.
Do not proactively hunt unflagged text — scope creep corrupts the evidence map.

### Where to spend effort first (section weighting)
Detection platforms weight sections unevenly — abstracts and introductions/conclusions
carry the most weight, theory sections the least. Interpret this as **where templated
writing hurts the reader most, and therefore where genuine rewriting pays off first**:
prioritize the abstract and conclusion. This is about directing real improvement
effort, not about gaming a score — the rewrite must still be a genuine improvement.

## Token budget
Process one chapter per invocation, ≤ 15k tokens output.

## Prompt Template

```text
You are rewriting chapter {N} for plagiarism reduction.

Read first:
- thesis/notes/ai_risk_audit.md       (find P2 flags for chapter {N})
- thesis/notes/chapter_evidence_map.md (fact anchors — do not alter these)
- docs/AI_TRIGGER_WORDS.md             (lexicon-layer replacements)
- thesis/{chapter_file}.md             (source to rewrite)

Pre-flight check: if ai_risk_audit.md contains unresolved P0 items, halt immediately.

Scope: improve writing quality only. Never apply detector-evasion tricks
(invisible characters, homoglyphs, docx-run manipulation). Decline if asked.

For each P2-flagged paragraph in chapter {N}, apply the three layers in order:
1. Layer 1 structure: vary sentence/paragraph length, remove templated sequencing.
2. Layer 2 lexicon: replace AI-signature phrases (per AI_TRIGGER_WORDS.md) with specifics.
3. Layer 3 content: inject real, evidence-backed analysis; add a new evidence-map row.
Preserve all fact anchors (metrics, model/dataset names, citations); verify
anchor_preserved = yes before logging each change to reduce_report.md.

Prioritize the abstract and conclusion (highest-weight sections) for genuine rewriting.
Do NOT touch paragraphs not flagged in ai_risk_audit.md.

Output budget ≤ 15k tokens.

Outputs:
- thesis/{chapter_file}_reduced.md
- append rows to thesis/notes/reduce_report.md
- append rows to thesis/notes/chapter_evidence_map.md for any Layer-3 injected claim
```
