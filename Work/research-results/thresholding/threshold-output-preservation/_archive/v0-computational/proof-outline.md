# Proof outline — threshold output preservation

1. **Setup.** Finite \(x,T\); \(\varepsilon\ge 0\); \(A_T(x)=\mathbf{1}\{x\ge T\}\).
2. **Lemma.** Admissible \(x'\) fill \([x-\varepsilon,x+\varepsilon]\).
3. **Pass.** \(x\ge T+\varepsilon\Rightarrow x-\varepsilon\ge T\Rightarrow A_T\equiv 1\).
4. **Fail.** \(x<T-\varepsilon\Rightarrow x+\varepsilon<T\Rightarrow A_T\equiv 0\).
5. **Unstable / sharpness.** Band \([T-\varepsilon,T+\varepsilon)\); adversary \(x\pm\varepsilon\); note \(x=T+\varepsilon\) still pass-safe, \(x=T-\varepsilon\) not fail-safe.

Discharge: claim string + formal fields + boundary fixtures + property trials (`verify.py`).
