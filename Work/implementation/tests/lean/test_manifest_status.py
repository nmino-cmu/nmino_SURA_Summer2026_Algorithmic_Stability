"""ART-10b DerivedLeanStatus pure function tests."""

from system_b.lean.manifest import DerivedLeanStatus, build_manifest, build_transcript, derived_lean_status


def _man(**kw):
    t = build_transcript(
        toolchain_digest="t",
        mathlib_pin_digest="m",
        entry_module_id="E",
        lean_statement_digest="s",
        proof_tree_digest="p",
        import_closure_digest="i",
        definition_pin_set=[],
        sorry_count=kw.get("sorry_count", 0),
        admit_count=kw.get("admit_count", 0),
        custom_axiom_ids_sorted=kw.get("axioms", []),
        imported_axiom_closure_sorted=kw.get("imported", ["propext"]),
        build_ok=kw.get("build_ok", True),
        rebuild_log_digest="l",
        custom_axiom_asserts_target=kw.get("asserts", False),
        axiom_closure_captured=kw.get("axiom_captured", True),
    )
    return build_manifest(claim_digest="c", claim_math_fingerprint="f", transcript=t)


def test_none_not_ready():
    assert derived_lean_status(manifest=None) == DerivedLeanStatus.NOT_READY_FOR_LEAN


def test_blocked():
    assert derived_lean_status(manifest=_man(build_ok=False)) == DerivedLeanStatus.LEAN_BLOCKED


def test_full():
    assert derived_lean_status(manifest=_man()) == DerivedLeanStatus.LEAN_FULL


def test_full_requires_axiom_capture():
    assert (
        derived_lean_status(manifest=_man(axiom_captured=False))
        == DerivedLeanStatus.LEAN_BLOCKED
    )


def test_statement_with_sorry():
    assert derived_lean_status(manifest=_man(sorry_count=1)) == DerivedLeanStatus.LEAN_STATEMENT


def test_core_with_gated_axiom():
    assert (
        derived_lean_status(manifest=_man(axioms=["ax1"])) == DerivedLeanStatus.LEAN_CORE
    )


def test_stale_toolchain():
    m = _man()
    head = {"toolchain_digest": "other", "mathlib_pin_digest": "m"}
    assert derived_lean_status(manifest=m, toolchain_head=head) == DerivedLeanStatus.LEAN_STALE
