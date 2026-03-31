# thesis-workflow

> A GitHub-ready Claude Code skill for thesis writing workflows: intake, evidence collection, outline planning, chapter drafting, citation verification, format auditing, AI-risk review, plagiarism-oriented rewriting, and final document build.

## Overview

`thesis-workflow` is a reusable Claude Code skill for long-form academic writing.

Its governing rule is simple:

**No formal thesis writing or final formatting before requirements are clarified.**

This repository is intended for users who need to:
- reverse-write a thesis from an existing codebase, experiment set, or graduation project
- manage a Markdown -> Word/PDF workflow with controlled checkpoints
- reduce hallucinated claims, fake references, formatting churn, and long-context drift

## Features

- **Intake-first workflow**: formal drafting is blocked until structure, formatting, citation, and delivery rules are explicit
- **Evidence-driven writing**: each major claim should be traceable to code, logs, figures, experiments, screenshots, or references
- **Citation truth checking**: references are not only formatted, but also existence-checked
- **AI-risk auditing**: detects hallucinated implementations, fabricated experiments, terminology drift, and inconsistent metrics
- **Agent team orchestration**: supports lead / researcher / writer / citation-checker / reviewer separation
- **Format gating**: prevents premature Word build before text-format rules are explicit
- **Rewrite / reduce mode**: supports plagiarism-oriented rewriting while preserving facts and anchors
- **GitHub-ready packaging**: documentation, examples, prompts, and helper tools are arranged for public distribution

## Repository Structure

```text
thesis-workflow/
├─ SKILL.md
├─ README.md
├─ README_EN.md
├─ DESIGN.md
├─ INSTALL.md
├─ LICENSE
├─ requirements.txt
├─ .gitignore
├─ docs/
│  └─ PRD.md
├─ prompts/
│  ├─ README.md
│  ├─ intake_prompt.md
│  ├─ writer_prompt.md
│  ├─ citation_checker_prompt.md
│  └─ audit_prompt.md
├─ tools/
│  ├─ README.md
│  ├─ build_thesis.py
│  ├─ collect_assets.py
│  └─ verify_citations.py
└─ examples/
   └─ example_dunhuang.md
```

## Core Commands

```text
/thesis-intake
/thesis-data
/thesis-outline
/thesis-assets
/thesis-write
/thesis-content
/thesis-citations
/thesis-format
/thesis-audit
/thesis-reduce
/thesis-build
/thesis-defense
/thesis-sync
```

## Recommended Flow

```text
/thesis-intake
  -> /thesis-data
  -> /thesis-outline
  -> /thesis-assets
  -> /thesis-write
  -> /thesis-content
  -> /thesis-citations
  -> /thesis-format
  -> /thesis-audit
  -> /thesis-reduce
  -> /thesis-build
  -> /thesis-defense
  -> /thesis-sync
```

## Run Modes

- `--assist` : analysis only, no formal output
- `--draft` : generate drafts without assuming final overwrite
- `--auto` : autonomously inspect project materials and produce notes/drafts
- `--team` : enable multi-agent collaboration
- `--team-strict` : strict split of file ownership and task boundaries
- `--safe` : conservative audit / rewrite mode
- `--aggressive` : stronger rewrite mode without changing conclusions or metrics

## What Makes This Different

Typical AI thesis workflows fail because:
- drafting starts before requirements are clear
- references are formatted but never truth-checked
- implementation claims exceed what the project really does
- final formatting begins before rules are locked

`thesis-workflow` is designed to break that failure chain with explicit gates.

## Quick Start

1. Put this repository under your Claude Code skills directory.
2. Ensure `SKILL.md` exists at the repository root.
3. Start with `/thesis-intake --assist`.
4. Do not enter `/thesis-format` or `/thesis-build` until requirements are explicit.

## Example Use Case

See [examples/example_dunhuang.md](examples/example_dunhuang.md) for a graduation-project-oriented command chain.

## Installation

See [INSTALL.md](INSTALL.md).

## Design

See [DESIGN.md](DESIGN.md).

## Product Notes

See [docs/PRD.md](docs/PRD.md).

## License

MIT
