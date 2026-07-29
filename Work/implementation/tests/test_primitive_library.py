"""Primitive Operator Library Section 1 — registry, metadata, deterministic index."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
LIB = REPO / "research-results" / "primitive-library"
sys.path.insert(0, str(LIB))

from common import (  # noqa: E402
    build_index,
    dump_canonical,
    validate_all_metadata,
    validate_index_file,
    validate_package_metadata,
    load_json,
)


def test_metadata_validation_passes() -> None:
    assert validate_all_metadata() == []


def test_index_deterministic_and_matches_disk() -> None:
    # Generate twice in-memory
    a = dump_canonical(build_index())
    b = dump_canonical(build_index())
    assert a == b
    errors = validate_index_file()
    assert errors == [], errors


def test_argmax_is_reserved_not_implemented() -> None:
    registry = load_json(LIB / "operators.json")
    argmax = next(e for e in registry["operators"] if e["operator_id"] == "argmax")
    assert argmax["status"] == "reserved_reference"
    assert argmax["reserved"] is True
    assert argmax["implemented"] is False
    assert argmax["sequence"] is None


def test_threshold_complete_with_two_theorems() -> None:
    registry = load_json(LIB / "operators.json")
    th = next(e for e in registry["operators"] if e["operator_id"] == "thresholding")
    assert th["status"] == "complete"
    assert th["implemented"] is True
    assert th["theorem_count"] == 2
    index = load_json(LIB / "index.json")
    th_ids = {
        t["theorem_id"]
        for t in index["theorems"]
        if t["operator_id"] == "thresholding"
    }
    assert th_ids == {"threshold-output-preservation", "bounded-noise-threshold"}


def test_malformed_metadata_fails_closed(tmp_path: Path) -> None:
    meta = load_json(
        REPO
        / "research-results"
        / "thresholding"
        / "threshold-output-preservation"
        / "metadata.json"
    )
    del meta["library"]["sharpness"]
    fake = tmp_path / "thresholding" / "threshold-output-preservation" / "metadata.json"
    fake.parent.mkdir(parents=True)
    fake.write_text(json.dumps(meta), encoding="utf-8")
    errors = validate_package_metadata(
        meta, path=fake, repo=REPO, require_library_schema=True
    )
    assert any("library.missing:sharpness" in e for e in errors), errors


def test_packaging_hop_requires_real_math_authority() -> None:
    pkg = REPO / "research-results" / "argmax" / "selection-stability-linf"
    meta = load_json(pkg / "metadata.json")
    assert validate_package_metadata(
        meta, path=pkg / "metadata.json", repo=REPO, require_library_schema=False
    ) == []

    meta["math_authority"] = "research-results/argmax/does-not-exist/"
    errors = validate_package_metadata(
        meta, path=pkg / "metadata.json", repo=REPO, require_library_schema=False
    )
    assert any("math_authority_package_missing" in e for e in errors), errors
    assert any("theorem_id_not_math_authority" in e for e in errors), errors


def test_cli_validators_exit_zero() -> None:
    for script in (
        LIB / "validation" / "validate_metadata.py",
        LIB / "validation" / "validate_index.py",
    ):
        proc = subprocess.run(
            [sys.executable, str(script)],
            cwd=REPO,
            capture_output=True,
            text=True,
            check=False,
        )
        assert proc.returncode == 0, proc.stdout + proc.stderr
