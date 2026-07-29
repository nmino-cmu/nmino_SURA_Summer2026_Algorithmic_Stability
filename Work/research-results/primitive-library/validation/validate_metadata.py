#!/usr/bin/env python3
"""Validate operator registry and theorem package metadata. Fail closed."""

from __future__ import annotations

import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parents[1]
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from common import fail_if, validate_all_metadata  # noqa: E402


def main() -> int:
    errors = validate_all_metadata()
    if errors:
        return fail_if(errors)
    print("OK: metadata validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
