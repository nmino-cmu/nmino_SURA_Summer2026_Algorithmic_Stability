"""Computational discharge of argmax bounded-perturbation-margin obligations."""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Any

from operators.argmax.math import (
    EVALUATION_METHOD,
    OPERATOR,
    SHARPNESS_STATEMENT,
    THEOREM_ID,
    THEOREM_STATEMENT,
    ArgmaxInstance,
    adversarial_break,
    apply_perturbation,
    invariance_holds,
    linf_norm,
)


@dataclass(frozen=True)
class VerifyResult:
    ok: bool
    detail: str
    counterexamples: tuple[dict[str, Any], ...] = ()
    limitations: tuple[str, ...] = (
        "COMPUTATIONAL_VERIFICATION_NOT_LEAN",
        "FINITE_SCORE_VECTORS_ONLY",
    )


def claim_is_argmax_margin(claim: dict[str, Any]) -> bool:
    return (
        claim.get("operator") == OPERATOR
        and claim.get("theorem_id") == THEOREM_ID
        and claim.get("evaluation") == EVALUATION_METHOD
    )


def _check_algebraic_lemma(epsilon: float, gamma: float) -> bool:
    """Worst-case bound: s_{i*}−ε − (s_j+ε) = gap_j − 2ε ≥ γ − 2ε."""
    return gamma - 2 * epsilon > 0


def _property_trials(rng: random.Random, n: int = 200) -> list[dict[str, Any]]:
    failures: list[dict[str, Any]] = []
    for _ in range(n):
        m = rng.randint(2, 8)
        scores = tuple(rng.uniform(-5, 5) for _ in range(m))
        # force unique winner
        i = max(range(m), key=lambda k: scores[k])
        bumped = list(scores)
        bumped[i] = max(scores) + rng.uniform(0.01, 3.0)
        scores = tuple(bumped)
        gamma = ArgmaxInstance(scores).margin()
        assert gamma is not None and gamma > 0
        eps = rng.uniform(0, gamma)  # may be above or below γ/2
        if invariance_holds(scores, eps):
            # sample random δ in ball; must preserve
            for _ in range(20):
                delta = tuple(rng.uniform(-eps, eps) for _ in range(m))
                assert linf_norm(delta) <= eps + 1e-12
                new = ArgmaxInstance(apply_perturbation(scores, delta))
                if new.unique_maximizer() != i:
                    failures.append({"scores": scores, "eps": eps, "delta": delta, "kind": "invariance"})
                    break
        else:
            br = adversarial_break(scores, eps)
            if br is None:
                failures.append({"scores": scores, "eps": eps, "kind": "missing_break"})
                continue
            new = ArgmaxInstance(apply_perturbation(scores, br))
            if new.unique_maximizer() == i and len(new.maximizers()) == 1:
                failures.append({"scores": scores, "eps": eps, "delta": br, "kind": "break_failed"})
    return failures


def verify_margin_theorem(claim: dict[str, Any]) -> VerifyResult:
    """Discharge obligations for the canonical margin theorem claim."""
    if not claim_is_argmax_margin(claim):
        return VerifyResult(False, "not_argmax_margin_claim")

    stmt = str(claim.get("statement", "")).strip()
    if stmt != THEOREM_STATEMENT.strip():
        return VerifyResult(False, "statement_mismatch")

    formal = claim.get("formal") or {}
    if formal.get("perturbation_norm") != "linf":
        return VerifyResult(False, "bad_perturbation_model")
    if formal.get("invariance_condition") != "gamma > 2*epsilon":
        return VerifyResult(False, "bad_invariance_condition")
    if formal.get("margin_definition") != "s_i_star - max_{j!=i_star} s_j":
        return VerifyResult(False, "bad_margin_definition")

    # algebraic core at symbolic boundary samples
    for gamma, eps in ((1.0, 0.4), (1.0, 0.5), (2.0, 0.9), (0.1, 0.0)):
        expect = gamma > 2 * eps
        if _check_algebraic_lemma(eps, gamma) != expect:
            return VerifyResult(False, "algebraic_lemma_failed")

    # concrete invariance / sharpness fixtures
    scores = (3.0, 1.0, 0.5)
    if not invariance_holds(scores, 0.9):  # γ=2 > 1.8
        return VerifyResult(False, "fixture_invariance")
    if invariance_holds(scores, 1.0):  # γ=2 ≯ 2
        return VerifyResult(False, "fixture_boundary_should_fail")
    br = adversarial_break(scores, 1.0)
    if br is None:
        return VerifyResult(False, "fixture_no_adversary")
    after = ArgmaxInstance(apply_perturbation(scores, br))
    if after.unique_maximizer() == 0 and len(after.maximizers()) == 1:
        return VerifyResult(False, "fixture_adversary_ineffective", ({"delta": br},))

    # ties: no unique maximizer ⇒ invariance false
    if invariance_holds((1.0, 1.0), 0.0):
        return VerifyResult(False, "tie_should_not_invariance")

    # malformed
    try:
        ArgmaxInstance((1.0,))
        return VerifyResult(False, "m1_scores_accepted")
    except ValueError:
        pass

    failures = _property_trials(random.Random(0))
    if failures:
        return VerifyResult(False, "property_trial_failed", tuple(failures[:3]))

    # sharpness statement present when claimed
    sharpness = claim.get("sharpness_statement")
    if sharpness and sharpness != SHARPNESS_STATEMENT:
        return VerifyResult(False, "sharpness_statement_mismatch")

    return VerifyResult(True, "argmax_margin_discharged")
