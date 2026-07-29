"""Filesystem LeanManifestStore (ART-10b surrogate)."""

from __future__ import annotations

import json
import os
import re
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator

_SAFE = re.compile(r"^[a-zA-Z0-9_-]+$")


def sanitize_id(name: str, *, field: str) -> str:
    if not _SAFE.match(name):
        raise ValueError(f"unsafe {field}: {name!r}")
    return name


def _atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".tmp_", suffix=".json")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(text)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    except Exception:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


@contextmanager
def _claim_lock(d: Path) -> Iterator[None]:
    """Best-effort exclusive lock for concurrent certificate writes (POSIX)."""
    d.mkdir(parents=True, exist_ok=True)
    lock_path = d / ".write.lock"
    fd = os.open(str(lock_path), os.O_CREAT | os.O_RDWR, 0o644)
    try:
        try:
            import fcntl

            fcntl.flock(fd, fcntl.LOCK_EX)
        except ImportError:
            pass
        yield
    finally:
        try:
            import fcntl

            fcntl.flock(fd, fcntl.LOCK_UN)
        except Exception:
            pass
        os.close(fd)


class LeanManifestStore:
    """store_kind=ART10b_SURROGATE_V1 — not an ART-06b Commit."""

    def __init__(self, root: Path):
        self.root = root.resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def path_for(self, operator_id: str, theorem_id: str) -> Path:
        op = sanitize_id(operator_id, field="operator_id")
        th = sanitize_id(theorem_id, field="theorem_id")
        d = (self.root / op / th).resolve()
        if not str(d).startswith(str(self.root) + os.sep) and d != self.root:
            raise ValueError("path escapes certificate root")
        return d

    def write(
        self,
        *,
        operator_id: str,
        theorem_id: str,
        manifest: dict[str, Any],
        transcript: dict[str, Any],
        report_md: str,
        status_display: dict[str, Any],
    ) -> Path:
        d = self.path_for(operator_id, theorem_id)
        with _claim_lock(d):
            _atomic_write(d / "lean_manifest.json", json.dumps(manifest, indent=2, sort_keys=True) + "\n")
            _atomic_write(
                d / "verifier_transcript.json", json.dumps(transcript, indent=2, sort_keys=True) + "\n"
            )
            _atomic_write(
                d / "status_recomputed.json",
                json.dumps(status_display, indent=2, sort_keys=True) + "\n",
            )
            _atomic_write(d / "formal_verification_report.md", report_md)
        return d

    def read_manifest(self, operator_id: str, theorem_id: str) -> dict[str, Any] | None:
        p = self.path_for(operator_id, theorem_id) / "lean_manifest.json"
        if not p.is_file():
            return None
        return json.loads(p.read_text(encoding="utf-8"))
