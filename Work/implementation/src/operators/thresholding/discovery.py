"""Discovery IR population for the thresholding operator."""

from __future__ import annotations

from typing import Any

from operators.thresholding.math import (
    EVALUATION_METHOD_DET,
    EVALUATION_METHOD_NOISY,
    LEVEL_STATUS,
    OPERATOR,
    SHARPNESS_STATEMENT_DET,
    SHARPNESS_STATEMENT_NOISY,
    THEOREM_ID_DETERMINISTIC,
    THEOREM_ID_NOISY,
    THEOREM_STATEMENT_DET,
    THEOREM_STATEMENT_NOISY,
    SequentialLevel,
)
from system_a import engines as a_engines
from system_a.ir import DiscoveryIR
from system_a.ownership import CLASS_OWNER


def _claim_det() -> dict[str, Any]:
    return {
        "statement": THEOREM_STATEMENT_DET,
        "chain_segment": "inference",
        "operator": OPERATOR,
        "theorem_id": THEOREM_ID_DETERMINISTIC,
        "evaluation": EVALUATION_METHOD_DET,
        "sharpness_statement": SHARPNESS_STATEMENT_DET,
        "formal": {
            "equality_convention": "x >= T passes",
            "perturbation": "|x'-x| <= epsilon",
            "pass_condition": "x >= T + epsilon",
            "fail_condition": "x < T - epsilon",
            "unstable_region": "[T - epsilon, T + epsilon)",
            "signed_margin": "m = x - T",
            "distance": "d = |x - T|",
        },
    }


def _claim_noisy() -> dict[str, Any]:
    return {
        "statement": THEOREM_STATEMENT_NOISY,
        "chain_segment": "inference",
        "operator": OPERATOR,
        "theorem_id": THEOREM_ID_NOISY,
        "evaluation": EVALUATION_METHOD_NOISY,
        "sharpness_statement": SHARPNESS_STATEMENT_NOISY,
        "formal": {
            "noise_model": "almost_sure_bounded |xi| <= eta",
            "mechanism": "1{x + xi >= T}",
            "pass_condition": "x >= T + eta",
            "fail_condition": "x < T - eta",
            "unstable_region": "[T - eta, T + eta)",
            "not_claimed": "full_sparse_vector_privacy",
        },
    }


def discover_thresholding(ir: DiscoveryIR) -> dict[str, Any]:
    """Run Discovery engines for thresholding; return tip ids and claim payloads."""
    op = a_engines.run_operator_analyzer(
        ir,
        {
            "name": OPERATOR,
            "form": "A_T(x) = 1{x >= T}",
            "input_type": "x in R (finite score)",
            "output_type": "{0,1}",
            "threshold": "fixed T in R (not data-dependent in scalar module)",
            "equality": "x >= T passes",
            "non_finite": "rejected at construction",
            "perturbation_model": "|x'-x| <= epsilon",
            "neighboring_data": "abstracted as score perturbation of radius epsilon",
            "downstream_selected": "pass/fail bit (sequential: first crossing index)",
            "downstream_inference": "selection-conditional inference when status stable",
            "downstream_utility": "margin |x-T| and abstention tradeoff",
            "decomposition": {
                "score_computation": "x(D) provided abstractly",
                "threshold_retrieval": "fixed T",
                "comparison": "x >= T",
                "boolean_output": "{0,1}",
                "optional_sequential_stopping": "tau = min{t: q_t >= T}",
                "optional_positive_release_counting": "candidate (Sparse Vector level)",
            },
            "decision_boundary": "x = T",
            "signed_margin": "m = x - T",
            "distance": "d = |x - T|",
            "margin_roles": {
                "output_preservation": "compare |m| to epsilon with equality asymmetry",
                "pass_fail_asymmetry": "pass uses >= T+eps; fail uses < T-eps",
                "false_positive": "failing-side sharpness near T-eps",
                "false_negative": "passing-side sharpness in [T, T+eps)",
                "utility_loss": "distance d and abstention band tau",
            },
        },
    )
    instab = a_engines.run_instability_characterization(ir, op.version_ids[0])
    qty = a_engines.run_structural_quantity(ir, op.version_ids[0])
    mech = a_engines.run_mechanism(ir, qty.version_ids[0])
    # Portfolio of noisy / abstaining / set-valued / sequential candidates
    portfolio_specs = {
        "A_query_noise_only": "1{x+xi >= T}",
        "B_threshold_noise_only": "1{x >= T+zeta}",
        "C_query_and_threshold_noise": "1{x+xi >= T+zeta}, W=xi-zeta",
        "D_abstaining": "1 / 0 / bot with band tau",
        "E_set_valued": "{0}, {1}, or {0,1} from perturbation interval",
        "sequential_noisy_first_crossing": "min{t: q_t+xi_t >= T+zeta}",
        "level_status": {lv.value: st for lv, st in LEVEL_STATUS.items()},
        "sparse_vector_status": LEVEL_STATUS[SequentialLevel.FULL_SPARSE_VECTOR],
    }
    tip_mech = ir.mint(
        artifact_class="MechanismProposal",
        caller_module=CLASS_OWNER["MechanismProposal"],
        payload={"local_id": "threshold-portfolio", "of": qty.version_ids[0], "portfolio": portfolio_specs},
    ).version_id
    psi = a_engines.run_psi_construction(ir, tip_mech)
    assum = a_engines.run_assumptions(
        ir,
        "Finite real score x; fixed finite T; epsilon>=0; equality x>=T passes; "
        "non-finite inputs rejected; neighboring datasets abstracted as |x'-x|<=epsilon.",
    )
    claim_det = _claim_det()
    claim_noisy = _claim_noisy()
    th_plain = a_engines.run_theorem(ir, THEOREM_STATEMENT_DET, evaluation=EVALUATION_METHOD_DET)
    tip_det = ir.mint(
        artifact_class="TheoremCandidate",
        caller_module=CLASS_OWNER["TheoremCandidate"],
        payload=claim_det,
    ).version_id
    tip_noisy = ir.mint(
        artifact_class="TheoremCandidate",
        caller_module=CLASS_OWNER["TheoremCandidate"],
        payload=claim_noisy,
    ).version_id
    sketch = a_engines.run_proof_strategy(ir, tip_det)
    bridge = a_engines.run_bridge(ir, tip_det, qty.version_ids[0])
    # Bridge candidates (not claimed verified unless System B discharges)
    bridge_cands = ir.mint(
        artifact_class="BridgeProposalDraft",
        caller_module=CLASS_OWNER["BridgeProposalDraft"],
        payload={
            "candidates": [
                "deterministic margin certificate implies unchanged selected status",
                "P(threshold-output change) bounds selection instability",
                "noisy-threshold LR control implies a stability parameter (candidate)",
                "stable pass/fail enables valid downstream inference conditional on selection",
                "abstention band partitions certified vs uncertified regions",
                "limited positive releases control cumulative adaptive leakage (candidate)",
            ],
            "status": "CANDIDATE_NOT_VERIFIED",
            "left": tip_det,
            "right": tip_noisy,
            "speculative": True,
            "speculation_label": "SPECULATIVE",
        },
    ).version_id
    util = a_engines.run_utility_tradeoff(ir, [tip_det, tip_noisy])
    open_q = a_engines.run_open_questions(
        ir,
        "Adaptive query sequences, limited positive releases, and full Sparse Vector "
        "accounting remain candidates — not verified in this module.",
    )
    cex = a_engines.run_conjecture(
        ir,
        "Equality asymmetry: at x=T+ε pass is preserved; at x=T−ε fail is not.",
    )
    soft = a_engines.run_soft_attack(ir, tip_det)
    port = a_engines.run_pareto_portfolio(ir, [tip_det, tip_noisy])
    return {
        "operator": op.version_ids[0],
        "instability": instab.version_ids[0],
        "quantity": qty.version_ids[0],
        "mechanism": tip_mech,
        "mechanism_plain": mech.version_ids[0],
        "psi": psi.version_ids[0],
        "assumptions": assum.version_ids[0],
        "theorem_plain": th_plain.version_ids[0],
        "theorem": tip_det,
        "theorem_noisy": tip_noisy,
        "proof_sketch": sketch.version_ids[0],
        "bridge": bridge.version_ids[0],
        "bridge_candidates": bridge_cands,
        "utility": util.version_ids[0],
        "open_questions": open_q.version_ids[0],
        "sharpness_conjecture": cex.version_ids[0],
        "soft_attack": soft.version_ids,
        "portfolio": port.version_ids[0],
        "claim_payload": claim_det,
        "claim_payload_noisy": claim_noisy,
        "level_status": {lv.value: st for lv, st in LEVEL_STATUS.items()},
    }
