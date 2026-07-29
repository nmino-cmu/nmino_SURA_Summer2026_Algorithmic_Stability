from __future__ import annotations
from pathlib import Path
from typing import Any
from operators.heap_extract_max.math import EVALUATION_METHOD, OPERATOR, THEOREM_ID, THEOREM_STATEMENT as _TS
CONCL_SCHEMA = "ARTLEAN.CONCL.heap_extract_max_margin.v1"
EXPECTED_FORMAL = {'reduction': 'argmax_margin', 'perturbation': 'linf_ball', 'margin_condition': 'gamma > 2*epsilon'}
CONCLUSION_TOKENS = {"schema_id": CONCL_SCHEMA}
TARGETS = [
  {
    "target_id": "preservation",
    "prop_fully_qualified": "Research.Operators.HeapExtractMax.Margin.HeapExtractMaxMarginInvarianceProp",
    "theorem_name": "heap_extract_max_margin_invariance",
    "lemma_deps": [],
  },
  {
    "target_id": "sharpness",
    "prop_fully_qualified": "Research.Operators.HeapExtractMax.Margin.HeapExtractMaxMarginSharpnessProp",
    "theorem_name": "heap_extract_max_margin_sharpness",
    "lemma_deps": [],
  }]
KNOWN_GAPS = ["DEFINITION_PINS_SURROGATE"]
LEAN_NAMESPACE = "Research.Operators.HeapExtractMax.Margin"
PROP_RELATIVE = Path("Research/Operators/HeapExtractMax/Margin.lean")
MATH_PY_RELATIVE = Path("implementation/src/operators/heap_extract_max/math.py")
THEOREM_STATEMENT = _TS
CONVENTIONS = {
    "tie_break": "UNIQUE_REQUIRED",
    "equality": "DEFAULT",
    "extensionality": "DEFAULT",
    "finiteness": "FINITE_VECTOR",
    "measure_stage": "NONE",
    "score_encoding": "REAL_MATHLIB",
}
PROP_DEPS = (
    Path("Research/Operators/HeapExtractMax/Margin.lean"),
    Path("Research/Operators/Argmax/Margin.lean"),
    Path("Research/Operators/Argmax/Basic.lean"),
)
def claim_matches_profile(claim):
    return (
        claim.get("operator") == OPERATOR
        and claim.get("theorem_id") == THEOREM_ID
        and claim.get("evaluation") == EVALUATION_METHOD
        and str(claim.get("statement", "")).strip() == THEOREM_STATEMENT.strip()
    )
def formal_matches(claim):
    formal = claim.get("formal") or {}
    return all(formal.get(k) == v for k, v in EXPECTED_FORMAL.items())
