# Assumptions and Open Decisions

## Recorded assumptions (nonblocking)

1. `DiscoverySlice` remains SessionEvent-embedded (not a taxonomy class).  
2. Verifier ART-04e stays unmodified; ART-A-04e is A-implementer extension until a human gate updates verifier roster.  
3. Engine stub markdown (NOV/ATP/MECH/CONJ) remains descriptive; A-05 is the invocation execution norm.  
4. Commits for architecture docs are permitted on `main`.  
5. No production runtime in this pass.  
6. ART-A-08 cases are formally enumerated, not a machine-readable manifest.

## Genuine open decisions (nonblocking)

1. When/whether human gate should promote ART-A-04e roles into verifier ART-04e.  
2. Storage technology for session IR (file/DB) — intentionally unspecified.  
3. Whether same-session DS12→DS05 continue is enabled by default SessionPolicy (default false per S-A04-POLICY).

## Blocking defects

None outstanding after 2026-07-25b adversarial repair (see FINAL_AUDIT).
