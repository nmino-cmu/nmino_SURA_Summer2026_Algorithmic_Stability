"""Bundle round-trip tests."""

from pathlib import Path

from operators.argmax.workflow import run_argmax_margin_workflow
from system_b.lean.bundle import load_bundle


def test_export_and_load_bundle(tmp_path: Path):
    r = run_argmax_margin_workflow(export_lean_bundle=True)
    assert r.audit_verdict == "PASS"
    assert r.lean_bundle_path
    b = load_bundle(Path(r.lean_bundle_path))
    assert b.crp_digest == r.crp_digest
    assert b.bundle_digest
    assert b.verification_run["audit_verdict"] == "PASS"
