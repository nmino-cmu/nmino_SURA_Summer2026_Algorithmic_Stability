"""Idempotency replay rules (I-INT-21)."""

from __future__ import annotations

from art_int.errors import IdempotencyConflict


def check_idempotency_replay(
    *,
    idempotency_key: str,
    incoming_digest: str,
    prior_key: str | None,
    prior_digest: str | None,
) -> str:
    """
    Returns:
      'fresh' — no prior
      'replay' — same key + same digest
    Raises IdempotencyConflict if same key + different digest.
    """
    if idempotency_key != incoming_digest:
        raise IdempotencyConflict("idempotency_key must equal digest")
    if prior_key is None:
        return "fresh"
    if prior_key != idempotency_key:
        return "fresh"
    if prior_digest == incoming_digest:
        return "replay"
    raise IdempotencyConflict(
        "same idempotency_key with different digest",
        code="IDEMPOTENCY_CONFLICT",
    )
