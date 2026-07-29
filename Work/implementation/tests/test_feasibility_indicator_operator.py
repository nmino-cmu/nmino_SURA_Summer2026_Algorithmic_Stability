from operators.feasibility_indicator.math import (
    EVALUATION_METHOD, OPERATOR, SHARPNESS_STATEMENT, THEOREM_ID, THEOREM_STATEMENT,
)
from operators.feasibility_indicator.verify import verify_feasibility_indicator_preservation
def test_verifier():
    claim = {
        "operator": OPERATOR,
        "theorem_id": THEOREM_ID,
        "evaluation": EVALUATION_METHOD,
        "statement": THEOREM_STATEMENT,
        "sharpness_statement": SHARPNESS_STATEMENT,
    }
    vr = verify_feasibility_indicator_preservation(claim)
    assert vr.ok, (vr.detail, vr.counterexamples)
