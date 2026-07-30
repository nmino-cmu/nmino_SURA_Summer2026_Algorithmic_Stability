"""IntakeReceipt (ART-CRP)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from art_int.canon import H_tagged
from art_int.enums import IntakeStatus

SCHEMA_RECEIPT = "ARTCRP.IN.v1"


@dataclass
class IntakeReceipt:
    crp_digest: str
    event_seq: int
    draft_claim_digests: list[str]
    status: IntakeStatus
    obligation_digests: list[str] = field(default_factory=list)
    reason_codes: list[str] = field(default_factory=list)
    receipt_digest: str | None = None
    schema_version: str = SCHEMA_RECEIPT

    def to_wire(self) -> dict[str, Any]:
        d: dict[str, Any] = {
            "schema_version": self.schema_version,
            "crp_digest": self.crp_digest,
            "event_seq": self.event_seq,
            "draft_claim_digests": list(self.draft_claim_digests),
            "obligation_digests": list(self.obligation_digests),
            "status": self.status.value,
        }
        if self.reason_codes:
            d["reason_codes"] = list(self.reason_codes)
        if self.receipt_digest is not None:
            d["receipt_digest"] = self.receipt_digest
        return d


def compute_receipt_digest(receipt: IntakeReceipt) -> str:
    """H(\"ARTCRP.IN.v1\", crp_digest, event_seq, draft_claim_digests_sorted)."""
    sorted_claims = sorted(receipt.draft_claim_digests)
    return H_tagged(SCHEMA_RECEIPT, receipt.crp_digest, receipt.event_seq, sorted_claims)
