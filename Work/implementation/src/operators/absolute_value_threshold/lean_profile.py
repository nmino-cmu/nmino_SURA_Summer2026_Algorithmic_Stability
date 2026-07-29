from __future__ import annotations

from pathlib import Path
from typing import Any

from operators.absolute_value_threshold.math import (
    EVALUATION_METHOD,
    OPERATOR,
    THEOREM_ID,
    THEOREM_STATEMENT as _TS,
)

CONCL_SCHEMA = "ARTLEAN.CONCL.abs_threshold.v1"
EXPECTED_FORMAL = {
    "equality_convention": "|x| >= T passes",
    "perturbation": "|x'-x| <= epsilon",
    "pass_condition": "|x| >= T + epsilon",
    "fail_condition": "|x| + epsilon < T",
    "T_nonnegative": "T >= 0",
}
CONCLUSION_TOKENS = {"schema_id": CONCL_SCHEMA, "score_space": "REAL_SCALAR"}
TARGETS = [
    {
        "target_id": "preservation",
        "prop_fully_qualified": "Research.Operators.AbsThreshold.Preservation.AbsThresholdPreservationProp",
        "theorem_name": "abs_threshold_preservation",
        "lemma_deps": [],
    },
    {
        "target_id": "sharpness",
        "prop_fully_qualified": "Research.Operators.AbsThreshold.Preservation.AbsThresholdSharpnessProp",
        "theorem_name": "abs_threshold_sharpness",
        "lemma_deps": [],
    }]
KNOWN_GAPS = ["DEFINITION_PINS_SURROGATE"]
LEAN_NAMESPACE = "Research.Operators.AbsThreshold.Preservation"
PROP_RELATIVE = Path("Research/Operators/AbsThreshold/Preservation.lean")
MATH_PY_RELATIVE = Path("implementation/src/operators/absolute_value_threshold/math.py")
THEOREM_STATEMENT = _TS
CONVENTIONS = {
    "tie_break": "NONE",
    "equality": "ABS_GE_T_PASSES",
    "extensionality": "DEFAULT",
    "finiteness": "SCALAR",
    "measure_stage": "NONE",
    "score_encoding": "REAL_MATHLIB",
}
PROP_DEPS = (
    Path("Research/Operators/AbsThreshold/Preservation.lean"),
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
