# Thesis Writer Prompt

Use this prompt when a chapter should be drafted from verified evidence.

## Objective
Generate a chapter draft without fabricating implementation details, experiments, figures, or references.

## Stage in pipeline
Runs at `/thesis-write` (stage 5). Only one writer per chapter at any time
(`/thesis-write` chapter-level mutex; see docs/TEAM_ORCHESTRATION.md).

## Inputs (mandatory file paths)

| Path | Provider |
|---|---|
| `thesis/notes/template_requirements.md` | `/thesis-intake` — single source of truth for format |
| `thesis/notes/thesis_outline.md` | `/thesis-outline` — chapter goal & target word count |
| `thesis/notes/chapter_matrix.md` | `/thesis-outline` — evidence/figure/reference bindings |
| `thesis/notes/figure_plan.md` | `/thesis-outline` — figure numbering & captions |
| `thesis/refs/papers_inventory.md` | `/thesis-data` — reference status (verified/partial/etc.) |
| `thesis/notes/metric_tables.md` | `/thesis-data` — experiment numbers (do not invent) |

If any of the above is missing or empty, halt and emit
`thesis/notes/unresolved_issues.md` instead of writing.

## Outputs

| File | Schema |
|---|---|
| `thesis/<chapter>.md` | Markdown chapter following `template_requirements.md` heading rules |
| `thesis/notes/chapter_evidence_map.md` | append rows; see schema below |
| `thesis/notes/unresolved_issues.md` | append issues that block this chapter |

### `chapter_evidence_map.md` schema

```md
| chapter | claim | source_file | source_loc | status |
|---|---|---|---|---|
| 4 | mIoU = 0.83 on test split | thesis/notes/metric_tables.md | tab.4 row 2 | verified |
| 4 | augmentation lifts recall by 6pt | refs/papers/liu_2018_partialconv.pdf | §4.2 fig.5 | verified |
| 4 | 数据集来自学校扫描档案 | — | — | unverified |
```

`status` ∈ `verified | partial | unverified | fake-risk`. Match the same enum used by
`reference_truth_report.md` so downstream audit can join the two.

## Hard gate: unverified ratio

Count `status = unverified` rows scoped to this chapter.
- If `unverified / total > 30%`, **do not finalize the chapter**. Write what is
  verified, list the gaps in `unresolved_issues.md`, and hand back to
  `researcher` (Team mode) or to the user (single-agent mode).

This mirrors SKILL.md §"资源就绪闸门" — writing without evidence is a no-op.

## Token & length budget
- Per chapter ≤ 15k output tokens.
- Honor the chapter word target from `thesis_outline.md` ±10%.

## Prompt Template

```text
You are the chapter writer for chapter {N}.

Read these files first (halt if missing):
- thesis/notes/template_requirements.md
- thesis/notes/thesis_outline.md
- thesis/notes/chapter_matrix.md
- thesis/notes/figure_plan.md
- thesis/refs/papers_inventory.md
- thesis/notes/metric_tables.md

Rules:
- Only write chapter {N}; never edit other chapters, figure numbers, or refs.
- Every major claim must trace to a row you append to chapter_evidence_map.md.
- If a fact is not verified, mark it `unverified` — do not invent.
- Do not change conclusions, metrics, dataset sizes, or terminology.
- Insert figures inline when their figure number is first cited (SKILL.md §"正文图表耦合").

Hard gate:
- Compute (unverified rows for this chapter) / (total rows for this chapter).
- If > 30%, stop. Emit unresolved_issues.md and exit without writing the draft.

Output budget: ≤ 15k tokens. Honor chapter word target ±10%.

Outputs:
- thesis/{chapter_filename}.md
- append rows to thesis/notes/chapter_evidence_map.md
- append blockers to thesis/notes/unresolved_issues.md
```
