#!/usr/bin/env python
"""Regenerate tests/fixtures/guess_golden.txt after an intentional
change to the guessing rules. Review the diff before committing."""

import sys
from pathlib import Path

TESTS = Path(__file__).resolve().parent
sys.path.insert(0, str(TESTS.parent))
sys.path.insert(0, str(TESTS))

from libwavescan import WSNote          # noqa: E402
from conftest import FakeArgs, FakeEnt  # noqa: E402

ws = WSNote(FakeArgs())
paths = (TESTS / "fixtures" / "drum_paths.txt").read_text(
    encoding="utf-8").splitlines()
lines = [f"{ws.guess(FakeEnt(p), 0)}\t{p}" for p in paths]
(TESTS / "fixtures" / "guess_golden.txt").write_text(
    "\n".join(lines) + "\n", encoding="utf-8")
print(f"regenerated golden for {len(paths)} paths")
