# Thesis Assets Prompt

Use this prompt for figure/table/screenshot asset management.

## Objective
Normalize all figure assets, enforce the figure-generation strategy split, and
record data provenance for every experiment-data figure.

## Stage in pipeline
Runs at `/thesis-assets` (stage 4), after `/thesis-outline` produced `figure_plan.md`.

## Inputs (mandatory)

| Path | Provider |
|---|---|
| `thesis/notes/figure_plan.md` | `/thesis-outline` — planned figures with source_type |
| `thesis/notes/metric_tables.md` | `/thesis-data` — data for experiment figures |
| raw images / screenshots / data files | user's project |

## Generation strategy (hard split — never mix)

| Figure class | How it is produced | Output |
|---|---|---|
| 概念图 (architecture, flow, module diagrams) | write a drawing **prompt**, never claim an image was generated | `thesis/figures/prompts/<name>_prompt.md` |
| 实验数据图 (curves, bars, confusion matrix, ROC) | **Python script** reading real data from `metric_tables.md` / results files | `thesis/figures/<name>.png` + `thesis/figures/scripts/<name>.py` |
| 截图 (system UI, run results) | actual capture via browser/system screenshot | `thesis/figures/<name>.png` |

Scripts must be re-runnable so figures regenerate when data updates.

## Outputs

| File | Content |
|---|---|
| `thesis/figures/*` | normalized assets |
| `thesis/figures/scripts/*.py` | generation scripts for experiment figures |
| `thesis/notes/assets_manifest.md` | manifest with provenance (schema below) |

### `assets_manifest.md` schema

```md
| fig_id | file | chapter | source_type | data_provenance | readability_check |
|---|---|---|---|---|---|
| fig4-1 | figures/loss_curve.png | 4 | python_script | scripts/loss_curve.py ← notes/metric_tables.md tab.2 | pass |
| fig3-1 | figures/sys_arch.png | 3 | prompt | figures/prompts/sys_arch_prompt.md (drawn externally) | pass |
| fig3-2 | figures/ui_main.png | 3 | screenshot | captured 2026-05-03 from localhost:8501 | pass |
```

`data_provenance` is mandatory for every row. An experiment figure whose script or
data source cannot be named MUST NOT enter the manifest — it would be an
unfalsifiable visual (audit dimension 8 treats it as P0).

## Hard rules

1. Per-chapter figure number ranges; numbering changes propagate to body + map + caption together.
2. Back up before overwriting an existing figure file.
3. Every figure passes a 答辩可读性 (defense readability) check: legible at projector
   scale, axes labeled, units present.
4. `tools/collect_assets.py` can bootstrap the file listing; this prompt adds the
   provenance and readability columns on top.

## Token budget
≤ 8k output tokens.

## Prompt Template

```text
You are running the thesis assets phase.

Read first:
- thesis/notes/figure_plan.md
- thesis/notes/metric_tables.md

For each planned figure, follow its source_type strictly:
- prompt        → write figures/prompts/<name>_prompt.md; never claim an image exists
- python_script → write figures/scripts/<name>.py reading REAL data; run it; save png
- screenshot    → capture via browser tools; save png

Then build thesis/notes/assets_manifest.md with data_provenance and
readability_check columns filled for every row.

Hard rule: no experiment figure without a script + named data source.

Append to thesis/notes/workflow_state.md:
| assets | done | provenance_ok=<yes/no> | <date> | <note> |
```
