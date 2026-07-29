"""Multi-threshold Lean formalization profile."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from operators.multi_threshold.math import (
    EVALUATION_METHOD,
    OPERATOR,
    THEOREM_ID,
    THEOREM_STATEMENT,
)

CONCL_SCHEMA = "ARTLEAN.CONCL.multi_threshold_preservation.v1"

EXPECTED_FORMAL = {
    "equality_convention": "x >= T_i passes per coordinate",
    "perturbation": "|x'-x| <= epsilon",
    "output": "count of passed thresholds",
    "stability": "every coordinate OutsideThresholdUnstableBand",
    "reduction": "coordinatewise AboveThreshold preservation",
}

CONCLUSION_TOKENS = {
    "schema_id": CONCL_SCHEMA,
    "score_space": "REAL_SCALAR",
    "equality_convention": "X_GE_TI_PASSES",
    "perturbation": "ABS_DIFF_LE_EPS",
    "output": "PASS_COUNT",
    "stability": "ALL_COORDINATES_STABLE",
}

TARGETS = [
    {
        "target_id": "preservation",
        "prop_fully_qualified": "Research.Operators.MultiThreshold.Preservation.MultiThresholdPreservationProp",
        "theorem_name": "multi_threshold_preservation",
        "lemma_deps": [],
    },
    {
        "target_id": "sharpness",
        "prop_fully_qualified": "Research.Operators.MultiThreshold.Preservation.MultiThresholdSharpnessProp",
        "theorem_name": "multi_threshold_sharpness",
        "lemma_deps": [],
    }]

KNOWN_GAPS = ["DEFINITION_PINS_SURROGATE"]

LEAN_NAMESPACE = "Research.Operators.MultiThreshold.Preservation"

PROP_RELATIVE = Path("Research/Operators/MultiThreshold/Preservation.lean")

MATH_PY_RELATIVE = Path("implementation/src/operators/multi_threshold/math.py")

THEOREM_STATEMENT = THEOREM_STATEMENT

CONVENTIONS = {
    "tie_break": "NONE",
    "equality": "INT_GE_PASSES_PER_CUT",
    "extensionality": "DEFAULT",
    "finiteness": "FINITE_THRESHOLD_LIST",
    "measure_stage": "NONE",
    "score_encoding": "REAL_MATHLIB",
}

PROP_DEPS = (
    Path("Research/Operators/MultiThreshold/Preservation.lean"),
    Path("Research/Operators/Threshold/Preservation.lean"),
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
