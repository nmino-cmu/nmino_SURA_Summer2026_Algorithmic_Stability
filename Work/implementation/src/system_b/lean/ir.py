"""FormalizationCandidate (ARTLEAN.FC.v1) — tokenized conclusion only."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from art_int.canon import H, H_tagged, digest_object
from system_b.lean.bundle import LeanInputBundle
from system_b.lean.profiles import resolve_profile

SCHEMA_FC = "ARTLEAN.FC.v1"
STATEMENT_BEGIN = "/- STATEMENT_BEGIN -/"
STATEMENT_END = "/- STATEMENT_END -/"


def extract_statement_region(lean_src: str) -> str:
    if STATEMENT_BEGIN not in lean_src or STATEMENT_END not in lean_src:
        raise ValueError("missing STATEMENT markers")
    start = lean_src.index(STATEMENT_BEGIN) + len(STATEMENT_BEGIN)
    end = lean_src.index(STATEMENT_END)
    region = lean_src[start:end]
    return "\n".join(line.rstrip() for line in region.strip("\n").splitlines())


def statement_region_digest(lean_src: str) -> str:
    return H(extract_statement_region(lean_src).encode("utf-8"))


def file_sha(path: Path) -> str:
    return H(path.read_bytes())


@dataclass
class FormalizationCandidate:
    operator_id: str
    theorem_id: str
    crp_digest: str
    draft_claim_digest: str
    verification_run_id: str
    bundle_digest: str
    source_evaluation_method: str
    conclusion: dict[str, Any]
    conclusion_digest: str
    operator_math_source_digest: str
    prop_module_digests: list[str]
    audit_verdict: str
    obligation_results: list[dict[str, Any]]
    verifier_limitations: list[str]
    lean_namespace: str
    targets: list[dict[str, Any]]
    conventions: dict[str, Any]
    known_gaps: list[str]
    semantic_freeze_digest: str
    schema_version: str = SCHEMA_FC
    candidate_digest: str | None = None
    prop_module_relative: str = ""
    system2_statement: str = ""

    def body_for_digest(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "operator_id": self.operator_id,
            "theorem_id": self.theorem_id,
            "crp_digest": self.crp_digest,
            "draft_claim_digest": self.draft_claim_digest,
            "verification_run_id": self.verification_run_id,
            "bundle_digest": self.bundle_digest,
            "source_evaluation_method": self.source_evaluation_method,
            "conclusion": self.conclusion,
            "conclusion_digest": self.conclusion_digest,
            "operator_math_source_digest": self.operator_math_source_digest,
            "prop_module_digests": list(self.prop_module_digests),
            "audit_verdict": self.audit_verdict,
            "obligation_results": list(self.obligation_results),
            "verifier_limitations": list(self.verifier_limitations),
            "lean_namespace": self.lean_namespace,
            "targets": list(self.targets),
            "conventions": dict(self.conventions),
            "known_gaps": list(self.known_gaps),
            "semantic_freeze_digest": self.semantic_freeze_digest,
        }

    def compute_digest(self) -> str:
        return H_tagged(SCHEMA_FC, self.body_for_digest())

    def to_wire(self) -> dict[str, Any]:
        if self.candidate_digest is None:
            self.candidate_digest = self.compute_digest()
        d = self.body_for_digest()
        d["candidate_digest"] = self.candidate_digest
        return d


def mint_candidate(
    bundle: LeanInputBundle,
    *,
    claim: dict[str, Any],
    draft_claim_digest: str,
    lean_root: Path,
    repo_root: Path,
) -> FormalizationCandidate:
    """Mint FC for an allowlisted Lean profile."""
    profile = resolve_profile(claim)
    if profile is None:
        raise ValueError("claim does not match any lean profile")
    if not profile.formal_matches(claim):
        raise ValueError("formal fields mismatch")

    conclusion = dict(profile.CONCLUSION_TOKENS)
    for v in conclusion.values():
        if isinstance(v, float):
            raise ValueError("floats forbidden in conclusion")

    conclusion_digest = digest_object(conclusion)
    prop_path = lean_root / profile.PROP_RELATIVE
    lean_src = prop_path.read_text(encoding="utf-8")
    region_digest = statement_region_digest(lean_src)
    prop_digests = [file_sha(lean_root / p) for p in profile.PROP_DEPS]
    math_py = repo_root / profile.MATH_PY_RELATIVE
    math_digest = file_sha(math_py)
    conventions = dict(profile.CONVENTIONS)
    freeze = H_tagged(
        "SEMANTIC_FREEZE.v1",
        conclusion_digest,
        region_digest,
        profile.TARGETS,
        conventions,
        prop_digests,
    )
    run = bundle.verification_run
    fc = FormalizationCandidate(
        operator_id=str(claim["operator"]),
        theorem_id=claim["theorem_id"],
        crp_digest=bundle.crp_digest,
        draft_claim_digest=draft_claim_digest,
        verification_run_id=str(run["run_id"]),
        bundle_digest=bundle.bundle_digest or bundle.compute_digest(),
        source_evaluation_method=str(claim["evaluation"]),
        conclusion=conclusion,
        conclusion_digest=conclusion_digest,
        operator_math_source_digest=math_digest,
        prop_module_digests=prop_digests,
        audit_verdict=str(run.get("audit_verdict")),
        obligation_results=list(run.get("results") or []),
        verifier_limitations=list(run.get("limitations") or []),
        lean_namespace=profile.LEAN_NAMESPACE,
        targets=list(profile.TARGETS),
        conventions=conventions,
        known_gaps=list(profile.KNOWN_GAPS),
        semantic_freeze_digest=freeze,
        prop_module_relative=str(profile.PROP_RELATIVE),
        system2_statement=str(profile.THEOREM_STATEMENT),
    )
    fc.candidate_digest = fc.compute_digest()
    object.__setattr__(fc, "_lean_statement_digest", region_digest)  # type: ignore[attr-defined]
    return fc


def lean_statement_digest_of(fc: FormalizationCandidate) -> str:
    return getattr(fc, "_lean_statement_digest", fc.conclusion_digest)
