# Proof outline — bounded-noise threshold

1. Assume \(\lvert\xi\rvert\le\eta\) a.s.
2. Parts (1)–(2): apply deterministic preservation pathwise with \(\varepsilon=\eta\).
3. Part (3) / sharpness: two-point law on \(\{\pm\eta\}\) realizes both outputs on the unstable band (existential over laws, not “every realization”).
4. Laplace closed form checked at \(m\in\{0,\pm\ln 2\}\) — utility only, not DP.

Discharge: `verify_bounded_noise_threshold` + formal `not_claimed: full_sparse_vector_privacy`.
