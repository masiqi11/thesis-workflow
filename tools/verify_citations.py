#!/usr/bin/env python3
"""Offline citation structure checker.

Verifies numbering structure (contiguous from 1) and detects duplicates in a
markdown references list. Does NOT verify references against the internet —
that responsibility belongs to /thesis-citations (citation_checker_prompt.md).

Usage:
    python verify_citations.py --input thesis/refs/references.md
    python verify_citations.py --input ... --allow-gaps   # allow non-contiguous numbering

Exit codes:
    0 — clean
    1 — generic / I/O error
    2 — duplicate numbering found
    3 — gap or out-of-order numbering (suppressed by --allow-gaps)
"""

from __future__ import annotations

import argparse
import logging
import re
import sys
from pathlib import Path

ENTRY_RE = re.compile(r"^\[(\d+)\]\s+")

EXIT_OK = 0
EXIT_ERROR = 1
EXIT_DUPLICATE = 2
EXIT_GAP = 3

logger = logging.getLogger("verify_citations")


def parse_entries(lines: list[str]) -> list[tuple[int, int]]:
    """Return list of (ref_number, line_number) for matched bibliography entries."""
    out: list[tuple[int, int]] = []
    for line_no, line in enumerate(lines, start=1):
        m = ENTRY_RE.match(line.strip())
        if m:
            out.append((int(m.group(1)), line_no))
    return out


def find_duplicates(entries: list[tuple[int, int]]) -> list[tuple[int, int, int]]:
    seen: dict[int, int] = {}
    dupes: list[tuple[int, int, int]] = []
    for num, line_no in entries:
        if num in seen:
            dupes.append((num, seen[num], line_no))
        else:
            seen[num] = line_no
    return dupes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="References markdown path")
    parser.add_argument(
        "--allow-gaps",
        action="store_true",
        help="Allow non-contiguous numbering (do not exit non-zero on gaps)",
    )
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s %(name)s: %(message)s",
    )

    path = Path(args.input)
    if not path.is_file():
        logger.error("input file not found: %s", path)
        return EXIT_ERROR

    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        logger.error("failed to read %s: %s", path, exc)
        return EXIT_ERROR

    entries = parse_entries(lines)
    if not entries:
        logger.info("no numbered references found")
        return EXIT_OK

    actual = [n for n, _ in entries]
    expected = list(range(1, len(entries) + 1))
    dupes = find_duplicates(entries)

    logger.info("entries: %d", len(entries))

    contiguous = actual == expected
    if contiguous:
        logger.info("numbering is contiguous")
    else:
        logger.warning("numbering is not contiguous")
        sys.stderr.write(f"expected: {expected}\nactual:   {actual}\n")

    if dupes:
        logger.error("duplicate numbering found:")
        for num, first_line, dup_line in dupes:
            sys.stderr.write(
                f"  [{num}] first at line {first_line}, duplicate at line {dup_line}\n"
            )
        return EXIT_DUPLICATE

    if not contiguous and not args.allow_gaps:
        return EXIT_GAP

    return EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
