"""Capture Lean `#print axioms` for accepted declarations."""

from __future__ import annotations

import os
import re
from pathlib import Path

from system_b.lean.lake_runner import LakeRunner

_AX_LINE = re.compile(
    r"'([^']+)'\s+depends on axioms:\s*\[([^\]]*)\]|"
    r"'([^']+)'\s+does not depend on any axioms"
)


def parse_print_axioms(output: str) -> dict[str, list[str]]:
    """Parse `#print axioms` stdout into decl → sorted axiom names."""
    out: dict[str, list[str]] = {}
    for m in _AX_LINE.finditer(output):
        if m.group(1) is not None:
            decl = m.group(1)
            raw = m.group(2).strip()
            axioms = [a.strip() for a in raw.split(",") if a.strip()] if raw else []
            out[decl] = sorted(axioms)
        else:
            out[m.group(3)] = []
    return out


def capture_axioms(
    lean_root: Path,
    *,
    import_module: str,
    decl_names: list[str],
    timeout_s: int | None = None,
) -> dict[str, list[str]]:
    """Run `#print axioms` via `lake env lean` on a temp file under lean_root."""
    if timeout_s is None:
        timeout_s = int(os.environ.get("LAKE_TIMEOUT_S", "600"))
    lines = [f"import {import_module}"]
    for d in decl_names:
        fq = d if "." in d else f"{import_module}.{d}"
        lines.append(f"#print axioms {fq}")
    text = "\n".join(lines) + "\n"
    # Write inside lean_root so Lake env resolves the package
    tmp_dir = lean_root / "scratch" / "_axiom_capture"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    tmp = tmp_dir / "print_axioms.lean"
    tmp.write_text(text, encoding="utf-8")
    runner = LakeRunner(lean_root, timeout_s=timeout_s)
    result = runner.env_lean(str(tmp.relative_to(lean_root)))
    combined = result.stdout + "\n" + result.stderr
    if result.returncode != 0:
        raise RuntimeError(f"axiom capture failed ({result.returncode}): {combined[-2000:]}")
    parsed = parse_print_axioms(combined)
    # Normalize keys to short names as well
    by_short: dict[str, list[str]] = {}
    for k, v in parsed.items():
        by_short[k] = v
        by_short[k.split(".")[-1]] = v
    return by_short


def union_axiom_closure(by_decl: dict[str, list[str]], decl_names: list[str]) -> list[str]:
    s: set[str] = set()
    for d in decl_names:
        axioms = by_decl.get(d) or by_decl.get(d.split(".")[-1])
        if axioms is None:
            raise KeyError(f"missing axiom report for {d}")
        s.update(axioms)
    return sorted(s)
