# Iteration 8 Record

**Status:** H-01..03 applied; ADV-FC-ITER8-1 clean; C12 holds at 2  
**Orchestrator:** Grok

## Changes (no C12 reset)

| ID | Fix |
|----|-----|
| H-01 | ART-15 `HARD_STOP` / `HARD_STOP_RELEASE`; ART-16 cites |
| H-02 | ART-25 full `convergence_ledger` |
| H-03 | ART-21 T01–T24 PASS under R17 |
| Doc | SUMMARIES/INDEX; ART-03 mermaid human gate only |

## Adversarial

- [ADV-FC-ITER8-1](1dca4252-f152-45d2-b8bc-83470e292409): `material_new=false`; ART-15 not on reset list; C12 stands

## Next polish (MEDIUM; non-reset preferred)

1. ART-16 “HARD_STOP soft” qualifier
2. Generic `I.IntegrationAudit` (ART-24) → cite ART-11
3. Dual-field `hop_chain_ok` ↔ Q16 consistency note
4. Continue until human halt

`DESIGN_FINAL` not approved. IMPLEMENTATION_BLOCK ACTIVE.
