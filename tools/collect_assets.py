#!/usr/bin/env python3
"""Collect figure assets into a markdown manifest.

Usage:
    python collect_assets.py --figures thesis/figures --output thesis/notes/assets_manifest.md
"""

from __future__ import annotations

import argparse
from pathlib import Path

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".bmp", ".webp", ".svg"}


def build_manifest(figures_dir: Path) -> str:
    lines = ["# Assets Manifest", "", f"Source directory: `{figures_dir}`", ""]
    files = sorted([p for p in figures_dir.iterdir() if p.is_file() and p.suffix.lower() in IMAGE_EXTS])
    if not files:
        lines.append("No image assets found.")
        return "\n".join(lines) + "\n"

    lines.extend(["| File | Stem | Suffix |", "|---|---|---|"])
    for path in files:
        lines.append(f"| `{path.name}` | `{path.stem}` | `{path.suffix}` |")
    lines.append("")
    lines.append(f"Total assets: **{len(files)}**")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--figures", required=True, help="Figures directory")
    parser.add_argument("--output", required=True, help="Markdown output path")
    args = parser.parse_args()

    figures_dir = Path(args.figures)
    output = Path(args.output)

    if not figures_dir.exists() or not figures_dir.is_dir():
        raise SystemExit(f"figures directory not found: {figures_dir}")

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(build_manifest(figures_dir), encoding="utf-8")
    print(f"wrote manifest: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
