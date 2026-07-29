"""Sandboxed Lake / Lean invocation (argv only, no shell)."""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path

_SAFE_ID = re.compile(r"^[a-zA-Z0-9_-]+$")


@dataclass(frozen=True)
class LakeResult:
    returncode: int
    stdout: str
    stderr: str
    elapsed_ms: int
    lake_path: str
    argv: tuple[str, ...]


class LakeRunner:
    """Invoke `lake` with fixed cwd under lean/; absolute binary path."""

    def __init__(self, lean_root: Path, *, timeout_s: int | None = None, lake_bin: str | None = None):
        self.lean_root = lean_root.resolve()
        if not self.lean_root.is_dir():
            raise FileNotFoundError(f"lean root missing: {self.lean_root}")
        # Env override for large Mathlib workspaces where package dirty-checks dominate.
        if timeout_s is None:
            timeout_s = int(os.environ.get("LAKE_TIMEOUT_S", "600"))
        self.timeout_s = timeout_s
        self.lake_bin = lake_bin or self._resolve_lake()

    def _resolve_lake(self) -> str:
        env = os.environ.get("LAKE_BIN")
        if env:
            p = Path(env)
            if p.is_file():
                return str(p.resolve())
        which = shutil.which("lake")
        if which:
            return str(Path(which).resolve())
        raise FileNotFoundError("lake not found; set LAKE_BIN or install elan")

    def build(self, *extra_args: str) -> LakeResult:
        # Only allow a tight allowlist of lake build flags / target names
        allowed_flags = {"--no-build", "--wfail", "--werror"}
        for a in extra_args:
            if a in allowed_flags:
                continue
            if a.startswith("-"):
                raise ValueError(f"refusing lake flag: {a!r}")
            # target names: Research.Operators.Argmax.Margin style
            if not re.match(r"^[A-Za-z0-9_.«»-]+$", a) or ".." in a or "/" in a or "\\" in a:
                raise ValueError(f"refusing lake target: {a!r}")
        argv = [self.lake_bin, "build", *extra_args]
        return self._run(argv)

    def env_lean(self, relative_lean_file: str) -> LakeResult:
        """Run `lake env lean <relpath>` with path confined to lean_root."""
        rel = Path(relative_lean_file)
        if rel.is_absolute() or ".." in rel.parts:
            raise ValueError(f"unsafe lean file path: {relative_lean_file!r}")
        target = (self.lean_root / rel).resolve()
        if not str(target).startswith(str(self.lean_root) + "/") and target != self.lean_root:
            raise ValueError("lean file escapes package root")
        argv = [self.lake_bin, "env", "lean", str(rel)]
        return self._run(argv)

    def _run(self, argv: list[str]) -> LakeResult:
        t0 = time.monotonic()
        try:
            proc = subprocess.run(
                argv,
                cwd=str(self.lean_root),
                capture_output=True,
                text=True,
                timeout=self.timeout_s,
                shell=False,
                env={**os.environ, "LEAN_PATH": ""},  # do not inherit model-injected LEAN_PATH
            )
            elapsed = int((time.monotonic() - t0) * 1000)
            return LakeResult(proc.returncode, proc.stdout, proc.stderr, elapsed, self.lake_bin, tuple(argv))
        except subprocess.TimeoutExpired as e:
            elapsed = int((time.monotonic() - t0) * 1000)
            out = e.stdout.decode() if isinstance(e.stdout, bytes) else (e.stdout or "")
            err = e.stderr.decode() if isinstance(e.stderr, bytes) else (e.stderr or "")
            return LakeResult(124, out, err + "\nTIMEOUT", elapsed, self.lake_bin, tuple(argv))


def sanitize_run_id(run_id: str) -> str:
    if not _SAFE_ID.match(run_id):
        raise ValueError(f"unsafe run_id: {run_id!r}")
    return run_id
