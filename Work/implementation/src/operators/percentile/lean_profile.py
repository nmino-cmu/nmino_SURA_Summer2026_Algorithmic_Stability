from __future__ import annotations
from pathlib import Path
from typing import Any
from operators.percentile.math import EVALUATION_METHOD, OPERATOR, THEOREM_ID, THEOREM_STATEMENT as _TS

CONCL_SCHEMA = "ARTLEAN.CONCL.percentile_margin.v1"
EXPECTED_FORMAL = {'selection': 'unique_strict_kth_smallest', 'perturbation': 'linf_ball', 'gap_condition': 'all_pairwise_gaps > 2*epsilon'}
CONCLUSION_TOKENS = {"schema_id": CONCL_SCHEMA}
TARGETS = [
    {
        "target_id": "preservation",
        "prop_fully_qualified": "Research.Operators.Percentile.Preservation.PercentileMarginInvarianceProp",
        "theorem_name": "percentile_margin_invariance",
        "lemma_deps": [],
    },
    {
        "target_id": "sharpness",
        "prop_fully_qualified": "Research.Operators.Percentile.Preservation.PercentileMarginSharpnessProp",
        "theorem_name": "percentile_margin_sharpness",
        "lemma_deps": [],
    }]
KNOWN_GAPS = ["DEFINITION_PINS_SURROGATE"]
LEAN_NAMESPACE = "Research.Operators.Percentile.Preservation"
PROP_RELATIVE = Path("Research/Operators/Percentile/Preservation.lean")
MATH_PY_RELATIVE = Path("implementation/src/operators/percentile/math.py")
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
    Path("Research/Operators/Percentile/Preservation.lean"),
    Path("Research/Operators/OrderStat/KthMargin.lean"),
    Path("Research/Operators/OrderStat/Basic.lean"),
    Path("Research/Operators/Argmax/Basic.lean"),
)

def claim_matches_profile(claim: dict[str, Any]) -> bool:
    return (
        claim.get("operator") == OPERATOR
        and claim.get("theorem_id") == THEOREM_ID
        and claim.get("evaluation") == EVALUATION_METHOD
        and str(claim.get("statement", "")).strip() == THEOREM_STATEMENT.strip()
    )

def formal_matches(claim: dict[str, Any]) -> bool:
    formal = claim.get("formal") or {}
    return all(formal.get(k) == v for k, v in EXPECTED_FORMAL.items())
