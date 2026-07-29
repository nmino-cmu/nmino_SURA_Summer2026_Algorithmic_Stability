"""Computational discharge of thresholding proof obligations."""

from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Any

from operators.thresholding.math import (
    EVALUATION_METHOD_DET,
    EVALUATION_METHOD_NOISY,
    OPERATOR,
    SHARPNESS_STATEMENT_DET,
    SHARPNESS_STATEMENT_NOISY,
    THEOREM_ID_DETERMINISTIC,
    THEOREM_ID_NOISY,
    THEOREM_STATEMENT_DET,
    THEOREM_STATEMENT_NOISY,
    ThresholdInstance,
    above_threshold,
    abstaining_threshold,
    adversarial_break_fail,
    adversarial_break_pass,
    certified_set,
    fail_preserved,
    first_crossing,
    laplace_pass_probability,
    noisy_first_crossing,
    pass_preserved,
    unstable_region,
)


@dataclass(frozen=True)
class VerifyResult:
    ok: bool
    detail: str
    counterexamples: tuple[dict[str, Any], ...] = ()
    limitations: tuple[str, ...] = (
        "COMPUTATIONAL_VERIFICATION_NOT_LEAN",
        "SCALAR_FINITE_SCORES_ONLY",
    )


def claim_is_threshold_preservation(claim: dict[str, Any]) -> bool:
    return (
        claim.get("operator") == OPERATOR
        and claim.get("theorem_id") == THEOREM_ID_DETERMINISTIC
        and claim.get("evaluation") == EVALUATION_METHOD_DET
    )


def claim_is_bounded_noise_threshold(claim: dict[str, Any]) -> bool:
    return (
        claim.get("operator") == OPERATOR
        and claim.get("theorem_id") == THEOREM_ID_NOISY
        and claim.get("evaluation") == EVALUATION_METHOD_NOISY
    )


def _all_perturbations_agree(x: float, T: float, eps: float, expected: int) -> bool:
    # Exact interval endpoints + midpoints suffice for monotone threshold rule
    samples = {x - eps, x, x + eps, x - eps / 2, x + eps / 2} if eps > 0 else {x}
    for xp in samples:
        if above_threshold(xp, T) != expected:
            return False
    return True


def _property_trials(rng: random.Random, n: int = 300) -> list[dict[str, Any]]:
    failures: list[dict[str, Any]] = []
    for _ in range(n):
        T = rng.uniform(-5, 5)
        x = rng.uniform(-5, 5)
        eps = rng.uniform(0, 3)
        if pass_preserved(x, T, eps):
            if not _all_perturbations_agree(x, T, eps, 1):
                failures.append({"kind": "pass", "x": x, "T": T, "eps": eps})
            if adversarial_break_pass(x, T, eps) is not None:
                failures.append({"kind": "pass_false_break", "x": x, "T": T, "eps": eps})
        elif fail_preserved(x, T, eps):
            if not _all_perturbations_agree(x, T, eps, 0):
                failures.append({"kind": "fail", "x": x, "T": T, "eps": eps})
            if adversarial_break_fail(x, T, eps) is not None:
                failures.append({"kind": "fail_false_break", "x": x, "T": T, "eps": eps})
        else:
            if not unstable_region(x, T, eps):
                failures.append({"kind": "unstable_flag", "x": x, "T": T, "eps": eps})
            # sharpness: must admit a flip relative to A_T(x) when in unstable band
            a = above_threshold(x, T)
            if a == 1:
                br = adversarial_break_pass(x, T, eps)
                if br is None or above_threshold(br, T) != 0:
                    failures.append({"kind": "sharp_pass", "x": x, "T": T, "eps": eps, "br": br})
            else:
                br = adversarial_break_fail(x, T, eps)
                if br is None or above_threshold(br, T) != 1:
                    failures.append({"kind": "sharp_fail", "x": x, "T": T, "eps": eps, "br": br})
        # set-valued consistency
        s = certified_set(x, T, eps)
        if pass_preserved(x, T, eps) and s != frozenset({1}):
            failures.append({"kind": "set_pass", "x": x, "T": T, "eps": eps})
        if fail_preserved(x, T, eps) and s != frozenset({0}):
            failures.append({"kind": "set_fail", "x": x, "T": T, "eps": eps})
        if unstable_region(x, T, eps) and s != frozenset({0, 1}):
            failures.append({"kind": "set_unstable", "x": x, "T": T, "eps": eps})
    return failures


def verify_threshold_preservation(claim: dict[str, Any]) -> VerifyResult:
    if not claim_is_threshold_preservation(claim):
        return VerifyResult(False, "not_threshold_preservation_claim")

    if str(claim.get("statement", "")).strip() != THEOREM_STATEMENT_DET.strip():
        return VerifyResult(False, "statement_mismatch")

    formal = claim.get("formal")
    if formal is None:
        formal = {}
    if not isinstance(formal, dict):
        return VerifyResult(False, "bad_formal_type")
    expected_formal = {
        "equality_convention": "x >= T passes",
        "perturbation": "|x'-x| <= epsilon",
        "pass_condition": "x >= T + epsilon",
        "fail_condition": "x < T - epsilon",
        "unstable_region": "[T - epsilon, T + epsilon)",
        "signed_margin": "m = x - T",
        "distance": "d = |x - T|",
    }
    for k, v in expected_formal.items():
        if formal.get(k) != v:
            return VerifyResult(False, f"bad_formal_{k}")

    T, eps = 0.0, 1.0
    # Boundary fixtures (equality asymmetry)
    fixtures = [
        # (x, expect_pass_pres, expect_fail_pres, expect_unstable)
        (2.0, True, False, False),   # x > T+ε
        (1.0, True, False, False),   # x = T+ε  — pass preserved (non-strict)
        (0.5, False, False, True),   # (T, T+ε)
        (0.0, False, False, True),   # x = T
        (-0.5, False, False, True),  # (T-ε, T)
        (-1.0, False, False, True),  # x = T-ε — NOT fail-preserved
        (-2.0, False, True, False),  # x < T-ε
    ]
    for x, ep, ef, eu in fixtures:
        if pass_preserved(x, T, eps) != ep:
            return VerifyResult(False, f"fixture_pass_x={x}")
        if fail_preserved(x, T, eps) != ef:
            return VerifyResult(False, f"fixture_fail_x={x}")
        if unstable_region(x, T, eps) != eu:
            return VerifyResult(False, f"fixture_unstable_x={x}")

    # ε = 0: always invariant; unstable band empty
    for x in (-1.0, 0.0, 1.0):
        if unstable_region(x, T, 0.0):
            return VerifyResult(False, "eps0_unstable")
        if above_threshold(x, T) == 1 and not pass_preserved(x, T, 0.0):
            return VerifyResult(False, "eps0_pass")
        if above_threshold(x, T) == 0 and not fail_preserved(x, T, 0.0):
            return VerifyResult(False, "eps0_fail")

    # Sharpness at boundaries
    if adversarial_break_pass(0.5, T, eps) is None:
        return VerifyResult(False, "missing_pass_break")
    if adversarial_break_fail(-0.5, T, eps) is None:
        return VerifyResult(False, "missing_fail_break")
    if adversarial_break_pass(1.0, T, eps) is not None:
        return VerifyResult(False, "spurious_break_at_T_plus_eps")
    if adversarial_break_fail(-1.0, T, eps) is None:
        # at T-ε, fail CAN be broken
        return VerifyResult(False, "missing_break_at_T_minus_eps")
    br = adversarial_break_fail(-1.0, T, eps)
    if br is None or above_threshold(br, T) != 1:
        return VerifyResult(False, "break_at_T_minus_eps_ineffective")

    # Negative threshold + large values
    if not pass_preserved(10.0, -100.0, 1.0):
        return VerifyResult(False, "neg_T_pass")
    if not fail_preserved(-1e9, 0.0, 1.0):
        return VerifyResult(False, "large_neg_fail")

    # Malformed
    for bad in (math.nan, math.inf, -math.inf):
        try:
            ThresholdInstance(bad, 0.0)
            return VerifyResult(False, "accepted_nonfinite_x")
        except ValueError:
            pass
        try:
            ThresholdInstance(0.0, bad)
            return VerifyResult(False, "accepted_nonfinite_T")
        except ValueError:
            pass
    try:
        pass_preserved(0.0, 0.0, -0.1)
        return VerifyResult(False, "accepted_neg_eps")
    except ValueError:
        pass

    failures = _property_trials(random.Random(0))
    if failures:
        return VerifyResult(False, "property_trial_failed", tuple(failures[:3]))

    sharpness = claim.get("sharpness_statement")
    if sharpness and sharpness != SHARPNESS_STATEMENT_DET:
        return VerifyResult(False, "sharpness_statement_mismatch")

    # Sequential smoke (not privacy): first crossing + noisy
    if first_crossing((0.0, 0.5, 2.0), 1.0) != 2:
        return VerifyResult(False, "seq_first_crossing")
    if first_crossing((0.0, 0.5), 1.0) is not None:
        return VerifyResult(False, "seq_no_crossing")
    if noisy_first_crossing((0.0, 0.5), 1.0, (0.0, 0.6), 0.0) != 1:
        return VerifyResult(False, "seq_noisy_crossing")

    return VerifyResult(True, "threshold_preservation_discharged")


def verify_bounded_noise_threshold(claim: dict[str, Any]) -> VerifyResult:
    if not claim_is_bounded_noise_threshold(claim):
        return VerifyResult(False, "not_bounded_noise_claim")

    if str(claim.get("statement", "")).strip() != THEOREM_STATEMENT_NOISY.strip():
        return VerifyResult(False, "statement_mismatch")

    formal = claim.get("formal")
    if formal is None:
        formal = {}
    if not isinstance(formal, dict):
        return VerifyResult(False, "bad_formal_type")
    if formal.get("noise_model") != "almost_sure_bounded |xi| <= eta":
        return VerifyResult(False, "bad_noise_model")
    if formal.get("pass_condition") != "x >= T + eta":
        return VerifyResult(False, "bad_pass_condition")
    if formal.get("fail_condition") != "x < T - eta":
        return VerifyResult(False, "bad_fail_condition")
    if formal.get("not_claimed") != "full_sparse_vector_privacy":
        return VerifyResult(False, "must_disclaim_sparse_vector")

    # Pathwise safe regions: same as deterministic with ε := η
    T, eta = 0.0, 1.5
    if not pass_preserved(2.0, T, eta):
        return VerifyResult(False, "noisy_pass_safe")
    if not fail_preserved(-2.0, T, eta):
        return VerifyResult(False, "noisy_fail_safe")
    if not unstable_region(0.0, T, eta):
        return VerifyResult(False, "noisy_unstable")

    # η=0: unstable band empty; every output is deterministic (vacuous part 3)
    if unstable_region(0.0, T, 0.0):
        return VerifyResult(False, "eta0_unstable")
    if above_threshold(1.0 + 0.0, T) != 1 or above_threshold(-1.0 + 0.0, T) != 0:
        return VerifyResult(False, "eta0_deterministic")
    # Safe regions
    for xi in (-eta, eta):
        if above_threshold(2.0 + xi, T) != 1:
            return VerifyResult(False, "two_point_pass_safe")
    for xi in (-eta, eta):
        if above_threshold(-2.0 + xi, T) != 0:
            return VerifyResult(False, "two_point_fail_safe")
    # Full unstable band including critical endpoint x=T-η
    for x in (T - eta, T - eta / 2, T, T + eta / 2, T + eta - 1e-9):
        if not unstable_region(x, T, eta):
            return VerifyResult(False, f"band_flag_x={x}")
        outs = {above_threshold(x + xi, T) for xi in (-eta, eta)}
        if outs != {0, 1}:
            return VerifyResult(False, f"two_point_band_x={x}")
    # At x=T+η pass is a.s. under every |ξ|≤η
    for xi in (-eta, 0.0, eta):
        if above_threshold(T + eta + xi, T) != 1:
            return VerifyResult(False, "noisy_at_T_plus_eta")

    # Abstention strict fail boundary (certified stabilizer)
    if abstaining_threshold(T - eta, T, eta) is not None:
        return VerifyResult(False, "abstain_must_bot_at_T_minus_tau")
    if abstaining_threshold(T + eta, T, eta) != 1:
        return VerifyResult(False, "abstain_pass_boundary")
    if abstaining_threshold(T - eta - 1e-9, T, eta) != 0:
        return VerifyResult(False, "abstain_fail_strict")

    # Laplace closed-form identity at known points (utility, not DP)
    # P(ξ ≥ −m) for Lap(0,1): m=0 → 1/2; m=ln2 → 1 - 1/4 = 0.75; m=−ln2 → 1/4
    if abs(laplace_pass_probability(0.0, 0.0, 1.0) - 0.5) > 1e-12:
        return VerifyResult(False, "laplace_at_threshold")
    if abs(laplace_pass_probability(math.log(2.0), 0.0, 1.0) - 0.75) > 1e-12:
        return VerifyResult(False, "laplace_closed_form_pos")
    if abs(laplace_pass_probability(-math.log(2.0), 0.0, 1.0) - 0.25) > 1e-12:
        return VerifyResult(False, "laplace_closed_form_neg")
    if laplace_pass_probability(10.0, 0.0, 1.0) <= laplace_pass_probability(1.0, 0.0, 1.0):
        return VerifyResult(False, "laplace_margin_monotone")
    for x, scale in ((1.0, 1.0), (-1.0, 0.5), (0.0, 2.0)):
        p = laplace_pass_probability(x, T, scale)
        if not (0.0 <= p <= 1.0):
            return VerifyResult(False, "laplace_prob_range")

    try:
        laplace_pass_probability(0.0, 0.0, 0.0)
        return VerifyResult(False, "accepted_bad_scale")
    except ValueError:
        pass

    sharpness = claim.get("sharpness_statement")
    if sharpness and sharpness != SHARPNESS_STATEMENT_NOISY:
        return VerifyResult(False, "sharpness_statement_mismatch")

    return VerifyResult(
        True,
        "bounded_noise_threshold_discharged",
        limitations=(
            "COMPUTATIONAL_VERIFICATION_NOT_LEAN",
            "SCALAR_FINITE_SCORES_ONLY",
            "BOUNDED_NOISE_NOT_FULL_SVT",
            "LAPLACE_CDF_IDENTITY_NOT_DP_PROOF",
        ),
    )
