# Release Notes — v0.1.0

## Title
Initial public release of `thesis-workflow`

## Summary
- Package `thesis-workflow` as a GitHub-ready Claude Code skill repository
- Enforce intake-first gating before formal thesis drafting or final formatting
- Add reusable prompt assets for intake, chapter writing, citation checking, and AI-risk audit
- Add minimal helper tools for asset collection, offline citation structure checks, and thesis build wrapping
- Include installation guide, design notes, PRD, and a graduation-project example workflow

## Highlights

### 1. Intake-first workflow
Formal writing is blocked until structure, formatting, citation, and delivery rules are explicit.

### 2. Evidence-driven writing
The skill is designed to tie major claims back to code, logs, figures, experiments, screenshots, or references.

### 3. Citation truth checking
References are treated as verification targets, not just formatting targets.

### 4. AI-risk auditing
The workflow explicitly checks hallucinated implementations, fabricated experiments, metric drift, and terminology drift.

### 5. GitHub-ready packaging
The repository includes:
- `SKILL.md`
- `README.md` / `README_EN.md`
- `DESIGN.md`
- `INSTALL.md`
- `docs/PRD.md`
- `prompts/`
- `tools/`
- `examples/`

## Notes
- This release is a reusable workflow scaffold, not a one-click thesis generator.
- Final Word formatting still depends on explicit text-format rules from the user or institution.
- The helper tools are starter assets meant to be extended per project.

## Suggested GitHub Release Body

```md
## Summary
- Package `thesis-workflow` as a GitHub-ready Claude Code skill repository
- Enforce intake-first gating before formal thesis drafting or final formatting
- Add reusable prompt assets and helper tools for real-world thesis workflows

## Highlights
- Intake-first workflow
- Evidence-driven writing
- Citation truth checking
- AI-risk auditing
- GitHub-ready packaging

## Notes
- This is a workflow scaffold, not a one-click thesis generator.
- Final formatting still depends on explicit text-format rules.
- Helper tools are starter assets and can be extended per project.
```
