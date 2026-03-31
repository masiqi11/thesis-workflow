#!/usr/bin/env python3
"""Thin wrapper for thesis build commands.

Usage:
    python build_thesis.py --cmd "python thesis/gen_word.py"
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cmd", required=True, help="Build command to execute")
    parser.add_argument("--cwd", default=".", help="Working directory")
    parser.add_argument("--log", default="build.log", help="Log file path")
    args = parser.parse_args()

    cwd = Path(args.cwd)
    log_path = Path(args.log)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    proc = subprocess.run(
        args.cmd,
        cwd=str(cwd),
        shell=True,
        capture_output=True,
        text=True,
    )

    combined = []
    combined.append(f"command: {args.cmd}")
    combined.append(f"cwd: {cwd.resolve()}")
    combined.append(f"returncode: {proc.returncode}")
    combined.append("")
    combined.append("[stdout]")
    combined.append(proc.stdout)
    combined.append("")
    combined.append("[stderr]")
    combined.append(proc.stderr)
    log_path.write_text("\n".join(combined), encoding="utf-8")

    print(f"build log written to: {log_path}")
    if proc.stdout:
        print(proc.stdout)
    if proc.stderr:
        print(proc.stderr, file=sys.stderr)
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
