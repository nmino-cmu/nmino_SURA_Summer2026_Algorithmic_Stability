"""Discovery IR population for multi-threshold."""

from __future__ import annotations

from typing import Any

from operators.multi_threshold.math import (
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
            "equality_convention": "x >= T_i passes per coordinate",
            "perturbation": "|x'-x| <= epsilon",
            "output": "count of passed thresholds",
            "stability": "every coordinate OutsideThresholdUnstableBand",
            "reduction": "coordinatewise AboveThreshold preservation",
        },
    }


def discover_multi_threshold(ir: DiscoveryIR) -> dict[str, Any]:
    op = a_engines.run_operator_analyzer(
        ir,
        {
            "name": OPERATOR,
            "form": "C_T(x) = |{i: x >= T_i}|",
            "input_type": "finite score x; finite threshold list T",
            "output_type": "Nat count in 0..n",
            "equality": "per-coordinate x >= T_i passes",
            "perturbation_model": "|x'-x| <= epsilon",
            "decision_boundary": "union of cuts T_i",
            "structural_quantity": "coordinatewise buffers to each T_i",
            "reduction": "sum of AboveThreshold indicators",
        },
    )
    instab = a_engines.run_instability_characterization(ir, op.version_ids[0])
    qty = a_engines.run_structural_quantity(ir, op.version_ids[0])
    mech = a_engines.run_mechanism(ir, qty.version_ids[0])
    psi = a_engines.run_psi_construction(ir, mech.version_ids[0])
    assum = a_engines.run_assumptions(
        ir,
        "Finite real score x; finite list of finite thresholds; epsilon>=0; "
        "equality x>=T_i passes per cut; neighboring scores |x'-x|<=epsilon.",
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
    open_q = a_engines.run_open_questions(
        ir,
        "Ordered cut-point bucket indices and interval-membership selectors are "
        "separate operators; this module certifies the unordered pass-count.",
    )
    cex = a_engines.run_conjecture(
        ir,
        "Any single unstable cut flips the multi-threshold count.",
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
