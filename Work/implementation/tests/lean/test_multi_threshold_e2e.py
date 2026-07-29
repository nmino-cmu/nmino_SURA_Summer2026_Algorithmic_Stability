"""E2E bundle → LEAN_FULL for multi-threshold (requires lake)."""

from pathlib import Path

import pytest

from operators.multi_threshold.workflow import run_multi_threshold_preservation_workflow
from system_b.lean.manifest import DerivedLeanStatus
from system_b.lean.workflow import run_lean_from_bundle


@pytest.mark.lean
def test_multi_threshold_e2e_full():
    r = run_multi_threshold_preservation_workflow(export_lean_bundle=True)
    assert r.audit_verdict == "PASS", (r.audit_verdict, r.limitations)
    assert r.lean_bundle_path
    res = run_lean_from_bundle(Path(r.lean_bundle_path), skip_lake=False)
    assert res.status == DerivedLeanStatus.LEAN_FULL, (res.status, res.reason_codes)
    assert res.lean_manifest_digest
    assert res.certificate_dir is not None
    assert (res.certificate_dir / "lean_manifest.json").is_file()
