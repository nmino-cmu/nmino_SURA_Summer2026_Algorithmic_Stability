"""Eligibility matrix."""

from pathlib import Path

from operators.argmax.workflow import run_argmax_margin_workflow
from system_b.lean.bundle import load_bundle
from system_b.lean.eligibility import check_eligibility


def test_pass_eligible():
    r = run_argmax_margin_workflow(export_lean_bundle=True)
    b = load_bundle(Path(r.lean_bundle_path))
    elig = check_eligibility(b)
    assert elig.ok
    assert elig.claim is not None


def test_demo_rejected():
    r = run_argmax_margin_workflow(export_lean_bundle=True)
    b = load_bundle(Path(r.lean_bundle_path))
    # mutate to DEMO
    for c in b.sealed_crp["payload"]["claims"]:
        if c.get("theorem_id") == "bounded-perturbation-margin":
            c["evaluation"] = "DEMO_TAUTOLOGY"
    elig = check_eligibility(b)
    assert not elig.ok
    assert "DEMO_EVALUATION" in elig.reason_codes or "NO_PROFILE_MATCH" in elig.reason_codes


def test_fail_audit_rejected():
    r = run_argmax_margin_workflow(export_lean_bundle=True)
    b = load_bundle(Path(r.lean_bundle_path))
    b.verification_run["audit_verdict"] = "FAIL"
    elig = check_eligibility(b)
    assert not elig.ok


def test_receipt_claim_mismatch():
    r = run_argmax_margin_workflow(export_lean_bundle=True)
    b = load_bundle(Path(r.lean_bundle_path))
    b.receipt["draft_claim_digests"] = ["00" * 32]
    elig = check_eligibility(b)
    assert not elig.ok
    assert "RECEIPT_CLAIM_MISMATCH" in elig.reason_codes


def test_crp_digest_tamper():
    r = run_argmax_margin_workflow(export_lean_bundle=True)
    b = load_bundle(Path(r.lean_bundle_path))
    b.crp_digest = "00" * 32
    elig = check_eligibility(b)
    assert not elig.ok
    assert "CRP_DIGEST_MISMATCH" in elig.reason_codes
