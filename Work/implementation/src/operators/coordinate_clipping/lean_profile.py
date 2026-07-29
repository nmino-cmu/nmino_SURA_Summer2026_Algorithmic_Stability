from __future__ import annotations
from pathlib import Path
from typing import Any
from operators.coordinate_clipping.math import EVALUATION_METHOD, OPERATOR, THEOREM_ID, THEOREM_STATEMENT as _TS
CONCL_SCHEMA = "ARTLEAN.CONCL.coordinate_clipping.v1"
EXPECTED_FORMAL = {'operator_kind': 'clamp_projection', 'perturbation': 'abs_ball', 'property': '1_lipschitz_nonexpansive'}
CONCLUSION_TOKENS = {"schema_id": CONCL_SCHEMA}
TARGETS = [{'target_id': 'preservation', 'prop_fully_qualified': 'Research.Operators.CoordinateClipping.Preservation.CoordinateClippingStabilityProp', 'theorem_name': 'coordinate_clipping_clamp_stability', 'lemma_deps': []}, {'target_id': 'sharpness', 'prop_fully_qualified': 'Research.Operators.CoordinateClipping.Preservation.CoordinateClippingSharpnessProp', 'theorem_name': 'coordinate_clipping_clamp_sharpness', 'lemma_deps': []}]
KNOWN_GAPS = ["DEFINITION_PINS_SURROGATE"]
LEAN_NAMESPACE = "Research.Operators.CoordinateClipping.Preservation"
PROP_RELATIVE = Path("Research/Operators/CoordinateClipping/Preservation.lean")
MATH_PY_RELATIVE = Path("implementation/src/operators/coordinate_clipping/math.py")
THEOREM_STATEMENT = _TS
CONVENTIONS = {
    "tie_break": "NONE",
    "equality": "DEFAULT",
    "extensionality": "DEFAULT",
    "finiteness": "SCALAR_OR_LIST",
    "measure_stage": "NONE",
    "score_encoding": "REAL_MATHLIB",
}
PROP_DEPS = tuple(Path(p) for p in ['Research/Operators/Projection/Clamp.lean', 'Research/Operators/Argmax/Basic.lean']) + (PROP_RELATIVE,)
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
