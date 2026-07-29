"""E2E Phase B selection_stability CRP → LEAN_FULL (requires lake)."""

from pathlib import Path

import pytest

from operators.argmax.phase_b import LINF_SCORE_BALL_MECHANISM
from operators.argmax.workflow import run_argmax_selection_stability_workflow
from system_b.lean.manifest import DerivedLeanStatus
from system_b.lean.workflow import run_lean_from_bundle


@pytest.mark.lean
def test_argmax_phase_b_selection_stability_e2e_full():
    from system_b.lean.store import LeanManifestStore

    lean_root = Path(__file__).resolve().parents[3] / "lean"
    store = LeanManifestStore(lean_root / "certificates")
    before = store.read_manifest("argmax", "bounded-perturbation-margin")
    assert before is not None
    before_digest = before["manifest_digest"]

    r = run_argmax_selection_stability_workflow(export_lean_bundle=True)
    assert r.lean_bundle_path
    assert r.profile == "PHASE_B_STABILIZATION"
    assert r.chain_segment == "selection_stability"
    assert r.mechanism_local_id == LINF_SCORE_BALL_MECHANISM["local_id"]
    res = run_lean_from_bundle(Path(r.lean_bundle_path), skip_lake=False)
    assert res.status == DerivedLeanStatus.LEAN_FULL, (res.status, res.reason_codes)
    assert res.lean_manifest_digest
    assert res.certificate_dir is not None
    assert (res.certificate_dir / "lean_manifest.json").is_file()
    # Packaging-only Phase B must not rewrite the published Phase A certificate.
    after = store.read_manifest("argmax", "bounded-perturbation-margin")
    assert after is not None
    assert after["manifest_digest"] == before_digest
    assert "PRESERVE_EXISTING_SAME_LEAN_MATH" in res.reason_codes
