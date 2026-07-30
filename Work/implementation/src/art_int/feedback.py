"""VerifierFeedbackExport (ART-INT feedback-export)."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from art_int.canon import H_tagged, digest_object
from art_int.enums import AuditVerdict, IntakeStatus
from art_int.errors import ProvenanceError, SchemaVersionError, ValidationError
from art_int.receipt import IntakeReceipt, compute_receipt_digest

SCHEMA_FB = "ARTINT.FB.v1"


@dataclass
class VerifierFeedbackExport:
    crp_digest: str
    sealed_digest: str
    intake_status: IntakeStatus
    profile: str
    draft_claim_digests: list[str] = field(default_factory=list)
    obligation_digests: list[str] = field(default_factory=list)
    obligations: list[dict[str, Any]] = field(default_factory=list)
    receipt_digest: str | None = None
    reason_codes: list[str] = field(default_factory=list)
    audit_profile_id: str | None = None
    cx_profile_id: str | None = None
    verification_run_id: str | None = None
    run_started_at: str | None = None
    run_completed_at: str | None = None
    audit_verdict: AuditVerdict | None = None
    audit_record_digest: str | None = None
    counterexamples: list[dict[str, Any]] = field(default_factory=list)
    failed_obligations: list[str] = field(default_factory=list)
    unresolved_obligations: list[str] = field(default_factory=list)
    discharged_obligations: list[str] = field(default_factory=list)
    assumptions_introduced: list[str] = field(default_factory=list)
    proof_sketches_refs: list[str] = field(default_factory=list)
    maturity_by_claim: list[dict[str, Any]] = field(default_factory=list)
    certified_object_digests: list[str] = field(default_factory=list)
    verifier_limitations: list[str] = field(default_factory=list)
    revision_guidance: list[str] = field(default_factory=list)
    confidence_notes: list[str] = field(default_factory=list)
    provenance: dict[str, Any] = field(default_factory=dict)
    lean_manifest_digest: str | None = None  # ART-10b; consumers recompute DerivedLeanStatus
    content_digest: str | None = None
    export_digest: str | None = None
    schema_version: str = SCHEMA_FB

    def body_for_digest(self) -> dict[str, Any]:
        """Normative body without export_digest. Required arrays retained even if empty."""
        required_keep_empty = {
            "draft_claim_digests",
            "obligation_digests",
            "obligations",
            "counterexamples",
            "failed_obligations",
            "unresolved_obligations",
            "discharged_obligations",
        }
        d = asdict(self)
        d.pop("export_digest", None)
        d["intake_status"] = self.intake_status.value
        if self.audit_verdict is not None:
            d["audit_verdict"] = self.audit_verdict.value
        else:
            d.pop("audit_verdict", None)
        out: dict[str, Any] = {}
        for k, v in d.items():
            if v is None:
                continue
            if v == [] and k not in required_keep_empty:
                continue
            if v == {} and k not in ("provenance",):
                continue
            out[k] = v
        # always include required arrays
        for k in required_keep_empty:
            out.setdefault(k, [])
        return out

    def to_wire(self) -> dict[str, Any]:
        d = self.body_for_digest()
        if self.export_digest is not None:
            d["export_digest"] = self.export_digest
        return d


def compute_export_digest(export: VerifierFeedbackExport) -> str:
    if export.schema_version != SCHEMA_FB:
        raise SchemaVersionError(f"unsupported feedback schema: {export.schema_version}")
    return H_tagged(SCHEMA_FB, export.body_for_digest())


def finalize_export(export: VerifierFeedbackExport) -> VerifierFeedbackExport:
    """Validate provenance and fill digests (I-INT-FB-01)."""
    if export.crp_digest != export.sealed_digest:
        raise ProvenanceError("sealed_digest must equal crp_digest")
    export.content_digest = digest_object(export.body_for_digest())
    export.export_digest = compute_export_digest(export)
    return export


def validate_feedback_for_prior(
    export: VerifierFeedbackExport,
    *,
    expected_crp_digest: str | None = None,
    expected_receipt: str | None = None,
    receipt: IntakeReceipt | None = None,
) -> None:
    """Wrong-package / forged receipt rejection (I-INT-61/63)."""
    if export.crp_digest != export.sealed_digest:
        raise ProvenanceError("sealed_digest ≠ crp_digest")
    if expected_crp_digest is not None and export.crp_digest != expected_crp_digest:
        raise ProvenanceError("feedback for wrong package")
    if receipt is not None:
        computed = compute_receipt_digest(receipt)
        if not export.receipt_digest or export.receipt_digest != computed:
            raise ProvenanceError("forged or mismatched receipt_digest")
        if receipt.crp_digest != export.crp_digest:
            raise ProvenanceError("receipt crp_digest ≠ export crp_digest")
    elif expected_receipt is not None:
        if not export.receipt_digest or export.receipt_digest != expected_receipt:
            raise ProvenanceError("forged or mismatched receipt_ref")
    expected = compute_export_digest(export)
    if not export.export_digest:
        raise ProvenanceError("export_digest required")
    if export.export_digest != expected:
        raise ProvenanceError("forged export_digest")
