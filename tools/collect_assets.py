#!/usr/bin/env python3
"""Collect figure assets into a markdown manifest.

Usage:
    python collect_assets.py --figures thesis/figures --output thesis/notes/assets_manifest.md
    python collect_assets.py --figures thesis/figures --output ... --ext .png --ext .pdf
"""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

DEFAULT_IMAGE_EXTS = (".png", ".jpg", ".jpeg", ".bmp", ".webp", ".svg")

logger = logging.getLogger("collect_assets")


def build_manifest(figures_dir: Path, exts: frozenset[str]) -> str:
    lines = ["# Assets Manifest", "", f"Source directory: `{figures_dir}`", ""]
    files = sorted(
        p
        for p in figures_dir.iterdir()
        if p.is_file() and p.suffix.lower() in exts
    )
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
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--figures", required=True, help="Figures directory")
    parser.add_argument("--output", required=True, help="Markdown output path")
    parser.add_argument(
        "--ext",
        action="append",
        default=None,
        help="File extension to include (repeatable). Defaults: "
        + ", ".join(DEFAULT_IMAGE_EXTS),
    )
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s %(name)s: %(message)s",
    )

    figures_dir = Path(args.figures)
    output = Path(args.output)
    exts = frozenset(
        e.lower() if e.startswith(".") else f".{e.lower()}"
        for e in (args.ext or DEFAULT_IMAGE_EXTS)
    )

    if not figures_dir.is_dir():
        logger.error("figures directory not found: %s", figures_dir)
        return 66

    try:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(build_manifest(figures_dir, exts), encoding="utf-8")
    except OSError as exc:
        logger.error("failed to write manifest %s: %s", output, exc)
        return 73

    logger.info("wrote manifest: %s", output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
