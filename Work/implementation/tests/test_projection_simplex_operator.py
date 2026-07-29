from operators.projection_simplex.math import (
    EVALUATION_METHOD, OPERATOR, SHARPNESS_STATEMENT, THEOREM_ID, THEOREM_STATEMENT,
)
from operators.projection_simplex.verify import verify_projection_simplex_preservation
def test_verifier():
    claim = {
        "operator": OPERATOR,
        "theorem_id": THEOREM_ID,
        "evaluation": EVALUATION_METHOD,
        "statement": THEOREM_STATEMENT,
        "sharpness_statement": SHARPNESS_STATEMENT,
    }
    vr = verify_projection_simplex_preservation(claim)
    assert vr.ok, (vr.detail, vr.counterexamples)
