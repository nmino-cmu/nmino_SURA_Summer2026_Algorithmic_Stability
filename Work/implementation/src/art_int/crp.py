"""CandidateResearchPackage wire model + digests (ART-CRP / ART-INT)."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from art_int.canon import H_tagged, BOT_TOKEN
from art_int.enums import AuthorKind, CrpProfile, CHAIN_SEGMENTS
from art_int.errors import AdmissibilityError, SchemaVersionError, UnsupportedEnumError, ValidationError

SCHEMA_CRP = "ARTCRP.v1"

PROFILE_HINT_ALIASES = {
    "PHASE_A": CrpProfile.PHASE_A_CHARACTERIZATION,
    "characterization": CrpProfile.PHASE_A_CHARACTERIZATION,
    "PHASE_B": CrpProfile.PHASE_B_STABILIZATION,
    "stabilization": CrpProfile.PHASE_B_STABILIZATION,
}


def normalize_profile_hint(hint: str) -> CrpProfile:
    """ART-INT profile-map I-INT-PR-01."""
    if hint in CrpProfile._value2member_map_:
        return CrpProfile(hint)
    if hint in PROFILE_HINT_ALIASES:
        return PROFILE_HINT_ALIASES[hint]
    raise UnsupportedEnumError(f"illegal profile_hint: {hint!r}", code="PROFILE_MISMATCH")


@dataclass
class CrpPayload:
    definitions: list[dict[str, Any]] = field(default_factory=list)
    assumptions: list[dict[str, Any]] = field(default_factory=list)
    claims: list[dict[str, Any]] = field(default_factory=list)
    proof_sketches: list[dict[str, Any]] = field(default_factory=list)
    bridge_proposals: list[dict[str, Any]] = field(default_factory=list)
    mechanism_proposals: list[dict[str, Any]] = field(default_factory=list)
    examples: list[dict[str, Any]] = field(default_factory=list)
    falsifiers: list[dict[str, Any]] = field(default_factory=list)
    counterexample_claims: list[dict[str, Any]] = field(default_factory=list)
    certificate_drafts: list[dict[str, Any]] = field(default_factory=list)
    literature_refs: list[dict[str, Any]] = field(default_factory=list)
    declared_reads: list[dict[str, Any]] = field(default_factory=list)
    free_text_notes: str | None = None

    def to_wire(self) -> dict[str, Any]:
        d = asdict(self)
        if d.get("free_text_notes") is None:
            d.pop("free_text_notes", None)
        return d


@dataclass
class CandidateResearchPackage:
    author_kind: AuthorKind
    author_principal_digest: str
    profile: CrpProfile
    math_scope_pin_digest: str
    payload: CrpPayload
    sealed_at: str
    author_binding_digest: str | None = None
    prior_crp_digest: str | None = None
    schema_version: str = SCHEMA_CRP
    crp_digest: str | None = None  # filled by compute

    def identity_args(self) -> list[Any]:
        binding = self.author_binding_digest if self.author_binding_digest is not None else BOT_TOKEN
        prior = self.prior_crp_digest if self.prior_crp_digest is not None else BOT_TOKEN
        return [
            SCHEMA_CRP,
            self.author_kind.value,
            self.author_principal_digest,
            binding,
            self.profile.value,
            self.math_scope_pin_digest,
            self.payload.to_wire(),
            prior,
        ]

    def to_wire(self) -> dict[str, Any]:
        d: dict[str, Any] = {
            "schema_version": self.schema_version,
            "author_kind": self.author_kind.value,
            "author_principal_digest": self.author_principal_digest,
            "profile": self.profile.value,
            "math_scope_pin_digest": self.math_scope_pin_digest,
            "payload": self.payload.to_wire(),
            "sealed_at": self.sealed_at,
        }
        if self.author_binding_digest is not None:
            d["author_binding_digest"] = self.author_binding_digest
        if self.prior_crp_digest is not None:
            d["prior_crp_digest"] = self.prior_crp_digest
        if self.crp_digest is not None:
            d["crp_digest"] = self.crp_digest
        return d


def compute_crp_digest(crp: CandidateResearchPackage) -> str:
    """I-INT-20 / ART-CRP: H(\"ARTCRP.v1\", …)."""
    return H_tagged(*crp.identity_args())


def validate_crp_admissibility(
    crp: CandidateResearchPackage,
    *,
    live_scope_pin: str,
    assistant_binding_live: bool = False,
) -> None:
    """admissible_package (ART-CRP §3) — interface subset."""
    if crp.schema_version != SCHEMA_CRP:
        raise SchemaVersionError(f"unsupported CRP schema_version={crp.schema_version!r}")
    if crp.math_scope_pin_digest != live_scope_pin:
        raise AdmissibilityError("math_scope_pin_digest mismatch", code="PACKAGE_INADMISSIBLE")
    if crp.author_kind == AuthorKind.RESEARCH_DISCOVERY_ASSISTANT:
        if not crp.author_binding_digest:
            raise AdmissibilityError("ASSISTANT requires author_binding_digest", code="CRP_AUTHOR")
        if not assistant_binding_live:
            raise AdmissibilityError("ASSISTANT binding not live", code="CRP_AUTHOR")
    if crp.profile == CrpProfile.PHASE_B_STABILIZATION and not crp.payload.mechanism_proposals:
        raise AdmissibilityError("Phase B requires mechanism_proposals", code="MECHANISM_REQUIRED")
    for claim in crp.payload.claims:
        seg = claim.get("chain_segment")
        if seg not in CHAIN_SEGMENTS:
            raise ValidationError(f"invalid chain_segment: {seg!r}", code="CRP_SCHEMA")
    # Phase A: empty mechanisms OK — no reject
