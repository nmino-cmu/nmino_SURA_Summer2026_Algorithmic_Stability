"""Unit tests for multi-threshold operator."""

from __future__ import annotations

import pytest

from operators.multi_threshold.math import (
    adversarial_flip,
    multi_stable,
    multi_threshold_count,
    unstable_index,
)
from operators.multi_threshold.verify import verify_multi_threshold_preservation
from operators.multi_threshold.math import EVALUATION_METHOD, OPERATOR, THEOREM_ID, THEOREM_STATEMENT, SHARPNESS_STATEMENT


def test_empty_and_singleton():
    assert multi_threshold_count(0.0, ()) == 0
    assert multi_threshold_count(1.0, (0.0,)) == 1
    assert multi_threshold_count(-1.0, (0.0,)) == 0
    assert multi_threshold_count(0.0, (0.0,)) == 1  # equality passes


def test_multi_count():
    assert multi_threshold_count(2.5, (0.0, 1.0, 2.0, 3.0)) == 3
    assert multi_threshold_count(0.0, (0.0, 0.0)) == 2


def test_stability_and_sharpness():
    assert multi_stable(5.0, (0.0, 1.0), 1.0)
    assert adversarial_flip(5.0, (0.0, 1.0), 1.0) is None
    assert unstable_index(0.5, (0.0, 2.0), 1.0) == 0
    br = adversarial_flip(0.5, (0.0, 2.0), 1.0)
    assert br is not None
    assert multi_threshold_count(br, (0.0, 2.0)) != multi_threshold_count(0.5, (0.0, 2.0))


def test_malformed():
    with pytest.raises(ValueError):
        multi_threshold_count(float("inf"), (0.0,))
    with pytest.raises(ValueError):
        multi_stable(0.0, (0.0,), -0.1)


def test_computational_verifier():
    claim = {
        "operator": OPERATOR,
        "theorem_id": THEOREM_ID,
        "evaluation": EVALUATION_METHOD,
        "statement": THEOREM_STATEMENT,
        "sharpness_statement": SHARPNESS_STATEMENT,
    }
    vr = verify_multi_threshold_preservation(claim)
    assert vr.ok, (vr.detail, vr.counterexamples)
