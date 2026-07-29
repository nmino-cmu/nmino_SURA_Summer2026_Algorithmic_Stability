"""ProofObligation minting at intake (ART-07b I-PO-01 subset / ART-CRP)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from art_int.canon import digest_object
from art_int.enums import ObligationStatus


@dataclass(frozen=True)
class ProofObligation:
    obligation_digest: str
    crp_digest: str
    draft_claim_digest: str
    profile: str
    status: ObligationStatus = ObligationStatus.OPEN
    method_hint: str = "intake_mint"
    superseded_by: str | None = None
    run_id: str | None = None

    def to_wire(self) -> dict[str, Any]:
        d: dict[str, Any] = {
            "obligation_digest": self.obligation_digest,
            "crp_digest": self.crp_digest,
            "draft_claim_digest": self.draft_claim_digest,
            "profile": self.profile,
            "status": self.status.value,
            "method_hint": self.method_hint,
        }
        if self.superseded_by is not None:
            d["superseded_by"] = self.superseded_by
        if self.run_id is not None:
            d["run_id"] = self.run_id
        return d


def mint_obligations_for_claims(
    *,
    crp_digest: str,
    profile: str,
    claim_digests: list[str],
    extra_per_claim: int = 1,
) -> list[ProofObligation]:
    """Mint ≥1 obligation per draft claim; multiple allowed (characterization + proof)."""
    out: list[ProofObligation] = []
    for cd in claim_digests:
        for i in range(max(1, extra_per_claim)):
            body = {
                "crp_digest": crp_digest,
                "draft_claim_digest": cd,
                "profile": profile,
                "index": i,
            }
            od = digest_object(body)
            out.append(
                ProofObligation(
                    obligation_digest=od,
                    crp_digest=crp_digest,
                    draft_claim_digest=cd,
                    profile=profile,
                    method_hint="characterization" if i == 0 else "symbolic_attempt",
                )
            )
    return out


def claim_digest(claim: dict[str, Any]) -> str:
    return digest_object({"claim": claim})
