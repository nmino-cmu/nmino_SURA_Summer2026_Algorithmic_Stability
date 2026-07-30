"""A-local SubmissionBatch / SubmissionAttempt (ART-A-06 / ART-INT §2)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from art_int.enums import BatchStatus, IntakeStatus, TransportResult


@dataclass
class SubmissionAttempt:
    attempt_id: str
    batch_id: str
    session_id: str
    sealed_snapshot_version_id: str
    sealed_digest: str
    idempotency_key: str
    logical_submission_id: str
    attempt_number: int = 1
    transport_result: TransportResult = TransportResult.OK
    b_intake_result: IntakeStatus | str = IntakeStatus.PENDING
    receipt_ref: str | None = None
    created_at: str = ""
    completed_at: str | None = None

    def to_wire(self) -> dict[str, Any]:
        d: dict[str, Any] = {
            "attempt_id": self.attempt_id,
            "batch_id": self.batch_id,
            "session_id": self.session_id,
            "sealed_snapshot_version_id": self.sealed_snapshot_version_id,
            "sealed_digest": self.sealed_digest,
            "idempotency_key": self.idempotency_key,
            "logical_submission_id": self.logical_submission_id,
            "attempt_number": self.attempt_number,
            "transport_result": self.transport_result.value,
            "b_intake_result": (
                self.b_intake_result.value
                if isinstance(self.b_intake_result, IntakeStatus)
                else self.b_intake_result
            ),
            "created_at": self.created_at,
        }
        if self.receipt_ref is not None:
            d["receipt_ref"] = self.receipt_ref
        if self.completed_at is not None:
            d["completed_at"] = self.completed_at
        return d


@dataclass
class SubmissionBatch:
    batch_id: str
    session_id: str
    gate_record_id: str
    seal_set: list[str]
    sealed_snapshot_version_ids: list[str] = field(default_factory=list)
    member_attempt_ids: list[str] = field(default_factory=list)
    batch_status: BatchStatus = BatchStatus.OPEN

    def to_wire(self) -> dict[str, Any]:
        return {
            "batch_id": self.batch_id,
            "session_id": self.session_id,
            "gate_record_id": self.gate_record_id,
            "seal_set": list(self.seal_set),
            "sealed_snapshot_version_ids": list(self.sealed_snapshot_version_ids),
            "member_attempt_ids": list(self.member_attempt_ids),
            "batch_status": self.batch_status.value,
        }

    def fan_out_digests(self, attempts: list[SubmissionAttempt]) -> list[str]:
        """I-INT-10: N independent submits; B never sees batch_id."""
        return [a.sealed_digest for a in attempts]


def recompute_batch_status(attempts: list[SubmissionAttempt]) -> BatchStatus:
    if not attempts:
        return BatchStatus.OPEN
    results = []
    for a in attempts:
        if a.transport_result != TransportResult.OK:
            if a.transport_result == TransportResult.EXHAUSTED:
                results.append("REJECTED")
            else:
                return BatchStatus.OPEN  # pending retry
        else:
            st = a.b_intake_result
            val = st.value if isinstance(st, IntakeStatus) else st
            results.append(val)
    if all(r == IntakeStatus.ACCEPTED_DRAFT.value for r in results):
        return BatchStatus.COMPLETED_ALL_ACCEPTED
    if all(r == IntakeStatus.REJECTED.value for r in results):
        return BatchStatus.COMPLETED_ALL_REJECTED
    if any(r == IntakeStatus.PENDING.value for r in results):
        return BatchStatus.OPEN
    return BatchStatus.COMPLETED_MIXED
