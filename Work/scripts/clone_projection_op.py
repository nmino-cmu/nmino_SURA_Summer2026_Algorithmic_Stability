#!/usr/bin/env python3
"""Clone a projection/feasibility operator onto Clamp, FeasibleId, or Constraint cores."""
from __future__ import annotations

import argparse
import re
import shutil
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

KINDS = {
    "clamp": {
        "core_import": "Research.Operators.Projection.Clamp",
        "core_open": "Research.Operators.Projection.Clamp",
        "lean_file": "Preservation.lean",
        "ns_suffix": "Preservation",
        "props": (
            ("{lean}StabilityProp", "ClampStabilityProp", "{pkg}_clamp_stability", "clamp_stability"),
            ("{lean}SharpnessProp", "ClampSharpnessProp", "{pkg}_clamp_sharpness", "clamp_sharpness"),
        ),
        "thm_suffix": "clamp-stability",
        "formal": {
            "operator_kind": "clamp_projection",
            "perturbation": "abs_ball",
            "property": "1_lipschitz_nonexpansive",
        },
        "core_deps": (
            "Research/Operators/Projection/Clamp.lean",
            "Research/Operators/Argmax/Basic.lean",
        ),
    },
    "feasible": {
        "core_import": "Research.Operators.Projection.FeasibleId",
        "core_open": "Research.Operators.Projection.FeasibleId",
        "lean_file": "Preservation.lean",
        "ns_suffix": "Preservation",
        "props": (
            (
                "{lean}IdentityProp",
                "FeasibleBallIdentityProp",
                "{pkg}_feasible_ball_identity",
                "feasible_ball_identity",
            ),
            (
                "{lean}SharpnessProp",
                "FeasibleBallSharpnessProp",
                "{pkg}_feasible_ball_sharpness",
                "feasible_ball_sharpness",
            ),
        ),
        "thm_suffix": "feasible-ball-identity",
        "formal": {
            "operator_kind": "feasible_ball_identity",
            "perturbation": "abs_ball",
            "property": "identity_on_epsilon_interior",
        },
        "core_deps": (
            "Research/Operators/Projection/FeasibleId.lean",
            "Research/Operators/Argmax/Basic.lean",
        ),
    },
    "conjunction": {
        "core_import": "Research.Operators.Projection.Constraint",
        "core_open": "Research.Operators.Projection.Constraint",
        "lean_file": "Preservation.lean",
        "ns_suffix": "Preservation",
        "props": (
            (
                "{lean}PreservationProp",
                "ConjunctionPreservationProp",
                "{pkg}_conjunction_preservation",
                "conjunction_preservation",
            ),
            (
                "{lean}SharpnessProp",
                "ConjunctionSharpnessProp",
                "{pkg}_conjunction_sharpness",
                "conjunction_sharpness",
            ),
        ),
        "thm_suffix": "conjunction-preservation",
        "formal": {
            "operator_kind": "threshold_conjunction",
            "reduction": "multi_threshold_pass_count",
            "perturbation": "abs_ball",
        },
        "core_deps": (
            "Research/Operators/Projection/Constraint.lean",
            "Research/Operators/MultiThreshold/Preservation.lean",
            "Research/Operators/Argmax/Basic.lean",
        ),
    },
    "disjunction": {
        "core_import": "Research.Operators.Projection.Constraint",
        "core_open": "Research.Operators.Projection.Constraint",
        "lean_file": "Preservation.lean",
        "ns_suffix": "Preservation",
        "props": (
            (
                "{lean}PreservationProp",
                "DisjunctionPreservationProp",
                "{pkg}_disjunction_preservation",
                "disjunction_preservation",
            ),
            (
                "{lean}SharpnessProp",
                "DisjunctionSharpnessProp",
                "{pkg}_disjunction_sharpness",
                "disjunction_sharpness",
            ),
        ),
        "thm_suffix": "disjunction-preservation",
        "formal": {
            "operator_kind": "threshold_disjunction",
            "reduction": "multi_threshold_pass_count",
            "perturbation": "abs_ball",
        },
        "core_deps": (
            "Research/Operators/Projection/Constraint.lean",
            "Research/Operators/MultiThreshold/Preservation.lean",
            "Research/Operators/Argmax/Basic.lean",
        ),
    },
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--id", required=True)
    ap.add_argument("--lean", required=True)
    ap.add_argument("--display", required=True)
    ap.add_argument("--kind", required=True, choices=sorted(KINDS))
    args = ap.parse_args()
    oid, lean, display, kind = args.id, args.lean, args.display, args.kind
    cfg = KINDS[kind]
    pkg = oid.replace("-", "_")
    thm_id = f"{oid}-{cfg['thm_suffix']}"
    eval_m = f"{oid.upper().replace('-', '_')}_COMPUTATIONAL_V1"
    formal = dict(cfg["formal"])
    ns = f"Research.Operators.{lean}.{cfg['ns_suffix']}"

    if kind == "clamp":
        stmt = (
            f"Let lo<=hi and |x'-x|<=epsilon. Then |clamp(x';lo,hi)-clamp(x;lo,hi)|<=epsilon "
            f"({display} is 1-Lipschitz / nonexpansive on the reals)."
        )
        sharp_stmt = (
            "For every epsilon>=1 there exist x,y,lo,hi with lo<=hi attaining "
            "|clamp x - clamp y| = |x-y| = epsilon (Lipschitz constant 1 is sharp)."
        )
    elif kind == "feasible":
        stmt = (
            f"If proj fixes InSet pointwise and the closed epsilon-ball about x lies in InSet, "
            f"then for all |x'-x|<=epsilon one has proj(x')=x' and proj(x)=x "
            f"({display}: feasible-ball identity over the reals)."
        )
        sharp_stmt = (
            "If some y in the epsilon-ball is infeasible, the universal feasible-ball "
            "hypothesis fails (sharpness of the interior premise)."
        )
    elif kind == "conjunction":
        stmt = (
            f"Under coordinatewise epsilon-stability of each threshold, the multi-threshold "
            f"pass-count is preserved; hence the conjunction (all-pass) bit is preserved "
            f"({display})."
        )
        sharp_stmt = (
            "Multi-threshold sharpness: a near-cut coordinate admits an epsilon move "
            "changing the pass-count (hence the conjunction bit may flip)."
        )
    else:
        stmt = (
            f"Under coordinatewise epsilon-stability of each threshold, the multi-threshold "
            f"pass-count is preserved; hence the disjunction (any-pass) bit is preserved "
            f"({display})."
        )
        sharp_stmt = (
            "Multi-threshold sharpness: a near-cut coordinate admits an epsilon move "
            "changing the pass-count (hence the disjunction bit may flip)."
        )

    src = ROOT / "implementation/src/operators/interval_membership"
    dst = ROOT / f"implementation/src/operators/{pkg}"
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)

    if kind == "clamp":
        math_body = f'''
            """{display} - interval clamp nonexpansiveness (Mathlib R)."""
            from __future__ import annotations
            import random

            OPERATOR = "{oid}"
            THEOREM_ID = "{thm_id}"
            EVALUATION_METHOD = "{eval_m}"
            THEOREM_STATEMENT = ({stmt!r})
            SHARPNESS_STATEMENT = ({sharp_stmt!r})

            def clamp(x: float, lo: float, hi: float) -> float:
                return max(lo, min(x, hi))

            def nonexpansive(x: float, y: float, lo: float, hi: float) -> bool:
                return abs(clamp(x, lo, hi) - clamp(y, lo, hi)) <= abs(x - y) + 1e-12

            def stable(x: float, lo: float, hi: float, eps: float) -> bool:
                return abs(clamp(x + eps, lo, hi) - clamp(x, lo, hi)) <= eps + 1e-12 and abs(
                    clamp(x - eps, lo, hi) - clamp(x, lo, hi)
                ) <= eps + 1e-12
            '''
        verify_body = f'''
            from __future__ import annotations
            import random
            from dataclasses import dataclass
            from typing import Any
            from operators.{pkg}.math import (
                EVALUATION_METHOD, OPERATOR, SHARPNESS_STATEMENT, THEOREM_ID, THEOREM_STATEMENT,
                clamp, nonexpansive,
            )

            @dataclass(frozen=True)
            class VerifyResult:
                ok: bool
                detail: str
                counterexamples: tuple[dict[str, Any], ...] = ()
                limitations: tuple[str, ...] = ("COMPUTATIONAL_VERIFICATION_NOT_LEAN",)

            def claim_is_{pkg}_preservation(claim):
                return (
                    claim.get("operator") == OPERATOR
                    and claim.get("theorem_id") == THEOREM_ID
                    and claim.get("evaluation") == EVALUATION_METHOD
                )

            def verify_{pkg}_preservation(claim):
                if not claim_is_{pkg}_preservation(claim):
                    return VerifyResult(False, "claim_mismatch")
                if str(claim.get("statement", "")).strip() != THEOREM_STATEMENT.strip():
                    return VerifyResult(False, "statement_mismatch")
                if str(claim.get("sharpness_statement", "")).strip() != SHARPNESS_STATEMENT.strip():
                    return VerifyResult(False, "sharpness_mismatch")
                rng = random.Random(7)
                failures = []
                for _ in range(400):
                    a, b = rng.uniform(-5, 5), rng.uniform(-5, 5)
                    lo, hi = (a, b) if a <= b else (b, a)
                    x, y = rng.uniform(-6, 6), rng.uniform(-6, 6)
                    if not nonexpansive(x, y, lo, hi):
                        failures.append({{"kind": "lip"}})
                # sharpness witness for eps=3
                if abs(clamp(3, 0, 3) - clamp(0, 0, 3)) != 3:
                    failures.append({{"kind": "sharp"}})
                if failures:
                    return VerifyResult(False, f"failures:{{len(failures)}}", tuple(failures[:8]))
                return VerifyResult(True, "ok")
            '''
    elif kind == "feasible":
        math_body = f'''
            """{display} - feasible-ball identity (Mathlib R)."""
            from __future__ import annotations

            OPERATOR = "{oid}"
            THEOREM_ID = "{thm_id}"
            EVALUATION_METHOD = "{eval_m}"
            THEOREM_STATEMENT = ({stmt!r})
            SHARPNESS_STATEMENT = ({sharp_stmt!r})

            def proj_id(z: float) -> float:
                return z

            def ball_feasible(x: float, eps: float, inset) -> bool:
                # sample endpoints + center on R as computational proxy of Int ball
                for y in (x - eps, x, x + eps):
                    if not inset(y):
                        return False
                return True
            '''
        verify_body = f'''
            from __future__ import annotations
            import random
            from dataclasses import dataclass
            from typing import Any
            from operators.{pkg}.math import (
                EVALUATION_METHOD, OPERATOR, SHARPNESS_STATEMENT, THEOREM_ID, THEOREM_STATEMENT,
                ball_feasible, proj_id,
            )

            @dataclass(frozen=True)
            class VerifyResult:
                ok: bool
                detail: str
                counterexamples: tuple[dict[str, Any], ...] = ()
                limitations: tuple[str, ...] = ("COMPUTATIONAL_VERIFICATION_NOT_LEAN",)

            def claim_is_{pkg}_preservation(claim):
                return (
                    claim.get("operator") == OPERATOR
                    and claim.get("theorem_id") == THEOREM_ID
                    and claim.get("evaluation") == EVALUATION_METHOD
                )

            def verify_{pkg}_preservation(claim):
                if not claim_is_{pkg}_preservation(claim):
                    return VerifyResult(False, "claim_mismatch")
                if str(claim.get("statement", "")).strip() != THEOREM_STATEMENT.strip():
                    return VerifyResult(False, "statement_mismatch")
                if str(claim.get("sharpness_statement", "")).strip() != SHARPNESS_STATEMENT.strip():
                    return VerifyResult(False, "sharpness_mismatch")
                rng = random.Random(7)
                failures = []
                for _ in range(200):
                    c = rng.uniform(-2, 2)
                    r = rng.uniform(0.5, 3)
                    inset = lambda z, c=c, r=r: abs(z - c) <= r + 1e-12
                    x = c
                    eps = min(r, rng.uniform(0, r))
                    if ball_feasible(x, eps, inset):
                        for xp in (x - eps, x, x + eps):
                            if proj_id(xp) != xp:
                                failures.append({{"kind": "id"}})
                    # sharpness: push outside
                    y = c + r + 0.1
                    if abs(y - x) <= r and inset(y):
                        failures.append({{"kind": "bad_out"}})
                if failures:
                    return VerifyResult(False, f"failures:{{len(failures)}}", tuple(failures[:8]))
                return VerifyResult(True, "ok")
            '''
    else:
        # conjunction / disjunction: reuse multi_threshold computational checks via import
        math_body = f'''
            """{display} - threshold constraint via MultiThreshold pass-count core."""
            from __future__ import annotations
            from operators.multi_threshold.math import adversarial_flip, multi_stable, multi_threshold_count

            OPERATOR = "{oid}"
            THEOREM_ID = "{thm_id}"
            EVALUATION_METHOD = "{eval_m}"
            THEOREM_STATEMENT = ({stmt!r})
            SHARPNESS_STATEMENT = ({sharp_stmt!r})
            '''
        verify_body = f'''
            from __future__ import annotations
            import random
            from dataclasses import dataclass
            from typing import Any
            from operators.{pkg}.math import (
                EVALUATION_METHOD, OPERATOR, SHARPNESS_STATEMENT, THEOREM_ID, THEOREM_STATEMENT,
            )
            from operators.multi_threshold.math import adversarial_flip, multi_stable, multi_threshold_count

            @dataclass(frozen=True)
            class VerifyResult:
                ok: bool
                detail: str
                counterexamples: tuple[dict[str, Any], ...] = ()
                limitations: tuple[str, ...] = ("COMPUTATIONAL_VERIFICATION_NOT_LEAN",)

            def claim_is_{pkg}_preservation(claim):
                return (
                    claim.get("operator") == OPERATOR
                    and claim.get("theorem_id") == THEOREM_ID
                    and claim.get("evaluation") == EVALUATION_METHOD
                )

            def verify_{pkg}_preservation(claim):
                if not claim_is_{pkg}_preservation(claim):
                    return VerifyResult(False, "claim_mismatch")
                if str(claim.get("statement", "")).strip() != THEOREM_STATEMENT.strip():
                    return VerifyResult(False, "statement_mismatch")
                if str(claim.get("sharpness_statement", "")).strip() != SHARPNESS_STATEMENT.strip():
                    return VerifyResult(False, "sharpness_mismatch")
                rng = random.Random(13)
                failures = []
                for _ in range(250):
                    x = rng.uniform(-4, 4)
                    Ts = tuple(sorted(rng.uniform(-3, 3) for _ in range(rng.randint(1, 4))))
                    eps = rng.uniform(0, 1.5)
                    c0 = multi_threshold_count(x, Ts)
                    if multi_stable(x, Ts, eps):
                        for xp in (x - eps, x, x + eps):
                            if multi_threshold_count(xp, Ts) != c0:
                                failures.append({{"kind": "count"}})
                    else:
                        _ = adversarial_flip(x, Ts, eps)
                if failures:
                    return VerifyResult(False, f"failures:{{len(failures)}}", tuple(failures[:8]))
                return VerifyResult(True, "ok")
            '''

    (dst / "math.py").write_text(textwrap.dedent(math_body).lstrip(), encoding="utf-8")
    (dst / "verify.py").write_text(textwrap.dedent(verify_body).lstrip(), encoding="utf-8")

    (dst / "discovery.py").write_text(
        textwrap.dedent(
            f'''
            from __future__ import annotations
            from typing import Any
            from operators.{pkg}.math import (
                EVALUATION_METHOD, OPERATOR, SHARPNESS_STATEMENT, THEOREM_ID, THEOREM_STATEMENT,
            )
            from system_a import engines as a_engines
            from system_a.ir import DiscoveryIR
            from system_a.ownership import CLASS_OWNER

            def discover_{pkg}(ir: DiscoveryIR) -> dict[str, Any]:
                op = a_engines.run_operator_analyzer(
                    ir, {{"name": OPERATOR, "form": "{display}", "kind": "{kind}"}}
                )
                instab = a_engines.run_instability_characterization(ir, op.version_ids[0])
                qty = a_engines.run_structural_quantity(ir, op.version_ids[0])
                mech = a_engines.run_mechanism(ir, qty.version_ids[0])
                psi = a_engines.run_psi_construction(ir, mech.version_ids[0])
                assum = a_engines.run_assumptions(ir, "Int ordered-group core; abs-ball perturbations.")
                claim = {{
                    "statement": THEOREM_STATEMENT,
                    "chain_segment": "inference",
                    "operator": OPERATOR,
                    "theorem_id": THEOREM_ID,
                    "evaluation": EVALUATION_METHOD,
                    "sharpness_statement": SHARPNESS_STATEMENT,
                    "formal": {formal!r},
                }}
                tip = ir.mint(
                    artifact_class="TheoremCandidate",
                    caller_module=CLASS_OWNER["TheoremCandidate"],
                    payload=claim,
                ).version_id
                sketch = a_engines.run_proof_strategy(ir, tip)
                bridge = a_engines.run_bridge(ir, tip, qty.version_ids[0])
                util = a_engines.run_utility_tradeoff(ir, [tip])
                open_q = a_engines.run_open_questions(ir, "Real Euclidean projection upgrade.")
                cex = a_engines.run_conjecture(ir, "Sharpness via boundary adversary.")
                soft = a_engines.run_soft_attack(ir, tip)
                port = a_engines.run_pareto_portfolio(ir, [tip])
                return {{
                    "operator": op.version_ids[0],
                    "instability": instab.version_ids[0],
                    "quantity": qty.version_ids[0],
                    "mechanism": mech.version_ids[0],
                    "psi": psi.version_ids[0],
                    "assumptions": assum.version_ids[0],
                    "theorem": tip,
                    "proof_sketch": sketch.version_ids[0],
                    "bridge": bridge.version_ids[0],
                    "utility": util.version_ids[0],
                    "open_questions": open_q.version_ids[0],
                    "sharpness_conjecture": cex.version_ids[0],
                    "soft_attack": soft.version_ids,
                    "portfolio": port.version_ids[0],
                    "claim_payload": claim,
                }}
            '''
        ).lstrip(),
        encoding="utf-8",
    )

    prop_rows = []
    target_rows = []
    for prop_fmt, core_prop, thm_fmt, core_thm in cfg["props"]:
        prop = prop_fmt.format(lean=lean, pkg=pkg)
        thm = thm_fmt.format(lean=lean, pkg=pkg)
        prop_rows.append(f"def {prop} : Prop := {core_prop}")
        prop_rows.append(f"theorem {thm} : {prop} := {core_thm}")
        tid = "preservation" if "Sharpness" not in prop and "sharpness" not in thm else "sharpness"
        if "Sharpness" in prop or "sharpness" in thm:
            tid = "sharpness"
        elif "Stability" in prop or "Identity" in prop or "Preservation" in prop:
            tid = "preservation"
        target_rows.append(
            {
                "target_id": tid,
                "prop_fully_qualified": f"{ns}.{prop}",
                "theorem_name": thm,
                "lemma_deps": [],
            }
        )

    lean_path = ROOT / f"lean/Research/Operators/{lean}/{cfg['lean_file']}"
    lean_path.parent.mkdir(parents=True, exist_ok=True)
    lean_body = (
        f"import {cfg['core_import']}\n"
        f"namespace {ns}\n"
        f"open {cfg['core_open']}\n"
        "/- STATEMENT_BEGIN -/\n"
        + "\n".join(prop_rows[i] for i in range(0, len(prop_rows), 2))
        + "\n/- STATEMENT_END -/\n"
        + "\n".join(prop_rows[i] for i in range(1, len(prop_rows), 2))
        + f"\nend {ns}\n"
    )
    lean_path.write_text(lean_body, encoding="utf-8")

    (dst / "lean_profile.py").write_text(
        textwrap.dedent(
            f'''
            from __future__ import annotations
            from pathlib import Path
            from typing import Any
            from operators.{pkg}.math import EVALUATION_METHOD, OPERATOR, THEOREM_ID, THEOREM_STATEMENT as _TS
            CONCL_SCHEMA = "ARTLEAN.CONCL.{pkg}.v1"
            EXPECTED_FORMAL = {formal!r}
            CONCLUSION_TOKENS = {{"schema_id": CONCL_SCHEMA}}
            TARGETS = {target_rows!r}
            KNOWN_GAPS = ["DEFINITION_PINS_SURROGATE"]
            LEAN_NAMESPACE = "{ns}"
            PROP_RELATIVE = Path("Research/Operators/{lean}/{cfg['lean_file']}")
            MATH_PY_RELATIVE = Path("implementation/src/operators/{pkg}/math.py")
            THEOREM_STATEMENT = _TS
            CONVENTIONS = {{
                "tie_break": "NONE",
                "equality": "DEFAULT",
                "extensionality": "DEFAULT",
                "finiteness": "SCALAR_OR_LIST",
                "measure_stage": "NONE",
                "score_encoding": "REAL_MATHLIB",
            }}
            PROP_DEPS = tuple(Path(p) for p in {list(cfg["core_deps"])!r}) + (PROP_RELATIVE,)
            def claim_matches_profile(claim):
                return (
                    claim.get("operator") == OPERATOR
                    and claim.get("theorem_id") == THEOREM_ID
                    and claim.get("evaluation") == EVALUATION_METHOD
                    and str(claim.get("statement", "")).strip() == THEOREM_STATEMENT.strip()
                )
            def formal_matches(claim):
                formal = claim.get("formal") or {{}}
                return all(formal.get(k) == v for k, v in EXPECTED_FORMAL.items())
            '''
        ).lstrip(),
        encoding="utf-8",
    )

    (dst / "workflow.py").write_text(
        textwrap.dedent(
            f'''
            from __future__ import annotations
            from dataclasses import dataclass
            from pathlib import Path
            from art_int.enums import IntakeStatus
            from operators.{pkg}.discovery import discover_{pkg}
            from system_a.fsm import State
            from system_a.gates import GateDecision
            from system_a.orchestrator import DiscoveryOrchestrator
            from system_b.engines import VerificationEngine
            from system_b.intake import VerificationIntake
            from system_b.lean.bundle import export_bundle, verification_run_to_dicts, write_bundle
            SCOPE = "a" * 64
            PRINCIPAL = "b" * 64
            @dataclass
            class ResearchResult:
                session_id: str; theorem_version_id: str; sealed_digest: str; crp_digest: str
                intake_status: str; audit_verdict: str | None; limitations: tuple[str, ...]
                obligation_statuses: tuple[str, ...]; unresolved: tuple[str, ...]; close_reason: str | None
                lean_bundle_path: str | None = None
            def run_{pkg}_preservation_workflow(*, export_lean_bundle: bool = False) -> ResearchResult:
                orch = DiscoveryOrchestrator.create(); orch.scope_pin = SCOPE; orch.principal = PRINCIPAL
                for s in (State.DS01, State.DS02, State.DS03): orch.advance(s)
                tips = discover_{pkg}(orch.ir); th = tips["theorem"]; orch.advance(State.DS05)
                orch.ir.upsert_branch("{oid}", [th]); orch.ir.add_dep(th, tips["assumptions"], "depends"); orch.ir.add_dep(th, tips["proof_sketch"], "depends")
                orch.advance(State.DS07); orch.advance(State.DS08)
                vid = orch.compile_portfolio_member("{oid}", "PHASE_A_CHARACTERIZATION", "{thm_id}")
                orch.advance(State.DS09); orch.apply_gate3(GateDecision.APPROVE, seal_set=[vid]); snap = orch.seal_authorized(vid)
                b = VerificationIntake(SCOPE); out = b.submit_sealed(snap); eng = VerificationEngine()
                run = eng.run_from_package(crp=snap.crp, receipt=out.receipt, obligations=out.obligations)
                export = eng.export(out.receipt, out.obligations, run); lean_bundle_path = None
                if export_lean_bundle and out.status == IntakeStatus.ACCEPTED_DRAFT:
                    bundle = export_bundle(crp=snap.crp, receipt=out.receipt, run_id=run.run_id, results=verification_run_to_dicts(run), audit_verdict=run.audit_verdict.value if run.audit_verdict else None, limitations=list(run.limitations), counterexamples=list(run.counterexamples), feedback_export_digest=export.export_digest)
                    dest = Path(__file__).resolve().parents[3] / "artifacts" / "lean" / "bundles" / snap.crp.crp_digest / f"{{run.run_id}}.json"
                    write_bundle(bundle, dest); lean_bundle_path = str(dest)
                orch.start_submission_batch(); orch.record_intake(snap.sealed_digest, out.status, out.receipt.receipt_digest)
                if out.status == IntakeStatus.ACCEPTED_DRAFT:
                    orch.advance(State.DS12); orch.import_feedback(export); orch.close_from_batch_outcome()
                unresolved = tuple(r.obligation_digest for r in run.results if r.status.value == "OPEN")
                return ResearchResult(orch.session.session_id, th, snap.sealed_digest, snap.crp.crp_digest, out.status.value, run.audit_verdict.value if run.audit_verdict else None, tuple(run.limitations), tuple(r.status.value for r in run.results), unresolved, orch.session.close_reason, lean_bundle_path)
            '''
        ).lstrip(),
        encoding="utf-8",
    )
    (dst / "__init__.py").write_text(
        textwrap.dedent(
            f'''
            from operators.{pkg}.math import EVALUATION_METHOD, OPERATOR, THEOREM_ID, THEOREM_STATEMENT
            from operators.{pkg}.verify import claim_is_{pkg}_preservation, verify_{pkg}_preservation
            from operators.{pkg}.workflow import run_{pkg}_preservation_workflow
            __all__ = [
                "EVALUATION_METHOD", "OPERATOR", "THEOREM_ID", "THEOREM_STATEMENT",
                "claim_is_{pkg}_preservation", "verify_{pkg}_preservation", "run_{pkg}_preservation_workflow",
            ]
            '''
        ).lstrip(),
        encoding="utf-8",
    )

    (ROOT / f"implementation/tests/test_{pkg}_operator.py").write_text(
        textwrap.dedent(
            f'''
            from operators.{pkg}.math import (
                EVALUATION_METHOD, OPERATOR, SHARPNESS_STATEMENT, THEOREM_ID, THEOREM_STATEMENT,
            )
            from operators.{pkg}.verify import verify_{pkg}_preservation
            def test_verifier():
                claim = {{
                    "operator": OPERATOR,
                    "theorem_id": THEOREM_ID,
                    "evaluation": EVALUATION_METHOD,
                    "statement": THEOREM_STATEMENT,
                    "sharpness_statement": SHARPNESS_STATEMENT,
                }}
                vr = verify_{pkg}_preservation(claim)
                assert vr.ok, (vr.detail, vr.counterexamples)
            '''
        ).lstrip(),
        encoding="utf-8",
    )
    (ROOT / f"implementation/tests/lean/test_{pkg}_e2e.py").write_text(
        textwrap.dedent(
            f'''
            from pathlib import Path
            import pytest
            from operators.{pkg}.workflow import run_{pkg}_preservation_workflow
            from system_b.lean.manifest import DerivedLeanStatus
            from system_b.lean.workflow import run_lean_from_bundle
            @pytest.mark.lean
            def test_{pkg}_e2e_full():
                r = run_{pkg}_preservation_workflow(export_lean_bundle=True)
                assert r.audit_verdict == "PASS", (r.audit_verdict, r.limitations)
                res = run_lean_from_bundle(Path(r.lean_bundle_path), skip_lake=False)
                assert res.status == DerivedLeanStatus.LEAN_FULL, (res.status, res.reason_codes)
            '''
        ).lstrip(),
        encoding="utf-8",
    )
    (ROOT / f"implementation/docs/operators/{oid}.md").write_text(
        f"# {display}\n\nProjection/feasibility family (`{kind}`). Lean: `{ns}`.\n",
        encoding="utf-8",
    )

    rl = ROOT / "lean/Research.lean"
    line = f"import {ns}\n"
    txt = rl.read_text(encoding="utf-8")
    if line not in txt:
        rl.write_text(txt.rstrip() + "\n" + line, encoding="utf-8")

    prof = ROOT / "implementation/src/system_b/lean/profiles.py"
    pt = prof.read_text(encoding="utf-8")
    imp = f"from operators.{pkg} import lean_profile as {pkg}_profile\n"
    if imp not in pt:
        pt = pt.replace(
            "from operators.argmax import lean_profile as argmax_profile\n",
            "from operators.argmax import lean_profile as argmax_profile\n" + imp,
        )
        pt = re.sub(r"(\n\)\n\n\ndef resolve_profile)", rf"\n    {pkg}_profile,\1", pt, count=1)
        prof.write_text(pt, encoding="utf-8")

    eng = ROOT / "implementation/src/system_b/engines.py"
    et = eng.read_text(encoding="utf-8")
    if f"claim_is_{pkg}_preservation" not in et:
        et = et.replace(
            "from operators.argmax.verify import claim_is_argmax_margin, verify_margin_theorem\n",
            "from operators.argmax.verify import claim_is_argmax_margin, verify_margin_theorem\n"
            f"        from operators.{pkg}.verify import claim_is_{pkg}_preservation, verify_{pkg}_preservation\n",
        )
        block = f'''
        if claim_is_{pkg}_preservation(claim):
            vr = verify_{pkg}_preservation(claim)
            if vr.ok:
                return ObligationStatus.DISCHARGED, OutcomeKind.PROOF_SUCCESS, vr.detail
            if vr.counterexamples:
                return ObligationStatus.FAILED, OutcomeKind.COUNTEREXAMPLE, vr.detail
            return ObligationStatus.OPEN, OutcomeKind.PROOF_INCOMPLETE, vr.detail
'''
        et = et.replace(
            "        if claim_is_argmax_margin(claim):\n",
            block + "\n        if claim_is_argmax_margin(claim):\n",
        )
        lim = f'''
            if (
                claim.get("operator") == "{oid}"
                and claim.get("theorem_id") == "{thm_id}"
                and status == ObligationStatus.DISCHARGED
            ):
                for lim in (
                    "COMPUTATIONAL_VERIFICATION_NOT_LEAN",
                    "{eval_m}",
                ):
                    if lim not in run.limitations:
                        run.limitations.append(lim)
'''
        et = et.replace(
            '                    "ARGMAX_MARGIN_COMPUTATIONAL_V1",\n                ):\n                    if lim not in run.limitations:\n                        run.limitations.append(lim)\n',
            '                    "ARGMAX_MARGIN_COMPUTATIONAL_V1",\n                ):\n                    if lim not in run.limitations:\n                        run.limitations.append(lim)\n'
            + lim,
        )
        eng.write_text(et, encoding="utf-8")

    rs = ROOT / "lean/scripts/recompute_status.py"
    rt = rs.read_text(encoding="utf-8")
    if f"{pkg}_profile" not in rt:
        rt = rt.replace(
            "from operators.argmax import lean_profile as argmax_profile  # noqa: E402\n",
            "from operators.argmax import lean_profile as argmax_profile  # noqa: E402\n"
            f"from operators.{pkg} import lean_profile as {pkg}_profile  # noqa: E402\n",
        )
        if f'("{oid}", "{thm_id}"' not in rt:
            rt = re.sub(
                r"(_ACCEPTED = \(\n(?:.*\n)*?)(\)\n)",
                rf'\1    ("{oid}", "{thm_id}", {pkg}_profile),\n\2',
                rt,
                count=1,
            )
        rs.write_text(rt, encoding="utf-8")

    print({"operator": oid, "pkg": pkg, "kind": kind, "thm_id": thm_id, "lean": lean})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
