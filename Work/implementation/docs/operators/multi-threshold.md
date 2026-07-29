# Operator: multi-threshold

## Operator

\[
C_{\mathbf{T}}(x)=\bigl|\{i:x\ge T_i\}\bigr|
\]

Finite score \(x\), finite threshold list \(\mathbf{T}=(T_0,\ldots,T_{n-1})\).
Equality passes per coordinate (same convention as Threshold).

## Stability quantity

Coordinatewise buffers: every cut must lie outside its half-open unstable band
\([T_i-\varepsilon,T_i+\varepsilon)\).

## Theorems

Primary: if all coordinates are \(\varepsilon\)-stable and \(|x'-x|\le\varepsilon\), then
\(C_{\mathbf{T}}(x')=C_{\mathbf{T}}(x)\).

Sharpness: a single unstable cut admits an admissible flip of the singleton count.

## Reduction

Coordinatewise Threshold preservation (`Research.Operators.Threshold.Preservation`).

## Implementation

| Piece | Path |
|-------|------|
| Math | `implementation/src/operators/multi_threshold/math.py` |
| Lean | `lean/Research/Operators/MultiThreshold/Preservation.lean` |
| Certificate | `lean/certificates/multi-threshold/multi-threshold-count-preservation/` |
