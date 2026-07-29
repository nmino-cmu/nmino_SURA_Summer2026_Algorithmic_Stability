"""End-to-end Lean formalization from a LeanInputBundle."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from art_int.canon import H
from system_b.lean.axioms import capture_axioms, union_axiom_closure
from system_b.lean.bundle import LeanInputBundle, load_bundle
from system_b.lean.eligibility import check_eligibility
from system_b.lean.ir import FormalizationCandidate, lean_statement_digest_of, mint_candidate
from system_b.lean.lake_runner import LakeRunner
from system_b.lean.manifest import (
    DerivedLeanStatus,
    build_manifest,
    build_transcript,
    derived_lean_status,
    file_digest,
)
from system_b.lean.placeholders import FORBIDDEN_IN_RESEARCH, scan_paths
from system_b.lean.report import write_report
from system_b.lean.semantic import audit_props_and_theorems
from system_b.lean.store import LeanManifestStore, sanitize_id


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[4]


@dataclass
class LeanFormalizationResult:
    status: DerivedLeanStatus
    reason_codes: tuple[str, ...]
    candidate: FormalizationCandidate | None
    manifest: dict[str, Any] | None
    certificate_dir: Path | None
    lean_manifest_digest: str | None


def run_lean_from_bundle(
    bundle_path: Path | LeanInputBundle,
    *,
    lean_root: Path | None = None,
    skip_lake: bool = False,
    enable_llm_repair: bool = False,
) -> LeanFormalizationResult:
    if enable_llm_repair:
        from system_b.lean.llm_repair import ProofBodyRepair

        _ = ProofBodyRepair
        raise RuntimeError(
            "LLM repair disabled in v1 DoD; set enable_llm_repair only after Phase 5 adapter is configured"
        )

    root = _repo_root()
    lean_root = lean_root or (root / "lean")
    bundle = load_bundle(bundle_path) if isinstance(bundle_path, Path) else bundle_path

    elig = check_eligibility(bundle)
    if not elig.ok:
        return LeanFormalizationResult(
            DerivedLeanStatus.NOT_READY_FOR_LEAN, elig.reason_codes, None, None, None, None
        )

    assert elig.claim is not None and elig.draft_claim_digest is not None
    sanitize_id(str(elig.claim["operator"]), field="operator_id")
    sanitize_id(str(elig.claim["theorem_id"]), field="theorem_id")

    try:
        fc = mint_candidate(
            bundle,
            claim=elig.claim,
            draft_claim_digest=elig.draft_claim_digest,
            lean_root=lean_root,
            repo_root=root,
        )
    except ValueError as e:
        return LeanFormalizationResult(
            DerivedLeanStatus.NOT_READY_FOR_LEAN,
            ("SCHEMA_FAIL", str(e)),
            None,
            None,
            None,
            None,
        )

    sem = audit_props_and_theorems(fc, lean_root)
    if not sem.ok:
        return LeanFormalizationResult(
            DerivedLeanStatus.NOT_READY_FOR_LEAN, sem.reason_codes, fc, None, None, None
        )

    research = lean_root / "Research"
    findings = scan_paths([research])
    sorry_count = sum(1 for f in findings if f.kind == "sorry")
    admit_count = sum(1 for f in findings if f.kind == "admit")
    custom_axioms = sorted({f.text for f in findings if f.kind == "axiom"})
    forbidden = [f for f in findings if f.kind in FORBIDDEN_IN_RESEARCH]

    build_ok = False
    lake_log = ""
    axiom_closure: list[str] = []
    axiom_captured = False
    reasons: list[str] = []

    if skip_lake:
        build_ok = False
        lake_log = "SKIP_LAKE"
        reasons.append("SKIP_LAKE_NO_KERNEL")
    elif forbidden:
        build_ok = False
        lake_log = "PLACEHOLDER_SCAN_FAILED"
        reasons.append("PLACEHOLDER_PRESENT")
    else:
        runner = LakeRunner(lean_root)
        result = runner.build()
        lake_log = result.stdout + "\n" + result.stderr
        build_ok = result.returncode == 0 and sorry_count == 0 and admit_count == 0 and not custom_axioms
        if result.returncode != 0:
            reasons.append("LEAN_BUILD_FAILED")
        if build_ok:
            try:
                decl_names = [t["theorem_name"] for t in fc.targets]
                by_decl = capture_axioms(
                    lean_root,
                    import_module=fc.lean_namespace,
                    decl_names=decl_names,
                )
                axiom_closure = union_axiom_closure(by_decl, decl_names)
                axiom_captured = True
            except Exception as e:
                build_ok = False
                axiom_captured = False
                reasons.append("AXIOM_CAPTURE_FAILED")
                lake_log += f"\nAXIOM_CAPTURE_FAILED: {e}"

    toolchain_path = lean_root / "lean-toolchain"
    manifest_lock = lean_root / "lake-manifest.json"
    toolchain_digest = file_digest(toolchain_path.read_bytes()) if toolchain_path.is_file() else H(b"missing")
    mathlib_pin_digest = (
        file_digest(manifest_lock.read_bytes()) if manifest_lock.is_file() else H(b"no-mathlib")
    )
    head = {
        "toolchain_digest": toolchain_digest,
        "mathlib_pin_digest": mathlib_pin_digest,
        "set_at_event_id": "SURROGATE",
    }
    (lean_root / "certificates").mkdir(parents=True, exist_ok=True)
    (lean_root / "certificates" / "toolchain_head.json").write_text(
        json.dumps(head, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    prop_rel = Path(fc.prop_module_relative)
    stmt_digest = lean_statement_digest_of(fc)
    proof_tree_digest = H((lean_root / prop_rel).read_bytes())
    # Import closure: top-level operator package under Research.Operators
    import_ns = fc.lean_namespace.rsplit(".", 1)[0] if "." in fc.lean_namespace else fc.lean_namespace
    transcript = build_transcript(
        toolchain_digest=toolchain_digest,
        mathlib_pin_digest=mathlib_pin_digest,
        entry_module_id=fc.lean_namespace,
        lean_statement_digest=stmt_digest,
        proof_tree_digest=proof_tree_digest,
        import_closure_digest=H(import_ns.encode("utf-8")),
        definition_pin_set=[fc.operator_math_source_digest, *fc.prop_module_digests],
        sorry_count=sorry_count,
        admit_count=admit_count,
        custom_axiom_ids_sorted=custom_axioms,
        imported_axiom_closure_sorted=axiom_closure,
        build_ok=build_ok,
        rebuild_log_digest=H(lake_log.encode("utf-8")),
        axiom_closure_captured=axiom_captured,
    )
    extra_lim = list(fc.known_gaps)
    if axiom_captured:
        extra_lim.append("AXIOM_CLOSURE_CAPTURED")
    else:
        extra_lim.append("AXIOM_CLOSURE_UNCAPTURED")
    if "MATHLIB_REAL_PENDING" in fc.known_gaps:
        extra_lim.append("INT_ORDERED_GROUP_CORE_NOT_REAL")
    score_enc = (fc.conventions or {}).get("score_encoding", "")
    is_real = score_enc == "REAL_MATHLIB"
    domain = "REAL_MATHLIB" if is_real else "INT_ORDERED_GROUP_CORE"
    force_recert = is_real  # ℝ upgrades must overwrite Int certificates

    manifest = build_manifest(
        claim_digest=fc.draft_claim_digest,
        claim_math_fingerprint=fc.draft_claim_digest,
        transcript=transcript,
        extra_limitations=sorted(set(extra_lim)),
    )
    status = derived_lean_status(manifest=manifest, toolchain_head=head)
    report = write_report(
        fc=fc,
        system2_statement=fc.system2_statement,
        status=status,
        build_ok=build_ok,
        sorry_count=sorry_count,
        admit_count=admit_count,
        imported_axioms=axiom_closure,
        semantic_ok=sem.ok,
        lake_log_digest=transcript["rebuild_log_digest"],
        axiom_captured=axiom_captured,
    )

    cert_dir: Path | None = None
    existing: dict[str, Any] | None = None
    persist = (not skip_lake) and build_ok and axiom_captured and status in (
        DerivedLeanStatus.LEAN_FULL,
        DerivedLeanStatus.LEAN_CORE,
    )
    if persist:
        store = LeanManifestStore(lean_root / "certificates")
        existing = store.read_manifest(fc.operator_id, fc.theorem_id)
        if existing is not None and not force_recert:
            from system_b.lean.verify import verify_certificate

            live = verify_certificate(
                lean_root=lean_root,
                operator_id=fc.operator_id,
                theorem_id=fc.theorem_id,
                prop_module_relative=fc.prop_module_relative,
                toolchain_head=head,
            )
            if live.ok and live.status == DerivedLeanStatus.LEAN_FULL and status != DerivedLeanStatus.LEAN_FULL:
                reasons.append("PRESERVE_EXISTING_LEAN_FULL")
                persist = False
                cert_dir = store.path_for(fc.operator_id, fc.theorem_id)
        # REAL force_recert still must not clobber a published cert when Lean math is unchanged
        # (e.g. Phase B selection_stability packaging of the same theorem_id).
        if persist and existing is not None and force_recert and status == DerivedLeanStatus.LEAN_FULL:
            from system_b.lean.verify import verify_certificate

            ex_tr = existing.get("transcript") or {}
            live = verify_certificate(
                lean_root=lean_root,
                operator_id=fc.operator_id,
                theorem_id=fc.theorem_id,
                prop_module_relative=fc.prop_module_relative,
                toolchain_head=head,
            )
            if (
                live.ok
                and live.status == DerivedLeanStatus.LEAN_FULL
                and ex_tr.get("lean_statement_digest") == stmt_digest
                and ex_tr.get("proof_tree_digest") == proof_tree_digest
                and ex_tr.get("build_ok")
                and existing.get("manifest_digest")
            ):
                reasons.append("PRESERVE_EXISTING_SAME_LEAN_MATH")
                persist = False
                cert_dir = store.path_for(fc.operator_id, fc.theorem_id)
        if persist:
            cert_dir = store.write(
                operator_id=fc.operator_id,
                theorem_id=fc.theorem_id,
                manifest=manifest,
                transcript=transcript,
                report_md=report,
                status_display={
                    "derived_lean_status": status.value,
                    "manifest_digest": manifest["manifest_digest"],
                    "note": "informational; recompute via derived_lean_status / verify_certificate",
                    "domain": domain,
                },
            )
    elif skip_lake:
        reasons.append("CERTIFICATE_NOT_PERSISTED")
    else:
        attempt_root = lean_root / "scratch" / "attempts"
        attempt_store = LeanManifestStore(attempt_root)
        cert_dir = attempt_store.write(
            operator_id=fc.operator_id,
            theorem_id=fc.theorem_id,
            manifest=manifest,
            transcript=transcript,
            report_md=report,
            status_display={
                "derived_lean_status": status.value,
                "manifest_digest": manifest["manifest_digest"],
                "note": "attempt only; not an accepted certificate",
                "domain": domain,
            },
        )
        reasons.append("CERTIFICATE_ATTEMPT_ONLY")

    if not build_ok and "LEAN_BLOCKED" not in reasons and "SKIP_LAKE_NO_KERNEL" not in reasons:
        reasons.append("LEAN_BLOCKED")
    digest_out = None
    if persist:
        digest_out = manifest["manifest_digest"]
    elif cert_dir is not None and "PRESERVE_EXISTING_SAME_LEAN_MATH" in reasons and existing is not None:
        digest_out = existing.get("manifest_digest")
    elif cert_dir is not None and "PRESERVE_EXISTING_LEAN_FULL" in reasons and existing is not None:
        digest_out = existing.get("manifest_digest")
    return LeanFormalizationResult(
        status,
        tuple(dict.fromkeys(reasons)),
        fc,
        manifest,
        cert_dir,
        digest_out,
    )


def main() -> None:
    import argparse

    p = argparse.ArgumentParser(description="Run Lean formalization from a LeanInputBundle")
    p.add_argument("bundle", type=Path)
    p.add_argument(
        "--skip-lake",
        action="store_true",
        help="Diagnostic only: never produces LEAN_FULL (no kernel check)",
    )
    args = p.parse_args()
    res = run_lean_from_bundle(args.bundle, skip_lake=args.skip_lake)
    print(
        json.dumps(
            {
                "status": res.status.value,
                "reasons": list(res.reason_codes),
                "manifest": res.lean_manifest_digest,
            }
        )
    )


if __name__ == "__main__":
    main()
