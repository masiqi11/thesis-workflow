# Thesis Build Prompt

Use this prompt for final document generation and release.

## Objective
Produce the official docx/pdf deliverables — only after independently re-verifying
every upstream gate. Build trusts files, not claims.

## Stage in pipeline
Runs at `/thesis-build` (stage 11), after `/thesis-format` reports PASS.
Build is the SOLE producer of docx/pdf artifacts (format only checks).

## Pre-flight gate re-check (mandatory, in this order)

Run `python tools/check_gates.py --thesis-dir thesis` or verify manually:

| # | Gate | Source of truth | Pass condition |
|---|---|---|---|
| 1 | intake | `thesis/notes/missing_requirements.md` | "必须补充" section empty |
| 2 | citations | `thesis/notes/unresolved_fake_risk.md` | file absent or no open items |
| 3 | audit | `thesis/notes/ai_risk_audit.md` | zero P0 entries |
| 4 | reduce | `thesis/*_reduced.md` | no leftover `_reduced.md` files |
| 5 | format | `thesis/notes/format_audit.md` | `Status: PASS` |

ANY failure → halt, report which gate failed and what fixes it. Do not build.

## Inputs

| Path | Provider |
|---|---|
| `thesis/*.md` | canonical chapters |
| `thesis/figures/` + `assets_manifest.md` | `/thesis-assets` |
| `thesis/refs/references_checked.md` | `/thesis-citations` — the verified bibliography |
| `thesis/notes/template_requirements.md` | `/thesis-intake` — naming & deliverable list |
| user's build script (e.g. `gen_word.py`) | user's project — wrap via `tools/build_thesis.py` |

## Outputs

Into `thesis/release/` (naming per `template_requirements.md` 交付要求; defaults):

- `毕业论文_<姓名>.docx` — official
- `毕业论文_<姓名>_验收版.docx` — acceptance copy
- `毕业论文_<姓名>.pdf`
- optional: 查重稿 / 盲审稿 variants
- `thesis/release/build_manifest.md` — what was built, from which chapter versions, when

### `build_manifest.md` schema

```md
| artifact | built_from | gate_check | result |
|---|---|---|---|
| 毕业论文_张三.docx | chapters @ <git-hash or timestamp> | 5/5 PASS | ok |
```

## Post-build verification

1. Open the docx — must not error.
2. Table of contents entries match actual headings and page numbers.
3. Every figure in `assets_manifest.md` appears; no broken image placeholders.
4. Bibliography count in docx == entry count in `references_checked.md`.

## Failure handling

- `PermissionError` → ask user to close Word; or emit `_验收版.docx` under a new name.
- ToC/style anomalies → go back to `/thesis-format`; NEVER hand-edit the final docx.

## Prompt Template

```text
You are running the thesis build phase.

Step 0 (gate re-check): run `python tools/check_gates.py --thesis-dir thesis`.
If exit code != 0, STOP. Report the failing gate and the file that must be fixed.

Step 1: read template_requirements.md 交付要求 for naming and required variants.
Step 2: run the user's generation script via tools/build_thesis.py (captures log).
Step 3: post-build verification (opens, ToC, figures, bibliography count).
Step 4: write thesis/release/build_manifest.md.

Never hand-edit the generated docx. On style problems, return to /thesis-format.

Append to thesis/notes/workflow_state.md:
| build | done | release_ok=<yes/no> | <date> | <artifacts> |
```
