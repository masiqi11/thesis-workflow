# Tools

This directory stores helper scripts for local thesis workflow automation.

## Included Helper Scripts

- `collect_assets.py` — scan a figures directory and emit a markdown manifest
- `verify_citations.py` — perform offline structural checks on a references markdown file
- `build_thesis.py` — wrap an existing build command or script and capture result metadata

## Design Rule

These scripts are intentionally minimal starter assets:
- safe to read and extend
- usable without heavy dependencies
- focused on repeatable local checks

They are not intended to replace project-specific build logic or school-specific formatting engines.
