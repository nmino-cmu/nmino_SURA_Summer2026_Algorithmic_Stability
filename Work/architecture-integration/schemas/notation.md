# Interface-facing mathematical notation (ART-INT)

**Authority:** ART-INT-00. Applies to CRP payload, ProofObligation statements, and VerifierFeedbackExport math fields. Internal A/B scratch may differ if translated at pack/export.

| Symbol | Interface meaning | Forbidden alternate at boundary |
|--------|-------------------|--------------------------------|
| \(D\) | Dataset | Decision / design state |
| \(D\sim D'\) | Neighboring datasets (ART-02 pin) | Arbitrary adjacency without pin |
| \(\Lambda\) | Finite candidate set | Continuous \(\Lambda\) without gate |
| \(F_D(\lambda)\) | Score / objective | Generic loss without pin |
| \(\hat\lambda(D)\) | Unperturbed selector | |
| \(\tilde\lambda(D;\xi)\) | Perturbed selector | |
| \(\xi\sim Q_\psi\) | Perturbation law / mechanism | Use only when mechanism present |
| \(S_D(\lambda)\) | Selected object | Session / state |
| \(\pi\) | Policy (when object_class=POLICY) | Probability measure (use \(P\) / \(\mathbb{P}\)) |
| \(\mathbb{P}\), \(\mathbb{E}\) | Probability / expectation | |
| \(\varepsilon\) | Typed approximation / privacy budget **only if** schema field names the kind | Ambiguous bare \(\varepsilon\) |
| \(\delta\) | Typed failure probability / perturbation size **only if** schema field names the kind | Ambiguous bare \(\delta\) |
| \(A\) | **Do not use** bare at boundary | Prefer `algorithm_id` / `operator_digest` |
| \(P\) | Population / law only if typed; else avoid | Proposition (use claim text) |

**I-INT-N01:** Every CRP claim MUST bind `definition_pins` / scope digests so symbols resolve.  
**I-INT-N02:** Mechanism-free Phase A packages MUST NOT require \(Q_\psi\) symbols in required fields.
