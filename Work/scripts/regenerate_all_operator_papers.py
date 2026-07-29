#!/usr/bin/env python3
"""Regenerate all LEAN_FULL operator papers from family sections."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    subprocess.check_call([sys.executable, str(ROOT / "scripts/build_family_sections.py")])
    ok = fail = 0
    for sections in sorted((ROOT / "research-results").glob("*/*/sections.v1.json")):
        if "_archive" in sections.parts:
            continue
        oid = sections.parent.parent.name
        thm = sections.parent.name
        r = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/generate_operator_paper.py"),
                oid,
                thm,
                "--sections",
                str(sections),
            ],
            cwd=ROOT,
        )
        if r.returncode == 0:
            ok += 1
            print(f"OK {oid}/{thm}")
        else:
            fail += 1
            print(f"FAIL {oid}/{thm}", file=sys.stderr)
    print(f"done ok={ok} fail={fail}")
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
