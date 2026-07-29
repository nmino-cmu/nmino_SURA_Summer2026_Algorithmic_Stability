#!/usr/bin/env python3
"""Generate research-results/primitive-library/index.json (never hand-edit)."""

from __future__ import annotations

import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from common import build_index, fail_if, library_dir, validate_all_metadata, write_canonical  # noqa: E402


def main() -> int:
    errors = validate_all_metadata()
    if errors:
        return fail_if(errors)
    index = build_index()
    out = library_dir() / "index.json"
    write_canonical(out, index)
    print(f"Wrote {out.relative_to(library_dir().parents[1])}")
    print(
        f"operators={index['counts']['operators']} "
        f"theorems={index['counts']['theorems']} "
        f"complete={index['counts']['complete_operators']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
