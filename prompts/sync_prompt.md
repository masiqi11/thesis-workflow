# Thesis Sync Prompt

Use this prompt for final synchronization and archival.

## Objective
Ensure body text, figures, references, release artifacts, and notes are mutually
consistent, then produce an archive index and close out the workflow state.

## Stage in pipeline
Runs at `/thesis-sync` (stage 13), the terminal stage. Also usable mid-project
after any batch of changes to re-align artifacts.

## Inputs

| Path | Provider |
|---|---|
| `thesis/` (entire tree) | all prior stages |
| `thesis/notes/workflow_state.md` | all prior stages |

## Consistency checks (report, then fix with user confirmation)

1. **正文 ↔ 图表**：every `图 N-M` referenced in body exists in `assets_manifest.md` and on disk; no orphaned figure files.
2. **正文 ↔ 文献**：in-text `[N]` set == `references_checked.md` entry set.
3. **正文 ↔ 终稿**：release docx was built from the CURRENT chapter files (compare `build_manifest.md` timestamp vs chapter mtimes; stale → flag rebuild).
4. **notes ↔ 现实**：`workflow_state.md` rows match actual gate files (e.g. state says `p0=0` but `ai_risk_audit.md` lists P0 → state is wrong, gate file wins, flag it).
5. **残留文件**：no `_reduced.md`, no `*.tmp`, no orphaned figure prompts.

## Outputs

| File | Content |
|---|---|
| `thesis/notes/sync_report.md` | check results + fixes applied |
| `thesis/release/ARCHIVE_INDEX.md` | final artifact inventory (schema below) |
| `thesis/notes/workflow_state.md` | terminal row appended |

### `ARCHIVE_INDEX.md` schema

```md
# Archive Index — <thesis title>

| artifact | path | version/date | sha or size |
|---|---|---|---|
| 终稿 docx | release/毕业论文_张三.docx | 2026-05-07 | 2.1 MB |
| 终稿 pdf | release/毕业论文_张三.pdf | 2026-05-07 | 3.4 MB |
| 章节源文件 | thesis/chapter_*.md | 2026-05-07 | 5 files |
| 证据映射 | notes/chapter_evidence_map.md | 2026-05-07 | 142 rows |
| 文献清单 | refs/references_checked.md | 2026-05-06 | 28 entries |
| 答辩材料 | notes/{defense_outline,innovation_points,qa_bank}.md | 2026-05-07 | 3 files |
```

## Token budget
≤ 8k output tokens.

## Prompt Template

```text
You are running the thesis sync/archival phase.

Run the 5 consistency checks from this prompt over the thesis/ tree.
For each mismatch: report it in sync_report.md; apply the fix only after user
confirmation (stale build → recommend /thesis-build rerun, don't silently rebuild).

Then write thesis/release/ARCHIVE_INDEX.md and append the terminal row:
| sync | done | consistent=<yes/no> | <date> | archive_ready |
```
