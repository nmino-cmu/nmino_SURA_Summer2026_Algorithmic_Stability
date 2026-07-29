"""Discovery for abs-threshold."""

from __future__ import annotations

from typing import Any

from operators.absolute_value_threshold.math import (
    EVALUATION_METHOD,
    OPERATOR,
    SHARPNESS_STATEMENT,
    THEOREM_ID,
    THEOREM_STATEMENT,
)
from system_a import engines as a_engines
from system_a.ir import DiscoveryIR
from system_a.ownership import CLASS_OWNER


def discover_abs_threshold(ir: DiscoveryIR) -> dict[str, Any]:
    op = a_engines.run_operator_analyzer(
        ir,
        {
            "name": OPERATOR,
            "form": "A(x)=1{|x|>=T}",
            "input_type": "finite x; T>=0",
            "output_type": "{0,1}",
            "perturbation_model": "|x'-x|<=epsilon",
            "reduction": "threshold on |x|",
        },
    )
    instab = a_engines.run_instability_characterization(ir, op.version_ids[0])
    qty = a_engines.run_structural_quantity(ir, op.version_ids[0])
    mech = a_engines.run_mechanism(ir, qty.version_ids[0])
    psi = a_engines.run_psi_construction(ir, mech.version_ids[0])
    assum = a_engines.run_assumptions(ir, "Finite x; T>=0; epsilon>=0; |x|>=T passes.")
    claim = {
        "statement": THEOREM_STATEMENT,
        "chain_segment": "inference",
        "operator": OPERATOR,
        "theorem_id": THEOREM_ID,
        "evaluation": EVALUATION_METHOD,
        "sharpness_statement": SHARPNESS_STATEMENT,
        "formal": {
            "equality_convention": "|x| >= T passes",
            "perturbation": "|x'-x| <= epsilon",
            "pass_condition": "|x| >= T + epsilon",
            "fail_condition": "|x| + epsilon < T",
            "T_nonnegative": "T >= 0",
        },
    }
    tip = ir.mint(
        artifact_class="TheoremCandidate",
        caller_module=CLASS_OWNER["TheoremCandidate"],
        payload=claim,
    ).version_id
    sketch = a_engines.run_proof_strategy(ir, tip)
    bridge = a_engines.run_bridge(ir, tip, qty.version_ids[0])
    util = a_engines.run_utility_tradeoff(ir, [tip])
    open_q = a_engines.run_open_questions(ir, "Signed two-sided bands vs radial threshold.")
    cex = a_engines.run_conjecture(ir, "Radial threshold inherits asymmetric equality from |x|>=T.")
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
