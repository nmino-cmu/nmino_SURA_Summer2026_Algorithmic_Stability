"""Lean-accurate section overrides for operators that generic family text mishandled."""

from __future__ import annotations

from typing import Any, Callable

# Imported late from build_family_sections to avoid cycles: pass formal_block/related in.


def multi_threshold_sections(oid: str, meta: dict[str, Any], *, formal_block, related) -> dict[str, Any]:
    return {
        "fundamentality": "derived",
        "title": meta.get("title") or "Multi-Threshold Pass-Count Preservation",
        "abstract": (
            "For a finite threshold list, the pass-count "
            "$C(x)=\\sum_i \\mathbf{1}\\{x\\ge T_i\\}$ is invariant under $|x'-x|\\le\\varepsilon$ "
            "whenever every cut is buffered ($x\\ge T_i+\\varepsilon$ or $x<T_i-\\varepsilon$). "
            "Lean \\texttt{LEAN\\_FULL}."
        ),
        "problem": (
            "The multi-threshold operator returns the Nat pass-count "
            "$C(x;T_\\bullet)=|\\{i:x\\ge T_i\\}|$ over a finite list of cuts (equality passes)."
        ),
        "stability": (
            "Perturbation: $|x'-x|\\le\\varepsilon$. "
            "Hypothesis allCoordsStable: each $T_i$ satisfies $x\\ge T_i+\\varepsilon$ or $x<T_i-\\varepsilon$. "
            "Stability: $C(x';T_\\bullet)=C(x;T_\\bullet)$. "
            "Sharpness: if $x$ lies in $[T-\\varepsilon,T+\\varepsilon)$ for a single cut, some admissible $x'$ changes the count."
        ),
        "definitions": (
            "\\begin{definition}[Pass bit / count]\n"
            "$\\mathrm{passBit}(x,T)=1$ if $x\\ge T$ else $0$; "
            "$C(x;[])=0$ and $C(x;T{::}\\mathrm{tail})=\\mathrm{passBit}(x,T)+C(x;\\mathrm{tail})$.\n"
            "\\end{definition}\n"
            "\\noindent\\textbf{Assumptions.} $\\varepsilon\\ge 0$, $|x'-x|\\le\\varepsilon$, and allCoordsStable."
        ),
        "theorem": (
            "\\begin{theorem}[Count preservation]\\label{thm:inv}\n"
            "If $|x'-x|\\le\\varepsilon$ and every $T\\in T_\\bullet$ is buffered as above, then $C(x';T_\\bullet)=C(x;T_\\bullet)$.\n"
            "\\end{theorem}\n"
            "\\begin{theorem}[Sharpness]\\label{thm:sharp}\n"
            "If $T-\\varepsilon\\le x<T+\\varepsilon$, there exists $|x'-x|\\le\\varepsilon$ with $C(x';[T])\\neq C(x;[T])$.\n"
            "\\end{theorem}"
        ),
        "intuition": (
            "Each buffered cut is a scalar threshold bit; the count is the sum of those bits. "
            "If any cut sits in its unstable band, that bit can flip."
        ),
        "examples": (
            "\\begin{example}\n"
            "$T=(1,3,5)$, $x=4$, $\\varepsilon=0.2$: passes $T=1,3$ so $C=2$; buffered cuts keep $C=2$. "
            "If $T=3$, $x=3.1$, $\\varepsilon=0.2$, then $x'=x-\\varepsilon$ can drop the pass bit.\n"
            "\\end{example}"
        ),
        "proof": (
            "\\paragraph{Preservation.}\n"
            "Induct on the threshold list. The empty list has count $0$. "
            "For $T{::}\\mathrm{tail}$, allCoordsStable gives a scalar buffer on $T$, so "
            "threshold preservation yields $\\mathrm{passBit}(x',T)=\\mathrm{passBit}(x,T)$. "
            "The inductive hypothesis equates the tail counts. Adding proves Theorem~\\ref{thm:inv}.\n\n"
            "\\paragraph{Sharpness.}\n"
            "Assume $T-\\varepsilon\\le x<T+\\varepsilon$. If $x\\ge T$, take $x'=x-\\varepsilon$ (bit drops). "
            "If $x<T$, take $x'=x+\\varepsilon$ (bit rises). This proves Theorem~\\ref{thm:sharp}."
        ),
        "formal": formal_block(
            meta,
            extra="Depends on \\texttt{Research.Operators.Threshold.Preservation} per cut.",
        ),
        "dependencies": (
            "\\begin{itemize}\n"
            "\\item \\texttt{Threshold.Preservation} (each pass bit).\n"
            "\\item List induction on the threshold spine.\n"
            "\\item No ranking / argmax theorems required.\n"
            "\\end{itemize}"
        ),
        "consequences": (
            "Unordered pass-counts for multiple cuts; constraint conjunction/disjunction reuse buffered bits. "
            "Ordered bucket indices are a separate ranking/bucket operator."
        ),
        "paper_card": {
            "difficulty": "elementary",
            "applications": related(meta) or ["constraint-threshold-conjunction", "constraint-threshold-disjunction"],
            "dependencies": [
                "Research.Operators.MultiThreshold.Preservation",
                "Research.Operators.Threshold.Preservation",
            ],
            "reduces_to": "threshold-preservation",
            "reduced_by": [],
        },
    }


def sign_sections(oid: str, meta: dict[str, Any], *, formal_block, related) -> dict[str, Any]:
    return {
        "fundamentality": "primitive",
        "title": meta.get("title") or "Sign Preservation under Bounded Perturbations",
        "abstract": (
            "For $\\mathrm{sign}(x)\\in\\{+1,-1,0\\}$, if $|x'-x|\\le\\varepsilon$ then "
            "$\\varepsilon<x\\Rightarrow\\mathrm{sign}(x')=+1$, $x<-\\varepsilon\\Rightarrow\\mathrm{sign}(x')=-1$, "
            "and $(\\varepsilon,x)=(0,0)\\Rightarrow\\mathrm{sign}(x')=0$. Lean \\texttt{LEAN\\_FULL}."
        ),
        "problem": (
            "The sign operator returns $\\mathrm{sign}(x)=+1$ if $x>0$, $-1$ if $x<0$, and $0$ if $x=0$."
        ),
        "stability": (
            "Perturbation: $|x'-x|\\le\\varepsilon$. Preservation uses \\emph{strict} buffers $\\varepsilon<x$ and $x<-\\varepsilon$. "
            "Zero output is preserved only when $\\varepsilon=0$ and $x=0$. "
            "Sharpness covers $(0,\\varepsilon]$, $[-\\varepsilon,0)$, and $x=0$ with $\\varepsilon>0$."
        ),
        "definitions": (
            "\\begin{definition}[sign]\n"
            "$\\mathrm{sign}(x)=1$ if $0<x$; $-1$ if $x<0$; else $0$.\n"
            "\\end{definition}"
        ),
        "theorem": (
            "\\begin{theorem}[Sign preservation]\\label{thm:inv}\n"
            "If $|x'-x|\\le\\varepsilon$, then: (i) $\\varepsilon<x\\Rightarrow\\mathrm{sign}(x')=1$; "
            "(ii) $x<-\\varepsilon\\Rightarrow\\mathrm{sign}(x')=-1$; "
            "(iii) $\\varepsilon=0\\land x=0\\Rightarrow\\mathrm{sign}(x')=0$.\n"
            "\\end{theorem}\n"
            "\\begin{theorem}[Sharpness]\\label{thm:sharp}\n"
            "If $0<x\\le\\varepsilon$ then some $|x'-x|\\le\\varepsilon$ has $\\mathrm{sign}(x')\\neq 1$; "
            "symmetrically for $-\\varepsilon\\le x<0$; if $x=0$ and $\\varepsilon>0$ then some $|x'-x|\\le\\varepsilon$ has $\\mathrm{sign}(x')\\neq 0$.\n"
            "\\end{theorem}"
        ),
        "intuition": (
            "A strict buffer larger than $\\varepsilon$ keeps the perturbed point away from $0$. "
            "On the closed band the push $x\\mapsto x-\\varepsilon$ can leave the positive ray."
        ),
        "examples": (
            "\\begin{example}\n"
            "$x=2$, $\\varepsilon=0.5$: $\\varepsilon<x$, so the sign stays $+1$. "
            "$x=0.4$, $\\varepsilon=0.5$: $x'=x-\\varepsilon=-0.1$ has sign $-1$.\n"
            "\\end{example}"
        ),
        "proof": (
            "From $|x'-x|\\le\\varepsilon$, $x-\\varepsilon\\le x'\\le x+\\varepsilon$. "
            "If $\\varepsilon<x$ then $x'>0$, so $\\mathrm{sign}(x')=1$. "
            "If $x<-\\varepsilon$ then $x'<0$, so $\\mathrm{sign}(x')=-1$. "
            "If $\\varepsilon=0$ and $x=0$ then $x'=0$. This is Theorem~\\ref{thm:inv}.\n\n"
            "Sharpness: if $0<x\\le\\varepsilon$, take $x'=x-\\varepsilon\\le 0$. "
            "If $-\\varepsilon\\le x<0$, take $x'=x+\\varepsilon\\ge 0$. "
            "If $x=0$ and $\\varepsilon>0$, take $x'=\\varepsilon$. This is Theorem~\\ref{thm:sharp}."
        ),
        "formal": formal_block(meta),
        "dependencies": (
            "\\begin{itemize}\\item Absolute-value ball arithmetic on $\\mathbb{R}$.\\item No other operator theorems.\\end{itemize}"
        ),
        "consequences": (
            "Primitive trichotomy gate; abs-threshold and interval membership use analogous 1D buffers."
        ),
        "paper_card": {
            "difficulty": "elementary",
            "applications": related(meta) or ["absolute-value-threshold", "thresholding"],
            "dependencies": ["Research.Operators.Sign.Preservation"],
            "reduces_to": None,
            "reduced_by": [],
        },
    }
