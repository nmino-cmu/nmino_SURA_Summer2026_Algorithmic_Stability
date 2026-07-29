"""FC.v1 mint + no floats."""

from pathlib import Path

from operators.argmax.workflow import run_argmax_margin_workflow
from system_b.lean.bundle import load_bundle
from system_b.lean.eligibility import check_eligibility
from system_b.lean.ir import mint_candidate


def test_mint_candidate():
    r = run_argmax_margin_workflow(export_lean_bundle=True)
    b = load_bundle(Path(r.lean_bundle_path))
    elig = check_eligibility(b)
    repo = Path(__file__).resolve().parents[3]
    lean_root = repo / "lean"
    fc = mint_candidate(
        b,
        claim=elig.claim,
        draft_claim_digest=elig.draft_claim_digest,
        lean_root=lean_root,
        repo_root=repo,
    )
    assert fc.candidate_digest
    assert fc.conclusion["score_space"] == "FIN_TO_REAL"
    assert not any(isinstance(v, float) for v in fc.conclusion.values())
