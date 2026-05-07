# Prompts

This directory stores reusable prompt fragments for the skill.

## Included Prompt Assets

| File | Sub-skill | Stage |
|---|---|---|
| `intake_prompt.md` | `/thesis-intake` | 1 — collect requirements |
| `outline_prompt.md` | `/thesis-outline` | 3 — chapter structure, word budget, thesis type |
| `writer_prompt.md` | `/thesis-write` | 5 — chapter draft from evidence |
| `citation_checker_prompt.md` | `/thesis-citations` | 7 — reference truth verification |
| `audit_prompt.md` | `/thesis-audit` | 9 — AI-risk and evidence review |
| `format_prompt.md` | `/thesis-format` | 8 — format compliance gate |
| `reduce_prompt.md` | `/thesis-reduce` | 10 — plagiarism-reduction rewriting |

All prompts list mandatory input/output file paths and define output schemas.
For the full I/O contracts (inputs, outputs, passing gates), see
[docs/TEMPLATES.md](../docs/TEMPLATES.md).

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
