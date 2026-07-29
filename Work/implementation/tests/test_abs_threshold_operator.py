from operators.absolute_value_threshold.math import (
    EVALUATION_METHOD,
    OPERATOR,
    SHARPNESS_STATEMENT,
    THEOREM_ID,
    THEOREM_STATEMENT,
    abs_threshold,
    adversarial_flip,
    pass_preserved,
)
from operators.absolute_value_threshold.verify import verify_abs_threshold_preservation


def test_abs_basics():
    assert abs_threshold(3.0, 2.0) == 1
    assert abs_threshold(1.0, 2.0) == 0
    assert abs_threshold(-3.0, 2.0) == 1
    assert pass_preserved(5.0, 2.0, 1.0)
    assert adversarial_flip(2.5, 2.0, 1.0) == 1.5


def test_abs_verifier():
    claim = {
        "operator": OPERATOR,
        "theorem_id": THEOREM_ID,
        "evaluation": EVALUATION_METHOD,
        "statement": THEOREM_STATEMENT,
        "sharpness_statement": SHARPNESS_STATEMENT,
    }
    vr = verify_abs_threshold_preservation(claim)
    assert vr.ok, (vr.detail, vr.counterexamples)
