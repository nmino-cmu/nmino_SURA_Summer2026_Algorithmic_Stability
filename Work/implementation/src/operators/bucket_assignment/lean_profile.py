from __future__ import annotations
from pathlib import Path
from typing import Any
from operators.bucket_assignment.math import EVALUATION_METHOD, OPERATOR, THEOREM_ID, THEOREM_STATEMENT as _TS
CONCL_SCHEMA = "ARTLEAN.CONCL.bucket_assignment_margin.v1"
EXPECTED_FORMAL = {'selection': 'full_pairwise_ranking', 'perturbation': 'linf_ball', 'gap_condition': 'all_pairwise_gaps > 2*epsilon'}
CONCLUSION_TOKENS = {"schema_id": CONCL_SCHEMA}
TARGETS = [
  {"target_id":"preservation","prop_fully_qualified":"Research.Operators.BucketAssignment.Preservation.BucketAssignmentMarginInvarianceProp","theorem_name":"bucket_assignment_margin_invariance","lemma_deps":[]},
  {"target_id":"sharpness","prop_fully_qualified":"Research.Operators.BucketAssignment.Preservation.BucketAssignmentMarginSharpnessProp","theorem_name":"bucket_assignment_margin_sharpness","lemma_deps":[]}]
KNOWN_GAPS = ["DEFINITION_PINS_SURROGATE"]
LEAN_NAMESPACE = "Research.Operators.BucketAssignment.Preservation"
PROP_RELATIVE = Path("Research/Operators/BucketAssignment/Preservation.lean")
MATH_PY_RELATIVE = Path("implementation/src/operators/bucket_assignment/math.py")
THEOREM_STATEMENT = _TS
CONVENTIONS = {"tie_break":"UNIQUE_REQUIRED","equality":"DEFAULT","extensionality":"DEFAULT","finiteness":"FINITE_VECTOR","measure_stage":"NONE","score_encoding": "REAL_MATHLIB"}
PROP_DEPS = (Path("Research/Operators/BucketAssignment/Preservation.lean"), Path("Research/Operators/OrderStat/Ranking.lean"), Path("Research/Operators/OrderStat/KthMargin.lean"), Path("Research/Operators/OrderStat/Basic.lean"), Path("Research/Operators/Argmax/Basic.lean"))
def claim_matches_profile(claim):
    return claim.get("operator")==OPERATOR and claim.get("theorem_id")==THEOREM_ID and claim.get("evaluation")==EVALUATION_METHOD and str(claim.get("statement","")).strip()==THEOREM_STATEMENT.strip()
def formal_matches(claim):
    formal=claim.get("formal") or {}
    return all(formal.get(k)==v for k,v in EXPECTED_FORMAL.items())
