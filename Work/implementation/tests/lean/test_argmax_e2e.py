"""E2E bundle → LEAN_FULL (requires lake)."""

from pathlib import Path

import pytest

from operators.argmax.workflow import run_argmax_margin_workflow
from system_b.lean.manifest import DerivedLeanStatus
from system_b.lean.workflow import run_lean_from_bundle


@pytest.mark.lean
def test_argmax_e2e_full():
    r = run_argmax_margin_workflow(export_lean_bundle=True)
    assert r.lean_bundle_path
    res = run_lean_from_bundle(Path(r.lean_bundle_path), skip_lake=False)
    assert res.status == DerivedLeanStatus.LEAN_FULL, (res.status, res.reason_codes)
    assert res.lean_manifest_digest
    assert res.certificate_dir is not None
    assert (res.certificate_dir / "lean_manifest.json").is_file()
