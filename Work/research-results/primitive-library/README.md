# Primitive Operator Library

Empirical foundation for comparing stabilization properties of optimization-based
selection primitives. Section 1 provides **infrastructure only**: registry,
metadata schema, deterministic aggregate index, and fail-closed validation.

## Operator vs theorem vs certificate

| Concept | What it is | Where it lives |
|---------|------------|----------------|
| **Operator** | Named selection primitive (e.g. Threshold) | `operators.json` |
| **Theorem** | One Lean-gated stability claim about an operator | `research-results/<operator>/<theorem-slug>/` |
| **Certificate** | Kernel-checked Lean evidence for a theorem | `lean/certificates/<operator>/<theorem-slug>/` |

An operator may have zero theorems (`planned`), one or more theorems
(`complete` / `in_progress`), or exist only as a **reference** outside the build
sequence (`reserved_reference`, e.g. Argmax).

## Layout

```text
research-results/primitive-library/
  README.md
  schema.json           # theorem metadata schema (authored / derived / library)
  operators.json        # canonical operator registry (hand-authored)
  index.json            # GENERATED aggregate — never hand-edit
  generate_index.py
  common.py             # shared validation / index builders
  validation/
    validate_metadata.py
    validate_index.py
```

## Operator registry (`operators.json`)

Canonical list of library operators. Controlled `status` enum:

- `planned` — in the build sequence; no theorem packages yet
- `in_progress` — packages may exist; not yet merge-complete
- `complete` — implemented, Lean-gated theorems present, metadata schema-conformant
- `reserved_reference` — excluded from the primitive build program; reference only

`argmax` is `reserved_reference` with `implemented: false`. It must not be
treated as an in-scope primitive.

`theorem_count` on a `complete` / `in_progress` entry must match the number of
non-archive theorem packages under `research-results/<operator_id>/`.

## Packaging-hop packages

A package that sets `packaging` (e.g. `PHASE_B_STABILIZATION`) plus a
`math_authority` path re-packages an existing theorem under a new directory
without new mathematics — `research-results/argmax/selection-stability-linf/`
is the Phase B hop for `bounded-perturbation-margin`. For these, validation
requires `crp_identifiers.theorem_id` to equal the basename of `math_authority`
(not the directory name) and requires the authority package to exist. They are
indexed like any other package, keyed by directory, so they raise
`theorem_count_indexed` above `theorem_count_registry`: the registry counts
theorems, the index counts packages.

## Theorem metadata

Each live package `research-results/<operator>/<theorem>/metadata.json` that
belongs to a `complete` or `in_progress` operator must set:

```text
library_schema_version = "primitive-library-1.0"
```

and include three blocks:

| Block | Authority | Contents |
|-------|-----------|----------|
| `authored` | Researchers | assumptions, perturbation model, theorem role, proof strategy, limitations, references, Lean theorem names |
| `derived` | Certificates / toolchain | Lean status, statement/proof digests, axiom summary, provenance, placeholder count |
| `library` | Researchers (comparison table) | primitive type, selected object, instability mechanism, stable/unstable regions, sharpness, related operators, … |

Legacy top-level publication fields (`derived_lean_status`, `lean_manifest_digest`,
…) are retained for ART compatibility and must stay consistent with `derived`.

**Do not invent digests.** Copy them from `lean/certificates/.../lean_manifest.json`.

Reserved-reference packages (Argmax) may keep legacy metadata until optionally
migrated; the index records them without full comparison blocks.

## Generated index (`index.json`)

Always produce via:

```bash
python3 research-results/primitive-library/generate_index.py
```

The generator:

1. Validates the operator registry and all theorem packages (fail closed)
2. Emits a deterministic `index.json` (`sort_keys`, stable ordering)

Never edit `index.json` by hand. Any manual change is rejected by index
validation on the next check.

## Validation

```bash
python3 research-results/primitive-library/validation/validate_metadata.py
python3 research-results/primitive-library/validation/validate_index.py
```

Validation **fails closed** on missing required fields, invalid enums, duplicate
operator/theorem IDs, malformed metadata, missing/invalid certificate paths,
missing Lean modules or theorem declarations, derived-field mismatches against
certificates, and stale/non-deterministic `index.json`.

There is no warning-only path.

## Comparison workflow

1. Complete an operator (math → Lean → certificate → paper) under repo gates
2. Extend its `metadata.json` with `authored` / `derived` / `library`
3. Update `operators.json` (`status`, `implemented`, `theorem_count`)
4. Run `generate_index.py`
5. Run both validators
6. Compare operators via `index.json` → `theorems[].comparison`

## Current roster snapshot

See `operators.json` and the generated `index.json` for live counts. Threshold
(`thresholding`) is the first `complete` in-scope operator (two theorems).
Argmax remains `reserved_reference`.
