"""LakeRunner sandbox tests."""

from pathlib import Path

import pytest

from system_b.lean.lake_runner import LakeRunner, sanitize_run_id


def test_sanitize_run_id():
    assert sanitize_run_id("abc-123") == "abc-123"
    with pytest.raises(ValueError):
        sanitize_run_id("../x")


def test_lake_runner_requires_root(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        LakeRunner(tmp_path / "missing")
