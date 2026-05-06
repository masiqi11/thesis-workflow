"""Tests for tools/verify_citations.py."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import verify_citations

SCRIPT = Path(__file__).resolve().parent.parent / "tools" / "verify_citations.py"


def _run(path: Path, *extra: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--input", str(path), *extra],
        capture_output=True,
        text=True,
    )


def test_parse_entries_skips_non_reference_lines() -> None:
    lines = [
        "## References",
        "[1] Foo et al., 2020",
        "some narrative",
        "[2] Bar, 2021",
    ]
    assert verify_citations.parse_entries(lines) == [(1, 2), (2, 4)]


def test_find_duplicates_reports_pairs() -> None:
    dupes = verify_citations.find_duplicates([(1, 1), (2, 2), (1, 5)])
    assert dupes == [(1, 1, 5)]


def test_cli_clean_input_returns_ok(tmp_path: Path) -> None:
    refs = tmp_path / "refs.md"
    refs.write_text("[1] A\n[2] B\n[3] C\n", encoding="utf-8")
    proc = _run(refs)
    assert proc.returncode == verify_citations.EXIT_OK


def test_cli_duplicate_returns_exit_2(tmp_path: Path) -> None:
    refs = tmp_path / "refs.md"
    refs.write_text("[1] A\n[2] B\n[2] dup\n", encoding="utf-8")
    proc = _run(refs)
    assert proc.returncode == verify_citations.EXIT_DUPLICATE
    assert "duplicate" in proc.stderr.lower() or "duplicate" in proc.stdout.lower() \
        or "[2]" in proc.stderr


def test_cli_gap_returns_exit_3(tmp_path: Path) -> None:
    refs = tmp_path / "refs.md"
    refs.write_text("[1] A\n[3] C\n", encoding="utf-8")
    proc = _run(refs)
    assert proc.returncode == verify_citations.EXIT_GAP


def test_cli_allow_gaps_silences_gap_exit(tmp_path: Path) -> None:
    refs = tmp_path / "refs.md"
    refs.write_text("[1] A\n[3] C\n", encoding="utf-8")
    proc = _run(refs, "--allow-gaps")
    assert proc.returncode == verify_citations.EXIT_OK


def test_cli_missing_input_returns_error(tmp_path: Path) -> None:
    proc = _run(tmp_path / "does_not_exist.md")
    assert proc.returncode == verify_citations.EXIT_ERROR
