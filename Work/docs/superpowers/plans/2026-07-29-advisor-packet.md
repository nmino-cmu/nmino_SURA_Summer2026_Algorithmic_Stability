# Advisor Packet Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce a polished faculty-facing `Advisor_Packet/` at the Curr repo root that meets `Work/docs/superpowers/specs/2026-07-29-advisor-packet-design.md`.

**Architecture:** Shared LaTeX style in `Assets/packet_style.tex`; one folder per document with matching `.tex`/`.pdf` names; timeline as a renamed copy of the redesigned source; all claims grounded in an evidence inventory; no combined PDF; no edits outside `Advisor_Packet/` and this plan/design path.

**Tech Stack:** LaTeX (`pdflatex` / `latexmk`), Markdown, repository file tree for path verification.

## Global Constraints

- Root: `Advisor_Packet/` at `/Users/nicholasmino/Desktop/Research/Curr/Advisor_Packet/`
- Do not overwrite, rewrite, relocate, rename, or regenerate `Formulation/writeup/Problem_Writeup.*`
- Do not modify original timeline locations; copy only into the packet
- Do not create a combined PDF
- Do not touch unrelated dirty files under `Work/`
- Prefer omission over speculation; verify every path before citing
- Notation follows Problem_Writeup
- Plan todos start as `pending` only

**Design status:** Treat `2026-07-29-advisor-packet-design.md` as APPROVED.

**Authoritative timeline source (verified 2026-07-29):** `Submission_Only/Timeline/intellectual_timeline.{tex,pdf}` (not flat `Submission_Only/`).

---

### Task 1: Scaffold, style, timeline copy, evidence inventory

**Files:**
- Create: `Advisor_Packet/Assets/packet_style.tex`
- Create: `Advisor_Packet/EVIDENCE_INVENTORY.md` (working file; may be summarized into audit later)
- Create: `Advisor_Packet/Intellectual_Timeline/Intellectual_Timeline.tex`
- Create: `Advisor_Packet/Intellectual_Timeline/Intellectual_Timeline.pdf`
- Create directories for all packet documents

- [ ] **Step 1: Confirm git hygiene**

Run from Curr root:
```bash
git -C Work status -sb | head -5
ls Formulation/writeup/Problem_Writeup.pdf Submission_Only/Timeline/intellectual_timeline.pdf
```
Expected: Work may show unrelated dirty files; do not modify them. Problem writeup and timeline PDF exist.

- [ ] **Step 2: Create directory tree**

```bash
cd /Users/nicholasmino/Desktop/Research/Curr
mkdir -p Advisor_Packet/{Assets/figures,Intellectual_Timeline,Research_Update_Summary,Questions_for_Advisors,Repository_Guide,Stabilized_Algorithm_Catalog_Overview}
```

- [ ] **Step 3: Write `Assets/packet_style.tex`**

Extract shared palette/header/tcolorbox styles from `Submission_Only/Timeline/intellectual_timeline.tex` into a reusable `\input`able style (colors, geometry defaults helpers, box styles, section formats). Documents may set `\documentclass` and `\input{../Assets/packet_style.tex}` (adjust relative path per folder depth: always `../Assets/packet_style.tex`).

- [ ] **Step 4: Copy timeline**

```bash
cp Submission_Only/Timeline/intellectual_timeline.tex Advisor_Packet/Intellectual_Timeline/Intellectual_Timeline.tex
cp Submission_Only/Timeline/intellectual_timeline.pdf Advisor_Packet/Intellectual_Timeline/Intellectual_Timeline.pdf
```
Do not edit the original. Packet copy may keep self-contained preamble (already complete) rather than forcing `\input` of packet_style if that would risk changing timeline layout; prefer byte-stable visual match. If filename-only rename is needed inside the copy, limit changes to `\jobname`-irrelevant content (none required if compiling as `Intellectual_Timeline.tex`).

- [ ] **Step 5: Write evidence inventory**

Create `Advisor_Packet/EVIDENCE_INVENTORY.md` listing each artifact as `OK` or `MISSING` with path. Must include at least:

| Artifact | Expected path |
|----------|---------------|
| Problem writeup | `Formulation/writeup/Problem_Writeup.pdf` |
| Timeline source | `Submission_Only/Timeline/intellectual_timeline.pdf` |
| FINAL-VERDICT | `Work/research-results/primitive-library/FINAL-VERDICT.md` |
| H1 catalog note | `Formulation/context/overview/swarm/04_H1_catalog.md` |
| Overview authority | `Formulation/context/overview/Research_Scope_Timeline_and_Authority.tex` |
| Paper index | `Formulation/context/papers/INDEX.md` |
| Zrnic digest | `Formulation/research/literature/digest_zrnic_jordan_stability.md` |
| CRC digest | `Formulation/research/literature/digest_angelopoulos_crc.md` |
| Architecture README | `Work/architecture-discovery/README.md` |
| Example operator paper | `Work/research-results/median/median-margin/median_paper.pdf` |
| Full structured catalog spreadsheet | record MISSING if not found |

---

### Task 2: Research_Update_Summary

**Files:**
- Create: `Advisor_Packet/Research_Update_Summary/Research_Update_Summary.tex`
- Create: `Advisor_Packet/Research_Update_Summary/Research_Update_Summary.pdf`

- [ ] **Step 1: Draft `.tex`** (≤2 pages, aim 1) with sections: Current research question; Intellectual progression; Main accomplishments; Current theorem agenda; Immediate next step; What I Would Like to Discuss. No workstream hour table. At most ~92h mention. Notation from writeup (\(\mathcal{C}\), \(\theta\), \(\mathcal{D}\)).

- [ ] **Step 2: Compile until clean**

```bash
cd Advisor_Packet/Research_Update_Summary && latexmk -pdf -interaction=nonstopmode Research_Update_Summary.tex
```
Expected: PDF produced; address overfull boxes >2pt.

- [ ] **Step 3: Visual QA** — page count 1–2; headers/footers; no orphan headings.

---

### Task 3: Questions_for_Advisors

**Files:**
- Create: `Advisor_Packet/Questions_for_Advisors/Questions_for_Advisors.tex`
- Create: `Advisor_Packet/Questions_for_Advisors/Questions_for_Advisors.pdf`

- [ ] **Step 1: Draft** one-page Qs A–D; visually highlight top 3 (tcolorbox or bold markers).

- [ ] **Step 2: Compile + visual QA** (target 1 page).

---

### Task 4: Repository_Guide

**Files:**
- Create: `Advisor_Packet/Repository_Guide/Repository_Guide.tex`
- Create: `Advisor_Packet/Repository_Guide/Repository_Guide.pdf`

- [ ] **Step 1: Draft** “How to Review This Project”; 5-min and 15–20-min orders; only verified paths from inventory; omit missing.

- [ ] **Step 2: Compile + visual QA** (target 1 page).

---

### Task 5: Stabilized_Algorithm_Catalog_Overview

**Files:**
- Create: `Advisor_Packet/Stabilized_Algorithm_Catalog_Overview/Stabilized_Algorithm_Catalog_Overview.tex`
- Create: `Advisor_Packet/Stabilized_Algorithm_Catalog_Overview/Stabilized_Algorithm_Catalog_Overview.pdf`

- [ ] **Step 1: Draft** purpose, fields, 6 mechanism-spanning entries grounded in digests/H1/overview (Zrnic–Jordan noisy/stable selection; CRC fixed-\(\theta\); DP/max-info style from Zrnic indistinguishability; regularization/Stable LASSO from digest; algorithmic stability / Bassily–Freund line as referenced; optimization robustness as hypothesized relevance from Formulation I — qualify if not a single paper entry). Patterns: literature vs hypothesis. Link to verified paths; state spreadsheet MISSING if so.

- [ ] **Step 2: Compile + visual QA** (2–4 pages).

---

### Task 6: README + PACKET_AUDIT + design status

**Files:**
- Create: `Advisor_Packet/README.md`
- Create: `Advisor_Packet/PACKET_AUDIT.md`
- Modify: `Work/docs/superpowers/specs/2026-07-29-advisor-packet-design.md` (status → APPROVED)

- [ ] **Step 1: README** GitHub-readable landing page with hierarchy, reading order, links, date 2026-07-29.

- [ ] **Step 2: PACKET_AUDIT** full checklist from design; page counts via `pdfinfo` or Python; confirm no combined PDF; recommend email attachments; confirm originals unchanged.

- [ ] **Step 3: Optionally remove `EVIDENCE_INVENTORY.md` after folding into audit, or keep and list it in audit as working artifact.

- [ ] **Step 4: Final verification**

```bash
# originals untouched
test -f Formulation/writeup/Problem_Writeup.pdf
test -f Submission_Only/Timeline/intellectual_timeline.pdf
# packet PDFs exist
ls Advisor_Packet/*/*.pdf
# no combined packet
test ! -f Advisor_Packet/SURA_Research_Update_Packet.pdf
```

**Do not commit** unless the user explicitly requests a commit.

---

## Spec coverage check

| Design requirement | Task |
|--------------------|------|
| Layout / Assets / copies | 1 |
| Research update | 2 |
| Questions | 3 |
| Repo guide + path verify | 1+4 |
| Catalog overview | 5 |
| README + audit | 6 |
| No combined PDF | 6 |
| Preserve authoritative docs | 1+6 |
| Evidence inventory | 1 |
| Visual/compile QC | 2–5 |
