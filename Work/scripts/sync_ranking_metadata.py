#!/usr/bin/env python3
"""Sync ranking-operator metadata digests to the live Lean certificate and regenerate index."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    oid = sys.argv[1]
    thm = f"{oid}-margin"
    cert = json.loads((ROOT / f"lean/certificates/{oid}/{thm}/lean_manifest.json").read_text())
    meta_path = ROOT / f"research-results/{oid}/{thm}/metadata.json"
    meta = json.loads(meta_path.read_text())
    tr = cert["transcript"]
    meta["lean_manifest_digest"] = cert["manifest_digest"]
    meta["verification_result_identifiers"] = ["LEAN_FULL", cert["manifest_digest"]]
    meta["derived"]["statement_digest"] = tr["lean_statement_digest"]
    meta["derived"]["proof_digest"] = tr["proof_tree_digest"]
    meta["derived"]["axiom_summary"] = {
        "imported_axiom_closure_sorted": tr["imported_axiom_closure_sorted"],
        "custom_axiom_ids_sorted": tr.get("custom_axiom_ids_sorted", []),
        "axiom_closure_captured": True,
    }
    meta["derived"]["provenance"]["lean_manifest_digest"] = cert["manifest_digest"]
    meta["derived"]["provenance"]["claim_digest"] = cert["claim_digest"]
    meta_path.write_text(json.dumps(meta, indent=2) + "\n")
    subprocess.check_call(["python3", "research-results/primitive-library/generate_index.py"], cwd=ROOT)
    subprocess.check_call(
        ["python3", "research-results/primitive-library/validation/validate_metadata.py"], cwd=ROOT
    )
    subprocess.check_call(
        ["python3", "research-results/primitive-library/validation/validate_index.py"], cwd=ROOT
    )
    print(cert["manifest_digest"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
