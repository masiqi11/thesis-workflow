# Tools

This directory stores helper scripts for local thesis workflow automation.

## Included Helper Scripts

- `collect_assets.py` — scan a figures directory and emit a markdown manifest
- `verify_citations.py` — perform offline structural checks on a references markdown file
- `build_thesis.py` — wrap an existing build command or script and capture result metadata
- `check_gates.py` — verify all pipeline gates from their gate files (the machine-checkable
  precondition for `/thesis-build`)

All four are stdlib-only (no third-party runtime deps). Tests live in `../tests/`
and require `pytest>=7.0`.

## Usage

```bash
# Scan thesis/figures/, accept .png/.jpg/.jpeg/.bmp/.webp/.svg by default
python tools/collect_assets.py --figures thesis/figures \
    --output thesis/notes/assets_manifest.md
# Add custom extensions:
python tools/collect_assets.py --figures thesis/figures \
    --output thesis/notes/assets_manifest.md --ext .pdf --ext .tif

# Offline structural check (does NOT verify references on the internet —
# that is /thesis-citations' job).
python tools/verify_citations.py --input thesis/refs/references.md
# Allow non-contiguous numbering:
python tools/verify_citations.py --input thesis/refs/references.md --allow-gaps

# Run a build command and capture stdout/stderr/returncode
python tools/build_thesis.py --cmd "python thesis/gen_word.py" --log build/build.log
# Use shell features (pipes/redirects) — only with trusted commands:
python tools/build_thesis.py --cmd "echo done | tee build.log" --shell

# Verify all pipeline gates (intake / citations / audit / reduce / format)
python tools/check_gates.py --thesis-dir thesis
# Check a single gate:
python tools/check_gates.py --thesis-dir thesis --gate format
```

## Exit codes

`verify_citations.py`:

| Code | Meaning |
|---|---|
| 0 | Clean (or non-contiguous + `--allow-gaps`) |
| 1 | I/O or generic error |
| 2 | Duplicate numbering found |
| 3 | Numbering gap or out-of-order |

`check_gates.py`:

| Code | Meaning |
|---|---|
| 0 | All requested gates pass |
| 1 | I/O or usage error |
| 4 | One or more gates fail (per-gate detail on stdout) |

Useful in CI and as the `/thesis-build` pre-flight: distinct codes mean no
stdout parsing is needed.

## Encoding

All scripts read and write UTF-8. If your environment defaults to a different
codec, set `PYTHONUTF8=1` before invoking.

## Tests

```bash
pip install pytest
python -m pytest tests/ -v
```

## Design Rule

These scripts are intentionally minimal starter assets:
- safe to read and extend
- usable without heavy dependencies
- focused on repeatable local checks

They are not intended to replace project-specific build logic or school-specific
formatting engines.
