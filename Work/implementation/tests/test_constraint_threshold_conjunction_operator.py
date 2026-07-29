from operators.constraint_threshold_conjunction.math import (
    EVALUATION_METHOD, OPERATOR, SHARPNESS_STATEMENT, THEOREM_ID, THEOREM_STATEMENT,
)
from operators.constraint_threshold_conjunction.verify import verify_constraint_threshold_conjunction_preservation
def test_verifier():
    claim = {
        "operator": OPERATOR,
        "theorem_id": THEOREM_ID,
        "evaluation": EVALUATION_METHOD,
        "statement": THEOREM_STATEMENT,
        "sharpness_statement": SHARPNESS_STATEMENT,
    }
    vr = verify_constraint_threshold_conjunction_preservation(claim)
    assert vr.ok, (vr.detail, vr.counterexamples)
