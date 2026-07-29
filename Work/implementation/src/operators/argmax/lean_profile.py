"""Argmax Lean formalization profile (allowlist + tokenized conclusion)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from operators.argmax.math import EVALUATION_METHOD, OPERATOR, THEOREM_ID, THEOREM_STATEMENT

CONCL_SCHEMA = "ARTLEAN.CONCL.argmax_margin.v1"

EXPECTED_FORMAL = {
    "perturbation_norm": "linf",
    "margin_definition": "s_i_star - max_{j!=i_star} s_j",
    "invariance_condition": "gamma > 2*epsilon",
}

CONCLUSION_TOKENS = {
    "schema_id": CONCL_SCHEMA,
    "m_min": 2,
    "score_space": "FIN_TO_REAL",
    "requires_unique_maximizer": True,
    "margin_def": "S_I_STAR_MINUS_MAX_OTHERS",
    "perturbation_norm": "LINF",
    "epsilon_domain": "NONNEG_REAL",
    "invariance_predicate": "GAMMA_GT_TWO_EPSILON_PRESERVES_UNIQUE_MAX",
    "sharpness_predicate": "GAMMA_LE_TWO_EPSILON_EXISTS_BREAKING_DELTA",
}

TARGETS = [
    {
        "target_id": "invariance",
        "prop_fully_qualified": "Research.Operators.Argmax.Margin.MarginInvarianceProp",
        "theorem_name": "margin_invariance",
        "lemma_deps": ["gap_shrinks_by_at_most_two_eps"],
    },
    {
        "target_id": "sharpness",
        "prop_fully_qualified": "Research.Operators.Argmax.Margin.MarginSharpnessProp",
        "theorem_name": "margin_sharpness",
        "lemma_deps": ["adversarialDelta_in_ball"],
    }]

KNOWN_GAPS = ["DEFINITION_PINS_SURROGATE"]

LEAN_NAMESPACE = "Research.Operators.Argmax.Margin"

PROP_RELATIVE = Path("Research/Operators/Argmax/Margin.lean")

MATH_PY_RELATIVE = Path("implementation/src/operators/argmax/math.py")

CONVENTIONS = {
    "tie_break": "NONE_UNIQUE_REQUIRED",
    "equality": "REAL_LE",
    "extensionality": "DEFAULT",
    "finiteness": "FIN_M",
    "measure_stage": "NONE",
    "score_encoding": "REAL_MATHLIB",
}

PROP_DEPS = (
    Path("Research/Operators/Argmax/Margin.lean"),
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
