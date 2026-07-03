# Prompts

This directory stores reusable prompt fragments for the skill.

## Included Prompt Assets (13/13 sub-skills covered)

| File | Sub-skill | Stage |
|---|---|---|
| `intake_prompt.md` | `/thesis-intake` | 1 — topic analysis + requirement collection |
| `data_prompt.md` | `/thesis-data` | 2 — evidence & reference collection |
| `outline_prompt.md` | `/thesis-outline` | 3 — chapter structure, word budget, thesis type |
| `assets_prompt.md` | `/thesis-assets` | 4 — figure assets with data provenance |
| `writer_prompt.md` | `/thesis-write` | 5 — chapter draft from evidence |
| `content_prompt.md` | `/thesis-content` | 6 — internal consistency vs code reality |
| `citation_checker_prompt.md` | `/thesis-citations` | 7 — reference truth verification |
| `audit_prompt.md` | `/thesis-audit` | 8 — AI-risk and evidence review |
| `reduce_prompt.md` | `/thesis-reduce` | 9 — plagiarism reduction (anchor-protected) |
| `format_prompt.md` | `/thesis-format` | 10 — format compliance gate (last text gate) |
| `build_prompt.md` | `/thesis-build` | 11 — gate re-check + docx/pdf generation |
| `defense_prompt.md` | `/thesis-defense` | 12 — defense materials from verified claims |
| `sync_prompt.md` | `/thesis-sync` | 13 — consistency sync + archival |

**Ordering rule**: audit (8) before reduce (9) before format (10) — reduce consumes
audit's P2 flags; format must check post-reduce text.

All prompts list mandatory input/output file paths and define output schemas.
For the full I/O contracts (inputs, outputs, passing gates), see
[docs/TEMPLATES.md](../docs/TEMPLATES.md). For the end-to-end journey from topic
input to final build, see [docs/WORKFLOW.md](../docs/WORKFLOW.md).

## Usage Principle

These prompts are **building blocks**, not rigid scripts.

Use them when:
- the current task matches the phase exactly
- you need repeatable output structure
- you want to reduce prompt drift across chapters or teammates

Do not use them blindly when the repository, school rules, or evidence model require custom constraints.

## Relationship to SKILL.md

`SKILL.md` defines the execution rules and gating logic.
These prompt files provide the reusable template text.
When using Agent Team mode, give each agent the relevant prompt as a starting frame,
then adjust with project-specific constraints.
