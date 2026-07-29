"""Helpers for operator-stability-v1 papers."""

from __future__ import annotations

import json
import re
import shutil
from pathlib import Path
from typing import Any

REQUIRED_SECTIONS = [
    "Problem",
    "Stability notion",
    "Definitions",
    "Theorem",
    "Intuition",
    "Examples",
    "Proof",
    "Formal statement",
    "Proof dependencies",
    "Consequences",
]

FUNDAMENTALITY = frozenset({"primitive", "derived", "reduction"})
LAYOUT = "operator-stability-v1"


def pdf_name(operator_id: str) -> str:
    return f"{operator_id.replace('-', '_')}_paper.pdf"


def fundamentality_label(card: str) -> str:
    return {"primitive": "Primitive", "derived": "Derived", "reduction": "Reduction"}[card]


def package_dir(root: Path, operator_id: str, theorem_id: str) -> Path:
    return root / "research-results" / operator_id / theorem_id


def archive_published(pkg: Path, operator_id: str) -> None:
    arch = pkg / "_archive" / "v0-thin"
    arch.mkdir(parents=True, exist_ok=True)
    for name in ("paper.tex", "paper.pdf", pdf_name(operator_id)):
        src = pkg / name
        if src.is_file():
            dest = arch / name
            if not dest.exists():
                shutil.copy2(src, dest)


def check_sections(tex: str) -> list[str]:
    errors: list[str] = []
    positions: list[int] = []
    for title in REQUIRED_SECTIONS:
        m = re.search(rf"\\section\{{{re.escape(title)}\}}", tex)
        if not m:
            errors.append(f"missing_section:{title}")
        else:
            positions.append(m.start())
    if len(positions) == len(REQUIRED_SECTIONS) and positions != sorted(positions):
        errors.append("section_order")
    if not re.search(r"This theorem is:\s*\\texttt\{(Primitive|Derived|Reduction)\}", tex):
        # also allow without texttt
        if not re.search(r"This theorem is:.*\b(Primitive|Derived|Reduction)\b", tex):
            errors.append("missing_fundamentality_label")
    return errors


_UNICODE_TEX = {
    "ℓ∞": r"$\ell_\infty$",
    "ℓ": r"$\ell$",
    "∞": r"$\infty$",
    "ε": r"$\varepsilon$",
    "δ": r"$\delta$",
    "γ": r"$\gamma$",
    "≤": r"$\le$",
    "≥": r"$\ge$",
    "≠": r"$\neq$",
    "—": "---",
    "–": "--",
    "′": "'",
    "ℝ": r"$\mathbb{R}$",
}


def latex_safe(text: str) -> str:
    for u, repl in _UNICODE_TEX.items():
        text = text.replace(u, repl)
    # Escape bare underscores only outside math ($...$, \[...\], \(...\)).
    out: list[str] = []
    i = 0
    in_dollar = False
    in_display = False
    in_inline = False
    while i < len(text):
        if text.startswith("\\[", i):
            in_display = True
            out.append("\\[")
            i += 2
            continue
        if text.startswith("\\]", i):
            in_display = False
            out.append("\\]")
            i += 2
            continue
        if text.startswith("\\(", i):
            in_inline = True
            out.append("\\(")
            i += 2
            continue
        if text.startswith("\\)", i):
            in_inline = False
            out.append("\\)")
            i += 2
            continue
        ch = text[i]
        if ch == "$":
            in_dollar = not in_dollar
            out.append(ch)
        elif (
            ch == "_"
            and not (in_dollar or in_display or in_inline)
            and (i == 0 or text[i - 1] != "\\")
        ):
            out.append(r"\_")
        else:
            out.append(ch)
        i += 1
    return "".join(out)


def render_template(template: str, slots: dict[str, str]) -> str:
    out = template
    for key, val in slots.items():
        out = out.replace("{{" + key + "}}", latex_safe(val))
    leftover = re.findall(r"\{\{[A-Z0-9_]+\}\}", out)
    if leftover:
        raise ValueError(f"unfilled_slots:{leftover}")
    return out


def build_formal_block(
    *,
    lean_module: str,
    theorem_names: list[str],
    cert_dir: str,
    lean_status: str,
    domain: str = "REAL_MATHLIB",
) -> str:
    lean_path = "lean/" + "/".join(lean_module.split(".")) + ".lean"
    name_lines = (
        "\n".join(f"  \\item \\leanpath{{{n}}}" for n in theorem_names)
        if theorem_names
        else "  \\item (see Lean module)"
    )
    return "\n".join(
        [
            "\\begin{description}[style=nextline,leftmargin=1.1em,font=\\normalfont\\bfseries]",
            f"\\item[Lean module] \\leanpath{{{lean_module}}}",
            f"\\item[Source file] \\leanpath{{{lean_path}}}",
            f"\\item[Theorems]\\leavevmode\\par\\vspace{{0.15em}}\\begin{{itemize}}[leftmargin=1.2em]\n{name_lines}\n\\end{{itemize}}",
            f"\\item[Certificate] \\leanpath{{{cert_dir}}}",
            f"\\item[Status] \\texttt{{{lean_status}}} on Mathlib $\\mathbb{{R}}$ (\\texttt{{{domain}}})",
            "\\end{description}",
        ]
    )


def merge_paper_card(meta: dict[str, Any], card: dict[str, Any]) -> dict[str, Any]:
    out = dict(meta)
    out["paper_card"] = card
    return out


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, obj: Any) -> None:
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
