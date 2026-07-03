# Thesis Format Prompt

Use this prompt for the final format-compliance pass before Word/PDF generation.

## Objective
Verify that all chapters, figures, tables, citations, and front matter comply with
`template_requirements.md` before invoking `/thesis-build`.

## Stage in pipeline
Runs at `/thesis-format` (stage 10). Runs after `/thesis-audit` (stage 8, P0 cleared)
and after `/thesis-reduce` (stage 9, if used — rewrites merged, evidence map synced).
This is the last gate before `/thesis-build`; any FAIL here blocks the build.

Format must run AFTER any step that mutates chapter text. If reduce runs again,
format must re-run.

## Inputs (mandatory)

| Path | Provider |
|---|---|
| `thesis/notes/template_requirements.md` | `/thesis-intake` — sole format source of truth |
| `thesis/*.md` | canonical chapter files (post-write, post-reduce-merge) |
| `thesis/notes/assets_manifest.md` | `/thesis-assets` — figure inventory |
| `thesis/notes/references_checked.md` | `/thesis-citations` — clean bibliography |
| `thesis/notes/ai_risk_audit.md` | `/thesis-audit` — must show P0 = none |

Hard gates (any one triggers `BLOCKED` and halt):
- `ai_risk_audit.md` still lists P0 items
- any unmerged `thesis/*_reduced.md` file exists (reduce output not yet consolidated
  into the canonical chapter files — format would check the wrong text)

## Outputs

| File | Content |
|---|---|
| `thesis/notes/format_audit.md` | Compliance check results (see schema below) |
| `thesis/notes/format_ready_chapters.md` | List of chapters that passed all checks |

`/thesis-build` may only run once `format_audit.md` reports status = `PASS`.

### `format_audit.md` schema

```md
# Format Audit

Status: PASS | FAIL | BLOCKED

## Checks

| dimension | result | details |
|---|---|---|
| heading_numbering | PASS | — |
| figure_caption_position | FAIL | fig3-2 caption above figure; template requires below |
| table_caption_position | PASS | — |
| citation_marker_style | PASS | all superscript [N] |
| bibliography_style | PASS | GB/T 7714-2015 compliant |
| page_layout | PASS | A4, margins verified |
| front_matter | PASS | abstract, ToC, acknowledgments present |
| word_count | PASS | 19842 / target 18000–22000 |
```

`result` ∈ `PASS | FAIL | SKIP` (SKIP = not applicable for this thesis).

Overall status = `PASS` only if zero `FAIL` rows.

## Audit dimensions

For each dimension, read the rule from `template_requirements.md` and verify:

1. **Heading numbering** — format matches `一、` / `1.1` / `第一章` as specified; no level skipping.
2. **Figure captions** — position (above/below), format (`图 N-M 标题`), all figures cited in body.
3. **Table captions** — position (above/below), format (`表 N-M 标题`), three-line rule applied.
4. **Formula numbering** — right-aligned, format `(N-M)` if required.
5. **Citation marker style** — superscript vs inline, before/after punctuation.
6. **Bibliography style** — standard (GB/T 7714, APA, IEEE), required fields present.
7. **Page layout** — size, margins, font, line spacing, first-line indent.
8. **Front matter** — abstract (CN+EN), ToC, acknowledgments, all required sections present.
9. **Word count** — body word count within school range from `intake_requirements.md`.
10. **Figure–body consistency** — every figure in `assets_manifest.md` is cited; no orphaned figures.

## Token budget
≤ 10k output tokens.

## Prompt Template

```text
You are running the thesis format check.

Read first:
- thesis/notes/template_requirements.md   (the format rules)
- thesis/notes/ai_risk_audit.md           (pre-flight: must show no P0)

Pre-flight: if P0 items exist in ai_risk_audit.md, write format_audit.md with
Status: BLOCKED and halt immediately.

Then audit each of the 10 format dimensions against the chapters and assets.
For each FAIL, include the specific location (chapter §section, figure/table id).

Outputs:
- thesis/notes/format_audit.md
- thesis/notes/format_ready_chapters.md   (chapters with zero FAIL rows)

Output budget ≤ 10k tokens.
```
