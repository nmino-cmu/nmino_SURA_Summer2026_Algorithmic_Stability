from operators.percentile.math import EVALUATION_METHOD, OPERATOR, SHARPNESS_STATEMENT, THEOREM_ID, THEOREM_STATEMENT, invariance_holds, is_strict_kth
from operators.percentile.verify import verify_percentile_margin

def test_strict_kth():
    scores = (1.0, 5.0, 3.0)
    assert is_strict_kth(scores, 1, 2)
    assert invariance_holds(scores, 1, 2, 0.9)

def test_verifier():
    claim = {
        "operator": OPERATOR, "theorem_id": THEOREM_ID, "evaluation": EVALUATION_METHOD,
        "statement": THEOREM_STATEMENT, "sharpness_statement": SHARPNESS_STATEMENT,
    }
    vr = verify_percentile_margin(claim)
    assert vr.ok, (vr.detail, vr.counterexamples)
