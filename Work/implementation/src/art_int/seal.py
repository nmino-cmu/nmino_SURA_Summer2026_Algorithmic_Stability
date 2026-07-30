"""SealedCRPSnapshot (S-INT-SEAL) and sealing helper."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from art_int.crp import (
    CandidateResearchPackage,
    compute_crp_digest,
    validate_crp_admissibility,
)
from art_int.draft import DraftCRPPayload
from art_int.enums import AuthorKind, CrpProfile
from art_int.errors import SchemaVersionError, ValidationError

SCHEMA_SEAL = "ARTINT.SEAL.v1"


@dataclass
class SealedCRPSnapshotPayload:
    draft_crp_version_id: str
    sealed_digest: str
    crp: CandidateResearchPackage
    gate_record_id: str
    sealed_at: str
    schema_version: str = SCHEMA_SEAL

    def to_wire(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "draft_crp_version_id": self.draft_crp_version_id,
            "sealed_digest": self.sealed_digest,
            "crp": self.crp.to_wire(),
            "gate_record_id": self.gate_record_id,
            "sealed_at": self.sealed_at,
        }


def seal_draft(
    draft: DraftCRPPayload,
    *,
    draft_crp_version_id: str,
    gate_record_id: str,
    sealed_at: str,
    author_kind: AuthorKind,
    author_principal_digest: str,
    author_binding_digest: str | None,
    live_scope_pin: str,
    assistant_binding_live: bool = False,
    prior_crp_digest: str | None = None,
) -> SealedCRPSnapshotPayload:
    """Mint immutable sealed snapshot; sealed_digest ≡ crp_digest (I-INT-20)."""
    if not draft.compile_ok:
        raise ValidationError("cannot seal CompileError / failed draft")
    draft.validate_schema()
    profile = draft.normalized_profile()
    crp = CandidateResearchPackage(
        author_kind=author_kind,
        author_principal_digest=author_principal_digest,
        author_binding_digest=author_binding_digest,
        profile=profile,
        math_scope_pin_digest=draft.math_scope_pin_digest,
        payload=draft.payload,
        sealed_at=sealed_at,
        prior_crp_digest=prior_crp_digest,
    )
    validate_crp_admissibility(
        crp, live_scope_pin=live_scope_pin, assistant_binding_live=assistant_binding_live
    )
    digest = compute_crp_digest(crp)
    crp.crp_digest = digest
    return SealedCRPSnapshotPayload(
        draft_crp_version_id=draft_crp_version_id,
        sealed_digest=digest,
        crp=crp,
        gate_record_id=gate_record_id,
        sealed_at=sealed_at,
    )


def validate_seal(snap: SealedCRPSnapshotPayload) -> None:
    if snap.schema_version != SCHEMA_SEAL:
        raise SchemaVersionError(f"unsupported seal schema: {snap.schema_version}")
    expected = compute_crp_digest(snap.crp)
    if snap.sealed_digest != expected:
        raise ValidationError("sealed_digest ≠ recomputed crp_digest", code="DIGEST_MISMATCH")
    if snap.crp.crp_digest is not None and snap.crp.crp_digest != expected:
        raise ValidationError("embedded crp.crp_digest ≠ sealed_digest", code="DIGEST_MISMATCH")
    if snap.crp.crp_digest is None:
        raise ValidationError("crp.crp_digest required on sealed snapshot", code="DIGEST_MISMATCH")
