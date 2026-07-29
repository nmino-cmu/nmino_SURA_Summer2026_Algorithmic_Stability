#!/usr/bin/env python3
"""Fail if Research/ contains sorry/admit/axiom/constant/unsafe/partial."""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_ROOT / "implementation" / "src"))

from system_b.lean.placeholders import FORBIDDEN_IN_RESEARCH, scan_paths  # noqa: E402


def main() -> int:
    research = Path(__file__).resolve().parents[1] / "Research"
    findings = scan_paths([research])
    bad = [f for f in findings if f.kind in FORBIDDEN_IN_RESEARCH]
    if bad:
        for f in bad:
            print(f"{f.path}:{f.line}: {f.kind}: {f.text}")
        return 1
    print("OK: no forbidden placeholders in Research/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
