from operators.weighted_score_selection.math import (
    EVALUATION_METHOD, OPERATOR, SHARPNESS_STATEMENT, THEOREM_ID, THEOREM_STATEMENT,
)
from operators.weighted_score_selection.verify import verify_weighted_score_selection_margin
def test_verifier():
    claim = {
        "operator": OPERATOR,
        "theorem_id": THEOREM_ID,
        "evaluation": EVALUATION_METHOD,
        "statement": THEOREM_STATEMENT,
        "sharpness_statement": SHARPNESS_STATEMENT,
    }
    vr = verify_weighted_score_selection_margin(claim)
    assert vr.ok, (vr.detail, vr.counterexamples)
