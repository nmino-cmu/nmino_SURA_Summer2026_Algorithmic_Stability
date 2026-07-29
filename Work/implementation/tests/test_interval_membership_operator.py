from operators.interval_membership.math import (
    EVALUATION_METHOD,
    OPERATOR,
    SHARPNESS_STATEMENT,
    THEOREM_ID,
    THEOREM_STATEMENT,
    interval_membership,
    pass_preserved,
)
from operators.interval_membership.verify import verify_interval_membership_preservation


def test_interval_basics():
    assert interval_membership(0.0, -1.0, 1.0) == 1
    assert interval_membership(2.0, -1.0, 1.0) == 0
    assert pass_preserved(0.0, -2.0, 2.0, 1.0)


def test_interval_verifier():
    claim = {
        "operator": OPERATOR,
        "theorem_id": THEOREM_ID,
        "evaluation": EVALUATION_METHOD,
        "statement": THEOREM_STATEMENT,
        "sharpness_statement": SHARPNESS_STATEMENT,
    }
    vr = verify_interval_membership_preservation(claim)
    assert vr.ok, (vr.detail, vr.counterexamples)
