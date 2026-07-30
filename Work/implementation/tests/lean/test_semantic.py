"""Semantic audit adversarial tests."""

from pathlib import Path

from operators.argmax.workflow import run_argmax_margin_workflow
from system_b.lean.bundle import load_bundle
from system_b.lean.eligibility import check_eligibility
from system_b.lean.ir import mint_candidate
from system_b.lean.semantic import audit_props_and_theorems


def _fc():
    r = run_argmax_margin_workflow(export_lean_bundle=True)
    b = load_bundle(Path(r.lean_bundle_path))
    elig = check_eligibility(b)
    repo = Path(__file__).resolve().parents[3]
    lean_root = repo / "lean"
    return mint_candidate(
        b,
        claim=elig.claim,
        draft_claim_digest=elig.draft_claim_digest,
        lean_root=lean_root,
        repo_root=repo,
    ), lean_root


def test_semantic_ok():
    fc, lean_root = _fc()
    a = audit_props_and_theorems(fc, lean_root)
    assert a.ok, a.reason_codes


def test_wrong_theorem_type(tmp_path: Path):
    fc, lean_root = _fc()
    src = (lean_root / "Research/Operators/Argmax/Margin.lean").read_text(encoding="utf-8")
    bad = src.replace(
        "theorem margin_invariance : MarginInvarianceProp",
        "theorem margin_invariance : True",
    )
    fake = tmp_path / "lean"
    margin = fake / "Research/Operators/Argmax/Margin.lean"
    margin.parent.mkdir(parents=True)
    margin.write_text(bad, encoding="utf-8")
    (fake / "Research/Operators/Argmax/Basic.lean").write_text(
        (lean_root / "Research/Operators/Argmax/Basic.lean").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    a = audit_props_and_theorems(fc, fake)
    assert not a.ok
