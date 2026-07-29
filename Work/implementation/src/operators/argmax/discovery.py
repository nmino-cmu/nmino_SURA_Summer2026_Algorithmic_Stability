"""Discovery IR population for the argmax operator (typed artifacts)."""

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


def discover_argmax(ir: DiscoveryIR) -> dict[str, Any]:
    """Run Discovery engines for argmax; return tip version ids and theorem payload."""
    op = a_engines.run_operator_analyzer(
        ir,
        {
            "name": OPERATOR,
            "form": "argmax_{i in [m]} s_i(D)",
            "decomposition": {
                "score_map": "s: D → ℝ^m",
                "selection": "unique or set-valued maximizers",
                "instability": "near-ties / ties under infinitesimal score noise",
            },
        },
    )
    instab = a_engines.run_instability_characterization(ir, op.version_ids[0])
    qty = a_engines.run_structural_quantity(ir, op.version_ids[0])
    # overwrite quantity tip with precise margin definition via mechanism + psi
    mech = a_engines.run_mechanism(ir, qty.version_ids[0])
    psi = a_engines.run_psi_construction(ir, mech.version_ids[0])
    assum = a_engines.run_assumptions(
        ir,
        "Finite m≥2; scores in ℝ^m; unique maximizer; perturbations δ with ||δ||_∞≤ε.",
    )
    claim_payload = {
        "statement": THEOREM_STATEMENT,
        "chain_segment": "inference",
        "operator": OPERATOR,
        "theorem_id": THEOREM_ID,
        "evaluation": EVALUATION_METHOD,
        "sharpness_statement": SHARPNESS_STATEMENT,
        "formal": {
            "perturbation_norm": "linf",
            "margin_definition": "s_i_star - max_{j!=i_star} s_j",
            "invariance_condition": "gamma > 2*epsilon",
            "sharpness": "gamma <= 2*epsilon admits adversarial delta",
        },
    }
    th = a_engines.run_theorem(ir, THEOREM_STATEMENT, evaluation=EVALUATION_METHOD)
    tip = th.version_ids[0]
    # Replace payload with full structured claim (same lineage tip via re-mint)
    from system_a.ownership import CLASS_OWNER

    tip = ir.mint(
        artifact_class="TheoremCandidate",
        caller_module=CLASS_OWNER["TheoremCandidate"],
        payload=claim_payload,
    ).version_id
    sketch = a_engines.run_proof_strategy(ir, tip)
    bridge = a_engines.run_bridge(ir, tip, qty.version_ids[0])
    util = a_engines.run_utility_tradeoff(ir, [tip])
    open_q = a_engines.run_open_questions(
        ir,
        "Extension to ties (set-valued argmax), ℓ_p balls, and data-dependent score maps s_i(D).",
    )
    cex = a_engines.run_conjecture(
        ir,
        "At γ=2ε the adversarial ∞-ball perturbation forces a tie or winner change (sharpness).",
    )
    soft = a_engines.run_soft_attack(ir, tip)
    port = a_engines.run_pareto_portfolio(ir, [tip])
    return {
        "operator": op.version_ids[0],
        "instability": instab.version_ids[0],
        "quantity": qty.version_ids[0],
        "mechanism": mech.version_ids[0],
        "psi": psi.version_ids[0],
        "assumptions": assum.version_ids[0],
        "theorem_plain": th.version_ids[0],
        "theorem": tip,
        "proof_sketch": sketch.version_ids[0],
        "bridge": bridge.version_ids[0],
        "utility": util.version_ids[0],
        "open_questions": open_q.version_ids[0],
        "sharpness_conjecture": cex.version_ids[0],
        "soft_attack": soft.version_ids,
        "portfolio": port.version_ids[0],
        "claim_payload": claim_payload,
    }
