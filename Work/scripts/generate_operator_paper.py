#!/usr/bin/env python3
"""Generate operator-stability-v1 paper.tex + <operator>_paper.pdf from verified metadata + sections JSON."""

from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from lib.operator_paper import (  # noqa: E402
    LAYOUT,
    archive_published,
    build_formal_block,
    check_sections,
    fundamentality_label,
    load_json,
    merge_paper_card,
    package_dir,
    pdf_name,
    render_template,
    write_json,
)


def _skip(reason: str, operator_id: str, theorem_id: str) -> int:
    log = ROOT / "research-results" / "_skip-log"
    log.mkdir(parents=True, exist_ok=True)
    path = log / f"{date.today().isoformat()}-{operator_id}-{theorem_id}-paper.txt"
    path.write_text(reason + "\n", encoding="utf-8")
    print(f"SKIP: {reason}", file=sys.stderr)
    return 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("operator_id")
    ap.add_argument("theorem_id")
    ap.add_argument(
        "--sections",
        type=Path,
        required=True,
        help="JSON payload with section LaTeX + paper_card fields",
    )
    ap.add_argument("--date", default=date.today().isoformat())
    args = ap.parse_args()

    pkg = package_dir(ROOT, args.operator_id, args.theorem_id)
    meta_path = pkg / "metadata.json"
    if not meta_path.is_file():
        return _skip(f"missing_metadata:{meta_path}", args.operator_id, args.theorem_id)
    meta = load_json(meta_path)

    status = meta.get("derived_lean_status") or (meta.get("derived") or {}).get("lean_status")
    if status != "LEAN_FULL":
        return _skip(f"lean_gate:{status}", args.operator_id, args.theorem_id)

    cert_dir = meta.get("lean_certificate_dir") or (meta.get("derived") or {}).get("certificate_path")
    if not cert_dir:
        return _skip("missing_certificate_dir", args.operator_id, args.theorem_id)
    manifest = ROOT / cert_dir / "lean_manifest.json"
    if not manifest.is_file():
        return _skip(f"missing_manifest:{manifest}", args.operator_id, args.theorem_id)

    sections = load_json(args.sections)
    fund = sections.get("fundamentality") or (sections.get("paper_card") or {}).get("fundamentality")
    if fund not in ("primitive", "derived", "reduction"):
        return _skip(f"bad_fundamentality:{fund}", args.operator_id, args.theorem_id)

    authored = meta.get("authored") or {}
    theorem_names = authored.get("lean_theorem_names") or []
    lean_module = meta.get("lean_entry_module") or ""
    formal = sections.get("formal") or build_formal_block(
        lean_module=lean_module,
        theorem_names=theorem_names,
        cert_dir=cert_dir,
        lean_status="LEAN_FULL",
    )

    template = (ROOT / "research-results/paper-templates/operator-stability-v1.tex").read_text(
        encoding="utf-8"
    )
    slots = {
        "TITLE": sections.get("title") or meta.get("title") or args.theorem_id,
        "OPERATOR_ID": args.operator_id,
        "DATE": args.date,
        "ABSTRACT": sections["abstract"],
        "FUNDAMENTALITY_LABEL": fundamentality_label(fund),
        "SECTION_PROBLEM": sections["problem"],
        "SECTION_STABILITY": sections["stability"],
        "SECTION_DEFINITIONS": sections["definitions"],
        "SECTION_THEOREM": sections["theorem"],
        "SECTION_INTUITION": sections["intuition"],
        "SECTION_EXAMPLES": sections["examples"],
        "SECTION_PROOF": sections["proof"],
        "SECTION_FORMAL": formal,
        "SECTION_DEPENDENCIES": sections["dependencies"],
        "SECTION_CONSEQUENCES": sections["consequences"],
    }
    tex = render_template(template, slots)
    errs = check_sections(tex)
    if errs:
        return _skip("layout:" + ",".join(errs), args.operator_id, args.theorem_id)

    archive_published(pkg, args.operator_id)
    (pkg / "paper.tex").write_text(tex, encoding="utf-8")

    tex_ok = True
    for _ in range(2):
        r = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "paper.tex"],
            cwd=pkg,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        if r.returncode != 0:
            tex_ok = False
    built = pkg / "paper.pdf"
    target = pkg / pdf_name(args.operator_id)
    if not built.is_file():
        return _skip("pdflatex_failed", args.operator_id, args.theorem_id)
    # Prefer success; if non-zero but PDF exists, check log for fatal '! ' without emergency stop recovery
    log = pkg / "paper.log"
    if not tex_ok and log.is_file():
        log_txt = log.read_text(errors="replace")
        if "Fatal error" in log_txt or "Emergency stop" in log_txt:
            return _skip("pdflatex_errors", args.operator_id, args.theorem_id)
    built.replace(target)
    for pat in ("*.aux", "*.log", "*.out"):
        for f in pkg.glob(pat):
            f.unlink()

    digest = meta.get("lean_manifest_digest") or (meta.get("derived") or {}).get("provenance", {}).get(
        "lean_manifest_digest"
    )
    pc_in = sections.get("paper_card") or {}
    paper_card = {
        "layout": LAYOUT,
        "fundamentality": fund,
        "difficulty": pc_in.get("difficulty", "standard"),
        "applications": pc_in.get("applications", []),
        "dependencies": pc_in.get("dependencies", []),
        "reduces_to": pc_in.get("reduces_to"),
        "reduced_by": pc_in.get("reduced_by", []),
        "verified": {
            "lean_status": "LEAN_FULL",
            "manifest_digest": digest,
            "domain": "REAL_MATHLIB",
        },
    }
    write_json(meta_path, merge_paper_card(meta, paper_card))

    outline = (
        f"# Proof outline ({args.operator_id}/{args.theorem_id})\n\n"
        f"- layout: {LAYOUT}\n"
        f"- fundamentality: {fund}\n"
        f"- pdf: {pdf_name(args.operator_id)}\n"
        f"- lean: {lean_module}\n"
        f"- theorems: {', '.join(theorem_names)}\n"
    )
    (pkg / "proof-outline.md").write_text(outline, encoding="utf-8")
    print(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
