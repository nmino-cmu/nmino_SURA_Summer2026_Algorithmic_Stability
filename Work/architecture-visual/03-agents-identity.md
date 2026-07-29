# 03 — Agents, identity, operable minimal

**Normative:** `ART-04c` identity · `ART-04d` operable binding  
**Appendix:** `ART-04b` profile prose · `AGENT_ROLES.md` labels

## Plain English

Every write has a **principal** and a **role binding**. Day-1 only a small roster can act; extras need triggers or a `ROLE_EXPANSION` human gate.

---

## Day-1 roster

```mermaid
flowchart TB
  subgraph Day1B["Day-1 B roles"]
    VO[VERIFICATION_ORCHESTRATOR]
    PP[PROOF_PROPOSER]
    PC[PROOF_CERTIFIER]
    CA[COUNTEREXAMPLE_ATTACKER]
    IA[INTEGRATION_AUDITOR]
    EIO[EIO]
    HG[HUMAN_GATE_OPERATOR]
    CT[COMMITTER]
  end

  subgraph Day1A["A roles (no B Commit)"]
    DO[DISCOVERY_ORCHESTRATOR]
    FS[FRONTIER_SCHEDULER]
  end

  subgraph Cond["Conditional"]
    LA[LITERATURE_ANALYST]
    LV[LEAN_VERIFIER]
    RS[RESEARCH_SCOPE]
  end

  Day1B --> Ceiling["I.RoleCeiling"]
  Cond -->|only with trigger| Ceiling
  Ceiling -->|fail| RC["ROLE_CEILING"]
```

**Hard rule:** proposer ≠ certifier (same principal cannot wear both live).

---

## Auth path

```mermaid
sequenceDiagram
  participant P as Principal
  participant B as RoleBinding
  participant C as I.Commit

  P->>B: live binding at event_seq
  B->>C: caller_principal + caller_binding
  C->>C: I-CMD-AUTH + RoleCeiling
  alt MODEL_RUNTIME
    C->>C: model_prov from binding
  end
```

---

## Identity objects

```mermaid
flowchart LR
  TR[TrustRoot] --> Prin[Principal]
  Prin --> Atom[IndependenceAtom]
  Prin --> Bind[RoleBinding]
  Bind --> MP[ModelProvenanceRecord]
  HD[HumanDecision] --> Prin
```
