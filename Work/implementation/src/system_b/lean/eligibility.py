"""Fail-closed Lean eligibility gate."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from art_int.canon import BOT_TOKEN, H_tagged
from art_int.crp import SCHEMA_CRP
from system_b.lean.bundle import LeanInputBundle, SCHEMA_BUNDLE
from system_b.lean.profiles import resolve_profile
from system_b.obligations import claim_digest

_ACCEPTED_RECEIPT = frozenset({"ACCEPTED_DRAFT", "ACCEPTED"})


@dataclass(frozen=True)
class EligibilityResult:
    ok: bool
    reason_codes: tuple[str, ...]
    claim: dict[str, Any] | None = None
    draft_claim_digest: str | None = None


def recompute_crp_digest_from_sealed(sealed: dict[str, Any]) -> str:
    """Recompute CRP digest from sealed wire identity fields (fail closed on missing)."""
    required = (
        "author_kind",
        "author_principal_digest",
        "profile",
        "math_scope_pin_digest",
        "payload",
        "schema_version",
    )
    for k in required:
        if k not in sealed:
            raise ValueError(f"sealed CRP missing {k}")
    if sealed["schema_version"] != SCHEMA_CRP:
        raise ValueError("unsupported sealed CRP schema")
    binding = sealed.get("author_binding_digest", BOT_TOKEN)
    if binding is None:
        binding = BOT_TOKEN
    prior = sealed.get("prior_crp_digest", BOT_TOKEN)
    if prior is None:
        prior = BOT_TOKEN
    return H_tagged(
        SCHEMA_CRP,
        sealed["author_kind"],
        sealed["author_principal_digest"],
        binding,
        sealed["profile"],
        sealed["math_scope_pin_digest"],
        sealed["payload"],
        prior,
    )


def check_eligibility(bundle: LeanInputBundle) -> EligibilityResult:
    reasons: list[str] = []
    run = bundle.verification_run
    if bundle.schema_version != SCHEMA_BUNDLE:
        return EligibilityResult(False, ("INVALID_BUNDLE",))

    sealed = bundle.sealed_crp or {}
    if not sealed:
        return EligibilityResult(False, ("SEALED_CRP_MISSING", "NOT_READY_FOR_LEAN"))

    if sealed.get("crp_digest") and sealed["crp_digest"] != bundle.crp_digest:
        reasons.append("CRP_DIGEST_MISMATCH")

    try:
        recomputed = recompute_crp_digest_from_sealed(sealed)
        if recomputed != bundle.crp_digest:
            reasons.append("CRP_DIGEST_MISMATCH")
    except ValueError:
        reasons.append("CRP_DIGEST_UNVERIFIABLE")

    receipt = bundle.receipt or {}
    if not receipt:
        reasons.append("RECEIPT_MISSING")
    else:
        if receipt.get("crp_digest") and receipt["crp_digest"] != bundle.crp_digest:
            reasons.append("RECEIPT_CRP_MISMATCH")
        st = str(receipt.get("status", ""))
        if st and st not in _ACCEPTED_RECEIPT:
            reasons.append("RECEIPT_NOT_ACCEPTED")

    verdict = run.get("audit_verdict")
    if verdict is None:
        reasons.append("UNKNOWN_STATUS")
    elif verdict not in ("PASS", "FAIL", "IRRELEVANT", "ESCALATE_HUMAN", "NONE"):
        reasons.append("UNKNOWN_STATUS")
    elif verdict != "PASS":
        reasons.append("AUDIT_NOT_PASS")

    limitations = list(run.get("limitations") or [])
    if "REJECTED_FOR_LEAN" in limitations:
        reasons.append("REJECTED_FOR_LEAN")

    claims = list((sealed.get("payload") or {}).get("claims") or [])
    if not claims:
        return EligibilityResult(False, tuple(dict.fromkeys(reasons + ["NO_CLAIMS", "NOT_READY_FOR_LEAN"])))

    target: dict[str, Any] | None = None
    cd: str | None = None
    profile = None
    for c in claims:
        profile = resolve_profile(c)
        if profile is not None:
            target = c
            cd = claim_digest(c)
            break
    if target is None or profile is None:
        return EligibilityResult(
            False, tuple(dict.fromkeys(reasons + ["NO_PROFILE_MATCH", "NOT_READY_FOR_LEAN"]))
        )

    digests = list(receipt.get("draft_claim_digests") or [])
    if digests and cd not in digests:
        reasons.append("RECEIPT_CLAIM_MISMATCH")

    if str(target.get("evaluation", "")).startswith("DEMO_"):
        reasons.append("DEMO_EVALUATION")

    if not profile.formal_matches(target):
        reasons.append("FORMAL_MISMATCH")

    saw_ob = False
    for r in run.get("results") or []:
        if r.get("draft_claim_digest") == cd:
            saw_ob = True
            if r.get("status") != "DISCHARGED":
                reasons.append("OBLIGATION_NOT_DISCHARGED")
            if r.get("kind") == "COUNTEREXAMPLE":
                reasons.append("COUNTEREXAMPLE")
    if not saw_ob:
        reasons.append("OBLIGATION_MISSING")

    for cx in run.get("counterexamples") or []:
        if cx.get("claim_digest") == cd or cd in (cx.get("target_claim_digests") or []):
            reasons.append("COUNTEREXAMPLE")

    if reasons:
        return EligibilityResult(False, tuple(dict.fromkeys(reasons + ["NOT_READY_FOR_LEAN"])))
    return EligibilityResult(True, (), target, cd)
