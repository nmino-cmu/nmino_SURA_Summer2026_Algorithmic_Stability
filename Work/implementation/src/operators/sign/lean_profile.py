"""Sign Lean profile."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from operators.sign.math import (
    EVALUATION_METHOD,
    OPERATOR,
    THEOREM_ID,
    THEOREM_STATEMENT as _THEOREM_STATEMENT,
)

CONCL_SCHEMA = "ARTLEAN.CONCL.sign_preservation.v1"
EXPECTED_FORMAL = {
    "equality_convention": "sign(0)=0; strict for nonzero",
    "perturbation": "|x'-x| <= epsilon",
    "plus_condition": "x > epsilon",
    "minus_condition": "x < -epsilon",
    "zero_condition": "epsilon = 0 and x = 0",
}
CONCLUSION_TOKENS = {
    "schema_id": CONCL_SCHEMA,
    "score_space": "REAL_SCALAR",
    "output": "SIGN_TRICHOTOMY",
    "perturbation": "ABS_DIFF_LE_EPS",
}
TARGETS = [
    {
        "target_id": "preservation",
        "prop_fully_qualified": "Research.Operators.Sign.Preservation.SignPreservationProp",
        "theorem_name": "sign_preservation",
        "lemma_deps": [],
    },
    {
        "target_id": "sharpness",
        "prop_fully_qualified": "Research.Operators.Sign.Preservation.SignSharpnessProp",
        "theorem_name": "sign_sharpness",
        "lemma_deps": [],
    }]
KNOWN_GAPS = ["DEFINITION_PINS_SURROGATE"]
LEAN_NAMESPACE = "Research.Operators.Sign.Preservation"
PROP_RELATIVE = Path("Research/Operators/Sign/Preservation.lean")
MATH_PY_RELATIVE = Path("implementation/src/operators/sign/math.py")
THEOREM_STATEMENT = _THEOREM_STATEMENT
CONVENTIONS = {
    "tie_break": "ZERO_AT_ORIGIN",
    "equality": "SIGN_ZERO_AT_ZERO",
    "extensionality": "DEFAULT",
    "finiteness": "SCALAR",
    "measure_stage": "NONE",
    "score_encoding": "REAL_MATHLIB",
}
PROP_DEPS = (
    Path("Research/Operators/Sign/Preservation.lean"),
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
