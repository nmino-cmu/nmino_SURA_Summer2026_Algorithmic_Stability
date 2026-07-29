"""Phase B: selection_stability packaging for argmax + ℓ∞ score ball."""

from art_int.enums import IntakeStatus
from operators.argmax.phase_b import LINF_SCORE_BALL_MECHANISM
from operators.argmax.workflow import run_argmax_selection_stability_workflow


def test_phase_b_selection_stability_workflow():
    r = run_argmax_selection_stability_workflow()
    assert r.intake_status == IntakeStatus.ACCEPTED_DRAFT.value
    assert r.audit_verdict == "PASS"
    assert not r.unresolved
    assert r.profile == "PHASE_B_STABILIZATION"
    assert r.chain_segment == "selection_stability"
    assert r.mechanism_local_id == LINF_SCORE_BALL_MECHANISM["local_id"]
    assert "COMPUTATIONAL_VERIFICATION_NOT_LEAN" in r.limitations
    assert "ARGMAX_MARGIN_COMPUTATIONAL_V1" in r.limitations


def test_phase_b_reuses_margin_math_not_new_theorem_id():
    """Charter hop is packaging; Lean profile keys stay identical."""
    from operators.argmax.math import THEOREM_ID, THEOREM_STATEMENT
    from operators.argmax.phase_b import discover_argmax_selection_stability
    from system_a.ir import DiscoveryIR

    tips = discover_argmax_selection_stability(DiscoveryIR("t"))
    claim = tips["claim_payload"]
    assert claim["theorem_id"] == THEOREM_ID
    assert claim["statement"] == THEOREM_STATEMENT
    assert claim["chain_segment"] == "selection_stability"
    assert claim["perturbation_mechanism_id"] == LINF_SCORE_BALL_MECHANISM["local_id"]
    assert claim["formal"]["phase"] == "PHASE_B_STABILIZATION"
    assert tips["mechanism_body"]["novelty_ladder"] == "KNOWN_MECHANISM"
    assert "differential_privacy" in tips["mechanism_body"]["non_claims"]
