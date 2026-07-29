from operators.coordinate_clipping.math import (
    EVALUATION_METHOD, OPERATOR, SHARPNESS_STATEMENT, THEOREM_ID, THEOREM_STATEMENT,
)
from operators.coordinate_clipping.verify import verify_coordinate_clipping_preservation
def test_verifier():
    claim = {
        "operator": OPERATOR,
        "theorem_id": THEOREM_ID,
        "evaluation": EVALUATION_METHOD,
        "statement": THEOREM_STATEMENT,
        "sharpness_statement": SHARPNESS_STATEMENT,
    }
    vr = verify_coordinate_clipping_preservation(claim)
    assert vr.ok, (vr.detail, vr.counterexamples)
