# Layout judge

## Pass iff ALL hold

1. Sections appear in exact order with exact titles:
   Problem, Stability notion, Definitions, Theorem, Intuition, Examples, Proof, Formal statement, Proof dependencies, Consequences
2. Front matter contains **This theorem is:** with exactly one of Primitive / Derived / Reduction
3. Published PDF name must be `<operator_id with - replaced by _>_paper.pdf`
4. Proof dependencies section is nonempty
5. Examples section contains a concrete numeric instance

## Output

`PASS` or `FAIL` with bullet reasons. No prose rewrite.
