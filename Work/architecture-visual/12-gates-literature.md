# 12 — Human gates & literature

**Normative / partial:** `ART-15` human gates · `architecture/14-literature/LITERATURE_BOUNDARY.md`

## Plain English

Humans approve the scary transitions. Literature stays quarantined until provenance is attached. Gate IDs ≠ audit verdicts (`ESCALATE_HUMAN` is not a gate).

---

## Gate families

```mermaid
flowchart TB
  subgraph Scope["Scope / notions"]
    SC[SCOPE_CHANGE]
    ST[STABILITY_NOTION_CHANGE]
    NB[NEIGHBOR_CHANGE]
  end
  subgraph Data["Data / ψ"]
    DP[DATA_DEP_PSI]
    CL[CONTINUOUS_LAMBDA]
  end
  subgraph Promo["Promotion-ish"]
    ITC[INFERENCE_THEOREM_CLAIM]
    NOV[PLAUSIBLE_NOVELTY_LABEL]
  end
  subgraph Control["Control"]
    HS[HARD_STOP]
    HSR[HARD_STOP_RELEASE]
    DF[DESIGN_FINAL]
    IS[IMPLEMENTATION_START]
    RE[RESEARCH_EXECUTION_START]
  end
  subgraph Ops["Ops"]
    RE2[ROLE_EXPANSION]
    OV[OVERRIDE_EIO]
  end
```

---

## Decision shape

```mermaid
flowchart LR
  U["HumanDecisionUnsigned<br/>gate_id + target_digest"] --> D["decision_digest"]
  D --> Sig["signature detached"]
  Sig --> Commit["RECORD_HUMAN_DECISION"]
```

---

## Literature boundary

```mermaid
flowchart TD
  Lit["External literature"] --> Q["Quarantine"]
  Q --> Prov["Provenance + IMPORTED_RESULT_REGISTER"]
  Prov --> Claim["Claim usable in research"]
```
