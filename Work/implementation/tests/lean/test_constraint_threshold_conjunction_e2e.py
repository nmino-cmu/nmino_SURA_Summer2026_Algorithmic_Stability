from pathlib import Path
import pytest
from operators.constraint_threshold_conjunction.workflow import run_constraint_threshold_conjunction_preservation_workflow
from system_b.lean.manifest import DerivedLeanStatus
from system_b.lean.workflow import run_lean_from_bundle
@pytest.mark.lean
def test_constraint_threshold_conjunction_e2e_full():
    r = run_constraint_threshold_conjunction_preservation_workflow(export_lean_bundle=True)
    assert r.audit_verdict == "PASS", (r.audit_verdict, r.limitations)
    res = run_lean_from_bundle(Path(r.lean_bundle_path), skip_lake=False)
    assert res.status == DerivedLeanStatus.LEAN_FULL, (res.status, res.reason_codes)
