from __future__ import annotations
from pathlib import Path
from typing import Any
from operators.lexicographic_best_first.math import EVALUATION_METHOD, OPERATOR, THEOREM_ID, THEOREM_STATEMENT as _TS
CONCL_SCHEMA = "ARTLEAN.CONCL.lexicographic_best_first_margin.v1"
EXPECTED_FORMAL = {'reduction': 'argmax_margin', 'perturbation': 'linf_ball', 'margin_condition': 'gamma > 2*epsilon'}
CONCLUSION_TOKENS = {"schema_id": CONCL_SCHEMA}
TARGETS = [
  {
    "target_id": "preservation",
    "prop_fully_qualified": "Research.Operators.LexicographicBestFirst.Margin.LexicographicBestFirstMarginInvarianceProp",
    "theorem_name": "lexicographic_best_first_margin_invariance",
    "lemma_deps": [],
  },
  {
    "target_id": "sharpness",
    "prop_fully_qualified": "Research.Operators.LexicographicBestFirst.Margin.LexicographicBestFirstMarginSharpnessProp",
    "theorem_name": "lexicographic_best_first_margin_sharpness",
    "lemma_deps": [],
  }]
KNOWN_GAPS = ["DEFINITION_PINS_SURROGATE"]
LEAN_NAMESPACE = "Research.Operators.LexicographicBestFirst.Margin"
PROP_RELATIVE = Path("Research/Operators/LexicographicBestFirst/Margin.lean")
MATH_PY_RELATIVE = Path("implementation/src/operators/lexicographic_best_first/math.py")
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
    Path("Research/Operators/LexicographicBestFirst/Margin.lean"),
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
