"""Threshold Lean profile — bounded almost-sure noise (pathwise ℝ core)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from operators.thresholding.math import (
    EVALUATION_METHOD_NOISY,
    OPERATOR,
    THEOREM_ID_NOISY,
    THEOREM_STATEMENT_NOISY,
)

THEOREM_ID = THEOREM_ID_NOISY
CONCL_SCHEMA = "ARTLEAN.CONCL.threshold_bounded_noise.v1"

EXPECTED_FORMAL = {
    "noise_model": "almost_sure_bounded |xi| <= eta",
    "mechanism": "1{x + xi >= T}",
    "pass_condition": "x >= T + eta",
    "fail_condition": "x < T - eta",
    "unstable_region": "[T - eta, T + eta)",
    "not_claimed": "full_sparse_vector_privacy",
}

CONCLUSION_TOKENS = {
    "schema_id": CONCL_SCHEMA,
    "score_space": "REAL_SCALAR",
    "equality_convention": "X_GE_T_PASSES",
    "noise_model": "PATHWISE_ABS_XI_LE_ETA",
    "mechanism": "ABOVE_THRESHOLD_X_PLUS_XI",
    "pass_condition": "X_GE_T_PLUS_ETA",
    "fail_condition": "X_LT_T_MINUS_ETA",
    "unstable_region": "HALF_OPEN_BAND",
    "not_claimed": "FULL_SPARSE_VECTOR_PRIVACY",
}

TARGETS = [
    {
        "target_id": "preservation",
        "prop_fully_qualified": "Research.Operators.Threshold.BoundedNoise.BoundedNoisePreservationProp",
        "theorem_name": "bounded_noise_preservation",
        "lemma_deps": ["threshold_preservation"],
    },
    {
        "target_id": "sharpness",
        "prop_fully_qualified": "Research.Operators.Threshold.BoundedNoise.BoundedNoiseSharpnessProp",
        "theorem_name": "bounded_noise_sharpness",
        "lemma_deps": [],
    },
]

KNOWN_GAPS = [
    "PATHWISE_NOT_MEASURE_THEORETIC_AS",
    "DEFINITION_PINS_SURROGATE",
    "BOUNDED_NOISE_NOT_FULL_SVT",
]

LEAN_NAMESPACE = "Research.Operators.Threshold.BoundedNoise"

PROP_RELATIVE = Path("Research/Operators/Threshold/BoundedNoise.lean")

MATH_PY_RELATIVE = Path("implementation/src/operators/thresholding/math.py")

THEOREM_STATEMENT = THEOREM_STATEMENT_NOISY

CONVENTIONS = {
    "tie_break": "NONE",
    "equality": "REAL_GE_PASSES",
    "extensionality": "DEFAULT",
    "finiteness": "SCALAR",
    "measure_stage": "PATHWISE_SURROGATE",
    "score_encoding": "REAL_MATHLIB",
}

PROP_DEPS = (
    Path("Research/Operators/Threshold/BoundedNoise.lean"),
    Path("Research/Operators/Threshold/Preservation.lean"),
    Path("Research/Operators/Argmax/Basic.lean"),
)


def claim_matches_profile(claim: dict[str, Any]) -> bool:
    return (
        claim.get("operator") == OPERATOR
        and claim.get("theorem_id") == THEOREM_ID
        and claim.get("evaluation") == EVALUATION_METHOD_NOISY
        and str(claim.get("statement", "")).strip() == THEOREM_STATEMENT.strip()
    )


def formal_matches(claim: dict[str, Any]) -> bool:
    formal = claim.get("formal") or {}
    return all(formal.get(k) == v for k, v in EXPECTED_FORMAL.items())
