"""Threshold Lean formalization profile (deterministic preservation)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from operators.thresholding.math import (
    EVALUATION_METHOD_DET,
    OPERATOR,
    THEOREM_ID_DETERMINISTIC,
    THEOREM_STATEMENT_DET,
)

THEOREM_ID = THEOREM_ID_DETERMINISTIC
CONCL_SCHEMA = "ARTLEAN.CONCL.threshold_preservation.v1"

EXPECTED_FORMAL = {
    "equality_convention": "x >= T passes",
    "perturbation": "|x'-x| <= epsilon",
    "pass_condition": "x >= T + epsilon",
    "fail_condition": "x < T - epsilon",
    "unstable_region": "[T - epsilon, T + epsilon)",
    "signed_margin": "m = x - T",
    "distance": "d = |x - T|",
}

CONCLUSION_TOKENS = {
    "schema_id": CONCL_SCHEMA,
    "score_space": "REAL_SCALAR",
    "equality_convention": "X_GE_T_PASSES",
    "perturbation": "ABS_DIFF_LE_EPS",
    "pass_condition": "X_GE_T_PLUS_EPS",
    "fail_condition": "X_LT_T_MINUS_EPS",
    "unstable_region": "HALF_OPEN_BAND",
}

TARGETS = [
    {
        "target_id": "preservation",
        "prop_fully_qualified": "Research.Operators.Threshold.Preservation.ThresholdPreservationProp",
        "theorem_name": "threshold_preservation",
        "lemma_deps": [],
    }
]

KNOWN_GAPS = ["DEFINITION_PINS_SURROGATE"]

LEAN_NAMESPACE = "Research.Operators.Threshold.Preservation"

PROP_RELATIVE = Path("Research/Operators/Threshold/Preservation.lean")

MATH_PY_RELATIVE = Path("implementation/src/operators/thresholding/math.py")

THEOREM_STATEMENT = THEOREM_STATEMENT_DET

CONVENTIONS = {
    "tie_break": "NONE",
    "equality": "REAL_GE_PASSES",
    "extensionality": "DEFAULT",
    "finiteness": "SCALAR",
    "measure_stage": "NONE",
    "score_encoding": "REAL_MATHLIB",
}

PROP_DEPS = (
    Path("Research/Operators/Threshold/Preservation.lean"),
    Path("Research/Operators/Argmax/Basic.lean"),  # shared natAbs_le_iff
)


def claim_matches_profile(claim: dict[str, Any]) -> bool:
    return (
        claim.get("operator") == OPERATOR
        and claim.get("theorem_id") == THEOREM_ID
        and claim.get("evaluation") == EVALUATION_METHOD_DET
        and str(claim.get("statement", "")).strip() == THEOREM_STATEMENT.strip()
    )


def formal_matches(claim: dict[str, Any]) -> bool:
    formal = claim.get("formal") or {}
    return all(formal.get(k) == v for k, v in EXPECTED_FORMAL.items())
