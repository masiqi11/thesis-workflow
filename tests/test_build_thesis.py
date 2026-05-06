"""Tests for tools/build_thesis.py."""
from __future__ import annotations

from pathlib import Path

import build_thesis


def test_run_build_writes_log_and_returns_zero(tmp_path: Path) -> None:
    log_path = tmp_path / "logs" / "build.log"
    rc = build_thesis.run_build(
        cmd="python -c \"print('ok')\"",
        cwd=tmp_path,
        log_path=log_path,
        use_shell=False,
    )
    assert rc == 0
    contents = log_path.read_text(encoding="utf-8")
    assert "returncode: 0" in contents
    assert "ok" in contents


def test_run_build_propagates_nonzero_exit(tmp_path: Path) -> None:
    log_path = tmp_path / "build.log"
    rc = build_thesis.run_build(
        cmd="python -c \"import sys; sys.exit(7)\"",
        cwd=tmp_path,
        log_path=log_path,
        use_shell=False,
    )
    assert rc == 7
    assert "returncode: 7" in log_path.read_text(encoding="utf-8")


def test_run_build_rejects_missing_cwd(tmp_path: Path) -> None:
    rc = build_thesis.run_build(
        cmd="python -c 'pass'",
        cwd=tmp_path / "nope",
        log_path=tmp_path / "build.log",
        use_shell=False,
    )
    assert rc == 64


def test_run_build_rejects_empty_command(tmp_path: Path) -> None:
    rc = build_thesis.run_build(
        cmd="   ",
        cwd=tmp_path,
        log_path=tmp_path / "build.log",
        use_shell=False,
    )
    assert rc == 64


def test_run_build_shell_mode_supports_pipes(tmp_path: Path) -> None:
    log_path = tmp_path / "build.log"
    rc = build_thesis.run_build(
        cmd="echo hello | tr a-z A-Z",
        cwd=tmp_path,
        log_path=log_path,
        use_shell=True,
    )
    assert rc == 0
    assert "HELLO" in log_path.read_text(encoding="utf-8")
