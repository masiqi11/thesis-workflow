# PRD

## Product Name
thesis-workflow

## Positioning
A reusable, GitHub-distributable thesis-writing workflow skill for Claude Code.

## Problem Statement
AI-assisted thesis writing often fails because drafting begins before requirements are clear, citations are formatted without truth-checking, implementation claims exceed the real project, and final formatting starts too early.

## Core Value
- Block formal writing until requirements are clarified
- Bind writing to evidence sources
- Separate content audit, citation audit, format audit, and AI-risk audit
- Support long-chain collaboration with agent teams
- Provide a GitHub-friendly packaging model for reuse

## Target Users
- Students writing graduation theses
- Engineers reverse-writing papers from existing projects
- Users needing Markdown -> Word thesis delivery workflows
- Claude Code users who want a reusable public skill repository

## Key Scenarios
1. Reverse-write a thesis from code, logs, and experiment outputs
2. Build a chapter plan tied to evidence and figures
3. Verify that references actually exist
4. Audit AI-generated text for hallucinations and metric drift
5. Export an acceptance-ready docx/pdf after format gates pass

## Success Criteria
- Intake requirements are captured completely
- Formal writing does not proceed on ambiguous formatting rules
- References are truth-checked before final build
- Final deliverables can be generated and audited
- Public repository structure is understandable and reusable by others

## Non-Goals
- Fully automated extraction of all format rules from doc/docx templates
- One-click thesis generation without evidence review
- School-specific hardcoding into the core workflow
