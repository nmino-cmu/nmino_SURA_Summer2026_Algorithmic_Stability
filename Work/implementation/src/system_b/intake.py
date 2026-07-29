"""B intake adapter — SUBMIT_CANDIDATE_PACKAGE (ART-CRP / ART-INT). No System A mutation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from art_int.crp import (
    SCHEMA_CRP,
    CandidateResearchPackage,
    compute_crp_digest,
    validate_crp_admissibility,
)
from art_int.enums import CrpProfile, IntakeStatus
from art_int.errors import (
    AdmissibilityError,
    IdempotencyConflict,
    SchemaVersionError,
    UnsupportedEnumError,
    ValidationError,
)
from art_int.envelope import SubmissionEnvelope, validate_envelope
from art_int.idempotency import check_idempotency_replay
from art_int.receipt import IntakeReceipt, compute_receipt_digest
from art_int.seal import SealedCRPSnapshotPayload, validate_seal
from system_b.obligations import ProofObligation, claim_digest, mint_obligations_for_claims


@dataclass
class IntakeOutcome:
    status: IntakeStatus
    receipt: IntakeReceipt | None
    obligations: list[ProofObligation] = field(default_factory=list)
    reason_codes: list[str] = field(default_factory=list)
    replay: bool = False


@dataclass
class VerificationIntake:
    """VERIFICATION_ORCHESTRATOR intake surface (adapters only; engines in M6)."""

    live_scope_pin: str
    event_seq: int = 0
    accepted: dict[str, IntakeReceipt] = field(default_factory=dict)
    obligations_by_crp: dict[str, list[ProofObligation]] = field(default_factory=dict)
    prior_keys: dict[str, str] = field(default_factory=dict)  # idempotency_key -> digest

    def submit_envelope(self, env: SubmissionEnvelope) -> IntakeOutcome:
        validate_envelope(env)
        recomputed = compute_crp_digest(env.crp)
        stated = env.crp.crp_digest
        if stated is not None and stated != recomputed:
            raise ValidationError("stated crp_digest ≠ recomputed digest", code="DIGEST_MISMATCH")
        env.crp.crp_digest = recomputed
        digest = recomputed
        if env.idempotency_key != digest:
            raise ValidationError("idempotency_key must equal recomputed crp_digest", code="IDEMPOTENCY_KEY_MISMATCH")
        kind = check_idempotency_replay(
            idempotency_key=env.idempotency_key,
            incoming_digest=digest,
            prior_key=env.idempotency_key if env.idempotency_key in self.prior_keys else None,
            prior_digest=self.prior_keys.get(env.idempotency_key),
        )
        if kind == "replay" and digest in self.accepted:
            prev = self.accepted[digest]
            return IntakeOutcome(
                status=IntakeStatus.ACCEPTED_DRAFT,
                receipt=prev,
                obligations=list(self.obligations_by_crp.get(digest, [])),
                replay=True,
            )
        out = self.submit_package(env.crp)
        if out.status == IntakeStatus.ACCEPTED_DRAFT and out.receipt:
            self.prior_keys[env.idempotency_key] = digest
        return out

    def submit_sealed(self, snap: SealedCRPSnapshotPayload) -> IntakeOutcome:
        validate_seal(snap)
        return self.submit_package(snap.crp)

    def submit_package(
        self,
        crp: CandidateResearchPackage,
        *,
        perturbation_mechanism_id: str | None = None,
    ) -> IntakeOutcome:
        try:
            if crp.schema_version != SCHEMA_CRP:
                raise SchemaVersionError(f"unsupported schema: {crp.schema_version}")

            # I-INT-23: never mutate sealed CRP. Alias must already be projected by A.
            if perturbation_mechanism_id:
                if not any(
                    m.get("local_id") == perturbation_mechanism_id for m in crp.payload.mechanism_proposals
                ):
                    return self._reject(
                        crp.crp_digest or "0" * 64,
                        ["MECHANISM_ALIAS_UNRESOLVED"],
                    )

            digest = compute_crp_digest(crp)
            if crp.crp_digest is not None and crp.crp_digest != digest:
                raise ValidationError("stated crp_digest ≠ recomputed digest", code="DIGEST_MISMATCH")
            crp.crp_digest = digest

            if digest in self.accepted:
                prev = self.accepted[digest]
                return IntakeOutcome(
                    status=IntakeStatus.ACCEPTED_DRAFT,
                    receipt=prev,
                    obligations=list(self.obligations_by_crp.get(digest, [])),
                    replay=True,
                )

            validate_crp_admissibility(
                crp, live_scope_pin=self.live_scope_pin, assistant_binding_live=bool(crp.author_binding_digest)
            )

            profile = crp.profile
            reasons: list[str] = []
            if profile == CrpProfile.PHASE_B_STABILIZATION and not crp.payload.mechanism_proposals:
                reasons.append("MECHANISM_REQUIRED")
            if profile == CrpProfile.PHASE_B_STABILIZATION:
                mech_ids = {m.get("local_id") for m in crp.payload.mechanism_proposals}
                for c in crp.payload.claims:
                    mid = c.get("perturbation_mechanism_id")
                    if not mid or mid not in mech_ids:
                        reasons.append("MECHANISM_ALIAS_UNRESOLVED")
                        break
            if profile == CrpProfile.BRIDGE_ONLY and not crp.payload.bridge_proposals:
                reasons.append("UNSUPPORTED_CANDIDATE_TYPE")
            if profile == CrpProfile.OBLIGATION_ONLY and not crp.payload.claims:
                reasons.append("UNSUPPORTED_CANDIDATE_TYPE")
            for c in crp.payload.claims:
                if "chain_segment" not in c:
                    reasons.append("CRP_SCHEMA")

            if reasons:
                return self._reject(digest, reasons)

            claim_digests = [claim_digest(c) for c in crp.payload.claims]
            if not claim_digests and profile == CrpProfile.PHASE_A_CHARACTERIZATION:
                claim_digests = [claim_digest({"characterization": True, "examples": crp.payload.examples})]
            if not claim_digests:
                return self._reject(digest, ["UNSUPPORTED_CANDIDATE_TYPE"])

            obs = mint_obligations_for_claims(
                crp_digest=digest,
                profile=profile.value,
                claim_digests=claim_digests,
                extra_per_claim=2 if len(crp.payload.claims) else 1,
            )
            self.event_seq += 1
            receipt = IntakeReceipt(
                crp_digest=digest,
                event_seq=self.event_seq,
                draft_claim_digests=claim_digests,
                obligation_digests=[o.obligation_digest for o in obs],
                status=IntakeStatus.ACCEPTED_DRAFT,
            )
            receipt.receipt_digest = compute_receipt_digest(receipt)
            self.accepted[digest] = receipt
            self.obligations_by_crp[digest] = obs
            return IntakeOutcome(status=IntakeStatus.ACCEPTED_DRAFT, receipt=receipt, obligations=obs)

        except SchemaVersionError as e:
            return self._reject("0" * 64, ["UNSUPPORTED_SCHEMA_VERSION", str(e)])
        except UnsupportedEnumError as e:
            return self._reject("0" * 64, ["PROFILE_MISMATCH", str(e)])
        except AdmissibilityError as e:
            d = getattr(crp, "crp_digest", None) or "0" * 64
            return self._reject(d, [e.code, str(e)])
        except (ValidationError, IdempotencyConflict) as e:
            d = getattr(crp, "crp_digest", None) or "0" * 64
            return self._reject(d, [getattr(e, "code", "VALIDATION"), str(e)])

    def _reject(self, crp_digest: str, reasons: list[str]) -> IntakeOutcome:
        self.event_seq += 1
        receipt = IntakeReceipt(
            crp_digest=crp_digest,
            event_seq=self.event_seq,
            draft_claim_digests=[],
            obligation_digests=[],
            status=IntakeStatus.REJECTED,
            reason_codes=reasons,
        )
        receipt.receipt_digest = compute_receipt_digest(receipt)
        return IntakeOutcome(status=IntakeStatus.REJECTED, receipt=receipt, reason_codes=reasons)

    def submit_batch_packages(self, packages: list[CandidateResearchPackage]) -> list[IntakeOutcome]:
        return [self.submit_package(p) for p in packages]
