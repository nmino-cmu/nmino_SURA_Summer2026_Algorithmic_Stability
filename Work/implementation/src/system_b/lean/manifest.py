"""ART-10b VerifierTranscript / LeanManifest digests + DerivedLeanStatus."""

from __future__ import annotations

from enum import Enum
from typing import Any

from art_int.canon import H, H_tagged, digest_object


class DerivedLeanStatus(str, Enum):
    LEAN_FULL = "LEAN_FULL"
    LEAN_CORE = "LEAN_CORE"
    LEAN_STATEMENT = "LEAN_STATEMENT"
    LEAN_BLOCKED = "LEAN_BLOCKED"
    NOT_READY_FOR_LEAN = "NOT_READY_FOR_LEAN"
    LEAN_STALE = "LEAN_STALE"


_RANK = {
    DerivedLeanStatus.LEAN_FULL: 5,
    DerivedLeanStatus.LEAN_CORE: 4,
    DerivedLeanStatus.LEAN_STATEMENT: 3,
    DerivedLeanStatus.LEAN_BLOCKED: 2,
    DerivedLeanStatus.NOT_READY_FOR_LEAN: 1,
    DerivedLeanStatus.LEAN_STALE: 0,
}


def status_rank(s: DerivedLeanStatus) -> int:
    return _RANK[s]


def derived_lean_status(
    *,
    manifest: dict[str, Any] | None,
    toolchain_head: dict[str, Any] | None = None,
    pin_mismatch: bool = False,
    full_cx_hits: bool = False,
    superseded: bool = False,
) -> DerivedLeanStatus:
    """I-LM-10 pure function. Status is never stored as authority (I-LM-11)."""
    if manifest is None:
        return DerivedLeanStatus.NOT_READY_FOR_LEAN

    transcript = manifest.get("transcript") or {}
    if toolchain_head is not None:
        if transcript.get("toolchain_digest") != toolchain_head.get("toolchain_digest"):
            return DerivedLeanStatus.LEAN_STALE
        if transcript.get("mathlib_pin_digest") != toolchain_head.get("mathlib_pin_digest"):
            return DerivedLeanStatus.LEAN_STALE
    if pin_mismatch or full_cx_hits or superseded:
        return DerivedLeanStatus.LEAN_STALE

    if not transcript.get("build_ok"):
        return DerivedLeanStatus.LEAN_BLOCKED

    sorry_count = int(transcript.get("sorry_count", 0))
    admit_count = int(transcript.get("admit_count", 0))
    custom_axioms = list(transcript.get("custom_axiom_ids_sorted") or [])
    target_asserting = bool(transcript.get("custom_axiom_asserts_target", False))
    axiom_captured = bool(transcript.get("axiom_closure_captured", False))

    if sorry_count == 0 and admit_count == 0 and not target_asserting and not custom_axioms:
        # LEAN_FULL requires a captured axiom closure (may be empty only if Lean reports none)
        if not axiom_captured:
            return DerivedLeanStatus.LEAN_BLOCKED
        return DerivedLeanStatus.LEAN_FULL
    if sorry_count == 0 and admit_count == 0:
        return DerivedLeanStatus.LEAN_CORE
    return DerivedLeanStatus.LEAN_STATEMENT


def build_transcript(
    *,
    toolchain_digest: str,
    mathlib_pin_digest: str,
    entry_module_id: str,
    lean_statement_digest: str,
    proof_tree_digest: str,
    import_closure_digest: str,
    definition_pin_set: list[str],
    sorry_count: int,
    admit_count: int,
    custom_axiom_ids_sorted: list[str],
    imported_axiom_closure_sorted: list[str],
    build_ok: bool,
    rebuild_log_digest: str,
    custom_axiom_asserts_target: bool = False,
    axiom_closure_captured: bool = False,
) -> dict[str, Any]:
    return {
        "toolchain_digest": toolchain_digest,
        "mathlib_pin_digest": mathlib_pin_digest,
        "entry_module_id": entry_module_id,
        "lean_statement_digest": lean_statement_digest,
        "proof_tree_digest": proof_tree_digest,
        "import_closure_digest": import_closure_digest,
        "definition_pin_set": list(definition_pin_set),
        "sorry_count": sorry_count,
        "admit_count": admit_count,
        "custom_axiom_ids_sorted": sorted(custom_axiom_ids_sorted),
        "imported_axiom_closure_sorted": sorted(imported_axiom_closure_sorted),
        "build_ok": build_ok,
        "rebuild_log_digest": rebuild_log_digest,
        "custom_axiom_asserts_target": custom_axiom_asserts_target,
        "axiom_closure_captured": axiom_closure_captured,
    }


def build_manifest(
    *,
    claim_digest: str,
    claim_math_fingerprint: str,
    transcript: dict[str, Any],
    store_kind: str = "ART10b_SURROGATE_V1",
    extra_limitations: list[str] | None = None,
) -> dict[str, Any]:
    """Filesystem surrogate for ART-10b LeanManifest (no Commit EventLog yet)."""
    transcript_digest = digest_object(transcript)
    manifest_digest = H_tagged("ART10b.LM.v4", claim_digest, claim_math_fingerprint, transcript_digest)
    limitations = sorted(
        {
            "LEAN_MANIFEST_WITHOUT_COMMIT",
            "DEFINITION_PINS_SURROGATE",
            *(extra_limitations or []),
        }
    )
    return {
        "store_kind": store_kind,
        "limitations": limitations,
        "claim_digest": claim_digest,
        "claim_math_fingerprint": claim_math_fingerprint,
        "transcript": transcript,
        "manifest_digest": manifest_digest,
    }


def file_digest(data: bytes) -> str:
    return H(data)
