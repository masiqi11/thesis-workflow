"""Tests for tools/check_gates.py."""
from __future__ import annotations

from pathlib import Path

import check_gates


def _mk_thesis(tmp_path: Path) -> Path:
    thesis = tmp_path / "thesis"
    (thesis / "notes").mkdir(parents=True)
    return thesis


def _all_pass_fixture(thesis: Path) -> None:
    notes = thesis / "notes"
    (notes / "missing_requirements.md").write_text(
        "## 必须补充\n\n## 建议补充\n- 各章目标字数\n", encoding="utf-8"
    )
    (notes / "ai_risk_audit.md").write_text(
        "# AI Risk Audit\n\n## P0 — must-fix\n\n## P1 — should-fix\n- 术语漂移\n",
        encoding="utf-8",
    )
    (notes / "format_audit.md").write_text(
        "# Format Audit\n\nStatus: PASS\n", encoding="utf-8"
    )
    # no unresolved_fake_risk.md, no *_reduced.md → citations/reduce pass


class TestIntakeGate:
    def test_empty_must_fill_passes(self, tmp_path: Path) -> None:
        thesis = _mk_thesis(tmp_path)
        _all_pass_fixture(thesis)
        ok, _ = check_gates.check_intake(thesis)
        assert ok

    def test_items_under_must_fill_fail(self, tmp_path: Path) -> None:
        thesis = _mk_thesis(tmp_path)
        (thesis / "notes" / "missing_requirements.md").write_text(
            "## 必须补充\n- 标题编号规则\n- 页边距\n## 建议补充\n", encoding="utf-8"
        )
        ok, detail = check_gates.check_intake(thesis)
        assert not ok
        assert "2" in detail

    def test_missing_file_fails(self, tmp_path: Path) -> None:
        thesis = _mk_thesis(tmp_path)
        ok, _ = check_gates.check_intake(thesis)
        assert not ok


class TestCitationsGate:
    def test_absent_file_passes(self, tmp_path: Path) -> None:
        thesis = _mk_thesis(tmp_path)
        ok, _ = check_gates.check_citations(thesis)
        assert ok

    def test_open_items_fail(self, tmp_path: Path) -> None:
        thesis = _mk_thesis(tmp_path)
        (thesis / "notes" / "unresolved_fake_risk.md").write_text(
            "## Refs requiring user decision\n- [7] Title X\n", encoding="utf-8"
        )
        ok, _ = check_gates.check_citations(thesis)
        assert not ok

    def test_empty_file_passes(self, tmp_path: Path) -> None:
        thesis = _mk_thesis(tmp_path)
        (thesis / "notes" / "unresolved_fake_risk.md").write_text(
            "## Refs requiring user decision\n\n(none)\n", encoding="utf-8"
        )
        ok, _ = check_gates.check_citations(thesis)
        assert ok


class TestAuditGate:
    def test_empty_p0_passes(self, tmp_path: Path) -> None:
        thesis = _mk_thesis(tmp_path)
        _all_pass_fixture(thesis)
        ok, _ = check_gates.check_audit(thesis)
        assert ok

    def test_open_p0_fails(self, tmp_path: Path) -> None:
        thesis = _mk_thesis(tmp_path)
        (thesis / "notes" / "ai_risk_audit.md").write_text(
            "## P0 — must-fix\n- 第 4 章 mIoU 无证据\n## P1\n", encoding="utf-8"
        )
        ok, detail = check_gates.check_audit(thesis)
        assert not ok
        assert "P0" in detail

    def test_p1_items_do_not_fail_gate(self, tmp_path: Path) -> None:
        thesis = _mk_thesis(tmp_path)
        (thesis / "notes" / "ai_risk_audit.md").write_text(
            "## P0 — must-fix\n\n## P1 — should-fix\n- 图 3-2 解释含糊\n",
            encoding="utf-8",
        )
        ok, _ = check_gates.check_audit(thesis)
        assert ok


class TestReduceGate:
    def test_no_leftovers_passes(self, tmp_path: Path) -> None:
        thesis = _mk_thesis(tmp_path)
        (thesis / "chapter_2.md").write_text("正文", encoding="utf-8")
        ok, _ = check_gates.check_reduce(thesis)
        assert ok

    def test_leftover_reduced_file_fails(self, tmp_path: Path) -> None:
        thesis = _mk_thesis(tmp_path)
        (thesis / "chapter_2_reduced.md").write_text("改写稿", encoding="utf-8")
        ok, detail = check_gates.check_reduce(thesis)
        assert not ok
        assert "chapter_2_reduced.md" in detail


class TestFormatGate:
    def test_pass_status(self, tmp_path: Path) -> None:
        thesis = _mk_thesis(tmp_path)
        _all_pass_fixture(thesis)
        ok, _ = check_gates.check_format(thesis)
        assert ok

    def test_fail_status(self, tmp_path: Path) -> None:
        thesis = _mk_thesis(tmp_path)
        (thesis / "notes" / "format_audit.md").write_text(
            "Status: FAIL\n", encoding="utf-8"
        )
        ok, detail = check_gates.check_format(thesis)
        assert not ok
        assert "FAIL" in detail

    def test_blocked_status(self, tmp_path: Path) -> None:
        thesis = _mk_thesis(tmp_path)
        (thesis / "notes" / "format_audit.md").write_text(
            "Status: BLOCKED\n", encoding="utf-8"
        )
        ok, _ = check_gates.check_format(thesis)
        assert not ok

    def test_missing_status_line(self, tmp_path: Path) -> None:
        thesis = _mk_thesis(tmp_path)
        (thesis / "notes" / "format_audit.md").write_text("# 空报告\n", encoding="utf-8")
        ok, _ = check_gates.check_format(thesis)
        assert not ok


class TestRunChecks:
    def test_all_pass_returns_ok(self, tmp_path: Path, capsys) -> None:
        thesis = _mk_thesis(tmp_path)
        _all_pass_fixture(thesis)
        rc = check_gates.run_checks(thesis, list(check_gates.GATE_NAMES))
        assert rc == check_gates.EXIT_OK
        assert "all 5 gate(s) passed" in capsys.readouterr().out

    def test_any_fail_returns_gate_fail(self, tmp_path: Path, capsys) -> None:
        thesis = _mk_thesis(tmp_path)
        _all_pass_fixture(thesis)
        (thesis / "chapter_3_reduced.md").write_text("残留", encoding="utf-8")
        rc = check_gates.run_checks(thesis, list(check_gates.GATE_NAMES))
        assert rc == check_gates.EXIT_GATE_FAIL
        assert "must not run" in capsys.readouterr().out

    def test_missing_thesis_dir_errors(self, tmp_path: Path) -> None:
        rc = check_gates.run_checks(tmp_path / "nope", ["intake"])
        assert rc == check_gates.EXIT_ERROR

    def test_gate_subset(self, tmp_path: Path) -> None:
        thesis = _mk_thesis(tmp_path)
        # only reduce gate requested; intake file missing but irrelevant
        rc = check_gates.run_checks(thesis, ["reduce"])
        assert rc == check_gates.EXIT_OK
