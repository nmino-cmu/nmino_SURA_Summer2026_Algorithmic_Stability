from operators.weighted_tournament_winner.math import (
    EVALUATION_METHOD, OPERATOR, SHARPNESS_STATEMENT, THEOREM_ID, THEOREM_STATEMENT,
)
from operators.weighted_tournament_winner.verify import verify_weighted_tournament_winner_margin
def test_verifier():
    claim = {
        "operator": OPERATOR,
        "theorem_id": THEOREM_ID,
        "evaluation": EVALUATION_METHOD,
        "statement": THEOREM_STATEMENT,
        "sharpness_statement": SHARPNESS_STATEMENT,
    }
    vr = verify_weighted_tournament_winner_margin(claim)
    assert vr.ok, (vr.detail, vr.counterexamples)
