"""Deterministic formal-verification report."""

from __future__ import annotations

from system_b.lean.ir import FormalizationCandidate
from system_b.lean.manifest import DerivedLeanStatus


def write_report(
    *,
    fc: FormalizationCandidate,
    system2_statement: str,
    status: DerivedLeanStatus,
    build_ok: bool,
    sorry_count: int,
    admit_count: int,
    imported_axioms: list[str],
    semantic_ok: bool,
    lake_log_digest: str,
    axiom_captured: bool = False,
) -> str:
    lines = [
        "# Formal verification report",
        "",
        f"- operator: `{fc.operator_id}`",
        f"- theorem_id: `{fc.theorem_id}`",
        f"- candidate_digest: `{fc.candidate_digest}`",
        f"- bundle_digest: `{fc.bundle_digest}`",
        f"- crp_digest: `{fc.crp_digest}`",
        f"- verification_run_id: `{fc.verification_run_id}`",
        "",
        "## Authority boundaries",
        "",
        "- Statement authority: handwritten `*Prop` definitions between STATEMENT markers.",
        "- Proof authority: Lean kernel (`lake build` + `#print axioms`), not this report.",
        "- Manifest store: ART-10b filesystem surrogate (`LEAN_MANIFEST_WITHOUT_COMMIT`).",
    ]
    score_enc = (fc.conventions or {}).get("score_encoding", "")
    is_real = score_enc == "REAL_MATHLIB"
    if is_real:
        lines.append("- Domain: Mathlib `ℝ` (`REAL_MATHLIB`).")
    else:
        lines.append(
            "- Domain: Int ordered-group core (`MATHLIB_REAL_PENDING`); not ℝ formalization."
        )
    lines += [
        "- LLM proof generation: not enabled in v1.",
        "",
        "## System 2 statement",
        "",
        system2_statement,
        "",
        "## Lean propositions",
        "",
    ]
    for t in fc.targets:
        lines.append(f"- `{t['theorem_name']}` : `{t['prop_fully_qualified']}`")
    lines += [
        "",
        "## Conclusion tokens",
        "",
        "```json",
        __import__("json").dumps(fc.conclusion, indent=2, sort_keys=True),
        "```",
        "",
        f"- conclusion_digest: `{fc.conclusion_digest}`",
        f"- semantic_freeze_digest: `{fc.semantic_freeze_digest}`",
        f"- semantic_audit: `{'YES' if semantic_ok else 'NO'}`",
        "",
        "## Conventions",
        "",
        "```json",
        __import__("json").dumps(fc.conventions, indent=2, sort_keys=True),
        "```",
        "",
        "## Build",
        "",
        f"- build_ok: `{build_ok}`",
        f"- sorry_count: `{sorry_count}`",
        f"- admit_count: `{admit_count}`",
        f"- lake_log_digest: `{lake_log_digest}`",
        f"- axiom_closure_captured: `{axiom_captured}`",
        "",
        "## Axiom closure (`#print axioms`)",
        "",
    ]
    if not axiom_captured:
        lines.append("- **missing** — cannot claim LEAN_FULL")
    elif imported_axioms:
        for a in imported_axioms:
            lines.append(f"- `{a}`")
    else:
        lines.append("- (empty closure; theorem depends on no axioms)")
    lines += [
        "",
        "## Derived status (recomputed; not authoritative storage)",
        "",
        f"- `{status.value}`",
        "",
        "## Known gaps",
        "",
    ]
    for g in fc.known_gaps:
        lines.append(f"- `{g}`")
    lines += [
        "",
        "## Limitations of this certificate",
        "",
    ]
    if is_real:
        lines.append(
            "- `LEAN_FULL` here means kernel-checked Mathlib `ℝ` propositions."
        )
    else:
        lines.append(
            "- `LEAN_FULL` here means kernel-checked Int-core props, not full System 2 ℝ claim."
        )
    lines += [
        "- Smoke theorems alone never authorize operator LEAN_FULL.",
        "- PDF / markdown reports are derived views, not proof authority.",
        "",
        "## Reuse",
        "",
        "- `Research.Operators.Argmax.Basic` / `Margin` shared by argmax-family aliases.",
        "",
    ]
    return "\n".join(lines)
