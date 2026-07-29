"""Semantic bind: theorem types must reference frozen Prop names; STATEMENT hash stable."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from art_int.canon import H_tagged
from system_b.lean.ir import FormalizationCandidate, extract_statement_region, statement_region_digest
from system_b.lean.placeholders import FORBIDDEN_IN_RESEARCH, scan_text


@dataclass(frozen=True)
class SemanticAudit:
    ok: bool
    reason_codes: tuple[str, ...]


_THEOREM = re.compile(
    r"(?:theorem|lemma)\s+([A-Za-z][A-Za-z0-9_]*)\s*:\s*([^\n:=]+)",
    re.MULTILINE,
)


def audit_props_and_theorems(fc: FormalizationCandidate, lean_root: Path) -> SemanticAudit:
    reasons: list[str] = []
    prop_rel = fc.prop_module_relative
    if not prop_rel:
        return SemanticAudit(False, ("PROP_PATH_MISSING",))
    prop_file = lean_root / prop_rel
    if not prop_file.is_file():
        return SemanticAudit(False, ("PROP_FILE_MISSING",))

    src = prop_file.read_text(encoding="utf-8")
    try:
        region = extract_statement_region(src)
        region_digest = statement_region_digest(src)
    except ValueError:
        return SemanticAudit(False, ("STATEMENT_MARKERS_MISSING",))

    live_freeze = H_tagged(
        "SEMANTIC_FREEZE.v1",
        fc.conclusion_digest,
        region_digest,
        fc.targets,
        fc.conventions,
        fc.prop_module_digests,
    )
    if live_freeze != fc.semantic_freeze_digest:
        reasons.append("SEMANTIC_FREEZE_MISMATCH")

    for t in fc.targets:
        prop = t["prop_fully_qualified"].split(".")[-1]
        thm = t["theorem_name"]
        if f"def {prop}" not in region:
            reasons.append(f"PROP_MISSING:{prop}")
        matches = [m for m in _THEOREM.finditer(src) if m.group(1) == thm]
        if len(matches) != 1:
            reasons.append(f"THEOREM_COUNT:{thm}:{len(matches)}")
        else:
            ty = matches[0].group(2).strip()
            if not re.search(rf"\b{re.escape(prop)}\b", ty):
                reasons.append(f"STATEMENT_MISMATCH:{thm}")

    findings = scan_text(src, path=str(prop_file))
    if any(f.kind in FORBIDDEN_IN_RESEARCH for f in findings):
        reasons.append("PLACEHOLDER_IN_PROP_MODULE")

    if reasons:
        return SemanticAudit(False, tuple(dict.fromkeys(reasons + ["SEMANTIC_AUDIT_FAILED"])))
    return SemanticAudit(True, ())
