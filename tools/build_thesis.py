#!/usr/bin/env python3
"""Thin wrapper for thesis build commands.

Usage:
    python build_thesis.py --cmd "python thesis/gen_word.py"
    python build_thesis.py --cmd "make -C thesis docx" --cwd thesis --log build/build.log
"""

from __future__ import annotations

import argparse
import logging
import shlex
import subprocess
import sys
from pathlib import Path


logger = logging.getLogger("build_thesis")


def run_build(cmd: str, cwd: Path, log_path: Path, use_shell: bool) -> int:
    cwd = cwd.resolve()
    if not cwd.is_dir():
        logger.error("cwd does not exist or is not a directory: %s", cwd)
        return 64

    argv: str | list[str]
    if use_shell:
        logger.warning("running with shell=True; ensure --cmd is trusted input")
        argv = cmd
    else:
        argv = shlex.split(cmd)
        if not argv:
            logger.error("empty command after parsing: %r", cmd)
            return 64

    proc = subprocess.run(
        argv,
        cwd=str(cwd),
        shell=use_shell,
        capture_output=True,
        text=True,
    )

    sections = [
        f"command: {cmd}",
        f"cwd: {cwd}",
        f"returncode: {proc.returncode}",
        "",
        "[stdout]",
        proc.stdout,
        "",
        "[stderr]",
        proc.stderr,
    ]
    try:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        log_path.write_text("\n".join(sections), encoding="utf-8")
    except OSError as exc:
        logger.error("failed to write log %s: %s", log_path, exc)
        return 73

    logger.info("build log written to: %s", log_path)
    if proc.stdout:
        sys.stdout.write(proc.stdout)
    if proc.stderr:
        sys.stderr.write(proc.stderr)
    return proc.returncode


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cmd", required=True, help="Build command to execute")
    parser.add_argument("--cwd", default=".", help="Working directory")
    parser.add_argument("--log", default="build.log", help="Log file path")
    parser.add_argument(
        "--shell",
        action="store_true",
        help="Execute --cmd via the system shell (allows pipes/redirects, less safe)",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable debug logging",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s %(name)s: %(message)s",
    )

    return run_build(
        cmd=args.cmd,
        cwd=Path(args.cwd),
        log_path=Path(args.log),
        use_shell=args.shell,
    )


if __name__ == "__main__":
    raise SystemExit(main())
