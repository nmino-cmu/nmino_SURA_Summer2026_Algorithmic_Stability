from __future__ import annotations

from pathlib import Path
from typing import Any

from operators.interval_membership.math import (
    EVALUATION_METHOD,
    OPERATOR,
    THEOREM_ID,
    THEOREM_STATEMENT as _TS,
)

CONCL_SCHEMA = "ARTLEAN.CONCL.interval_membership.v1"
EXPECTED_FORMAL = {
    "equality_convention": "closed interval L<=x<=U",
    "perturbation": "|x'-x| <= epsilon",
    "pass_condition": "L+epsilon <= x <= U-epsilon",
    "fail_condition": "x < L-epsilon or x > U+epsilon",
}
CONCLUSION_TOKENS = {"schema_id": CONCL_SCHEMA}
TARGETS = [
    {
        "target_id": "preservation",
        "prop_fully_qualified": "Research.Operators.IntervalMembership.Preservation.IntervalMembershipPreservationProp",
        "theorem_name": "interval_membership_preservation",
        "lemma_deps": [],
    },
    {
        "target_id": "sharpness",
        "prop_fully_qualified": "Research.Operators.IntervalMembership.Preservation.IntervalMembershipSharpnessProp",
        "theorem_name": "interval_membership_sharpness",
        "lemma_deps": [],
    }]
KNOWN_GAPS = ["DEFINITION_PINS_SURROGATE"]
LEAN_NAMESPACE = "Research.Operators.IntervalMembership.Preservation"
PROP_RELATIVE = Path("Research/Operators/IntervalMembership/Preservation.lean")
MATH_PY_RELATIVE = Path("implementation/src/operators/interval_membership/math.py")
THEOREM_STATEMENT = _TS
CONVENTIONS = {
    "tie_break": "NONE",
    "equality": "CLOSED_INTERVAL",
    "extensionality": "DEFAULT",
    "finiteness": "SCALAR",
    "measure_stage": "NONE",
    "score_encoding": "REAL_MATHLIB",
}
PROP_DEPS = (
    Path("Research/Operators/IntervalMembership/Preservation.lean"),
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
