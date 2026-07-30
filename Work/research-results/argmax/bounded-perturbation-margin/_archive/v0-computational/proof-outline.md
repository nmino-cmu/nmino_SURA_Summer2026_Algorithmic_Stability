# Proof outline — bounded perturbation margin

1. **Setup.** Unique \(i^\star\), \(\gamma(s)>0\), \(\|\delta\|_\infty\le\varepsilon\).
2. **Lemma (worst-case gap).** \((s+\delta)_{i^\star}-(s+\delta)_j \ge s_{i^\star}-s_j-2\varepsilon \ge \gamma-2\varepsilon\).
3. **Theorem.** If \(\gamma>2\varepsilon\), all gaps stay strictly positive ⇒ unique maximizer preserved.
4. **Sharpness.** \(\delta_{i^\star}=-\varepsilon\), \(\delta_{j^\star}=+\varepsilon\) yields gap \(\gamma-2\varepsilon\le 0\).

Repository discharge: exact claim string match + formal fields + fixtures + adversarial sharpness + randomized trials (`verify.py`).
