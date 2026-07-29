"""Optional Phase-5 LLM proof-body repair (disabled by default).

LLM may only return a new proof body for a named theorem; STATEMENT regions
are never spliced from model output.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ProofBodyRepair:
    """Adapter interface — v1 refuses all proposals."""

    max_rounds: int = 8

    def propose_proof_body(
        self,
        prop_name: str,
        current_proof: str,
        lake_diagnostics: str,
    ) -> str:
        raise NotImplementedError(
            "ProofBodyRepair not configured; handwritten proofs are the v1 path"
        )

    def splice_proof_body(self, lean_src: str, theorem_name: str, new_body: str) -> str:
        """Replace proof after `theorem <name> ... :=` without touching STATEMENT markers."""
        begin = "/- STATEMENT_BEGIN -/"
        end = "/- STATEMENT_END -/"
        if begin in new_body or end in new_body:
            raise ValueError("model output must not contain STATEMENT markers")
        marker = f"theorem {theorem_name}"
        idx = lean_src.find(marker)
        if idx < 0:
            raise ValueError(f"theorem not found: {theorem_name}")
        # find := by after theorem
        assign = lean_src.find(":=", idx)
        if assign < 0:
            raise ValueError("missing :=")
        # find next top-level theorem/end/namespace after assign — simplistic: to EOF or next theorem
        rest = lean_src[assign:]
        next_thm = rest.find("\ntheorem ", 1)
        next_end = rest.find("\nend ", 1)
        cut_rel = len(rest)
        for cand in (next_thm, next_end):
            if cand > 0:
                cut_rel = min(cut_rel, cand)
        return lean_src[: assign + 2] + "\n" + new_body.rstrip() + "\n" + lean_src[assign + cut_rel :]
