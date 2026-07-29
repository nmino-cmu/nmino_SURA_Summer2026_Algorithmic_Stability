from operators.lexicographic_best_first.math import (
    EVALUATION_METHOD, OPERATOR, SHARPNESS_STATEMENT, THEOREM_ID, THEOREM_STATEMENT,
)
from operators.lexicographic_best_first.verify import verify_lexicographic_best_first_margin
def test_verifier():
    claim = {
        "operator": OPERATOR,
        "theorem_id": THEOREM_ID,
        "evaluation": EVALUATION_METHOD,
        "statement": THEOREM_STATEMENT,
        "sharpness_statement": SHARPNESS_STATEMENT,
    }
    vr = verify_lexicographic_best_first_margin(claim)
    assert vr.ok, (vr.detail, vr.counterexamples)
