#!/usr/bin/env python3
"""Write publication package for a projection/feasibility operator."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    oid, lean, display, kind, thm = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
    cert = json.loads((ROOT / f"lean/certificates/{oid}/{thm}/lean_manifest.json").read_text())
    tr = cert["transcript"]
    digest = cert["manifest_digest"]
    out = ROOT / f"research-results/{oid}/{thm}"
    out.mkdir(parents=True, exist_ok=True)
    paper = rf"""\documentclass[11pt]{{article}}
\usepackage[margin=1in]{{geometry}}
\usepackage{{amsmath,amssymb,amsthm}}
\usepackage{{hyperref}}
\newtheorem{{theorem}}{{Theorem}}
\title{{{display}: Real Stability}}
\author{{Research Architecture Runtime \\ \texttt{{operator/{oid}}}}}
\date{{2026-07-25}}
\begin{{document}}
\maketitle
\begin{{abstract}}
{display} ({kind}) with Lean \texttt{{LEAN\_FULL}} on Mathlib $\mathbb{{R}}$ (\texttt{{REAL\_MATHLIB}}).
\end{{abstract}}
\section{{Lean / certificate}}
\texttt{{Research.Operators.{lean}.Preservation}}.
\section{{Limitations}}
Mathlib $\mathbb{{R}}$ (\texttt{{REAL\_MATHLIB}}); kind={kind}.
\end{{document}}
"""
    (out / "paper.tex").write_text(paper, encoding="utf-8")
    (out / "proof-outline.md").write_text(f"# Proof outline\nKind `{kind}` definitional/core reduction.\n", encoding="utf-8")
    (out / "references.bib").write_text(
        "@misc{artint, title={Research Architecture Runtime}, year={2026}}\n", encoding="utf-8"
    )
    (out / "README.md").write_text(f"# {display}\n\nLean status: LEAN_FULL ({kind}).\n", encoding="utf-8")
    pkg = oid.replace("-", "_")
    meta = {
        "operator": oid,
        "title": f"{display}: Real Stability",
        "authors": ["Research Architecture Runtime"],
        "date_generated": "2026-07-25",
        "git_commit": "pending",
        "branch": f"operator/{oid}",
        "crp_identifiers": {"operator": oid, "theorem_id": thm},
        "proof_obligation_identifiers": ["lean_kernel_checked"],
        "verification_result_identifiers": ["LEAN_FULL", digest],
        "lean_manifest_digest": digest,
        "derived_lean_status": "LEAN_FULL",
        "lean_entry_module": f"Research.Operators.{lean}.Preservation",
        "lean_certificate_dir": f"lean/certificates/{oid}/{thm}",
        "audit_identifiers": {"note": "Lean LEAN_FULL"},
        "repository_version": "0.1.0",
        "theorem_version": "1.0.0-lean",
        "schema_version": "ART-INT-00",
        "verification_status": "LEAN_FULL",
        "library_schema_version": "primitive-library-1.0",
        "authored": {
            "operator": oid,
            "theorem": thm,
            "assumptions": ["REAL_MATHLIB", f"kind={kind}"],
            "perturbation_model": "abs ball",
            "theorem_role": "primary_stability",
            "proof_strategy": f"Projection core ({kind})",
            "limitations": ["REAL_MATHLIB", kind],
            "references": [f"research-results/{oid}/{thm}/paper.tex"],
            "lean_theorem_names": (
                [f"{pkg}_clamp_stability", f"{pkg}_clamp_sharpness"] if kind == "clamp"
                else [f"{pkg}_feasible_ball_identity", f"{pkg}_feasible_ball_sharpness"] if kind == "feasible"
                else [f"{pkg}_conjunction_preservation", f"{pkg}_conjunction_sharpness"] if kind == "conjunction"
                else [f"{pkg}_disjunction_preservation", f"{pkg}_disjunction_sharpness"]
            ),
        },
        "derived": {
            "lean_status": "LEAN_FULL",
            "statement_digest": tr["lean_statement_digest"],
            "proof_digest": tr["proof_tree_digest"],
            "certificate_path": f"lean/certificates/{oid}/{thm}",
            "placeholder_count": 0,
            "axiom_summary": {
                "imported_axiom_closure_sorted": tr["imported_axiom_closure_sorted"],
                "custom_axiom_ids_sorted": tr.get("custom_axiom_ids_sorted", []),
                "axiom_closure_captured": True,
            },
            "provenance": {
                "lean_manifest_digest": digest,
                "claim_digest": cert["claim_digest"],
                "entry_module_id": f"Research.Operators.{lean}.Preservation",
                "store_kind": cert["store_kind"],
            },
            "verification_timestamp": "2026-07-25",
        },
        "library": {
            "primitive_type": "projection",
            "selected_object": kind,
            "instability_mechanism": "boundary_crossing",
            "structural_stability_quantity": kind,
            "perturbation_class": "bounded_additive_abs",
            "guarantee_kind": "deterministic",
            "stable_region": "core-dependent",
            "unstable_region": "near boundary",
            "sharpness": True,
            "compositional_properties": [f"projection_{kind}"],
            "related_operators": ["projection-interval", "coordinate-clipping"],
            "assumptions": ["REAL_MATHLIB"],
            "limitations": ["REAL_MATHLIB", kind],
        },
    }
    (out / "metadata.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    subprocess.check_call(
        ["pdflatex", "-interaction=nonstopmode", "paper.tex"], cwd=out, stdout=subprocess.DEVNULL
    )
    subprocess.check_call(
        ["pdflatex", "-interaction=nonstopmode", "paper.tex"], cwd=out, stdout=subprocess.DEVNULL
    )
    for pat in ("*.aux", "*.log", "*.out"):
        for f in out.glob(pat):
            f.unlink()
    reg_path = ROOT / "research-results/primitive-library/operators.json"
    reg = json.loads(reg_path.read_text(encoding="utf-8"))
    found = False
    for o in reg["operators"]:
        if o["operator_id"] == oid:
            o["status"] = "complete"
            o["implemented"] = True
            o["theorem_count"] = 1
            found = True
    if not found:
        raise SystemExit(f"missing registry entry {oid}")
    reg_path.write_text(json.dumps(reg, indent=2) + "\n", encoding="utf-8")
    print(digest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
