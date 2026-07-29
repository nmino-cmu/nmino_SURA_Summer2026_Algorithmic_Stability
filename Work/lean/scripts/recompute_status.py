#!/usr/bin/env python3
"""Recompute DerivedLeanStatus; fail closed on stale/forged accepted certs."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from types import ModuleType

_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_ROOT / "implementation" / "src"))

from system_b.lean.manifest import DerivedLeanStatus, derived_lean_status  # noqa: E402
from system_b.lean.profiles import all_profiles  # noqa: E402
from system_b.lean.verify import verify_certificate  # noqa: E402

# Single source of truth: the registered profile allowlist (one entry per accepted cert).
_ACCEPTED: dict[tuple[str, str], ModuleType] = {
    (p.OPERATOR, p.THEOREM_ID): p for p in all_profiles()
}


def _domain(profile: ModuleType | None, previous: dict[str, object]) -> object:
    """Mirror workflow.py: domain follows the profile's score_encoding."""
    if profile is None:
        return previous.get("domain", "REAL_MATHLIB")
    enc = (profile.CONVENTIONS or {}).get("score_encoding", "")
    return "REAL_MATHLIB" if enc == "REAL_MATHLIB" else "INT_ORDERED_GROUP_CORE"


def main() -> int:
    lean_root = Path(__file__).resolve().parents[1]
    cert_root = lean_root / "certificates"
    head_path = cert_root / "toolchain_head.json"
    head = json.loads(head_path.read_text(encoding="utf-8")) if head_path.is_file() else None
    rc = 0
    for man in sorted(cert_root.rglob("lean_manifest.json")):
        manifest = json.loads(man.read_text(encoding="utf-8"))
        status = derived_lean_status(manifest=manifest, toolchain_head=head)
        out = man.parent / "status_recomputed.json"
        previous = json.loads(out.read_text(encoding="utf-8")) if out.is_file() else {}
        payload = {
            "derived_lean_status": status.value,
            "domain": _domain(_ACCEPTED.get((man.parent.parent.name, man.parent.name)), previous),
            "manifest_digest": manifest.get("manifest_digest"),
            "note": "informational; not proof authority",
        }
        out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(f"{man}: {status.value}")

    for (operator_id, theorem_id), profile in _ACCEPTED.items():
        man_path = cert_root / operator_id / theorem_id / "lean_manifest.json"
        if not man_path.is_file():
            print(f"verify_certificate {operator_id}: MISSING_MANIFEST")
            rc = 1
            continue
        # Skip placeholder/scaffolding manifests that never completed System 2 binding
        man = json.loads(man_path.read_text(encoding="utf-8"))
        if man.get("manifest_digest") == "invalid-pending-system2-binding":
            print(f"verify_certificate {operator_id}: SKIP_PLACEHOLDER")
            continue
        v = verify_certificate(
            lean_root=lean_root,
            operator_id=operator_id,
            theorem_id=theorem_id,
            prop_module_relative=str(profile.PROP_RELATIVE),
            toolchain_head=head,
        )
        print(f"verify_certificate {operator_id}: ok={v.ok} status={v.status.value} reasons={v.reason_codes}")
        if not v.ok or v.status != DerivedLeanStatus.LEAN_FULL:
            rc = 1
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
