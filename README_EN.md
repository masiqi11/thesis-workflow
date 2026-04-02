# thesis-workflow

[![Version](https://img.shields.io/badge/version-v0.2.0-blue.svg)](https://github.com/masiqi11/thesis-workflow/releases/tag/v0.2.0)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Claude Code Skill](https://img.shields.io/badge/Claude%20Code-Skill-purple.svg)](SKILL.md)

[中文](README.md) | English

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
- **Reference collection**: mandatory paper collection during data preparation, prioritizing accessible sources
- **Resource readiness gate**: blocks writing until references, data, figures, and evidence sources are ready
- **Inline figure integration**: figures are inserted while writing, not after
- **Template persistence**: format requirements saved to file, not dependent on context memory
- **Figure strategy split**: concept diagrams via prompts, experiment charts via Python scripts, screenshots via capture
- **Word budget planning**: chapter-level word count targets based on thesis type (algorithm / system / balanced)
- **AI-detection mitigation**: writing rules that avoid mechanical structuring and other AI fingerprints
- **GitHub-ready packaging**: documentation, examples, prompts, and helper tools are arranged for public distribution

## Repository Structure

```text
thesis-workflow/
├── SKILL.md
├── README.md
├── README_EN.md
├── DESIGN.md
├── INSTALL.md
├── LICENSE
├── requirements.txt
├── .gitignore
├── docs/
│   └── PRD.md
├── prompts/
│   ├── README.md
│   ├── intake_prompt.md
│   ├── writer_prompt.md
│   ├── citation_checker_prompt.md
│   └── audit_prompt.md
├── tools/
│   ├── README.md
│   ├── build_thesis.py
│   ├── collect_assets.py
│   └── verify_citations.py
└── examples/
    └── example_dunhuang.md
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
  -> /thesis-data (includes reference collection)
  -> /thesis-outline (includes word budget)
  -> /thesis-assets
  -> /thesis-write (resource readiness gate)
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

## Changelog

### v0.2.0

- Mandatory reference collection during data preparation (prioritize accessible sources, notify user on download failure)
- Resource readiness gate (blocks writing until references, data, figures, and evidence are ready)
- Inline figure integration (insert figures while writing, not after)
- Template requirement persistence (saved to file, not dependent on context memory)
- Figure generation strategy split (concept diagrams via prompts, experiment charts via Python scripts, screenshots via capture)
- Word budget planning (chapter-level targets based on thesis type: algorithm-focused / system-focused / balanced)
- AI-detection mitigation writing rules (ban mechanical structuring, symmetric numbering, AI boilerplate)
- Abstract, table of contents, acknowledgments set as default required sections
- Citation rule refinement (in-text marker format, marker placement, required bibliography fields)
- Fixed 5 recorded issues (#13-#17)

### v0.1.0

- Initial release with complete thesis workflow
