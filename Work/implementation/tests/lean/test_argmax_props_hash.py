"""STATEMENT marker stability."""

from pathlib import Path

from system_b.lean.ir import extract_statement_region, statement_region_digest


def test_markers_stable():
    lean_root = Path(__file__).resolve().parents[3] / "lean"
    src = (lean_root / "Research/Operators/Argmax/Margin.lean").read_text(encoding="utf-8")
    region = extract_statement_region(src)
    assert "MarginInvarianceProp" in region
    assert "MarginSharpnessProp" in region
    d1 = statement_region_digest(src)
    d2 = statement_region_digest(src)
    assert d1 == d2
