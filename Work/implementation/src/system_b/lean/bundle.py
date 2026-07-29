"""LeanInputBundle persistence (ARTLEAN.BUNDLE.v1)."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from art_int.canon import H_tagged
from art_int.crp import CandidateResearchPackage, compute_crp_digest
from art_int.receipt import IntakeReceipt

SCHEMA_BUNDLE = "ARTLEAN.BUNDLE.v1"


@dataclass
class LeanInputBundle:
    sealed_crp: dict[str, Any]
    crp_digest: str
    receipt: dict[str, Any]
    verification_run: dict[str, Any]
    created_at: str
    feedback_export_digest: str | None = None
    schema_version: str = SCHEMA_BUNDLE
    bundle_digest: str | None = None

    def body_for_digest(self) -> dict[str, Any]:
        d: dict[str, Any] = {
            "schema_version": self.schema_version,
            "sealed_crp": self.sealed_crp,
            "crp_digest": self.crp_digest,
            "receipt": self.receipt,
            "verification_run": self.verification_run,
            "created_at": self.created_at,
        }
        if self.feedback_export_digest is not None:
            d["feedback_export_digest"] = self.feedback_export_digest
        return d

    def compute_digest(self) -> str:
        return H_tagged(SCHEMA_BUNDLE, self.body_for_digest())

    def to_wire(self) -> dict[str, Any]:
        if self.bundle_digest is None:
            self.bundle_digest = self.compute_digest()
        d = self.body_for_digest()
        d["bundle_digest"] = self.bundle_digest
        return d


def export_bundle(
    *,
    crp: CandidateResearchPackage,
    receipt: IntakeReceipt,
    run_id: str,
    results: list[dict[str, Any]],
    audit_verdict: str | None,
    limitations: list[str],
    counterexamples: list[dict[str, Any]] | None = None,
    feedback_export_digest: str | None = None,
) -> LeanInputBundle:
    recomputed = compute_crp_digest(crp)
    b = LeanInputBundle(
        sealed_crp=crp.to_wire(),
        crp_digest=recomputed,
        receipt=receipt.to_wire(),
        verification_run={
            "run_id": run_id,
            "results": results,
            "audit_verdict": audit_verdict,
            "limitations": list(limitations),
            "counterexamples": list(counterexamples or []),
        },
        created_at=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        feedback_export_digest=feedback_export_digest,
    )
    b.bundle_digest = b.compute_digest()
    return b


def write_bundle(bundle: LeanInputBundle, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(bundle.to_wire(), indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_bundle(path: Path) -> LeanInputBundle:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if raw.get("schema_version") != SCHEMA_BUNDLE:
        raise ValueError(f"unsupported bundle schema: {raw.get('schema_version')}")
    stated = raw.get("bundle_digest")
    b = LeanInputBundle(
        sealed_crp=raw["sealed_crp"],
        crp_digest=raw["crp_digest"],
        receipt=raw["receipt"],
        verification_run=raw["verification_run"],
        created_at=raw["created_at"],
        feedback_export_digest=raw.get("feedback_export_digest"),
    )
    computed = b.compute_digest()
    if stated is not None and stated != computed:
        raise ValueError("bundle_digest mismatch")
    b.bundle_digest = computed
    return b


def verification_run_to_dicts(run: Any) -> list[dict[str, Any]]:
    out = []
    for r in run.results:
        out.append(
            {
                "obligation_digest": r.obligation_digest,
                "draft_claim_digest": r.draft_claim_digest,
                "status": r.status.value,
                "kind": r.kind.value,
                "detail": r.detail,
            }
        )
    return out
