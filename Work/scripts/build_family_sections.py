#!/usr/bin/env python3
"""Build operator-stability-v1 sections JSON deterministically from metadata + Lean family."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def load(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def esc(s: str) -> str:
    return s.replace("_", "\\_")


def tt_id(s: str) -> str:
    """Breakable monospace for Lean modules / operator ids (needs \\leanpath in template)."""
    return f"\\leanpath{{{s}}}"


def formal_block(meta: dict[str, Any], extra: str = "") -> str:
    authored = meta.get("authored") or {}
    names = list(authored.get("lean_theorem_names") or [])
    if not names:
        mod0 = meta.get("lean_entry_module") or ""
        lean_file = ROOT / "lean" / Path(*mod0.split(".")).with_suffix(".lean")
        if lean_file.is_file():
            src = lean_file.read_text(encoding="utf-8")
            found = re.findall(r"(?:theorem|lemma)\s+([A-Za-z][A-Za-z0-9_]*)\b", src)
            names = [
                n
                for n in found
                if any(k in n for k in ("invariance", "sharpness", "preservation", "identity"))
            ]
            names = names or found[:4]
        if not names and "Argmax.Margin" in mod0:
            names = ["margin_invariance", "margin_sharpness"]
    mod = meta.get("lean_entry_module") or ""
    lean_path = "lean/" + "/".join(mod.split(".")) + ".lean"
    cert = meta.get("lean_certificate_dir") or ""
    name_lines = "\n".join(f"  \\item \\leanpath{{{n}}}" for n in names) if names else "  \\item (see Lean module)"
    bits = [
        "\\begin{description}[style=nextline,leftmargin=1.1em,font=\\normalfont\\bfseries]",
        f"\\item[Lean module] \\leanpath{{{mod}}}",
        f"\\item[Source file] \\leanpath{{{lean_path}}}",
        f"\\item[Theorems]\\leavevmode\\par\\vspace{{0.15em}}\\begin{{itemize}}[leftmargin=1.2em]\n{name_lines}\n\\end{{itemize}}",
    ]
    if extra:
        # strip raw texttt paths in extras when possible; keep as prose
        bits.append(f"\\item[Note] {extra}")
    if meta.get("math_authority"):
        bits.append(f"\\item[Math authority] \\leanpath{{{meta['math_authority'].rstrip('/')}}}")
    bits += [
        f"\\item[Certificate] \\leanpath{{{cert}}}",
        "\\item[Status] \\texttt{LEAN\\_FULL} on Mathlib $\\mathbb{R}$ (\\texttt{REAL\\_MATHLIB})",
        "\\end{description}",
    ]
    return "\n".join(bits)


def family_of(meta: dict[str, Any]) -> str:
    strat = ((meta.get("authored") or {}).get("proof_strategy") or "").lower()
    mod = (meta.get("lean_entry_module") or "").lower()
    mod_full = meta.get("lean_entry_module") or ""
    lib = meta.get("library") or {}
    th = (meta.get("crp_identifiers") or {}).get("theorem_id", "")
    # Order matters: MultiThreshold contains the substring "threshold".
    if "multithreshold" in mod.replace(".", "") or "MultiThreshold" in mod_full:
        return "multi_threshold"
    if "kth" in strat or "kthmargin" in mod.replace(".", "") or "orderstat.kth" in mod:
        return "kth"
    if "ranking" in strat or "orderstat.ranking" in mod:
        return "ranking"
    if mod_full.endswith(".Margin") or "Argmax.Margin" in mod_full:
        return "argmax"
    if "definitional reduction to argmax" in strat:
        return "argmax"
    if any(x in mod for x in ("sign", "absthreshold", "intervalmembership")):
        return "threshold_scalar"
    if "boundednoise" in mod.replace(".", ""):
        return "threshold"
    if "threshold.preservation" in mod or (
        "threshold" in mod and "multi" not in mod and "then" not in th
    ):
        if "Threshold.Preservation" in mod_full or oid_is_thresholding(meta):
            return "threshold"
    if "clamp" in strat or "projection.clamp" in mod or "clip" in mod:
        return "clamp"
    if "feasible" in strat or "feasibleid" in mod.replace(".", "") or "feasible-ball" in th:
        return "feasible"
    if "constraint" in strat or "conjunction" in th or "disjunction" in th:
        return "constraint"
    if "Preservation" in mod_full:
        if lib.get("primitive_type") == "ordering":
            return "ranking"
        if lib.get("primitive_type") == "scalar_selection":
            if oid_hint_kth(th, mod_full):
                return "kth"
            if any(x in mod_full for x in ("Sign", "AbsThreshold", "IntervalMembership")):
                return "threshold_scalar"
            if "Threshold" in mod_full and "Multi" not in mod_full:
                return "threshold"
            return "kth" if "margin" in th else "threshold_scalar"
        if lib.get("primitive_type") == "projection":
            if "feasible" in th:
                return "feasible"
            if "conjunction" in th or "disjunction" in th:
                return "constraint"
            return "clamp"
        if any(x in mod_full for x in ("TopK", "Sorting", "Rank", "Bucket", "Lexicographic")):
            return "ranking"
        if any(x in mod_full for x in ("Median", "Quantile", "Percentile", "Kth")):
            return "kth"
    return "generic"


def oid_is_thresholding(meta: dict[str, Any]) -> bool:
    return (meta.get("operator") or meta.get("crp_identifiers", {}).get("operator")) == "thresholding"


def oid_hint_kth(th: str, mod: str) -> bool:
    return any(x in th or x in mod for x in ("median", "quantile", "percentile", "kth", "Median", "Quantile", "Kth"))


def display_name(operator_id: str, meta: dict[str, Any]) -> str:
    return meta.get("title") or operator_id.replace("-", " ").title()


def related(meta: dict[str, Any]) -> list[str]:
    return list((meta.get("library") or {}).get("related_operators") or [])


def sections_kth(oid: str, meta: dict[str, Any]) -> dict[str, Any]:
    name = oid.replace("-", " ")
    rel = ", ".join(tt_id(r) for r in related(meta)[:6]) or "related order-statistic operators"
    is_median_like = oid in {"median", "quantile", "percentile", "kth-order-statistic"}
    fund = "reduction" if "KthMargin" in (meta.get("lean_entry_module") or "") or "reduction" in (
        (meta.get("authored") or {}).get("proof_strategy") or ""
    ).lower() else "reduction"
    # all these are KthMargin aliases in this library
    fund = "reduction"
    return {
        "fundamentality": fund,
        "title": meta.get("title") or f"{name.title()} Index Preservation under Bounded Score Perturbations",
        "abstract": (
            f"The {name} operator selects a unique strict $k$-th order-statistic index. "
            f"When every pairwise score gap exceeds $2\\varepsilon$, that index is invariant under "
            f"$\\|\\delta\\|_\\infty\\le\\varepsilon$. Lean: \\texttt{{LEAN\\_FULL}} (reduction of "
            f"\\texttt{{OrderStat.KthMargin}})."
        ),
        "problem": (
            f"The {tt_id(oid)} operator on scores $s\\in\\mathbb{{R}}^n$ ($n\\ge 2$) returns the unique "
            f"index $i$ that is the strict $k$-th smallest coordinate of $s$ (operator-specific choice of $k$). "
            f"The selected object is this index under a unique strict-order presentation."
        ),
        "stability": (
            "Perturbations are additive $\\delta$ with $\\|\\delta\\|_\\infty\\le\\varepsilon$. "
            "Stability: if $i$ is the unique strict $k$-th smallest and $\\mathrm{AllGapsExceed}(s,2\\varepsilon)$, "
            "then $i$ remains the unique strict $k$-th smallest of $s+\\delta$. "
            "Sharpness: a rival within distance $2\\varepsilon$ admits an admissible tying adversary."
        ),
        "definitions": (
            "\\begin{definition}[Strict $k$-th smallest]\n"
            "Index $i$ is strict $k$-th smallest if $\\#\\{j:s_j<s_i\\}=k$ and $s_j=s_i\\Rightarrow j=i$.\n"
            "\\end{definition}\n"
            "\\begin{definition}[All-gaps]\n"
            "$|s_p-s_q|>g$ for all $p\\neq q$.\n"
            "\\end{definition}\n"
            "\\noindent\\textbf{Assumptions.} $n\\ge 2$, $\\varepsilon\\ge 0$, unique strict $k$-th index, "
            "and (for invariance) all pairwise gaps $>2\\varepsilon$."
        ),
        "theorem": (
            "\\begin{theorem}[Invariance]\\label{thm:inv}\n"
            "If $i$ is strict $k$-th smallest and $\\mathrm{AllGapsExceed}(s,2\\varepsilon)$, then for every "
            "$\\|\\delta\\|_\\infty\\le\\varepsilon$, $i$ remains strict $k$-th smallest for $s+\\delta$.\n"
            "\\end{theorem}\n"
            "\\begin{theorem}[Sharpness]\\label{thm:sharp}\n"
            "If some $j\\neq i$ has $|s_i-s_j|\\le 2\\varepsilon$, an admissible midpoint $\\delta$ destroys uniqueness.\n"
            "\\end{theorem}"
        ),
        "intuition": (
            "An $\\ell_\\infty$ adversary moves any two scores by at most $2\\varepsilon$ relative to each other. "
            "Gaps larger than $2\\varepsilon$ cannot reverse or tie; gaps of size at most $2\\varepsilon$ admit a midpoint collision."
        ),
        "examples": (
            "\\begin{example}\n"
            "Scores $(1,4,7)$, $k=1$, $\\varepsilon=1$: gaps $3,6,3$ all exceed $2$, so the middle index is stable. "
            "For $\\varepsilon=2$, the gap $3\\le 4$ admits a midpoint tie between the first two coordinates.\n"
            "\\end{example}"
        ),
        "proof": (
            "Let $s'=s+\\delta$ with $\\|\\delta\\|_\\infty\\le\\varepsilon$.\n\n"
            "\\paragraph{Pairwise orders.}\n"
            "If $s_p<s_q$ and $s_q-s_p>2\\varepsilon$, then "
            "$s'_p-s'_q\\le -(s_q-s_p)+2\\varepsilon<0$, so $s'_p<s'_q$. "
            "The converse is symmetric. Hence $s_p<s_q\\Leftrightarrow s'_p<s'_q$ whenever $|s_p-s_q|>2\\varepsilon$; "
            "under all-gaps this holds for every distinct pair.\n\n"
            "\\paragraph{Count.}\n"
            "Taking $q=i$ yields $\\#\\{j:s_j<s_i\\}=\\#\\{j:s'_j<s'_i\\}$. "
            "If the left side equals $k$, so does the right.\n\n"
            "\\paragraph{Uniqueness.}\n"
            "If $s'_j=s'_i$ and $j\\neq i$, all-gaps give $|s_j-s_i|>2\\varepsilon$, hence $s'_j\\neq s'_i$, contradiction. "
            "Thus $i$ remains the unique strict $k$-th index (Theorem~\\ref{thm:inv}).\n\n"
            "\\paragraph{Sharpness.}\n"
            "For $j\\neq i$ with $|s_i-s_j|\\le 2\\varepsilon$, set "
            "$\\delta_i=-(s_i-s_j)/2$, $\\delta_j=(s_i-s_j)/2$, and $\\delta_t=0$ otherwise. "
            "Then $\\|\\delta\\|_\\infty\\le\\varepsilon$ and $s'_i=s'_j$, so uniqueness fails (Theorem~\\ref{thm:sharp})."
        ),
        "formal": formal_block(
            meta,
            extra="Definitional reduction of OrderStat.KthMargin.",
        ),
        "dependencies": (
            "\\begin{itemize}\n"
            f"\\item Reduces to {tt_id('Research.Operators.OrderStat.KthMargin')}.\n"
            "\\item Uses the $\\ell_\\infty$ relative-gap bound $|\\delta_p-\\delta_q|\\le 2\\varepsilon$.\n"
            "\\item Midpoint collision adversary.\n"
            "\\item No other operator theorems required.\n"
            "\\end{itemize}"
        ),
        "consequences": (
            f"Operators reducing to the same $k$-th core include {rel}. "
            f"The {tt_id(oid)} theorem is the stability certificate for unique strict order-statistic selection "
            f"under bounded score noise."
        ),
        "paper_card": {
            "difficulty": "elementary",
            "applications": related(meta),
            "dependencies": [
                "Research.Operators.OrderStat.KthMargin",
                "kth_margin_invariance",
                "kth_margin_sharpness",
            ],
            "reduces_to": "order-stat-kth-margin",
            "reduced_by": [],
        },
    }


def sections_ranking(oid: str, meta: dict[str, Any]) -> dict[str, Any]:
    rel = ", ".join(tt_id(r) for r in related(meta)[:8]) or "related ranking operators"
    return {
        "fundamentality": "reduction",
        "title": meta.get("title") or f"{oid} Ranking Preservation under Bounded Score Perturbations",
        "abstract": (
            f"{tt_id(oid)} is certified by pairwise ranking preservation when all gaps exceed $2\\varepsilon$. "
            f"Lean \\texttt{{LEAN\\_FULL}} via \\texttt{{OrderStat.Ranking}}."
        ),
        "problem": (
            f"The {tt_id(oid)} operator depends on the pairwise order of scores $s\\in\\mathbb{{R}}^n$. "
            f"The certified object is the full pairwise ranking (and thereby any ranking-determined selection such as top-$k$ index sets)."
        ),
        "stability": (
            "Perturbations: $\\|\\delta\\|_\\infty\\le\\varepsilon$. "
            "Stability: if $\\mathrm{AllGapsExceed}(s,2\\varepsilon)$, then $s_i<s_j\\Leftrightarrow (s+\\delta)_i<(s+\\delta)_j$ for all $i,j$. "
            "Sharpness: a gap $\\le 2\\varepsilon$ admits a collision adversary."
        ),
        "definitions": (
            "\\begin{definition}[All-gaps]\n$|s_p-s_q|>g$ for $p\\neq q$.\\end{definition}\n"
            "\\noindent\\textbf{Assumptions.} $n\\ge 2$, $\\varepsilon\\ge 0$, and (for invariance) all pairwise gaps $>2\\varepsilon$."
        ),
        "theorem": (
            "\\begin{theorem}[Ranking invariance]\\label{thm:inv}\n"
            "If $\\mathrm{AllGapsExceed}(s,2\\varepsilon)$, then for every $\\|\\delta\\|_\\infty\\le\\varepsilon$ and all $i,j$, "
            "$s_i<s_j\\Leftrightarrow s_i+\\delta_i<s_j+\\delta_j$.\n"
            "\\end{theorem}\n"
            "\\begin{theorem}[Sharpness]\\label{thm:sharp}\n"
            "If some distinct pair has $|s_i-s_j|\\le 2\\varepsilon$, an admissible $\\delta$ forces a value collision.\n"
            "\\end{theorem}"
        ),
        "intuition": (
            "Relative $\\ell_\\infty$ moves cost at most $2\\varepsilon$. Gaps larger than $2\\varepsilon$ cannot reverse; "
            "smaller gaps can be closed by a midpoint push."
        ),
        "examples": (
            "\\begin{example}\n"
            "Scores $(0,3,8)$, $\\varepsilon=1$: all gaps $>2$, so the ranking is stable. "
            "If scores are $(0,1.5)$ and $\\varepsilon=1$, the gap $1.5\\le 2$ admits a midpoint tie.\n"
            "\\end{example}"
        ),
        "proof": (
            "Fix $\\|\\delta\\|_\\infty\\le\\varepsilon$. If $i=j$ both sides of the claimed equivalence are false for strict $<$. "
            "If $i\\neq j$ and $|s_i-s_j|>2\\varepsilon$, the estimate "
            "$(s_i+\\delta_i)-(s_j+\\delta_j)\\ge (s_i-s_j)-2\\varepsilon$ (and its swap) yields "
            "$s_i<s_j\\Leftrightarrow s_i+\\delta_i<s_j+\\delta_j$ (Theorem~\\ref{thm:inv}).\n\n"
            "For sharpness, take $i\\neq j$ with $|s_i-s_j|\\le 2\\varepsilon$ and the midpoint "
            "$\\delta_i=-(s_i-s_j)/2$, $\\delta_j=(s_i-s_j)/2$ (elsewhere $0$). "
            "Then $\\|\\delta\\|_\\infty\\le\\varepsilon$ and $s_i+\\delta_i=s_j+\\delta_j$ (Theorem~\\ref{thm:sharp})."
        ),
        "formal": formal_block(meta, extra="Reduction of OrderStat.Ranking."),
        "dependencies": (
            "\\begin{itemize}\n"
            f"\\item {tt_id('Research.Operators.OrderStat.Ranking')} / shared pairwise lemma from {tt_id('KthMargin')}.\n"
            "\\item Midpoint collision adversary.\n"
            "\\item No other operator theorems required.\n"
            "\\end{itemize}"
        ),
        "consequences": (
            f"Ranking stability implies stability of any functional of the pairwise order used by {tt_id(oid)}. "
            f"Related operators: {rel}."
        ),
        "paper_card": {
            "difficulty": "elementary",
            "applications": related(meta),
            "dependencies": ["Research.Operators.OrderStat.Ranking", "ranking_invariance"],
            "reduces_to": "order-stat-ranking",
            "reduced_by": [],
        },
    }


def sections_argmax(oid: str, meta: dict[str, Any]) -> dict[str, Any]:
    rel = ", ".join(tt_id(r) for r in related(meta)[:8]) or "related unique-max operators"
    return {
        "fundamentality": "reduction",
        "title": meta.get("title") or f"{oid} Unique-Max Margin under Bounded Perturbations",
        "abstract": (
            f"{tt_id(oid)} selects a unique maximizer. Margin $\\gamma(s)>2\\varepsilon$ is necessary and sufficient "
            f"for unique-max invariance under $\\|\\delta\\|_\\infty\\le\\varepsilon$. Lean \\texttt{{LEAN\\_FULL}} "
            f"(reduction to \\texttt{{Argmax.Margin}})."
        ),
        "problem": (
            f"The {tt_id(oid)} operator returns the unique maximizer index $i^\\star$ of scores $s\\in\\mathbb{{R}}^m$ "
            f"($m\\ge 2$), up to the operator's definitional presentation (heap top, tournament winner, masked max, etc.)."
        ),
        "stability": (
            "Perturbations: $\\|\\delta\\|_\\infty\\le\\varepsilon$. "
            "Let $\\gamma(s)=s_{i^\\star}-\\max_{j\\neq i^\\star}s_j$. "
            "Stability: $\\gamma(s)>2\\varepsilon$ implies $i^\\star$ remains the unique maximizer of $s+\\delta$. "
            "Sharpness: $\\gamma(s)\\le 2\\varepsilon$ admits an adversary destroying unique maximality."
        ),
        "definitions": (
            "\\begin{definition}[Unique maximizer]\n"
            "$i^\\star$ uniquely maximizes $s$ if $s_j\\le s_{i^\\star}$ for all $j$ and $s_j=s_{i^\\star}\\Rightarrow j=i^\\star$.\n"
            "\\end{definition}\n"
            "\\begin{definition}[Margin]\n$\\gamma(s)=s_{i^\\star}-\\max_{j\\neq i^\\star}s_j$.\\end{definition}"
        ),
        "theorem": (
            "\\begin{theorem}[Margin invariance]\\label{thm:inv}\n"
            "If $i^\\star$ uniquely maximizes $s$ and $s_{i^\\star}-s_j>2\\varepsilon$ for all $j\\neq i^\\star$, "
            "then for every $\\|\\delta\\|_\\infty\\le\\varepsilon$, $i^\\star$ uniquely maximizes $s+\\delta$.\n"
            "\\end{theorem}\n"
            "\\begin{theorem}[Sharpness]\\label{thm:sharp}\n"
            "If some $j\\neq i^\\star$ has $s_{i^\\star}-s_j\\le 2\\varepsilon$, an admissible $\\delta$ destroys unique maximality.\n"
            "\\end{theorem}"
        ),
        "intuition": (
            "Depressing the winner by $\\varepsilon$ and elevating a rival by $\\varepsilon$ consumes $2\\varepsilon$ of margin. "
            "Strict margin above $2\\varepsilon$ leaves the winner unique; otherwise a two-point adversary forces a tie or loss."
        ),
        "examples": (
            "\\begin{example}\n"
            "Scores $(7,5,4)$, $i^\\star=0$, $\\gamma=2$. For $\\varepsilon=0.8$, $2\\varepsilon=1.6<2$, so the winner is stable. "
            "For $\\varepsilon=1$, $2\\varepsilon=2\\ge\\gamma$; $\\delta=(-1,+1,0)$ yields a tie between the first two scores.\n"
            "\\end{example}"
        ),
        "proof": (
            "Let $s'=s+\\delta$ with $\\|\\delta\\|_\\infty\\le\\varepsilon$. For $j\\neq i^\\star$,\n"
            "\\[\n"
            "s'_{i^\\star}-s'_j\n"
            "=(s_{i^\\star}-s_j)+(\\delta_{i^\\star}-\\delta_j)\n"
            "\\ge (s_{i^\\star}-s_j)-2\\varepsilon\n"
            ">0,\n"
            "\\]\n"
            "using $s_{i^\\star}-s_j>2\\varepsilon$. Thus $s'_j<s'_{i^\\star}$ for all $j\\neq i^\\star$, so $i^\\star$ "
            "uniquely maximizes $s'$ (Theorem~\\ref{thm:inv}).\n\n"
            "For sharpness, pick $j$ with $s_{i^\\star}-s_j\\le 2\\varepsilon$, set $\\delta_{i^\\star}=-\\varepsilon$, "
            "$\\delta_j=+\\varepsilon$, and $0$ elsewhere. Then $\\|\\delta\\|_\\infty\\le\\varepsilon$ and "
            "$s'_{i^\\star}-s'_j=\\gamma_{ij}-2\\varepsilon\\le 0$, so unique maximality fails (Theorem~\\ref{thm:sharp})."
        ),
        "formal": formal_block(meta, extra="Definitional reduction of Argmax.Margin."),
        "dependencies": (
            "\\begin{itemize}\n"
            f"\\item {tt_id('Research.Operators.Argmax.Margin')} "
            f"({tt_id('margin_invariance')}, {tt_id('margin_sharpness')}).\n"
            "\\item $\\ell_\\infty$ gap shrinkage by at most $2\\varepsilon$.\n"
            "\\item No other operator theorems required.\n"
            "\\end{itemize}"
        ),
        "consequences": (
            f"Any unique-max presentation of {tt_id(oid)} inherits Argmax margin stability. Related: {rel}."
        ),
        "paper_card": {
            "difficulty": "elementary",
            "applications": related(meta),
            "dependencies": ["Research.Operators.Argmax.Margin", "margin_invariance"],
            "reduces_to": "argmax-margin",
            "reduced_by": [],
        },
    }


def sections_threshold(oid: str, meta: dict[str, Any], *, noisy: bool = False) -> dict[str, Any]:
    if noisy:
        return {
            "fundamentality": "primitive",
            "title": meta.get("title") or "Bounded Noise Threshold Preservation",
            "abstract": (
                "Pathwise threshold preservation under almost-sure $|\\xi|\\le\\eta$ reduces to the deterministic "
                "buffer theorem with $\\varepsilon:=\\eta$. Lean \\texttt{LEAN\\_FULL}."
            ),
            "problem": (
                "The noisy threshold $\\widetilde A_T(x)=\\mathbf{1}\\{x+\\xi\\ge T\\}$ with $|\\xi|\\le\\eta$ a.s. "
                "The selected object is the binary pass/fail bit."
            ),
            "stability": (
                "Noise is query-side and bounded. Outside $[T-\\eta,T+\\eta)$ the output is a.s.\\ constant; "
                "inside the band it need not be."
            ),
            "definitions": (
                "Pass convention: $x\\ge T$ passes. Pathwise: apply deterministic threshold preservation with $\\varepsilon=\\eta$."
            ),
            "theorem": (
                "\\begin{theorem}\\label{thm:inv}\n"
                "If $|\\xi|\\le\\eta$ a.s., then $x\\ge T+\\eta\\Rightarrow\\widetilde A_T=1$ a.s.\\ and "
                "$x<T-\\eta\\Rightarrow\\widetilde A_T=0$ a.s. On the open band with $\\eta>0$, two-point noise "
                "shows the bit need not be a.s.\\ constant.\n"
                "\\end{theorem}"
            ),
            "intuition": "Bounded noise cannot cross a buffer of width $\\eta$ on either side of $T$.",
            "examples": (
                "\\begin{example}\n$T=3$, $x=5$, $\\eta=0.2$: $x\\ge T+\\eta$, so the bit stays $1$ a.s.\n\\end{example}"
            ),
            "proof": (
                "On almost every outcome, $|\\xi(\\omega)|\\le\\eta$. Apply deterministic threshold preservation "
                "to $(x,T,\\varepsilon,x')=(x,T,\\eta,x+\\xi(\\omega))$: if $x\\ge T+\\eta$ then $x+\\xi\\ge T$; "
                "if $x<T-\\eta$ then $x+\\xi<T$. For the band claim, the two-point law on $\\{\\pm\\eta\\}$ realizes "
                "both sides of the cut (Theorem~\\ref{thm:inv}). This is a pathwise surrogate of a.s.\\ bounded noise, "
                "not a differential-privacy accounting proof."
            ),
            "formal": formal_block(meta),
            "dependencies": (
                "\\begin{itemize}\n"
                "\\item Deterministic \\texttt{Threshold.Preservation}.\n"
                "\\item Pathwise reduction; no DP claim.\n"
                "\\end{itemize}"
            ),
            "consequences": "Use for a.s.\\ bounded query noise on scalar thresholds; not Sparse Vector.",
            "paper_card": {
                "difficulty": "elementary",
                "applications": ["thresholding"],
                "dependencies": ["Research.Operators.Threshold.Preservation", "Threshold.BoundedNoise"],
                "reduces_to": "threshold-preservation",
                "reduced_by": [],
            },
        }
    return {
        "fundamentality": "primitive",
        "title": meta.get("title") or "Threshold Output Preservation under Bounded Perturbations",
        "abstract": (
            "Scalar threshold $A_T(x)=\\mathbf{1}\\{x\\ge T\\}$ is invariant outside the $2\\varepsilon$ unstable band "
            "when $|x'-x|\\le\\varepsilon$. Lean \\texttt{LEAN\\_FULL}."
        ),
        "problem": "The operator returns the binary indicator $A_T(x)=1$ iff $x\\ge T$ (equality passes).",
        "stability": (
            "Perturbation: $|x'-x|\\le\\varepsilon$. Pass buffer $x\\ge T+\\varepsilon\\Rightarrow A_T(x')=1$; "
            "fail buffer $x<T-\\varepsilon\\Rightarrow A_T(x')=0$."
        ),
        "definitions": (
            "\\begin{definition}\n$A_T(x)\\Leftrightarrow x\\ge T$.\\end{definition}\n"
            "\\noindent\\textbf{Assumptions.} $\\varepsilon\\ge 0$ and $|x'-x|\\le\\varepsilon$."
        ),
        "theorem": (
            "\\begin{theorem}\\label{thm:inv}\n"
            "If $|x'-x|\\le\\varepsilon$, then $x\\ge T+\\varepsilon\\Rightarrow x'\\ge T$ and "
            "$x<T-\\varepsilon\\Rightarrow x'<T$.\n"
            "\\end{theorem}"
        ),
        "intuition": "Moving $x$ by at most $\\varepsilon$ cannot cross $T$ from outside the $\\varepsilon$-neighborhood.",
        "examples": (
            "\\begin{example}\n$T=3$, $x=5$, $\\varepsilon=0.2$: $x\\ge T+\\varepsilon$, so every $x'$ in the ball still passes.\n\\end{example}"
        ),
        "proof": (
            "From $|x'-x|\\le\\varepsilon$ one has $x'-\\varepsilon\\le x\\le x'+\\varepsilon$. "
            "If $x\\ge T+\\varepsilon$ then $x'\\ge x-\\varepsilon\\ge T$. "
            "If $x<T-\\varepsilon$ then $x'\\le x+\\varepsilon<T$ (Theorem~\\ref{thm:inv})."
        ),
        "formal": formal_block(meta),
        "dependencies": (
            "\\begin{itemize}\\item Absolute-value ball arithmetic only.\\item No other operator theorems.\\end{itemize}"
        ),
        "consequences": (
            "Primitive scalar gate used by multi-threshold, abs-threshold, interval membership, and noisy threshold variants."
        ),
        "paper_card": {
            "difficulty": "elementary",
            "applications": related(meta) or ["multi-threshold", "sign"],
            "dependencies": ["Research.Operators.Threshold.Preservation"],
            "reduces_to": None,
            "reduced_by": [],
        },
    }


def sections_threshold_scalar(oid: str, meta: dict[str, Any]) -> dict[str, Any]:
    # sign / abs / interval — buffer arithmetic primitives
    return {
        "fundamentality": "primitive",
        "title": meta.get("title") or f"{oid} Preservation under Bounded Perturbations",
        "abstract": (
            f"{tt_id(oid)} is a scalar region indicator preserved outside an $\\varepsilon$-buffer under "
            f"$|x'-x|\\le\\varepsilon$. Lean \\texttt{{LEAN\\_FULL}}."
        ),
        "problem": f"The {tt_id(oid)} operator maps a scalar score to a discrete region label/bit.",
        "stability": "Additive $|x'-x|\\le\\varepsilon$; outputs agree when $x$ is at least $\\varepsilon$ inside its region.",
        "definitions": (
            "Region boundaries are thresholds (sign at $0$, abs-threshold at $T\\ge 0$, interval $[L,U]$). "
            "Assumptions follow the Lean module."
        ),
        "theorem": (
            "\\begin{theorem}\\label{thm:inv}\n"
            "Under the module's buffer hypotheses, $|x'-x|\\le\\varepsilon$ preserves the operator output; "
            "sharpness pushes across a boundary when the buffer fails.\n"
            "\\end{theorem}"
        ),
        "intuition": "Same one-dimensional buffer logic as thresholding, applied to the operator's cut set.",
        "examples": (
            "\\begin{example}\nFor sign: $x=2$, $\\varepsilon=0.5$ stays positive. For abs-threshold $T=3$, $x=5$, $\\varepsilon=0.2$ stays pass.\n\\end{example}"
        ),
        "proof": (
            "Write $|x'-x|\\le\\varepsilon$. On the pass side of each cut, $x$ is at least $\\varepsilon$ beyond the cut, "
            "so $x'$ cannot cross it; on the fail side, $x'$ cannot reach the cut. "
            "Sharpness uses a $\\pm\\varepsilon$ push from a point within $\\varepsilon$ of the boundary "
            "(Theorem~\\ref{thm:inv}), matching the Lean cases."
        ),
        "formal": formal_block(meta),
        "dependencies": (
            "\\begin{itemize}\\item Interval arithmetic on $\\mathbb{R}$.\\item Threshold-style buffers.\\end{itemize}"
        ),
        "consequences": f"Scalar building block; related: {', '.join(related(meta)[:6]) or 'thresholding'}.",
        "paper_card": {
            "difficulty": "elementary",
            "applications": related(meta),
            "dependencies": [meta.get("lean_entry_module") or ""],
            "reduces_to": None,
            "reduced_by": [],
        },
    }


def sections_multi_threshold(oid: str, meta: dict[str, Any]) -> dict[str, Any]:
    return {
        "fundamentality": "derived",
        "title": meta.get("title") or "Multi-threshold Count Preservation",
        "abstract": (
            "Pass-count $C_T(x)=|\\{i:x\\ge T_i\\}|$ is preserved when each threshold bit is preserved. "
            "Lean \\texttt{LEAN\\_FULL}."
        ),
        "problem": "Finite threshold list; output is the number of passed cuts.",
        "stability": "|x'-x|≤ε and each cut buffered ⇒ the pass-count is unchanged.",
        "definitions": "Inductive extension of scalar threshold preservation over a list.",
        "theorem": (
            "\\begin{theorem}\\label{thm:inv}\n"
            "If each threshold satisfies the scalar buffer hypotheses for $(x,x',\\varepsilon)$, "
            "then $C_T(x)=C_T(x')$. Sharpness reduces to a single failing cut.\n"
            "\\end{theorem}"
        ),
        "intuition": "Counts add independent bits; each bit is a threshold.",
        "examples": (
            "\\begin{example}\n$T=(1,3,5)$, $x=4$, $\\varepsilon=0.2$: passes two cuts; nearby $x'$ with $|x'-x|\\le 0.2$ still passes the same two.\n\\end{example}"
        ),
        "proof": (
            "Proceed by induction on the threshold list. The empty list has count $0$. "
            "For $T::\\mathrm{tail}$, the head bit is preserved by scalar threshold preservation, "
            "and the inductive hypothesis preserves the tail count; summing yields Theorem~\\ref{thm:inv}."
        ),
        "formal": formal_block(meta),
        "dependencies": (
            "\\begin{itemize}\\item \\texttt{Threshold.Preservation} per cut.\\item List induction.\\end{itemize}"
        ),
        "consequences": "Unordered pass-counts; ordered buckets are a separate ranking/bucket operator.",
        "paper_card": {
            "difficulty": "elementary",
            "applications": ["constraint-threshold-conjunction", "constraint-threshold-disjunction"],
            "dependencies": ["Research.Operators.MultiThreshold.Preservation", "Threshold.Preservation"],
            "reduces_to": "threshold-preservation",
            "reduced_by": [],
        },
    }


def sections_clamp(oid: str, meta: dict[str, Any]) -> dict[str, Any]:
    return {
        "fundamentality": "reduction",
        "title": meta.get("title") or f"{oid} Clamp Stability",
        "abstract": (
            f"{tt_id(oid)} uses interval clamp, which is $1$-Lipschitz; hence $|x'-x|\\le\\varepsilon$ implies "
            f"the clamped values move by at most $\\varepsilon$. Lean \\texttt{{LEAN\\_FULL}}."
        ),
        "problem": f"{tt_id(oid)} projects coordinates onto intervals via $\\mathrm{{clamp}}(x;\\mathrm{{lo}},\\mathrm{{hi}})=\\max(\\mathrm{{lo}},\\min(x,\\mathrm{{hi}}))$.",
        "stability": "Nonexpansiveness of clamp: output perturbation $\\le$ input perturbation in absolute value.",
        "definitions": "Require $\\mathrm{lo}\\le\\mathrm{hi}$. Stability form is the Lipschitz claim with $|x'-x|\\le\\varepsilon$.",
        "theorem": (
            "\\begin{theorem}\\label{thm:inv}\n"
            "If $\\mathrm{lo}\\le\\mathrm{hi}$ and $|x'-x|\\le\\varepsilon$, then "
            "$|\\mathrm{clamp}(x')-\\mathrm{clamp}(x)|\\le\\varepsilon$. "
            "The Lipschitz constant $1$ is sharp.\n"
            "\\end{theorem}"
        ),
        "intuition": "Clipping cannot expand distances: points move weakly toward the interval.",
        "examples": (
            "\\begin{example}\n$\\mathrm{lo}=0$, $\\mathrm{hi}=1$, $x=0.4$, $x'=0.7$, $\\varepsilon=0.3$: both clamp to themselves and move by $0.3$.\n\\end{example}"
        ),
        "proof": (
            "The map $x\\mapsto\\max(\\mathrm{lo},\\min(x,\\mathrm{hi}))$ is $1$-Lipschitz on $\\mathbb{R}$ when "
            "$\\mathrm{lo}\\le\\mathrm{hi}$ (standard case analysis on the three regions $(-\\infty,\\mathrm{lo}]$, "
            "$[\\mathrm{lo},\\mathrm{hi}]$, $[\\mathrm{hi},\\infty)$). Therefore "
            "$|\\mathrm{clamp}(x')-\\mathrm{clamp}(x)|\\le|x'-x|\\le\\varepsilon$ (Theorem~\\ref{thm:inv}). "
            "Sharpness: take an interior segment of length $\\varepsilon$ inside $[\\mathrm{lo},\\mathrm{hi}]$."
        ),
        "formal": formal_block(meta, extra="Uses Projection.Clamp."),
        "dependencies": (
            "\\begin{itemize}\\item \\texttt{Projection.Clamp} nonexpansiveness.\\item Case analysis on regions.\\end{itemize}"
        ),
        "consequences": f"Interval/box/clipping operators reduce to clamp. Related: {', '.join(related(meta)[:6])}.",
        "paper_card": {
            "difficulty": "elementary",
            "applications": related(meta),
            "dependencies": ["Research.Operators.Projection.Clamp"],
            "reduces_to": "projection-clamp",
            "reduced_by": [],
        },
    }


def sections_feasible(oid: str, meta: dict[str, Any]) -> dict[str, Any]:
    return {
        "fundamentality": "reduction",
        "title": meta.get("title") or f"{oid} Feasible-Ball Identity",
        "abstract": (
            f"If a projector fixes feasible points and the closed $\\varepsilon$-ball about $x$ lies in the feasible set, "
            f"then every $x'$ in the ball is fixed. This is an identity certificate, not full Euclidean projection "
            f"nonexpansiveness. Lean \\texttt{{LEAN\\_FULL}}."
        ),
        "problem": f"{tt_id(oid)} is treated via a feasibility indicator / projection that fixes InSet points.",
        "stability": "Interior feasible-ball identity under $|x'-x|\\le\\varepsilon$.",
        "definitions": (
            "Assumptions: $\\mathrm{proj}(z)=z$ whenever $\\mathrm{InSet}(z)$, and $|y-x|\\le\\varepsilon\\Rightarrow\\mathrm{InSet}(y)$."
        ),
        "theorem": (
            "\\begin{theorem}\\label{thm:inv}\n"
            "Under those assumptions, every $|x'-x|\\le\\varepsilon$ satisfies $\\mathrm{proj}(x')=x'$ and $\\mathrm{proj}(x)=x$. "
            "Sharpness: if some ball point is infeasible, the ball-feasibility hypothesis fails.\n"
            "\\end{theorem}"
        ),
        "intuition": "Deep inside the feasible set, projection is the identity, so small moves stay fixed points.",
        "examples": (
            "\\begin{example}\nIf $\\mathrm{InSet}=[-1,1]$, $x=0$, $\\varepsilon=0.25$, every $x'$ in the ball is feasible and fixed by identity projection.\n\\end{example}"
        ),
        "proof": (
            "Take $|x'-x|\\le\\varepsilon$. Feasibility of the ball gives $\\mathrm{InSet}(x')$ and $\\mathrm{InSet}(x)$. "
            "Fixing feasible points yields $\\mathrm{proj}(x')=x'$ and $\\mathrm{proj}(x)=x$ (Theorem~\\ref{thm:inv}). "
            "Sharpness is the contrapositive of ball feasibility. "
            "\\textbf{Limitation:} this does not prove general Euclidean projection nonexpansiveness."
        ),
        "formal": formal_block(meta, extra="Uses Projection.FeasibleId (not Euclidean nonexpansiveness)."),
        "dependencies": (
            "\\begin{itemize}\\item \\texttt{Projection.FeasibleId}.\\item No Euclidean nonexpansiveness claim.\\end{itemize}"
        ),
        "consequences": (
            f"Honest limited certificate for simplex/$\\ell_p$-ball style operators in this library. Related: {', '.join(related(meta)[:6])}."
        ),
        "paper_card": {
            "difficulty": "elementary",
            "applications": related(meta),
            "dependencies": ["Research.Operators.Projection.FeasibleId"],
            "reduces_to": "projection-feasible-id",
            "reduced_by": [],
        },
    }


def sections_constraint(oid: str, meta: dict[str, Any]) -> dict[str, Any]:
    return {
        "fundamentality": "reduction",
        "title": meta.get("title") or f"{oid} Constraint Preservation",
        "abstract": (
            f"{tt_id(oid)} preserves a Boolean combination of threshold constraints under buffered scalar noise. "
            f"Lean \\texttt{{LEAN\\_FULL}}."
        ),
        "problem": "Conjunction or disjunction of threshold predicates on coordinates/scores.",
        "stability": "Each literal is threshold-stable; Boolean combinations inherit preservation.",
        "definitions": "Reduce to multi-threshold / threshold preservation on each cut.",
        "theorem": (
            "\\begin{theorem}\\label{thm:inv}\n"
            "If every atomic threshold is buffer-stable for $(x,x',\\varepsilon)$, the conjunction/disjunction value is preserved.\n"
            "\\end{theorem}"
        ),
        "intuition": "Boolean operations are deterministic functions of stable bits.",
        "examples": (
            "\\begin{example}\nTwo cuts $x\\ge 1$ and $x\\ge 3$ with $x=4$, $\\varepsilon=0.2$: both bits stable, so their conjunction stays true.\n\\end{example}"
        ),
        "proof": (
            "Each atomic predicate is preserved by scalar threshold preservation under the buffer hypotheses. "
            "Conjunction (resp.\\ disjunction) is a fixed Boolean function of those bits, hence preserved "
            "(Theorem~\\ref{thm:inv})."
        ),
        "formal": formal_block(meta),
        "dependencies": (
            "\\begin{itemize}\\item Threshold / multi-threshold cores.\\item Boolean congruence.\\end{itemize}"
        ),
        "consequences": "Constraint-side companion to multi-threshold counts.",
        "paper_card": {
            "difficulty": "elementary",
            "applications": related(meta),
            "dependencies": [meta.get("lean_entry_module") or "", "Threshold.Preservation"],
            "reduces_to": "threshold-preservation",
            "reduced_by": [],
        },
    }


def sections_generic(oid: str, meta: dict[str, Any]) -> dict[str, Any]:
    # packaging hops / leftovers
    authority = meta.get("math_authority")
    return {
        "fundamentality": "derived" if authority else "reduction",
        "title": meta.get("title") or f"{oid} Stability Certificate",
        "abstract": f"Lean-gated stability package for {tt_id(oid)} (\\texttt{{LEAN\\_FULL}}).",
        "problem": f"Operator {tt_id(oid)} as recorded in metadata.",
        "stability": (meta.get("authored") or {}).get("perturbation_model") or "See Lean proposition.",
        "definitions": "As in the Lean \\texttt{*Prop} statement and metadata assumptions.",
        "theorem": (
            "\\begin{theorem}\\label{thm:inv}\n"
            "The Lean-certified invariance (and sharpness, if present) hold under the module hypotheses.\n"
            "\\end{theorem}"
        ),
        "intuition": ((meta.get("authored") or {}).get("proof_strategy") or "See proof dependencies.")[:400],
        "examples": (
            "\\begin{example}\nSee the operator's score/threshold encoding in the Lean profile; "
            "numeric buffers follow the $2\\varepsilon$ or $\\varepsilon$-Lipschitz pattern of the parent core.\n\\end{example}"
        ),
        "proof": (
            "By the kernel-checked proof of the cited Lean theorems. "
            + (
                f"This packaging hop defers mathematics to \\texttt{{{authority}}}."
                if authority
                else "Expanding the parent-core argument in operator language yields the same $\\ell_\\infty$ gap or Lipschitz estimate as in the formal statement."
            )
            + " The hypotheses and conclusion are exactly those of the \\texttt{*Prop} objects named below (Theorem~\\ref{thm:inv})."
        ),
        "formal": formal_block(meta, extra=f"Math authority: \\texttt{{{authority}}}." if authority else ""),
        "dependencies": (
            "\\begin{itemize}\n"
            f"\\item Lean module \\texttt{{{meta.get('lean_entry_module')}}}.\n"
            + (f"\\item Authority package \\texttt{{{authority}}}.\n" if authority else "")
            + "\\end{itemize}"
        ),
        "consequences": f"Related: {', '.join(related(meta)[:8]) or 'see library index'}.",
        "paper_card": {
            "difficulty": "standard",
            "applications": related(meta),
            "dependencies": [meta.get("lean_entry_module") or ""],
            "reduces_to": authority,
            "reduced_by": [],
        },
    }


def build_sections(oid: str, meta: dict[str, Any]) -> dict[str, Any]:
    from section_overrides import multi_threshold_sections, sign_sections

    fam = family_of(meta)
    th = (meta.get("crp_identifiers") or {}).get("theorem_id", "")
    if oid == "sign" or fam == "threshold_scalar" and oid == "sign":
        return sign_sections(oid, meta, formal_block=formal_block, related=related)
    if fam == "multi_threshold" or "MultiThreshold" in (meta.get("lean_entry_module") or ""):
        return multi_threshold_sections(oid, meta, formal_block=formal_block, related=related)
    if fam == "kth":
        return sections_kth(oid, meta)
    if fam == "ranking":
        return sections_ranking(oid, meta)
    if fam == "argmax":
        return sections_argmax(oid, meta)
    if fam == "threshold":
        return sections_threshold(oid, meta, noisy="noise" in th)
    if fam == "threshold_scalar":
        return sections_threshold_scalar(oid, meta)
    if fam == "multi_threshold":
        return multi_threshold_sections(oid, meta, formal_block=formal_block, related=related)
    if fam == "clamp":
        return sections_clamp(oid, meta)
    if fam == "feasible":
        return sections_feasible(oid, meta)
    if fam == "constraint":
        return sections_constraint(oid, meta)
    return sections_generic(oid, meta)


def main() -> int:
    if len(sys.argv) >= 3:
        oid, thm = sys.argv[1], sys.argv[2]
        pkg = ROOT / "research-results" / oid / thm
        meta = load(pkg / "metadata.json")
        sec = build_sections(oid, meta)
        out = pkg / "sections.v1.json"
        out.write_text(json.dumps(sec, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(out)
        return 0

    # bulk: all non-archive metadata packages
    n = 0
    for meta_path in sorted((ROOT / "research-results").glob("*/*/metadata.json")):
        if "_archive" in meta_path.parts or meta_path.parent.parent.name == "primitive-library":
            continue
        oid = meta_path.parent.parent.name
        thm = meta_path.parent.name
        # skip median if already has custom sections? still rebuild ok except keep median custom
        if oid == "median" and thm == "median-margin" and (meta_path.parent / "sections.v1.json").is_file():
            print(f"KEEP {oid}/{thm}")
            n += 1
            continue
        if (meta_path.parent / "sections.v1.lock").is_file():
            print(f"LOCK {oid}/{thm}")
            n += 1
            continue
        meta = load(meta_path)
        if (meta.get("derived_lean_status") or (meta.get("derived") or {}).get("lean_status")) != "LEAN_FULL":
            print(f"SKIP lean {oid}/{thm}")
            continue
        sec = build_sections(oid, meta)
        out = meta_path.parent / "sections.v1.json"
        out.write_text(json.dumps(sec, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(out)
        n += 1
    print(f"wrote {n} section files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
