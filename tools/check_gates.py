#!/usr/bin/env python3
"""Machine-checkable gate verifier for the thesis workflow.

Reads the gate files under <thesis-dir>/notes/ and reports whether each pipeline
gate actually passes. Gate files are the source of truth — workflow_state.md is a
log, not an authority.

Usage:
    python check_gates.py --thesis-dir thesis
    python check_gates.py --thesis-dir thesis --gate build   # only gates build needs

Exit codes:
    0 — all requested gates pass
    1 — I/O or usage error
    4 — one or more gates fail (details on stdout)

Gates checked:
    intake     missing_requirements.md has an empty "必须补充" section
    citations  unresolved_fake_risk.md absent or has no list items
    audit      ai_risk_audit.md contains no entries under the P0 heading
    reduce     no *_reduced.md leftovers in the thesis dir
    format     format_audit.md contains "Status: PASS"
"""

from __future__ import annotations

import argparse
import logging
import re
import sys
from pathlib import Path

EXIT_OK = 0
EXIT_ERROR = 1
EXIT_GATE_FAIL = 4

logger = logging.getLogger("check_gates")

GATE_NAMES = ("intake", "citations", "audit", "reduce", "format")


def _section_items(text: str, heading_pattern: str) -> list[str]:
    """Return markdown list items under the first heading matching the pattern,
    up to the next heading of the same or higher level."""
    lines = text.splitlines()
    heading_re = re.compile(heading_pattern)
    any_heading_re = re.compile(r"^#{1,6}\s")
    items: list[str] = []
    in_section = False
    for line in lines:
        if in_section:
            if any_heading_re.match(line):
                break
            stripped = line.strip()
            if stripped.startswith(("-", "*")) and len(stripped) > 1:
                items.append(stripped)
        elif heading_re.match(line):
            in_section = True
    return items


def check_intake(thesis_dir: Path) -> tuple[bool, str]:
    path = thesis_dir / "notes" / "missing_requirements.md"
    if not path.is_file():
        return False, f"missing gate file: {path}"
    items = _section_items(path.read_text(encoding="utf-8"), r"^#{1,6}\s*必须补充")
    if items:
        return False, f"{len(items)} item(s) under 必须补充 in {path.name}"
    return True, "必须补充 section is empty"


def check_citations(thesis_dir: Path) -> tuple[bool, str]:
    path = thesis_dir / "notes" / "unresolved_fake_risk.md"
    if not path.is_file():
        return True, f"{path.name} absent (no unresolved fake-risk refs)"
    text = path.read_text(encoding="utf-8")
    open_items = [
        line for line in text.splitlines() if line.strip().startswith(("-", "*"))
    ]
    if open_items:
        return False, f"{len(open_items)} unresolved fake-risk item(s) in {path.name}"
    return True, f"{path.name} present but empty"


def check_audit(thesis_dir: Path) -> tuple[bool, str]:
    path = thesis_dir / "notes" / "ai_risk_audit.md"
    if not path.is_file():
        return False, f"missing gate file: {path}"
    items = _section_items(path.read_text(encoding="utf-8"), r"^#{1,6}\s*P0\b")
    if items:
        return False, f"{len(items)} open P0 item(s) in {path.name}"
    return True, "P0 count is zero"


def check_reduce(thesis_dir: Path) -> tuple[bool, str]:
    leftovers = sorted(thesis_dir.glob("*_reduced.md"))
    if leftovers:
        names = ", ".join(p.name for p in leftovers)
        return False, f"unmerged reduce output: {names}"
    return True, "no *_reduced.md leftovers"


def check_format(thesis_dir: Path) -> tuple[bool, str]:
    path = thesis_dir / "notes" / "format_audit.md"
    if not path.is_file():
        return False, f"missing gate file: {path}"
    text = path.read_text(encoding="utf-8")
    m = re.search(r"^Status:\s*(\S+)", text, re.MULTILINE)
    if not m:
        return False, f"no 'Status:' line in {path.name}"
    status = m.group(1).upper()
    if status != "PASS":
        return False, f"format_audit status is {status}"
    return True, "format_audit status is PASS"


CHECKS = {
    "intake": check_intake,
    "citations": check_citations,
    "audit": check_audit,
    "reduce": check_reduce,
    "format": check_format,
}


def run_checks(thesis_dir: Path, gates: list[str]) -> int:
    if not thesis_dir.is_dir():
        logger.error("thesis directory not found: %s", thesis_dir)
        return EXIT_ERROR

    failed = 0
    for gate in gates:
        ok, detail = CHECKS[gate](thesis_dir)
        marker = "PASS" if ok else "FAIL"
        print(f"[{marker}] {gate:<10} {detail}")
        if not ok:
            failed += 1

    if failed:
        print(f"\n{failed}/{len(gates)} gate(s) failed — /thesis-build must not run")
        return EXIT_GATE_FAIL
    print(f"\nall {len(gates)} gate(s) passed")
    return EXIT_OK


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--thesis-dir", default="thesis", help="Thesis root directory (default: thesis)"
    )
    parser.add_argument(
        "--gate",
        action="append",
        choices=GATE_NAMES,
        default=None,
        help="Check only this gate (repeatable). Default: all gates.",
    )
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s %(name)s: %(message)s",
    )

    gates = args.gate or list(GATE_NAMES)
    return run_checks(Path(args.thesis_dir), gates)


if __name__ == "__main__":
    raise SystemExit(main())
