"""VerifierFeedbackExport construction (B→A read-only boundary)."""

from __future__ import annotations

from typing import Any

from art_int.enums import AuditVerdict, IntakeStatus
from art_int.feedback import VerifierFeedbackExport, finalize_export
from art_int.receipt import IntakeReceipt
from system_b.obligations import ProofObligation


def build_feedback_export(
    *,
    receipt: IntakeReceipt,
    obligations: list[ProofObligation],
    profile: str,
    audit_verdict: AuditVerdict | None = None,
    verification_run_id: str | None = None,
    counterexamples: list[dict[str, Any]] | None = None,
    failed: list[str] | None = None,
    unresolved: list[str] | None = None,
    discharged: list[str] | None = None,
    limitations: list[str] | None = None,
    supersedes_run_id: str | None = None,
    lean_manifest_digest: str | None = None,
) -> VerifierFeedbackExport:
    """Populate export with exact package/receipt provenance; never mutates System A."""
    obs = [o.to_wire() for o in obligations]
    ex = VerifierFeedbackExport(
        crp_digest=receipt.crp_digest,
        sealed_digest=receipt.crp_digest,
        intake_status=receipt.status,
        profile=profile,
        draft_claim_digests=list(receipt.draft_claim_digests),
        obligation_digests=[o.obligation_digest for o in obligations],
        obligations=obs,
        receipt_digest=receipt.receipt_digest,
        reason_codes=list(receipt.reason_codes),
        verification_run_id=verification_run_id,
        audit_verdict=audit_verdict,
        counterexamples=list(counterexamples or []),
        failed_obligations=list(failed or []),
        unresolved_obligations=list(unresolved or []),
        discharged_obligations=list(discharged or []),
        verifier_limitations=list(limitations or []),
        lean_manifest_digest=lean_manifest_digest,
        provenance={
            "receipt_digest": receipt.receipt_digest,
            "crp_digest": receipt.crp_digest,
            "supersedes_run_id": supersedes_run_id,
        },
    )
    return finalize_export(ex)
