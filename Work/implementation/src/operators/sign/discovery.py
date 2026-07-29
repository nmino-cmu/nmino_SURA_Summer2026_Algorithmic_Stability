"""Discovery IR for sign."""

from __future__ import annotations

from typing import Any

from operators.sign.math import (
    EVALUATION_METHOD,
    OPERATOR,
    SHARPNESS_STATEMENT,
    THEOREM_ID,
    THEOREM_STATEMENT,
)
from system_a import engines as a_engines
from system_a.ir import DiscoveryIR
from system_a.ownership import CLASS_OWNER


def _claim() -> dict[str, Any]:
    return {
        "statement": THEOREM_STATEMENT,
        "chain_segment": "inference",
        "operator": OPERATOR,
        "theorem_id": THEOREM_ID,
        "evaluation": EVALUATION_METHOD,
        "sharpness_statement": SHARPNESS_STATEMENT,
        "formal": {
            "equality_convention": "sign(0)=0; strict for nonzero",
            "perturbation": "|x'-x| <= epsilon",
            "plus_condition": "x > epsilon",
            "minus_condition": "x < -epsilon",
            "zero_condition": "epsilon = 0 and x = 0",
        },
    }


def discover_sign(ir: DiscoveryIR) -> dict[str, Any]:
    op = a_engines.run_operator_analyzer(
        ir,
        {
            "name": OPERATOR,
            "form": "sign(x) in {-1,0,1}",
            "input_type": "finite score x",
            "output_type": "{-1,0,1}",
            "perturbation_model": "|x'-x| <= epsilon",
            "decision_boundary": "{0}",
            "structural_quantity": "|x| vs epsilon with strict sides",
        },
    )
    instab = a_engines.run_instability_characterization(ir, op.version_ids[0])
    qty = a_engines.run_structural_quantity(ir, op.version_ids[0])
    mech = a_engines.run_mechanism(ir, qty.version_ids[0])
    psi = a_engines.run_psi_construction(ir, mech.version_ids[0])
    assum = a_engines.run_assumptions(
        ir,
        "Finite real score x; epsilon>=0; sign(0)=0; neighboring |x'-x|<=epsilon.",
    )
    claim = _claim()
    tip = ir.mint(
        artifact_class="TheoremCandidate",
        caller_module=CLASS_OWNER["TheoremCandidate"],
        payload=claim,
    ).version_id
    sketch = a_engines.run_proof_strategy(ir, tip)
    bridge = a_engines.run_bridge(ir, tip, qty.version_ids[0])
    util = a_engines.run_utility_tradeoff(ir, [tip])
    open_q = a_engines.run_open_questions(ir, "Relation to thresholding at T=0 with ternary output.")
    cex = a_engines.run_conjecture(ir, "Zero is unstable for every ε>0.")
    soft = a_engines.run_soft_attack(ir, tip)
    port = a_engines.run_pareto_portfolio(ir, [tip])
    return {
        "operator": op.version_ids[0],
        "instability": instab.version_ids[0],
        "quantity": qty.version_ids[0],
        "mechanism": mech.version_ids[0],
        "psi": psi.version_ids[0],
        "assumptions": assum.version_ids[0],
        "theorem": tip,
        "proof_sketch": sketch.version_ids[0],
        "bridge": bridge.version_ids[0],
        "utility": util.version_ids[0],
        "open_questions": open_q.version_ids[0],
        "sharpness_conjecture": cex.version_ids[0],
        "soft_attack": soft.version_ids,
        "portfolio": port.version_ids[0],
        "claim_payload": claim,
    }
