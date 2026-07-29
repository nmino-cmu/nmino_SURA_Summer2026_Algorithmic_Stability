from operators.groupwise_then_global_maximum.math import (
    EVALUATION_METHOD, OPERATOR, SHARPNESS_STATEMENT, THEOREM_ID, THEOREM_STATEMENT,
)
from operators.groupwise_then_global_maximum.verify import verify_groupwise_then_global_maximum_margin
def test_verifier():
    claim = {
        "operator": OPERATOR,
        "theorem_id": THEOREM_ID,
        "evaluation": EVALUATION_METHOD,
        "statement": THEOREM_STATEMENT,
        "sharpness_statement": SHARPNESS_STATEMENT,
    }
    vr = verify_groupwise_then_global_maximum_margin(claim)
    assert vr.ok, (vr.detail, vr.counterexamples)
