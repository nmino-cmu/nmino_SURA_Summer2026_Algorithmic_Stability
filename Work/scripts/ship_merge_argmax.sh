#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
OID="$1"; LEAN="$2"; DISPLAY="$3"
FAMILY="${4:-primitive_search}"
SCORE="${5:-finite scores with unique maximizer}"
PKG="${OID//-/_}"
THM="${OID}-margin"
export OID THM
VENV="$ROOT/implementation/.venv/bin"

git checkout main
git pull origin main
if git show-ref --verify --quiet "refs/heads/operator/$OID"; then git branch -D "operator/$OID"; fi
if git ls-remote --exit-code --heads origin "operator/$OID" >/dev/null 2>&1; then git push origin --delete "operator/$OID" || true; fi
git checkout -b "operator/$OID"
git push -u origin HEAD

python3 scripts/clone_argmax_op.py --id "$OID" --lean "$LEAN" --display "$DISPLAY" --score-construction "$SCORE"
"$VENV/pytest" "implementation/tests/test_${PKG}_operator.py" "implementation/tests/lean/test_${PKG}_e2e.py" -q --tb=short
test -f "lean/certificates/$OID/$THM/lean_manifest.json"

python3 scripts/write_argmax_package.py "$OID" "$LEAN" "$DISPLAY" "$FAMILY"
python3 scripts/build_family_sections.py "$OID" "$THM"
python3 scripts/generate_operator_paper.py "$OID" "$THM" --sections "research-results/$OID/$THM/sections.v1.json"
python3 scripts/sync_ranking_metadata.py "$OID"

"$VENV/pytest" implementation/tests --ignore=implementation/tests/test_primitive_library.py -q --tb=line
python3 scripts/sync_ranking_metadata.py "$OID"
"$VENV/pytest" implementation/tests/test_primitive_library.py -q --tb=line

# Restore dirty unrelated certificates; keep this operator's cert.
shopt -s nullglob
for d in lean/certificates/*/; do
  base="$(basename "$d")"
  if [[ "$base" != "$OID" ]]; then
    git checkout -- "$d" 2>/dev/null || true
  fi
done
# Drop accidental Finder duplicate junk if present
find . -name '* 2.*' -type f -print -delete 2>/dev/null || true

git add -A
git commit -m "feat(operator): add ${OID} via Argmax-margin reduction (LEAN_FULL)"
git push
git checkout main && git pull
git merge --no-ff "operator/$OID" -m "Merge branch 'operator/${OID}'"
git push origin main
git branch -d "operator/$OID"
git push origin --delete "operator/$OID"
echo "MERGED $OID $(git rev-parse --short HEAD)"
