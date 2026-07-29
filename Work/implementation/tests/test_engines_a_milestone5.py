"""Milestone 5 — System A mathematical engines."""

from system_a.engines import (
    assert_no_seal_submit_authority,
    consume_verifier_prior,
    run_assumptions,
    run_bridge,
    run_conjecture,
    run_engine_safe,
    run_instability_characterization,
    run_literature,
    run_mechanism,
    run_open_questions,
    run_operator_analyzer,
    run_pareto_portfolio,
    run_proof_strategy,
    run_psi_construction,
    run_soft_attack,
    run_structural_quantity,
    run_theorem,
    run_utility_tradeoff,
)
from system_a.ir import DiscoveryIR, OwnershipError
from system_a.ownership import CLASS_OWNER
import pytest


def test_each_engine_typed_ir_and_speculation():
    ir = DiscoveryIR("e")
    op = run_operator_analyzer(ir, {"op": "argmax"})
    assert ir.versions[op.version_ids[0]].artifact_class == "OperatorAnalysis"
    inst = run_instability_characterization(ir, op.version_ids[0])
    assert ir.versions[inst.version_ids[0]].payload["speculative"] is True
    run_structural_quantity(ir, op.version_ids[0])
    run_mechanism(ir, op.version_ids[0])
    run_psi_construction(ir, op.version_ids[0])
    th = run_theorem(ir, "1+1=2")
    run_conjecture(ir, "maybe")
    run_bridge(ir, "a", "b")
    run_proof_strategy(ir, th.version_ids[0])
    run_assumptions(ir, "A")
    run_utility_tradeoff(ir, th.version_ids)
    run_open_questions(ir, "Q?")
    pf = run_pareto_portfolio(ir, th.version_ids)
    assert ir.versions[pf.version_ids[0]].payload["diverse"] is True
    sa = run_soft_attack(ir, th.version_ids[0])
    assert ir.versions[sa.version_ids[0]].payload["authoritative"] is False
    run_literature(ir, "ref")
    consume_verifier_prior(ir, {"export_ref": "e1"})


def test_ownership_and_no_seal_authority():
    ir = DiscoveryIR("e")
    with pytest.raises(OwnershipError):
        ir.mint(artifact_class="TheoremCandidate", caller_module="SOFT_ATTACK", payload={})
    assert_no_seal_submit_authority("SOFT_ATTACK")
    assert CLASS_OWNER["SealedCRPSnapshot"] != "SOFT_ATTACK"


def test_engine_failure_isolated():
    ir = DiscoveryIR("e")
    ir.close()
    r = run_engine_safe(run_theorem, ir, "x")
    assert r.error


def test_packager_not_called_by_engines():
    import system_a.engines as m

    src = open(m.__file__).read()
    assert "seal_draft" not in src
    assert "from art_int.seal" not in src
    assert "SubmissionEnvelope" not in src
