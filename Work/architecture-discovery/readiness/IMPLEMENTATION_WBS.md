# Implementation Work Breakdown

## Required core

1. Session store implementing ART-A-04 schemas + A-02 ownership enforcement  
2. Discovery Orchestrator FSM (ART-A-03)  
3. DiscoverySlice scheduler (A-03/A-05)  
4. CRP_PACKAGER compile + A-06 projection  
5. Seal + SubmissionAttempt + I.DiscoverySubmit client  
6. Gate packet UI/API for Gates 1–3 + SessionPolicy  
7. Frontier Scheduler binding (ART-08b + DS02)  
8. Soft Attack + engine adapters behind A-05 envelope  

## Optional extensions

- Richer literature graph UX  
- Parallel compile workers  
- Same-session continue after DS12  

## Test infrastructure

- Conformance harness for ART-A-08 CF-A-* and TR-A-01…14  
- Fixtures for DraftCRP / CompileError / seal_set  

## Migration work

- ART-08 → A-03 session adapter (A-07)  
- Document LEGACY_CYCLE_INTAKE coexistence  

## Documentation work

- Keep readiness INDEX current  
- Operator runbooks for gates  

## Out of scope this architecture pass

Production model weights; B implementation; editing `architecture_verifier/`.
