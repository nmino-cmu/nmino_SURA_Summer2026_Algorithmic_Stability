from __future__ import annotations
from pathlib import Path
from typing import Any
from operators.projection_simplex.math import EVALUATION_METHOD, OPERATOR, THEOREM_ID, THEOREM_STATEMENT as _TS
CONCL_SCHEMA = "ARTLEAN.CONCL.projection_simplex.v1"
EXPECTED_FORMAL = {'operator_kind': 'feasible_ball_identity', 'perturbation': 'abs_ball', 'property': 'identity_on_epsilon_interior'}
CONCLUSION_TOKENS = {"schema_id": CONCL_SCHEMA}
TARGETS = [{'target_id': 'preservation', 'prop_fully_qualified': 'Research.Operators.ProjectionSimplex.Preservation.ProjectionSimplexIdentityProp', 'theorem_name': 'projection_simplex_feasible_ball_identity', 'lemma_deps': []}, {'target_id': 'sharpness', 'prop_fully_qualified': 'Research.Operators.ProjectionSimplex.Preservation.ProjectionSimplexSharpnessProp', 'theorem_name': 'projection_simplex_feasible_ball_sharpness', 'lemma_deps': []}]
KNOWN_GAPS = ["DEFINITION_PINS_SURROGATE"]
LEAN_NAMESPACE = "Research.Operators.ProjectionSimplex.Preservation"
PROP_RELATIVE = Path("Research/Operators/ProjectionSimplex/Preservation.lean")
MATH_PY_RELATIVE = Path("implementation/src/operators/projection_simplex/math.py")
THEOREM_STATEMENT = _TS
CONVENTIONS = {
    "tie_break": "NONE",
    "equality": "DEFAULT",
    "extensionality": "DEFAULT",
    "finiteness": "SCALAR_OR_LIST",
    "measure_stage": "NONE",
    "score_encoding": "REAL_MATHLIB",
}
PROP_DEPS = tuple(Path(p) for p in ['Research/Operators/Projection/FeasibleId.lean', 'Research/Operators/Argmax/Basic.lean']) + (PROP_RELATIVE,)
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
