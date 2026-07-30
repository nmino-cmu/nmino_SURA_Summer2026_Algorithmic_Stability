"""Mandatory adversarial audit matrix for System 3 Lean formalization."""

from __future__ import annotations

import json
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest

from operators.argmax import lean_profile as argmax_profile
from operators.argmax.workflow import run_argmax_margin_workflow
from system_b.lean.axioms import parse_print_axioms
from system_b.lean.bundle import load_bundle
from system_b.lean.eligibility import check_eligibility
from system_b.lean.ir import statement_region_digest
from system_b.lean.lake_runner import LakeRunner
from system_b.lean.manifest import (
    DerivedLeanStatus,
    build_manifest,
    build_transcript,
    derived_lean_status,
)
from system_b.lean.placeholders import scan_text
from system_b.lean.report import write_report
from system_b.lean.store import LeanManifestStore, sanitize_id
from system_b.lean.verify import verify_certificate
from system_b.lean.workflow import run_lean_from_bundle


def _bundle():
    r = run_argmax_margin_workflow(export_lean_bundle=True)
    return load_bundle(Path(r.lean_bundle_path))


def test_01_sorry_rejected():
    f = scan_text("theorem t : True := by\n  sorry\n")
    assert any(x.kind == "sorry" for x in f)


def test_02_custom_axiom_rejected():
    f = scan_text("axiom evil : False\ntheorem t : False := evil\n")
    assert any(x.kind == "axiom" for x in f)
    f2 = scan_text("constant Evil : False\n")
    assert any(x.kind == "constant" for x in f2)


def test_03_weakened_conclusion_detected(tmp_path: Path):
    """Changing > to ≥ in STATEMENT region changes digest."""
    lean = Path(__file__).resolve().parents[3] / "lean"
    src = (lean / argmax_profile.PROP_RELATIVE).read_text(encoding="utf-8")
    d0 = statement_region_digest(src)
    assert "> 2 * ε" in src
    weakened = src.replace("> 2 * ε", "≥ 2 * ε", 1)
    assert statement_region_digest(weakened) != d0


def test_04_added_assumption_detected():
    lean = Path(__file__).resolve().parents[3] / "lean"
    src = (lean / argmax_profile.PROP_RELATIVE).read_text(encoding="utf-8")
    d0 = statement_region_digest(src)
    added = src.replace(
        "IsUniqueMaximizer s iStar →",
        "IsUniqueMaximizer s iStar → True →",
        1,
    )
    assert statement_region_digest(added) != d0


def test_05_prop_change_invalidates_certificate(tmp_path: Path):
    """After prop digest drift, verify_certificate fails closed."""
    lean = Path(__file__).resolve().parents[3] / "lean"
    # Use live cert if present; forge a stale statement digest
    store = LeanManifestStore(tmp_path / "certificates")
    t = build_transcript(
        toolchain_digest="t",
        mathlib_pin_digest="m",
        entry_module_id="E",
        lean_statement_digest="STALE",
        proof_tree_digest="STALE",
        import_closure_digest="i",
        definition_pin_set=[],
        sorry_count=0,
        admit_count=0,
        custom_axiom_ids_sorted=[],
        imported_axiom_closure_sorted=["propext"],
        build_ok=True,
        rebuild_log_digest="l",
        axiom_closure_captured=True,
    )
    m = build_manifest(claim_digest="c", claim_math_fingerprint="f", transcript=t)
    store.write(
        operator_id="argmax",
        theorem_id="bounded-perturbation-margin",
        manifest=m,
        transcript=t,
        report_md="#x",
        status_display={"derived_lean_status": "LEAN_FULL"},
    )
    # Point verify at real lean root but tmp certs — use lean_root with our certs
    fake_lean = tmp_path / "lean"
    fake_lean.mkdir()
    (fake_lean / "certificates").mkdir()
    # copy store root content
    import shutil

    shutil.copytree(tmp_path / "certificates", fake_lean / "certificates", dirs_exist_ok=True)
    prop = fake_lean / "Research/Operators/Argmax/Margin.lean"
    prop.parent.mkdir(parents=True)
    prop.write_text(
        (lean / argmax_profile.PROP_RELATIVE).read_text(encoding="utf-8"), encoding="utf-8"
    )
    (fake_lean / "certificates" / "toolchain_head.json").write_text(
        json.dumps({"toolchain_digest": "t", "mathlib_pin_digest": "m"}), encoding="utf-8"
    )
    v = verify_certificate(
        lean_root=fake_lean,
        operator_id="argmax",
        theorem_id="bounded-perturbation-margin",
        prop_module_relative=str(argmax_profile.PROP_RELATIVE),
    )
    assert not v.ok
    assert "STATEMENT_DIGEST_MISMATCH" in v.reason_codes or "PROOF_DIGEST_MISMATCH" in v.reason_codes


def test_06_copied_manifest_claim_mismatch():
    t = build_transcript(
        toolchain_digest="t",
        mathlib_pin_digest="m",
        entry_module_id="E",
        lean_statement_digest="s",
        proof_tree_digest="p",
        import_closure_digest="i",
        definition_pin_set=[],
        sorry_count=0,
        admit_count=0,
        custom_axiom_ids_sorted=[],
        imported_axiom_closure_sorted=["propext"],
        build_ok=True,
        rebuild_log_digest="l",
        axiom_closure_captured=True,
    )
    m_a = build_manifest(claim_digest="claim-A", claim_math_fingerprint="f", transcript=t)
    m_b = build_manifest(claim_digest="claim-B", claim_math_fingerprint="f", transcript=t)
    assert m_a["manifest_digest"] != m_b["manifest_digest"]
    assert m_a["claim_digest"] != m_b["claim_digest"]


def test_07_stale_olean_source_delete(tmp_path: Path):
    """Missing prop file → LEAN_STALE, not FULL."""
    fake_lean = tmp_path / "lean"
    certs = fake_lean / "certificates"
    store = LeanManifestStore(certs)
    t = build_transcript(
        toolchain_digest="t",
        mathlib_pin_digest="m",
        entry_module_id="E",
        lean_statement_digest="s",
        proof_tree_digest="p",
        import_closure_digest="i",
        definition_pin_set=[],
        sorry_count=0,
        admit_count=0,
        custom_axiom_ids_sorted=[],
        imported_axiom_closure_sorted=["propext"],
        build_ok=True,
        rebuild_log_digest="l",
        axiom_closure_captured=True,
    )
    m = build_manifest(claim_digest="c", claim_math_fingerprint="f", transcript=t)
    store.write(
        operator_id="argmax",
        theorem_id="bounded-perturbation-margin",
        manifest=m,
        transcript=t,
        report_md="#x",
        status_display={"derived_lean_status": DerivedLeanStatus.LEAN_FULL.value},
    )
    (certs / "toolchain_head.json").write_text(
        json.dumps({"toolchain_digest": "t", "mathlib_pin_digest": "m"}), encoding="utf-8"
    )
    v = verify_certificate(
        lean_root=fake_lean,
        operator_id="argmax",
        theorem_id="bounded-perturbation-margin",
        prop_module_relative="Research/Operators/Argmax/Margin.lean",
    )
    assert not v.ok
    assert "PROP_FILE_MISSING" in v.reason_codes


def test_08_forged_lean_full_status_display(tmp_path: Path):
    """Editing status_recomputed.json to LEAN_FULL while transcript is blocked is detected."""
    fake_lean = tmp_path / "lean"
    lean_real = Path(__file__).resolve().parents[3] / "lean"
    store = LeanManifestStore(fake_lean / "certificates")
    t = build_transcript(
        toolchain_digest="t",
        mathlib_pin_digest="m",
        entry_module_id="E",
        lean_statement_digest=statement_region_digest(
            (lean_real / argmax_profile.PROP_RELATIVE).read_text(encoding="utf-8")
        ),
        proof_tree_digest=__import__("art_int.canon", fromlist=["H"]).H(
            (lean_real / argmax_profile.PROP_RELATIVE).read_bytes()
        ),
        import_closure_digest="i",
        definition_pin_set=[],
        sorry_count=0,
        admit_count=0,
        custom_axiom_ids_sorted=[],
        imported_axiom_closure_sorted=[],
        build_ok=False,  # blocked
        rebuild_log_digest="l",
        axiom_closure_captured=False,
    )
    m = build_manifest(claim_digest="c", claim_math_fingerprint="f", transcript=t)
    store.write(
        operator_id="argmax",
        theorem_id="bounded-perturbation-margin",
        manifest=m,
        transcript=t,
        report_md="#x",
        status_display={"derived_lean_status": "LEAN_FULL"},  # forged
    )
    prop = fake_lean / argmax_profile.PROP_RELATIVE
    prop.parent.mkdir(parents=True)
    prop.write_text((lean_real / argmax_profile.PROP_RELATIVE).read_text(encoding="utf-8"))
    (fake_lean / "Research").mkdir(exist_ok=True)
    (fake_lean / "certificates" / "toolchain_head.json").write_text(
        json.dumps({"toolchain_digest": "t", "mathlib_pin_digest": "m"}), encoding="utf-8"
    )
    status = derived_lean_status(
        manifest=m, toolchain_head={"toolchain_digest": "t", "mathlib_pin_digest": "m"}
    )
    assert status == DerivedLeanStatus.LEAN_BLOCKED
    v = verify_certificate(
        lean_root=fake_lean,
        operator_id="argmax",
        theorem_id="bounded-perturbation-margin",
        prop_module_relative=str(argmax_profile.PROP_RELATIVE),
    )
    assert not v.ok
    assert "STATUS_DISPLAY_FORGERY" in v.reason_codes


def test_09_mismatched_receipt_claim():
    b = _bundle()
    b.receipt["draft_claim_digests"] = ["deadbeef" * 8]
    elig = check_eligibility(b)
    assert not elig.ok
    assert "RECEIPT_CLAIM_MISMATCH" in elig.reason_codes


def test_10_unknown_system2_status():
    b = _bundle()
    b.verification_run["audit_verdict"] = "TOTALLY_UNKNOWN"
    elig = check_eligibility(b)
    assert not elig.ok
    assert "UNKNOWN_STATUS" in elig.reason_codes


def test_11_path_traversal_operator_id():
    with pytest.raises(ValueError):
        sanitize_id("../etc", field="operator_id")
    store = LeanManifestStore(Path("/tmp"))
    with pytest.raises(ValueError):
        store.path_for("../../etc", "passwd")


def test_12_shell_injection_theorem_name():
    with pytest.raises(ValueError):
        sanitize_id("margin; rm -rf /", field="theorem_id")
    lean = Path(__file__).resolve().parents[3] / "lean"
    runner = LakeRunner(lean)
    with pytest.raises(ValueError):
        runner.build("foo;evil")


def test_13_namespace_shadow_changes_region():
    """A shadowed Prop short name still changes STATEMENT region if redefined."""
    lean = Path(__file__).resolve().parents[3] / "lean"
    src = (lean / argmax_profile.PROP_RELATIVE).read_text(encoding="utf-8")
    d0 = statement_region_digest(src)
    shadow = src.replace(
        "def MarginInvarianceProp : Prop :=",
        "def MarginInvarianceProp : Prop := True ∨",
        1,
    )
    assert statement_region_digest(shadow) != d0


def test_14_test_only_axiom_in_research_scan():
    f = scan_text("axiom TestOnlyEvil : True\n")
    assert any(x.kind == "axiom" for x in f)


def test_15_partial_manifest_write_atomic(tmp_path: Path):
    store = LeanManifestStore(tmp_path)
    t = build_transcript(
        toolchain_digest="t",
        mathlib_pin_digest="m",
        entry_module_id="E",
        lean_statement_digest="s",
        proof_tree_digest="p",
        import_closure_digest="i",
        definition_pin_set=[],
        sorry_count=0,
        admit_count=0,
        custom_axiom_ids_sorted=[],
        imported_axiom_closure_sorted=["propext"],
        build_ok=True,
        rebuild_log_digest="l",
        axiom_closure_captured=True,
    )
    m = build_manifest(claim_digest="c", claim_math_fingerprint="f", transcript=t)
    store.write(
        operator_id="op",
        theorem_id="th",
        manifest=m,
        transcript=t,
        report_md="# ok",
        status_display={"derived_lean_status": "LEAN_FULL"},
    )
    path = store.path_for("op", "th") / "lean_manifest.json"
    assert path.is_file()
    json.loads(path.read_text(encoding="utf-8"))  # not truncated garbage


def test_16_concurrent_certificate_writes(tmp_path: Path):
    store = LeanManifestStore(tmp_path)
    errors: list[BaseException] = []

    def one(i: int) -> None:
        try:
            t = build_transcript(
                toolchain_digest="t",
                mathlib_pin_digest="m",
                entry_module_id="E",
                lean_statement_digest=f"s{i}",
                proof_tree_digest="p",
                import_closure_digest="i",
                definition_pin_set=[],
                sorry_count=0,
                admit_count=0,
                custom_axiom_ids_sorted=[],
                imported_axiom_closure_sorted=["propext"],
                build_ok=True,
                rebuild_log_digest="l",
                axiom_closure_captured=True,
            )
            m = build_manifest(claim_digest=f"c{i}", claim_math_fingerprint="f", transcript=t)
            store.write(
                operator_id="op",
                theorem_id="th",
                manifest=m,
                transcript=t,
                report_md=f"# {i}",
                status_display={"derived_lean_status": "LEAN_FULL", "i": i},
            )
        except BaseException as e:  # noqa: BLE001
            errors.append(e)

    with ThreadPoolExecutor(max_workers=8) as ex:
        list(ex.map(one, range(20)))
    assert not errors
    # final file must be valid JSON
    json.loads((tmp_path / "op" / "th" / "lean_manifest.json").read_text(encoding="utf-8"))


def test_17_build_timeout(tmp_path: Path):
    lean = Path(__file__).resolve().parents[3] / "lean"
    runner = LakeRunner(lean, timeout_s=0)
    # timeout_s=0 may fire immediately on build
    res = runner.build()
    assert res.returncode == 124 or res.returncode != 0


def test_18_vacuous_requires_m_ge_2():
    """Accepted props require 2 ≤ m — not vacuously true on empty domain."""
    lean = Path(__file__).resolve().parents[3] / "lean"
    src = (lean / argmax_profile.PROP_RELATIVE).read_text(encoding="utf-8")
    region = src[src.index("STATEMENT_BEGIN") : src.index("STATEMENT_END")]
    assert "2 ≤ m" in region or "2 <= m" in region


def test_19_missing_axiom_report_blocks_full():
    t = build_transcript(
        toolchain_digest="t",
        mathlib_pin_digest="m",
        entry_module_id="E",
        lean_statement_digest="s",
        proof_tree_digest="p",
        import_closure_digest="i",
        definition_pin_set=[],
        sorry_count=0,
        admit_count=0,
        custom_axiom_ids_sorted=[],
        imported_axiom_closure_sorted=[],
        build_ok=True,
        rebuild_log_digest="l",
        axiom_closure_captured=False,
    )
    m = build_manifest(claim_digest="c", claim_math_fingerprint="f", transcript=t)
    assert derived_lean_status(manifest=m) == DerivedLeanStatus.LEAN_BLOCKED


def test_20_smoke_report_not_full_authority():
    """Report text must not treat smoke theorems as operator formalization authority."""
    from system_b.lean.ir import FormalizationCandidate

    fc = FormalizationCandidate(
        operator_id="argmax",
        theorem_id="bounded-perturbation-margin",
        crp_digest="x",
        draft_claim_digest="y",
        verification_run_id="z",
        bundle_digest="b",
        source_evaluation_method="ARGMAX_MARGIN_COMPUTATIONAL_V1",
        conclusion={"schema_id": "x"},
        conclusion_digest="c",
        operator_math_source_digest="m",
        prop_module_digests=[],
        audit_verdict="PASS",
        obligation_results=[],
        verifier_limitations=[],
        lean_namespace="Research.Operators.Argmax.Margin",
        targets=[],
        conventions={},
        known_gaps=["MATHLIB_REAL_PENDING"],
        semantic_freeze_digest="f",
        candidate_digest="cd",
    )
    md = write_report(
        fc=fc,
        system2_statement="stmt",
        status=DerivedLeanStatus.LEAN_FULL,
        build_ok=True,
        sorry_count=0,
        admit_count=0,
        imported_axioms=["propext"],
        semantic_ok=True,
        lake_log_digest="l",
        axiom_captured=True,
    )
    assert "Smoke" in md or "smoke" in md.lower()
    assert "MATHLIB_REAL_PENDING" in md
    assert "not proof authority" in md.lower() or "not this report" in md.lower()


def test_skip_lake_never_full():
    b = _bundle()
    # Ensure a good cert exists first
    good = run_lean_from_bundle(b, skip_lake=False)
    assert good.status == DerivedLeanStatus.LEAN_FULL
    before = (good.certificate_dir / "lean_manifest.json").read_text(encoding="utf-8")
    res = run_lean_from_bundle(b, skip_lake=True)
    assert res.status != DerivedLeanStatus.LEAN_FULL
    assert "SKIP_LAKE_NO_KERNEL" in res.reason_codes
    after = (good.certificate_dir / "lean_manifest.json").read_text(encoding="utf-8")
    assert before == after  # must not clobber accepted certificate
    assert "CERTIFICATE_NOT_PERSISTED" in res.reason_codes or res.lean_manifest_digest is None


def test_axiom_parser_classical():
    out = (
        "'Research.Operators.Argmax.Margin.margin_invariance' depends on axioms: [propext, Quot.sound]\n"
    )
    parsed = parse_print_axioms(out)
    assert parsed["Research.Operators.Argmax.Margin.margin_invariance"] == ["Quot.sound", "propext"]


@pytest.mark.lean
def test_e2e_axiom_closure_populated():
    b = _bundle()
    res = run_lean_from_bundle(b, skip_lake=False)
    assert res.status == DerivedLeanStatus.LEAN_FULL
    assert res.manifest is not None
    axioms = res.manifest["transcript"]["imported_axiom_closure_sorted"]
    assert "propext" in axioms
    assert res.manifest["transcript"]["axiom_closure_captured"] is True
    lean = Path(__file__).resolve().parents[3] / "lean"
    v = verify_certificate(
        lean_root=lean,
        operator_id="argmax",
        theorem_id="bounded-perturbation-margin",
        prop_module_relative=str(argmax_profile.PROP_RELATIVE),
    )
    assert v.ok, v.reason_codes
