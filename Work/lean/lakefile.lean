import Lake
open Lake DSL

package «research» where
  moreLeanArgs := #["-Dpp.unicode.fun=true"]

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @ "v4.16.0"

@[default_target]
lean_lib «Research» where
  globs := #[.submodules `Research]
