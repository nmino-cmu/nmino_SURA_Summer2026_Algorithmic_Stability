#!/usr/bin/env python3
"""Self-check for operator paper layout helpers."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from lib.operator_paper import REQUIRED_SECTIONS, check_sections, pdf_name  # noqa: E402


def main() -> int:
    assert pdf_name("multi-threshold") == "multi_threshold_paper.pdf"
    assert pdf_name("median") == "median_paper.pdf"
    stub = "\n".join(f"\\section{{{t}}}\nx" for t in REQUIRED_SECTIONS)
    stub = "This theorem is: \\texttt{Reduction}.\n" + stub
    assert check_sections(stub) == []
    assert "missing_section:Proof" in check_sections("\\section{Problem}\n")
    print("OK: operator_paper self-check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
