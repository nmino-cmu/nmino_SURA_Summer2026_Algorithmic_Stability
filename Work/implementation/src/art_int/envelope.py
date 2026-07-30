"""SubmissionEnvelope (S-INT-ENV)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from art_int.crp import CandidateResearchPackage, compute_crp_digest
from art_int.errors import IdempotencyConflict, SchemaVersionError, UnknownFieldError, ValidationError

SCHEMA_ENV = "ARTINT.ENV.v1"
ALLOWED_TELEMETRY = frozenset({"a_session_id", "a_batch_id", "a_attempt_id"})


@dataclass
class SubmissionEnvelope:
    crp: CandidateResearchPackage
    idempotency_key: str
    schema_version: str = SCHEMA_ENV
    a_session_id: str | None = None
    a_batch_id: str | None = None
    a_attempt_id: str | None = None

    def to_wire(self) -> dict[str, Any]:
        d: dict[str, Any] = {
            "schema_version": self.schema_version,
            "crp": self.crp.to_wire(),
            "idempotency_key": self.idempotency_key,
        }
        if self.a_session_id is not None:
            d["a_session_id"] = self.a_session_id
        if self.a_batch_id is not None:
            d["a_batch_id"] = self.a_batch_id
        if self.a_attempt_id is not None:
            d["a_attempt_id"] = self.a_attempt_id
        return d


def validate_envelope(env: SubmissionEnvelope, *, known_extra_keys: set[str] | None = None) -> None:
    if env.schema_version != SCHEMA_ENV:
        raise SchemaVersionError(f"unsupported envelope schema: {env.schema_version}")
    digest = env.crp.crp_digest or compute_crp_digest(env.crp)
    if env.idempotency_key != digest:
        raise ValidationError(
            "idempotency_key must equal crp_digest", code="IDEMPOTENCY_KEY_MISMATCH"
        )


def strip_or_reject_unknown(raw: dict[str, Any]) -> dict[str, Any]:
    """I-INT-ENV-01: strip a_* telemetry; reject other unknown keys."""
    known = {
        "schema_version",
        "crp",
        "idempotency_key",
        *ALLOWED_TELEMETRY,
    }
    out = {}
    for k, v in raw.items():
        if k in known:
            out[k] = v
        elif k.startswith("a_"):
            continue  # strip unknown telemetry
        else:
            raise UnknownFieldError(f"unknown field: {k}")
    return out
