# Operator paper writer

Fill classification + all 10 sections for one Lean-gated operator theorem package.

## Inputs (authoritative)

- `metadata.json` (authored + derived + library)
- Lean formal verification report + `*Prop` / theorem names
- Certificate limitations (do not strengthen)
- Registry relations (related / reduces_to)

## Rules

1. Mathematics must be **deterministic from verified information** — never invent stronger claims than Lean.
2. **Proof** must be a **complete mathematical proof** suitable for a research paper (not a sketch; not “see Lean”).
3. If Lean is a definitional reduction, write a full operator-language proof and record the reduction in Proof dependencies.
4. Exactly one fundamentality label: Primitive | Derived | Reduction.
5. One concrete **Examples** instance with numbers.
6. Formal statement cites full Lean module path, theorem names, certificate directory, `LEAN_FULL`, `REAL_MATHLIB`.

## Output

JSON object with keys:
`fundamentality`, `title`, `abstract`, `problem`, `stability`, `definitions`, `theorem`, `intuition`, `examples`, `proof`, `formal`, `dependencies`, `consequences`, `paper_card` (difficulty, applications, dependencies, reduces_to, reduced_by).

LaTeX fragments only in section values (no `\documentclass`).
