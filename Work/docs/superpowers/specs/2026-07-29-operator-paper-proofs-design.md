# Operator paper proofs (human-readable) — Design

**Date:** 2026-07-29  
**Status:** APPROVED for implementation — executed 2026-07-29  
**Scope:** `Work/` research-results papers + ship/publication infrastructure for all operators and future operators

## Problem

Most operator packages ship thin LaTeX with theorems but no human-readable proofs; authority is Lean-only. Transform the library into a research reference: every primitive/derived theorem gets a publication-quality write-up with a complete prose proof, Lean citation, examples, consequences, and searchable dependency metadata — while Lean remains the only formal authority.

## Philosophy

| Role | Owns |
|------|------|
| **Lean** | Proves (kernel-checked `*Prop`; digests; `LEAN_FULL`) |
| **Human-readable paper** | Explains (complete research-paper proof, intuition, example, consequences) |
| **Never reverse** | Prose must not invent or strengthen mathematics beyond the verified claim |

Prose is **generated deterministically from metadata and verified information** (Lean report, theorem names, limitations, registry relations). Prose may be written by agents, but the mathematics must never appear synthesized beyond what Lean certifies.

Avoid saying “generated from scratch.” Prefer: filled from verified sources into a fixed skeleton; proof argument written in full for that operator’s stated claim.

## Locked decisions

| Topic | Choice | Rationale |
|-------|--------|-----------|
| Paper structure | Fixed sparse LaTeX skeleton with **10 body sections** + front classification | Usable research library; consistent navigation |
| Proof body | **Complete mathematical proof** suitable for a research paper (not a sketch), per operator | Theorems are small; credibility comes from full arguments |
| Front matter label | Exactly one of: **Primitive** / **Derived** / **Reduction** | Instant fundamentality signal |
| Lean paths (existing) | **Keep stable** (Sol+Fable consensus: B) | Digests/certs; no cosmetic mass rename |
| Lean naming (new ops) | `Research/Operators/<PascalOperator>/{Preservation\|Margin}.lean` | Appropriate names going forward only |
| PDF artifact | `<operator_id with -→_>_paper.pdf` (e.g. `median_paper.pdf`); keep `paper.tex` | Stable tooling + readable published name |
| Old `paper.pdf` | Archive under `_archive/v0-thin/` before replace | Never clobber history |
| Proof authority | Lean kernel; prose ≤ Lean claim | Fail closed on overclaim |
| Formal statement | Module path, theorem ids, certificate dir, `LEAN_FULL`, `REAL_MATHLIB` | Reference the Lean file without renaming it |
| Proof dependencies | Dedicated section: lemmas used / reduces-to / “no other results” | Builds mathematical dependency graph |
| Searchable cards | Metadata fields: Difficulty, Primitive/Derived/Reduction, Applications, Dependencies, Verified | Indexable library later |
| Generation path | Deterministic fill from metadata + Lean report + audited complete proof | One script for every future operator |
| Pilot | `median` / `median-margin` first; compare; then bulk | User gate |
| Multi-agent | Writer → Lean-fidelity → Math (complete-proof bar) → Layout; ≤3 rewrites | Careful correctness |

**Sol + Fable (only extremely important fork):** Lean rename → both **B** (keep paths; cite precisely).

## Paper contract (every live theorem package)

### Files

```text
research-results/<operator>/<theorem-slug>/
  paper.tex                 # LaTeX source
  <operator>_paper.pdf      # published PDF (- → _ in operator_id)
  metadata.json             # includes paper_card + layout version
  proof-outline.md          # outline + judge log
  README.md
  references.bib
  _archive/…                # prior thin / superseded PDFs
```

### Front matter (before §1)

Immediately after title/abstract (or as a labeled block under the title):

**This theorem is:** `Primitive` | `Derived` | `Reduction`  
(exactly one; sourced from metadata `paper_card.fundamentality`)

Definitions for labeling:

| Label | Meaning |
|-------|---------|
| **Primitive** | Core math proved in this package’s Lean module (or shared core owned as the statement site), not a thin alias |
| **Reduction** | Lean statement is definitionally / by reduction equal to another operator or shared core (e.g. Median → `KthMargin`) |
| **Derived** | Composition or specialization that is neither a raw core nor a pure alias (rare; use when both reduction and extra structure apply — prefer Reduction when Lean is `:=` alias) |

Median pilot expects **Reduction** (aliases `KthMargin`).

### LaTeX sections (exact titles, exact order)

1. **Problem** — What is the operator? What does it compute?
2. **Stability notion** — Allowed perturbation; certified stability notion
3. **Definitions** — Margin / gap / norm / assumptions as applicable
4. **Theorem** — Preservation (+ sharpness when certified)
5. **Intuition** — 2–4 sentences
6. **Examples** — One tiny concrete example (scores/threshold + ε/noise; optional small figure). Conveys the theorem fast.
7. **Proof** — **Complete mathematical proof suitable for a research paper** (typically ~½–1 page for these primitives). Mirrors Lean’s argument at mathematical level; not a sketch; not “see Lean.”
8. **Formal statement** — Lean module path (file reference), theorem identifiers, certificate path, `LEAN_FULL`, domain
9. **Proof dependencies** — What this proof relies on / reduces to (e.g. `OrderStat.KthMargin`, triangle inequality for ℓ∞, margin definition, “no other results”). Enables the library dependency graph.
10. **Consequences** — Why this primitive matters; which operators reduce to it; which higher-level results use it. Research value, not filler.

Preamble: `article` 11pt, geometry, amsmath/amssymb/amsthm, hyperref. Theorems/lemmas/definitions/remarks as needed. Optional `example` environment for §Examples.

### Proof writing rules

- Complete proof of the **stated** theorem under the **same** hypotheses as Lean `*Prop` / metadata.
- If Lean is a definitional reduction, write a full operator-language proof **and** record the reduction in **Proof dependencies** / Formal statement — still no “proof omitted.”
- Forbidden: stronger claims than Lean (full Euclidean projection vs feasible-ball identity; DP vs pathwise surrogate; invented axioms).
- Sharpness: full sharpness argument iff the certificate has a sharpness theorem.
- Mathematics never synthesized beyond verified claim; prose only presents that claim.

### Searchable paper card (metadata)

Generator writes/updates `metadata.json` → `paper_card` (and keeps ART compatibility fields):

| Field | Content |
|-------|---------|
| `layout` | `"operator-stability-v1"` |
| `fundamentality` | `primitive` \| `derived` \| `reduction` |
| `difficulty` | `elementary` \| `standard` \| `involved` (heuristic from core family; not a Lean status) |
| `applications` | list of operator_ids / phrases from Consequences |
| `dependencies` | Lean modules / theorem ids / named lemmas this proof uses |
| `reduces_to` | operator or core id if Reduction; else `null` |
| `reduced_by` | operator_ids that reduce to this (from index / registry where known) |
| `verified` | `{ "lean_status": "LEAN_FULL", "manifest_digest": "...", "domain": "REAL_MATHLIB" }` |

These fields are for search/index later; validators require `fundamentality`, `dependencies`, `verified.lean_status`.

## Infrastructure

### Template

`research-results/paper-templates/operator-stability-v1.tex` — sparse skeleton (classification block + 10 sections). **No** shared proof paragraphs.

### Generator

`scripts/generate_operator_paper.py`:

1. Gate on `LEAN_FULL` + certificate/metadata consistency; else `_skip-log/` + nonzero exit.
2. Load metadata, formal verification report, Lean theorem names, registry/index relations.
3. Derive `paper_card` fields deterministically where possible (`reduces_to` from Lean `:=` / known family map; `verified` from cert).
4. Run writer/judge loop → section payloads (complete Proof required).
5. Render `paper.tex`; `pdflatex` ×2 → `<operator>_paper.pdf`; archive prior published PDF; clean aux.
6. Update `proof-outline.md` + `paper_card` in metadata.
7. Never mutate Lean sources or certificate digests.

Thin-wrap or replace `write_*_package.py`; all `ship_merge_*.sh` call this generator.

### Rules / validation

- `.cursor/rules/research-results-publication.mdc`: 10-section contract + classification + PDF name + Lean citation + archive + complete-proof bar.
- Validators for each `complete` package:
  - required `\section{...}` titles in order (list above)
  - classification block present with one of the three labels
  - `<operator>_paper.pdf` exists
  - Formal statement contains `lean_entry_module` and a theorem name
  - Proof dependencies section nonempty
  - `paper_card.fundamentality` and `paper_card.verified.lean_status == LEAN_FULL`
- README one-liners in `research-results/` and `primitive-library/`.

### Prompts

`Work/prompts/operator-paper/`:

| File | Job |
|------|-----|
| `writer.md` | Fill classification + all 10 sections; **complete** research-paper proof; no overclaim; deterministic from verified inputs |
| `lean-fidelity-judge.md` | Pass/fail: claim ↔ Lean props / limitations |
| `math-correctness-judge.md` | Pass/fail: **complete** proof (not sketch); sharpness; norms; no gaps |
| `layout-judge.md` | Pass/fail: section titles/order; classification; PDF name; proof-dependencies present |

### Agents loop

```text
Writer(draft) → LeanFidelityJudge → MathJudge → LayoutJudge
  FAIL → revise with notes (≤3 rounds)
  still FAIL → abort; skip log; do not publish PDF
```

Human audit after median pilot before bulk.

## Pilot: median

1. Archive current thin `paper.tex` / `paper.pdf` → `_archive/v0-thin/`.
2. Run generator + agent loop.
3. Expect: fundamentality **Reduction**; complete Proof; Examples; Proof dependencies → `OrderStat.KthMargin`; PDF `median_paper.pdf`.
4. Compare: same math claim / Lean pins as before; structure and complete proof added.
5. Independent math + Lean-fidelity audit; then bulk.

## Bulk

After pilot PASS: all live theorem packages. Phase B packaging hop: still full layout; Proof/Formal may point at `math_authority` theorem; Proof dependencies must name that authority. Parallelize by family; no shared Lean mutation.

## Non-goals

- Renaming existing Lean modules / mass digest recompute
- Soft-alias wrapper modules
- Changing Lean proofs or CRP schemas
- Rewriting `Problem_Writeup.tex`
- Claiming Part I/II UQ results in operator papers
- Sketch-only proofs for “alias” operators

## Success criteria

1. Median: `median_paper.pdf`; classification; 10 sections; **complete** Proof; Examples; Proof dependencies; Lean citation; `paper_card` filled.
2. Same verified claim as archived thin paper; no strengthened mathematics.
3. Validators + new-operator ship path documented.
4. Bulk: every `complete` package meets the contract — research-library quality, not thin stubs.

## Spec self-review

- User mods incorporated: complete proofs; Examples; Primitive/Derived/Reduction; Proof dependencies; paper_card search fields; “deterministic from verified info” language.
- Lean rename still B.
- Section count is **10** body sections + front classification (not 8).
- PDF naming rule explicit (`-` → `_`).
