"""Tests for tools/collect_assets.py."""
from __future__ import annotations

from pathlib import Path

import collect_assets


def test_build_manifest_lists_known_image_files(tmp_path: Path) -> None:
    (tmp_path / "fig1.png").write_bytes(b"")
    (tmp_path / "fig2.JPG").write_bytes(b"")
    (tmp_path / "notes.txt").write_text("ignore me", encoding="utf-8")

    manifest = collect_assets.build_manifest(
        tmp_path, frozenset(collect_assets.DEFAULT_IMAGE_EXTS)
    )

    assert "fig1.png" in manifest
    assert "fig2.JPG" in manifest
    assert "notes.txt" not in manifest
    assert "Total assets: **2**" in manifest


def test_build_manifest_empty_dir_emits_no_assets_message(tmp_path: Path) -> None:
    manifest = collect_assets.build_manifest(
        tmp_path, frozenset(collect_assets.DEFAULT_IMAGE_EXTS)
    )
    assert "No image assets found." in manifest


def test_build_manifest_honors_custom_extensions(tmp_path: Path) -> None:
    (tmp_path / "diagram.pdf").write_bytes(b"")
    (tmp_path / "ignored.png").write_bytes(b"")

    manifest = collect_assets.build_manifest(tmp_path, frozenset({".pdf"}))

    assert "diagram.pdf" in manifest
    assert "ignored.png" not in manifest
