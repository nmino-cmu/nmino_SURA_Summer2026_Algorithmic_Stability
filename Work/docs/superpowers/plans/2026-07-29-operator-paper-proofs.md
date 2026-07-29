# Operator paper proofs Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship publication-quality operator papers (classification + 10 sections + complete proofs + Lean cites + `*_paper.pdf`) with generator/prompts/validators, pilot on median, then regenerate the library.

**Architecture:** Sparse LaTeX template + `generate_operator_paper.py` fills from verified metadata/Lean + audited section payload; Lean paths unchanged; ship scripts call the generator.

**Tech Stack:** Python 3, pdflatex, JSON metadata, Cursor agent prompts for writer/judges.

## Global Constraints

- Lean is authority; prose ≤ Lean claim
- Complete research-paper proofs (not sketches)
- PDF name: `<operator_id with -→_>_paper.pdf`
- Archive old PDFs under `_archive/v0-thin/`
- Spec: `docs/superpowers/specs/2026-07-29-operator-paper-proofs-design.md`
- No Lean module renames; no digest mutation

---

### Task 1: Template + prompts + generator + rules/validators

**Files:**
- Create: `research-results/paper-templates/operator-stability-v1.tex`
- Create: `prompts/operator-paper/{writer,lean-fidelity-judge,math-correctness-judge,layout-judge}.md`
- Create: `scripts/generate_operator_paper.py`
- Create: `scripts/lib/operator_paper.py` (helpers: PDF name, archive, section check, paper_card)
- Modify: `.cursor/rules/research-results-publication.mdc`
- Modify: `research-results/primitive-library/common.py` (validate paper_card + layout)
- Modify: `scripts/write_{ranking,argmax,projection}_package.py` → call generator
- Modify: `research-results/README.md`

- [ ] **Step 1:** Add template with slots for classification + 10 sections
- [ ] **Step 2:** Add four prompts per spec
- [ ] **Step 3:** Implement generator (LEAN_FULL gate, render, pdflatex, archive, paper_card)
- [ ] **Step 4:** Update publication rule + validators
- [ ] **Step 5:** Self-check: `python3 -c` import + dry-run help

### Task 2: Median pilot

**Files:**
- Modify: `research-results/median/median-margin/*`
- Create: sections payload under that package or inline via generator `--sections`

- [ ] **Step 1:** Archive thin paper to `_archive/v0-thin/`
- [ ] **Step 2:** Write complete median sections (Reduction → KthMargin); run generator
- [ ] **Step 3:** Parallel judges (Lean fidelity, math completeness, layout)
- [ ] **Step 4:** Fix until all PASS; confirm `median_paper.pdf`

### Task 3: Pilot compare gate

- [ ] **Step 1:** Diff claim pins (module, theorems, LEAN_FULL) vs archive
- [ ] **Step 2:** If functionally same + complete proof → proceed Task 4; else stop

### Task 4: Bulk regenerate all operators

- [ ] **Step 1:** Family maps + parallel content generation for all packages
- [ ] **Step 2:** Run generator per package; spot-judge primitives; validate library
- [ ] **Step 3:** Update ship scripts if needed; FINAL note in proof-outline for median

### Task 5: Verification

- [ ] **Step 1:** `validate_metadata.py` / layout checks PASS
- [ ] **Step 2:** Spot-check argmax, threshold, projection-simplex PDFs exist with 10 sections
