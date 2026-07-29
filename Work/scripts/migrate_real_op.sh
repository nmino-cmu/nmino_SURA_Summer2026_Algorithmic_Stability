#!/usr/bin/env bash
# Migrate one operator profile+cert to REAL_MATHLIB. Target-only Lean e2e.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
OID="$1"
PKG="${OID//-/_}"
VENV="$ROOT/implementation/.venv/bin"

git checkout main
git pull origin main
if git show-ref --verify --quiet "refs/heads/operator/${OID}-real"; then git branch -D "operator/${OID}-real"; fi
git checkout -b "operator/${OID}-real"

# Patch lean_profile.py
python3 << PY
from pathlib import Path
import re
p = Path("implementation/src/operators/${PKG}/lean_profile.py")
t = p.read_text()
t2 = t.replace('"MATHLIB_REAL_PENDING", ', '').replace(', "MATHLIB_REAL_PENDING"', '')
t2 = t2.replace('"MATHLIB_REAL_PENDING"', '')
# clean empty gaps list artifacts like KNOWN_GAPS = [,]
t2 = re.sub(r'KNOWN_GAPS = \[\s*,', 'KNOWN_GAPS = [', t2)
t2 = re.sub(r',\s*\]', ']', t2)
if 'MATHLIB_REAL_PENDING' in t2:
    t2 = t2.replace('KNOWN_GAPS = ["MATHLIB_REAL_PENDING", "DEFINITION_PINS_SURROGATE"]',
                    'KNOWN_GAPS = ["DEFINITION_PINS_SURROGATE"]')
    t2 = t2.replace('KNOWN_GAPS = ["MATHLIB_REAL_PENDING"]', 'KNOWN_GAPS = []')
t2 = t2.replace('"INT_ORDERED_GROUP_CORE"', '"REAL_MATHLIB"')
t2 = t2.replace('"score_encoding": "INT_ORDERED_GROUP_CORE"', '"score_encoding": "REAL_MATHLIB"')
if 'REAL_MATHLIB' not in t2:
    t2 = t2.replace(
        '"score_encoding":',
        '"score_encoding": "REAL_MATHLIB",  # migrated\n    "score_encoding_old":',
    )
# Force score_encoding
t2 = re.sub(
    r'"score_encoding":\s*"[^"]*"',
    '"score_encoding": "REAL_MATHLIB"',
    t2,
)
p.write_text(t2)
print('patched', p)
PY

# Find e2e/unit tests (operator id slug ≠ always test filename, e.g. thresholding → test_threshold_e2e)
E2E=""
for cand in \
  "implementation/tests/lean/test_${PKG}_e2e.py" \
  "implementation/tests/lean/test_${OID//-/_}_e2e.py" \
  "implementation/tests/lean/test_threshold_e2e.py" \
  "implementation/tests/lean/test_abs_threshold_e2e.py"
do
  if [[ -f "$cand" && ( "$cand" == *"/${PKG}"* || "$OID" == thresholding && "$cand" == *threshold_e2e* || "$OID" == absolute-value-threshold && "$cand" == *abs_threshold* ) ]]; then
    E2E="$cand"
    break
  fi
done
# Prefer glob match by package fragments
if [[ -z "$E2E" ]]; then
  E2E=$(ls implementation/tests/lean/test_*${PKG}*_e2e.py 2>/dev/null | head -1 || true)
fi
if [[ -z "$E2E" && "$OID" == "thresholding" ]]; then
  E2E="implementation/tests/lean/test_threshold_e2e.py implementation/tests/lean/test_threshold_noise_e2e.py"
fi
if [[ -z "$E2E" && "$OID" == "absolute-value-threshold" ]]; then
  E2E="implementation/tests/lean/test_abs_threshold_e2e.py"
fi
UNIT=$(ls implementation/tests/test_${PKG}_operator.py 2>/dev/null || ls implementation/tests/test_thresholding_operator.py 2>/dev/null || ls implementation/tests/test_abs_threshold_operator.py 2>/dev/null || true)
# Also patch lean_profile_noise.py when present (thresholding dual theorem)
if [[ -f "implementation/src/operators/${PKG}/lean_profile_noise.py" ]]; then
python3 << PY
from pathlib import Path
import re
p = Path("implementation/src/operators/${PKG}/lean_profile_noise.py")
t = p.read_text()
t2 = t.replace('"MATHLIB_REAL_PENDING", ', '').replace(', "MATHLIB_REAL_PENDING"', '').replace('"MATHLIB_REAL_PENDING"', '')
t2 = re.sub(r',\s*\]', ']', t2)
t2 = re.sub(r'KNOWN_GAPS = \[\s*,', 'KNOWN_GAPS = [', t2)
t2 = re.sub(r'"score_encoding":\s*"[^"]*"', '"score_encoding": "REAL_MATHLIB"', t2)
p.write_text(t2)
print('patched', p)
PY
fi
"$VENV/pytest" ${UNIT:-} $E2E -q --tb=short

# Sync metadata digests for all theorems under this operator
python3 << PY
import json
from pathlib import Path
oid = "${OID}"
cert_root = Path(f"lean/certificates/{oid}")
if not cert_root.is_dir():
    raise SystemExit(f"missing certs {cert_root}")
for man in cert_root.rglob("lean_manifest.json"):
    thm = man.parent.name
    cert = json.loads(man.read_text())
    meta_path = Path(f"research-results/{oid}/{thm}/metadata.json")
    if not meta_path.is_file():
        print("skip meta", meta_path)
        continue
    meta = json.loads(meta_path.read_text())
    tr = cert["transcript"]
    meta["lean_manifest_digest"] = cert["manifest_digest"]
    meta["verification_result_identifiers"] = ["LEAN_FULL", cert["manifest_digest"]]
    meta["derived_lean_status"] = "LEAN_FULL"
    if "derived" in meta:
        meta["derived"]["statement_digest"] = tr["lean_statement_digest"]
        meta["derived"]["proof_digest"] = tr["proof_tree_digest"]
        meta["derived"]["axiom_summary"] = {
            "imported_axiom_closure_sorted": tr["imported_axiom_closure_sorted"],
            "custom_axiom_ids_sorted": tr.get("custom_axiom_ids_sorted", []),
            "axiom_closure_captured": True,
        }
        if "provenance" in meta["derived"]:
            meta["derived"]["provenance"]["lean_manifest_digest"] = cert["manifest_digest"]
            meta["derived"]["provenance"]["claim_digest"] = cert["claim_digest"]
    meta_path.write_text(json.dumps(meta, indent=2) + "\n")
    print("synced", oid, thm, cert["manifest_digest"][:12])
PY

# Restore unrelated dirty certs
shopt -s nullglob
for d in lean/certificates/*/; do
  base="$(basename "$d")"
  if [[ "$base" != "$OID" && "$base" != "toolchain_head.json" ]]; then
    git checkout -- "$d" 2>/dev/null || true
  fi
done
# keep toolchain_head from this run
git add -A
git commit -m "feat(operator): migrate ${OID} certificate to Mathlib Real (LEAN_FULL)"
git push -u origin HEAD
git checkout main && git pull
git merge --no-ff "operator/${OID}-real" -m "Merge branch 'operator/${OID}-real'"
git push origin main
git branch -d "operator/${OID}-real"
git push origin --delete "operator/${OID}-real" || true
echo "MIGRATED $OID $(git rev-parse --short HEAD)"
