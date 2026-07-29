"""Re-verify an on-disk certificate against live Lean sources (anti-forgery)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from art_int.canon import H
from system_b.lean.ir import statement_region_digest
from system_b.lean.manifest import DerivedLeanStatus, derived_lean_status
from system_b.lean.placeholders import FORBIDDEN_IN_RESEARCH, scan_paths


@dataclass(frozen=True)
class CertVerification:
    ok: bool
    status: DerivedLeanStatus
    reason_codes: tuple[str, ...]


def verify_certificate(
    *,
    lean_root: Path,
    operator_id: str,
    theorem_id: str,
    prop_module_relative: str,
    toolchain_head: dict[str, Any] | None = None,
) -> CertVerification:
    """Fail closed if manifest digests do not match live sources / scans."""
    from system_b.lean.store import LeanManifestStore, sanitize_id

    sanitize_id(operator_id, field="operator_id")
    sanitize_id(theorem_id, field="theorem_id")
    store = LeanManifestStore(lean_root / "certificates")
    manifest = store.read_manifest(operator_id, theorem_id)
    if manifest is None:
        return CertVerification(False, DerivedLeanStatus.NOT_READY_FOR_LEAN, ("MANIFEST_MISSING",))

    reasons: list[str] = []
    transcript = manifest.get("transcript") or {}

    if toolchain_head is None:
        head_path = lean_root / "certificates" / "toolchain_head.json"
        if head_path.is_file():
            import json

            toolchain_head = json.loads(head_path.read_text(encoding="utf-8"))

    prop_path = (lean_root / prop_module_relative).resolve()
    lean_resolved = lean_root.resolve()
    if not str(prop_path).startswith(str(lean_resolved)):
        return CertVerification(False, DerivedLeanStatus.LEAN_STALE, ("PROP_PATH_ESCAPE",))
    if not prop_path.is_file():
        return CertVerification(False, DerivedLeanStatus.LEAN_STALE, ("PROP_FILE_MISSING",))

    live_proof_digest = H(prop_path.read_bytes())
    if transcript.get("proof_tree_digest") != live_proof_digest:
        reasons.append("PROOF_DIGEST_MISMATCH")

    src = prop_path.read_text(encoding="utf-8")
    try:
        live_stmt = statement_region_digest(src)
    except ValueError:
        return CertVerification(False, DerivedLeanStatus.LEAN_STALE, ("STATEMENT_MARKERS_MISSING",))
    if transcript.get("lean_statement_digest") != live_stmt:
        reasons.append("STATEMENT_DIGEST_MISMATCH")

    findings = scan_paths([lean_root / "Research"])
    sorry_count = sum(1 for f in findings if f.kind == "sorry")
    admit_count = sum(1 for f in findings if f.kind == "admit")
    if sorry_count != int(transcript.get("sorry_count", -1)):
        reasons.append("SORRY_COUNT_MISMATCH")
    if admit_count != int(transcript.get("admit_count", -1)):
        reasons.append("ADMIT_COUNT_MISMATCH")
    if any(f.kind in FORBIDDEN_IN_RESEARCH for f in findings):
        reasons.append("PLACEHOLDER_PRESENT")

    status = derived_lean_status(manifest=manifest, toolchain_head=toolchain_head)
    if status == DerivedLeanStatus.LEAN_FULL:
        if not transcript.get("axiom_closure_captured"):
            reasons.append("AXIOM_CLOSURE_MISSING")
        # For FULL, closure list must be present (may include classical axioms)
        if "imported_axiom_closure_sorted" not in transcript:
            reasons.append("AXIOM_CLOSURE_MISSING")

    # Forged status_display JSON must not override derived status
    status_path = store.path_for(operator_id, theorem_id) / "status_recomputed.json"
    if status_path.is_file():
        import json

        displayed = json.loads(status_path.read_text(encoding="utf-8"))
        if displayed.get("derived_lean_status") != status.value:
            reasons.append("STATUS_DISPLAY_FORGERY")

    if reasons:
        return CertVerification(False, DerivedLeanStatus.LEAN_STALE, tuple(dict.fromkeys(reasons)))
    return CertVerification(True, status, ())
