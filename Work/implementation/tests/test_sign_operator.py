from operators.sign.math import (
    EVALUATION_METHOD,
    OPERATOR,
    SHARPNESS_STATEMENT,
    THEOREM_ID,
    THEOREM_STATEMENT,
    adversarial_flip_sign,
    sign_select,
    sign_stable,
)
from operators.sign.verify import verify_sign_preservation


def test_sign_basics():
    assert sign_select(2.0) == 1
    assert sign_select(-2.0) == -1
    assert sign_select(0.0) == 0
    assert sign_stable(2.0, 1.0)
    assert not sign_stable(0.5, 1.0)
    br = adversarial_flip_sign(0.5, 1.0)
    assert br is not None and sign_select(br) != 1


def test_sign_verifier():
    claim = {
        "operator": OPERATOR,
        "theorem_id": THEOREM_ID,
        "evaluation": EVALUATION_METHOD,
        "statement": THEOREM_STATEMENT,
        "sharpness_statement": SHARPNESS_STATEMENT,
    }
    vr = verify_sign_preservation(claim)
    assert vr.ok, (vr.detail, vr.counterexamples)
