"""Forbidden Lean construct scanner (sorry / admit / axiom / constant / unsafe / partial)."""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path

# Declaration-like forms (conservative: flag executable bypasses)
_SORRY = re.compile(r"\bsorry\b")
_ADMIT = re.compile(r"\badmit\b")
_AXIOM = re.compile(r"(^|\s)axiom\s+\S")
_CONSTANT = re.compile(r"(^|\s)constant\s+\S")
_UNSAFE = re.compile(r"(^|\s)unsafe\s+")
_PARTIAL = re.compile(r"(^|\s)partial\s+def\b")


@dataclass(frozen=True)
class Finding:
    path: str
    line: int
    kind: str
    text: str


def _strip_line_comment(line: str) -> str:
    if "--" in line:
        return line[: line.index("--")]
    return line


def _normalize(text: str) -> str:
    # Strip zero-width / format chars that could hide tokens
    cleaned = "".join(ch for ch in text if unicodedata.category(ch) != "Cf")
    return unicodedata.normalize("NFKC", cleaned)


def scan_text(text: str, *, path: str = "<mem>") -> list[Finding]:
    text = _normalize(text)
    out: list[Finding] = []
    in_block = False
    for i, raw in enumerate(text.splitlines(), start=1):
        line = raw
        if in_block:
            if "-/" in line:
                line = line[line.index("-/") + 2 :]
                in_block = False
            else:
                continue
        while "/-" in line:
            start = line.index("/-")
            rest = line[start + 2 :]
            if "-/" in rest:
                end = rest.index("-/")
                line = line[:start] + rest[end + 2 :]
            else:
                line = line[:start]
                in_block = True
                break
        # Strip string literals conservatively (double-quoted)
        code = _strip_line_comment(line)
        code_no_str = re.sub(r'"([^"\\]|\\.)*"', '""', code)
        for kind, rx in (
            ("sorry", _SORRY),
            ("admit", _ADMIT),
            ("axiom", _AXIOM),
            ("constant", _CONSTANT),
            ("unsafe", _UNSAFE),
            ("partial", _PARTIAL),
        ):
            if rx.search(code_no_str):
                out.append(Finding(path, i, kind, raw.rstrip()))
    return out


def scan_paths(paths: list[Path]) -> list[Finding]:
    findings: list[Finding] = []
    skip_parts = {".lake", "scratch", "_axiom_capture", "fixtures"}
    for p in paths:
        if p.is_file() and p.suffix == ".lean":
            findings.extend(scan_text(p.read_text(encoding="utf-8"), path=str(p)))
        elif p.is_dir():
            for f in sorted(p.rglob("*.lean")):
                if any(part in skip_parts for part in f.parts):
                    continue
                findings.extend(scan_text(f.read_text(encoding="utf-8"), path=str(f)))
    return findings


FORBIDDEN_IN_RESEARCH = frozenset({"sorry", "admit", "axiom", "constant", "unsafe", "partial"})
