"""CRP_PACKAGER — deterministic compile with package coherence (ART-A-02 §1.3.1)."""

from __future__ import annotations

from art_int.canon import digest_object
from art_int.crp import CrpPayload, normalize_profile_hint
from art_int.draft import CompileErrorPayload, DraftCRPPayload
from art_int.enums import CrpProfile
from art_int.errors import UnsupportedEnumError
from system_a.freeze import deep_thaw
from system_a.ir import DiscoveryIR


def _closure(ir: DiscoveryIR, tips: list[str]) -> tuple[set[str], list[str]]:
    """BFS over DepLink; return (nodes, error_codes)."""
    missing = [t for t in tips if t not in ir.versions]
    if missing:
        return set(), ["MISSING_FIELD"]
    seen: set[str] = set()
    stack = list(tips)
    while stack:
        n = stack.pop()
        if n in seen:
            continue
        seen.add(n)
        for d in ir.deps:
            if d.from_version_id == n and d.to_version_id not in seen:
                if d.to_version_id not in ir.versions:
                    return set(), ["MISSING_FIELD"]
                stack.append(d.to_version_id)
    return seen, []


def _has_cycle(ir: DiscoveryIR, nodes: set[str]) -> bool:
    adj: dict[str, list[str]] = {n: [] for n in nodes}
    for d in ir.deps:
        if d.from_version_id in nodes and d.to_version_id in nodes:
            adj[d.from_version_id].append(d.to_version_id)
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {n: WHITE for n in nodes}

    def dfs(u: str) -> bool:
        color[u] = GRAY
        for v in adj[u]:
            if color[v] == GRAY:
                return True
            if color[v] == WHITE and dfs(v):
                return True
        color[u] = BLACK
        return False

    return any(color[n] == WHITE and dfs(n) for n in nodes)


def _lineage_contradiction(ir: DiscoveryIR, nodes: set[str]) -> bool:
    """Two distinct versions of same lineage both pinned without conflict exclusion."""
    by_lin: dict[str, list[str]] = {}
    for n in nodes:
        av = ir.versions[n]
        by_lin.setdefault(av.lineage_id, []).append(n)
    for vids in by_lin.values():
        if len(vids) > 1:
            # allowed only if every pair is in an OPEN conflict (excluded from packaging)
            # if both present in closure without conflict → contradiction
            for i in range(len(vids)):
                for j in range(i + 1, len(vids)):
                    pair = frozenset({vids[i], vids[j]})
                    if pair not in ir._conflicts_open:
                        return True
    return False


def _conflict_pins(ir: DiscoveryIR, nodes: set[str]) -> bool:
    for pair in ir._conflicts_open:
        if pair <= nodes:
            return True
    return False


def _profile_projection_ok(profile: CrpProfile, payload: CrpPayload) -> list[str]:
    if profile == CrpProfile.PHASE_B_STABILIZATION and not payload.mechanism_proposals:
        return ["MECHANISM_REQUIRED"]
    if profile == CrpProfile.BRIDGE_ONLY and not payload.bridge_proposals:
        return ["MISSING_FIELD"]
    if profile == CrpProfile.OBLIGATION_ONLY and not payload.claims:
        return ["MISSING_FIELD"]
    return []


def compile_branch(
    ir: DiscoveryIR,
    *,
    branch_id: str,
    profile_hint: str,
    math_scope_pin_digest: str,
    member_id: str | None = None,
    created_at: str = "",
) -> DraftCRPPayload | CompileErrorPayload:
    """Pure projection; invents no mathematics; enforces §1.3.1 coherence."""

    def err(codes: list[str], msg: str) -> CompileErrorPayload:
        return CompileErrorPayload(
            branch_id=branch_id,
            error_codes=codes,
            message=msg,
            member_id=member_id,
            profile_hint=profile_hint,
            created_at=created_at,
        )

    branch = ir.branches.get(branch_id)
    if not branch:
        return err(["COHERENCE"], "unknown branch")
    tips = list(branch.tip_pins)
    nodes, codes = _closure(ir, tips)
    if codes:
        return err(codes, "tip/closure unresolved")
    if _has_cycle(ir, nodes):
        return err(["COHERENCE"], "dependency cycle")
    for n in nodes:
        if ir.lifecycle_state(n) == "ABANDONED":
            return err(["COHERENCE"], "abandoned artifact in closure")
    if _conflict_pins(ir, nodes):
        return err(["COHERENCE"], "OPEN conflict among pinned artifacts")
    if _lineage_contradiction(ir, nodes):
        return err(["COHERENCE"], "contradictory lineage pins")

    if branch.abandoned:
        return err(["COHERENCE"], "branch abandoned")

    payload = CrpPayload()
    for tid in sorted(nodes):
        av = ir.versions[tid]
        p = deep_thaw(av.payload)
        if av.artifact_class in ("TheoremCandidate", "ConjectureCandidate"):
            payload.claims.append(p)
        elif av.artifact_class == "DefinitionDraft":
            payload.definitions.append(p)
        elif av.artifact_class == "AssumptionDraft":
            payload.assumptions.append(p)
        elif av.artifact_class == "MechanismProposal":
            payload.mechanism_proposals.append(p)
        elif av.artifact_class == "ProofSketch":
            payload.proof_sketches.append(p)
        elif av.artifact_class == "ExampleCard":
            payload.examples.append(p)
        elif av.artifact_class in ("FalsificationTarget", "SoftFalsifierDraft"):
            payload.falsifiers.append(p)
        elif av.artifact_class == "BridgeProposalDraft":
            payload.bridge_proposals.append(p)
        elif av.artifact_class == "CertificateDraft":
            payload.certificate_drafts.append(p)
        elif av.artifact_class in ("LiteratureNode", "NoveltyAssessment"):
            payload.literature_refs.append(p)
        elif av.artifact_class == "VerifierPrior":
            payload.declared_reads.append({"content_digest": p.get("content_digest")})

    try:
        profile = normalize_profile_hint(profile_hint)
    except UnsupportedEnumError as e:
        return err(["PROFILE_MISMATCH"], str(e))

    proj_err = _profile_projection_ok(profile, payload)
    if proj_err:
        return err(proj_err, "profile required fields missing from IR projection")

    edges = sorted(
        (d.from_version_id, d.to_version_id, d.link_kind)
        for d in ir.deps
        if d.from_version_id in nodes and d.to_version_id in nodes
    )
    dep_closure_digest = digest_object({"nodes": sorted(nodes), "tips": tips, "edges": edges})
    draft = DraftCRPPayload(
        branch_id=branch_id,
        profile_hint=profile_hint,
        math_scope_pin_digest=math_scope_pin_digest,
        tip_pins=list(tips),
        dep_closure_digest=dep_closure_digest,
        payload=payload,
        member_id=member_id,
        created_at=created_at or "t0",
    )
    draft.validate_schema()
    return draft
