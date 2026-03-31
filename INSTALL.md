# Installation

## Local Skill Installation

### 1. Copy into the Claude Code skills directory

Recommended path:

```bash
~/.claude/skills/thesis-workflow
```

Typical Windows path:

```text
C:\Users\<you>\.claude\skills\thesis-workflow
```

### 2. Check required files

Required:
- `SKILL.md`

Recommended supporting files:
- `README.md`
- `README_EN.md`
- `DESIGN.md`
- `docs/`
- `prompts/`
- `tools/`
- `examples/`

### 3. Invoke the skill

Typical command chain:

```text
/thesis-intake --assist
/thesis-data --auto
/thesis-outline --draft
/thesis-assets --auto
/thesis-write chapter=2 --draft
/thesis-citations --safe
/thesis-format --draft
/thesis-build
```

## Publishing to GitHub

### Option A: manual git workflow

```bash
cd "E:/Project/Final-Exam/lxy/skills/thesis-workflow"
git init
git add .
git commit -m "feat: scaffold thesis-workflow skill"
git branch -M main
git remote add origin https://github.com/<your-username>/thesis-workflow.git
git push -u origin main
```

### Option B: use GitHub CLI

```bash
cd "E:/Project/Final-Exam/lxy/skills/thesis-workflow"
git init
git add .
git commit -m "feat: scaffold thesis-workflow skill"
git branch -M main
gh repo create thesis-workflow --public --source=. --remote=origin --push
```

## Recommended First Release

After the first push:

```bash
git tag v0.1.0
git push origin v0.1.0
```

Use a GitHub Release note that states:
- this is the initial public packaging of the skill
- intake-first gating is enforced
- prompts and helper tools are starter assets, not a fully automated thesis engine

## Operational Notes

- Do not rely on a `doc/docx` template alone for exact formatting rules.
- Provide text-format rules if final Word output must match a school template exactly.
- Treat prompts and tools in this repository as reusable building blocks.
- Run citation checking and AI-risk audit before final build.
