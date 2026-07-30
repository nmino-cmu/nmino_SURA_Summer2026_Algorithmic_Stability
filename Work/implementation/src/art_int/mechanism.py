"""perturbation_mechanism_id → mechanism_proposals alias (ART-INT)."""

from __future__ import annotations

from typing import Any

from art_int.crp import CrpPayload


def apply_perturbation_mechanism_alias(
    payload: CrpPayload,
    *,
    perturbation_mechanism_id: str | None,
    mechanism_body: dict[str, Any] | None = None,
) -> CrpPayload:
    """
    If ExampleCard.perturbation_mechanism_id is set, ensure a matching
    mechanism_proposals entry with local_id. Phase A may omit (id=None).
    B has no perturbation_mechanism_id field.
    """
    if not perturbation_mechanism_id:
        return payload
    for m in payload.mechanism_proposals:
        if m.get("local_id") == perturbation_mechanism_id:
            return payload
    entry = dict(mechanism_body or {})
    entry["local_id"] = perturbation_mechanism_id
    payload.mechanism_proposals = list(payload.mechanism_proposals) + [entry]
    return payload
