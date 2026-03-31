#!/usr/bin/env python3
"""Offline citation structure checker.

This script does not verify references on the internet.
It checks numbering structure and duplicate numbering in a markdown references list.

Usage:
    python verify_citations.py --input thesis/refs/references.md
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

ENTRY_RE = re.compile(r"^\[(\d+)\]\s+")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="References markdown path")
    args = parser.parse_args()

    path = Path(args.input)
    if not path.exists():
        raise SystemExit(f"input file not found: {path}")

    lines = path.read_text(encoding="utf-8").splitlines()
    numbers = []
    for idx, line in enumerate(lines, start=1):
        m = ENTRY_RE.match(line.strip())
        if m:
            numbers.append((int(m.group(1)), idx))

    if not numbers:
        print("no numbered references found")
        return 0

    seen = {}
    dupes = []
    for num, line_no in numbers:
        if num in seen:
            dupes.append((num, seen[num], line_no))
        else:
            seen[num] = line_no

    expected = list(range(1, len(numbers) + 1))
    actual = [n for n, _ in numbers]

    print(f"entries: {len(numbers)}")
    if actual != expected:
        print("numbering is not contiguous")
        print(f"expected: {expected}")
        print(f"actual:   {actual}")
    else:
        print("numbering is contiguous")

    if dupes:
        print("duplicate numbering found:")
        for num, first_line, dup_line in dupes:
            print(f"  [{num}] first at line {first_line}, duplicate at line {dup_line}")
        return 1

    return 0 if actual == expected else 1


if __name__ == "__main__":
    raise SystemExit(main())
