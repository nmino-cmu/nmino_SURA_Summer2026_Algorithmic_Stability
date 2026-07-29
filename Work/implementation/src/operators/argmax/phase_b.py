"""Phase B: selection_stability packaging for argmax under structured ℓ∞ score perturbation.

Advances the Area-1 charter chain hop
  Q_ψ (mechanism) → selection_application (argmax) → selection_stability
without inventing new mathematics beyond the Lean-certified margin theorem.
"""

from __future__ import annotations

from typing import Any

from operators.argmax.math import (
    EVALUATION_METHOD,
    OPERATOR,
    SHARPNESS_STATEMENT,
    THEOREM_ID,
    THEOREM_STATEMENT,
)
from system_a import engines as a_engines
from system_a.ir import DiscoveryIR
from system_a.ownership import CLASS_OWNER

# Structured perturbation mechanism (Q_ψ) — adversarial closed ℓ∞ ball on scores.
# Honest: not Laplace / DP; KNOWN_MECHANISM baseline for deterministic robustness.
LINF_SCORE_BALL_MECHANISM: dict[str, Any] = {
    "local_id": "qpsi-linf-score-ball",
    "family": "additive_score_perturbation",
    "norm": "linf",
    "law": "adversarial_closed_ball",
    "domain": "Fin_m_to_Real",
    "parameter_schema": {"epsilon": "nonneg_real"},
    "novelty_ladder": "KNOWN_MECHANISM",
    "literature_refs": ["classical_linf_margin_robustness"],
    "non_claims": ["differential_privacy", "post_hoc_inference", "policy_validity"],
}


def discover_argmax_selection_stability(ir: DiscoveryIR) -> dict[str, Any]:
    """Discovery IR for Phase B selection_stability CRP (mechanism required)."""
    op = a_engines.run_operator_analyzer(
        ir,
        {
            "name": OPERATOR,
            "form": "argmax_{i in [m]} s_i",
            "role": "selection_operator",
            "charter_chain": "selection_application",
        },
    )
    instab = a_engines.run_instability_characterization(ir, op.version_ids[0])
    qty = a_engines.run_structural_quantity(ir, op.version_ids[0])
    mech = ir.mint(
        artifact_class="MechanismProposal",
        caller_module=CLASS_OWNER["MechanismProposal"],
        payload=dict(LINF_SCORE_BALL_MECHANISM),
    )
    assum = a_engines.run_assumptions(
        ir,
        "Finite m≥2; s∈ℝ^m; unique maximizer; Q_ψ = adversarial closed ℓ∞ ball "
        "of radius ε≥0 on scores; chain_segment=selection_stability. "
        "No DP / post-hoc inference / policy claim.",
    )
    claim_payload = {
        "statement": THEOREM_STATEMENT,
        "chain_segment": "selection_stability",
        "operator": OPERATOR,
        "theorem_id": THEOREM_ID,
        "evaluation": EVALUATION_METHOD,
        "sharpness_statement": SHARPNESS_STATEMENT,
        "perturbation_mechanism_id": LINF_SCORE_BALL_MECHANISM["local_id"],
        "guarantee_kind": "UNIQUE_MAXIMIZER_PRESERVATION",
        "formal": {
            "perturbation_norm": "linf",
            "margin_definition": "s_i_star - max_{j!=i_star} s_j",
            "invariance_condition": "gamma > 2*epsilon",
            "sharpness": "gamma <= 2*epsilon admits adversarial delta",
            "phase": "PHASE_B_STABILIZATION",
            "mechanism_local_id": LINF_SCORE_BALL_MECHANISM["local_id"],
        },
    }
    tip = ir.mint(
        artifact_class="TheoremCandidate",
        caller_module=CLASS_OWNER["TheoremCandidate"],
        payload=claim_payload,
    ).version_id
    sketch = a_engines.run_proof_strategy(ir, tip)
    util = a_engines.run_utility_tradeoff(ir, [tip])
    open_q = a_engines.run_open_questions(
        ir,
        "Next charter hops: utility certificates; composition; selected-object binding; "
        "post-hoc inference; stochastic Q_ψ (Laplace RNM) as separate KNOWN_MECHANISM cycles.",
    )
    return {
        "operator": op.version_ids[0],
        "instability": instab.version_ids[0],
        "quantity": qty.version_ids[0],
        "mechanism": mech.version_id,
        "assumptions": assum.version_ids[0],
        "theorem": tip,
        "proof_sketch": sketch.version_ids[0],
        "utility": util.version_ids[0],
        "open_questions": open_q.version_ids[0],
        "claim_payload": claim_payload,
        "mechanism_body": LINF_SCORE_BALL_MECHANISM,
    }
