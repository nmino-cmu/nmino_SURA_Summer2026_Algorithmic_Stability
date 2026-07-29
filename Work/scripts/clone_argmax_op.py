#!/usr/bin/env python3
"""Clone Argmax-margin reduction operator package and wire profiles/engines/recompute."""
from __future__ import annotations

import argparse
import re
import shutil
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--id", required=True)
    ap.add_argument("--lean", required=True)
    ap.add_argument("--display", required=True)
    ap.add_argument(
        "--score-construction",
        default="finite scores with unique maximizer",
    )
    args = ap.parse_args()
    oid, lean, display = args.id, args.lean, args.display
    pkg = oid.replace("-", "_")
    thm_id = f"{oid}-margin"
    eval_m = f"{oid.upper().replace('-', '_')}_MARGIN_COMPUTATIONAL_V1"
    prop = f"{lean}MarginInvarianceProp"
    sharp = f"{lean}MarginSharpnessProp"
    thm = f"{pkg}_margin_invariance"
    thm_s = f"{pkg}_margin_sharpness"
    stmt = (
        f"Let m>=2 and let scores be constructed by ({args.score_construction}). "
        f"If i* is the unique maximizer with margin gamma>2*epsilon and ||delta||_inf<=epsilon, "
        f"then i* remains the unique maximizer after perturbation "
        f"({display} reduces to Argmax margin)."
    )
    sharp_stmt = (
        "If gamma<=2*epsilon with unique maximizer i*, some ||delta||_inf<=epsilon "
        "destroys uniqueness of i* (Argmax margin sharpness)."
    )
    formal = {
        "reduction": "argmax_margin",
        "perturbation": "linf_ball",
        "margin_condition": "gamma > 2*epsilon",
    }

    src = ROOT / "implementation/src/operators/top_k"
    dst = ROOT / f"implementation/src/operators/{pkg}"
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)

    (dst / "math.py").write_text(
        textwrap.dedent(
            f'''
            """{display} - unique-max Argmax-margin reduction (Mathlib R)."""
            from __future__ import annotations
            from operators.argmax.math import ArgmaxInstance, adversarial_break, invariance_holds

            OPERATOR = "{oid}"
            THEOREM_ID = "{thm_id}"
            EVALUATION_METHOD = "{eval_m}"
            THEOREM_STATEMENT = ({stmt!r})
            SHARPNESS_STATEMENT = ({sharp_stmt!r})

            def select_winner(scores):
                return ArgmaxInstance(scores).unique_maximizer()

            def stable(scores, epsilon):
                return invariance_holds(scores, epsilon)
            '''
        ).lstrip(),
        encoding="utf-8",
    )
    (dst / "verify.py").write_text(
        textwrap.dedent(
            f'''
            from __future__ import annotations
            import random
            from dataclasses import dataclass
            from typing import Any
            from operators.{pkg}.math import (
                EVALUATION_METHOD, OPERATOR, SHARPNESS_STATEMENT, THEOREM_ID, THEOREM_STATEMENT,
            )
            from operators.argmax.math import adversarial_break, invariance_holds

            @dataclass(frozen=True)
            class VerifyResult:
                ok: bool
                detail: str
                counterexamples: tuple[dict[str, Any], ...] = ()
                limitations: tuple[str, ...] = ("COMPUTATIONAL_VERIFICATION_NOT_LEAN",)

            def claim_is_{pkg}_margin(claim):
                return (
                    claim.get("operator")==OPERATOR
                    and claim.get("theorem_id")==THEOREM_ID
                    and claim.get("evaluation")==EVALUATION_METHOD
                )

            def verify_{pkg}_margin(claim):
                if not claim_is_{pkg}_margin(claim):
                    return VerifyResult(False, "claim_mismatch")
                if str(claim.get("statement", "")).strip() != THEOREM_STATEMENT.strip():
                    return VerifyResult(False, "statement_mismatch")
                if str(claim.get("sharpness_statement", "")).strip() != SHARPNESS_STATEMENT.strip():
                    return VerifyResult(False, "sharpness_mismatch")
                rng = random.Random(19)
                failures = []
                for _ in range(250):
                    m = rng.randint(2, 7)
                    scores = tuple(float(v) for v in rng.sample(range(-20, 21), m))
                    if len(set(scores)) < m:
                        continue
                    top = max(scores)
                    if scores.count(top) != 1:
                        continue
                    gamma = top - max(v for v in scores if v != top)
                    eps_ok = max(0.0, gamma / 2 - 1e-9)
                    if invariance_holds(scores, eps_ok) is False:
                        failures.append({{"kind": "inv"}})
                    br = adversarial_break(scores, gamma / 2)
                    if br is None:
                        failures.append({{"kind": "miss"}})
                        continue
                    news = tuple(scores[t] + br[t] for t in range(m))
                    if news.count(max(news)) == 1 and news.index(max(news)) == scores.index(top):
                        failures.append({{"kind": "nobreak"}})
                if failures:
                    return VerifyResult(False, f"failures:{{len(failures)}}", tuple(failures[:8]))
                return VerifyResult(True, "ok")
            '''
        ).lstrip(),
        encoding="utf-8",
    )
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
                    ir,
                    {{"name": OPERATOR, "form": "{display} via Argmax margin", "reduction": "argmax_margin"}},
                )
                instab = a_engines.run_instability_characterization(ir, op.version_ids[0])
                qty = a_engines.run_structural_quantity(ir, op.version_ids[0])
                mech = a_engines.run_mechanism(ir, qty.version_ids[0])
                psi = a_engines.run_psi_construction(ir, mech.version_ids[0])
                assum = a_engines.run_assumptions(
                    ir, "Finite m>=2; unique maximizer; ell_inf perturbations; Argmax reduction."
                )
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
                open_q = a_engines.run_open_questions(ir, "Composition with masks and filters.")
                cex = a_engines.run_conjecture(ir, "Argmax margin sharp via rival lift adversary.")
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
    (dst / "lean_profile.py").write_text(
        textwrap.dedent(
            f'''
            from __future__ import annotations
            from pathlib import Path
            from typing import Any
            from operators.{pkg}.math import EVALUATION_METHOD, OPERATOR, THEOREM_ID, THEOREM_STATEMENT as _TS
            CONCL_SCHEMA = "ARTLEAN.CONCL.{pkg}_margin.v1"
            EXPECTED_FORMAL = {formal!r}
            CONCLUSION_TOKENS = {{"schema_id": CONCL_SCHEMA}}
            TARGETS = [
              {{
                "target_id": "preservation",
                "prop_fully_qualified": "Research.Operators.{lean}.Margin.{prop}",
                "theorem_name": "{thm}",
                "lemma_deps": [],
              }},
              {{
                "target_id": "sharpness",
                "prop_fully_qualified": "Research.Operators.{lean}.Margin.{sharp}",
                "theorem_name": "{thm_s}",
                "lemma_deps": [],
              }},
            ]
            KNOWN_GAPS = ["DEFINITION_PINS_SURROGATE"]
            LEAN_NAMESPACE = "Research.Operators.{lean}.Margin"
            PROP_RELATIVE = Path("Research/Operators/{lean}/Margin.lean")
            MATH_PY_RELATIVE = Path("implementation/src/operators/{pkg}/math.py")
            THEOREM_STATEMENT = _TS
            CONVENTIONS = {{
                "tie_break": "UNIQUE_REQUIRED",
                "equality": "DEFAULT",
                "extensionality": "DEFAULT",
                "finiteness": "FINITE_VECTOR",
                "measure_stage": "NONE",
                "score_encoding": "REAL_MATHLIB",
            }}
            PROP_DEPS = (
                Path("Research/Operators/{lean}/Margin.lean"),
                Path("Research/Operators/Argmax/Margin.lean"),
                Path("Research/Operators/Argmax/Basic.lean"),
            )
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
            def run_{pkg}_margin_workflow(*, export_lean_bundle: bool = False) -> ResearchResult:
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
            from operators.{pkg}.verify import claim_is_{pkg}_margin, verify_{pkg}_margin
            from operators.{pkg}.workflow import run_{pkg}_margin_workflow
            __all__ = [
                "EVALUATION_METHOD", "OPERATOR", "THEOREM_ID", "THEOREM_STATEMENT",
                "claim_is_{pkg}_margin", "verify_{pkg}_margin", "run_{pkg}_margin_workflow",
            ]
            '''
        ).lstrip(),
        encoding="utf-8",
    )

    lean_path = ROOT / f"lean/Research/Operators/{lean}/Margin.lean"
    lean_path.parent.mkdir(parents=True, exist_ok=True)
    lean_path.write_text(
        textwrap.dedent(
            f'''
            import Research.Operators.Argmax.Margin
            namespace Research.Operators.{lean}.Margin
            open Research.Operators.Argmax.Margin
            /- STATEMENT_BEGIN -/
            def {prop} : Prop := MarginInvarianceProp
            def {sharp} : Prop := MarginSharpnessProp
            /- STATEMENT_END -/
            theorem {thm} : {prop} := margin_invariance
            theorem {thm_s} : {sharp} := margin_sharpness
            end Research.Operators.{lean}.Margin
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
            from operators.{pkg}.verify import verify_{pkg}_margin
            def test_verifier():
                claim = {{
                    "operator": OPERATOR,
                    "theorem_id": THEOREM_ID,
                    "evaluation": EVALUATION_METHOD,
                    "statement": THEOREM_STATEMENT,
                    "sharpness_statement": SHARPNESS_STATEMENT,
                }}
                vr = verify_{pkg}_margin(claim)
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
            from operators.{pkg}.workflow import run_{pkg}_margin_workflow
            from system_b.lean.manifest import DerivedLeanStatus
            from system_b.lean.workflow import run_lean_from_bundle
            @pytest.mark.lean
            def test_{pkg}_e2e_full():
                r = run_{pkg}_margin_workflow(export_lean_bundle=True)
                assert r.audit_verdict == "PASS", (r.audit_verdict, r.limitations)
                res = run_lean_from_bundle(Path(r.lean_bundle_path), skip_lake=False)
                assert res.status == DerivedLeanStatus.LEAN_FULL, (res.status, res.reason_codes)
            '''
        ).lstrip(),
        encoding="utf-8",
    )
    (ROOT / f"implementation/docs/operators/{oid}.md").write_text(
        f"# {display}\n\nArgmax-margin reduction. Lean: `Research.Operators.{lean}.Margin`.\n",
        encoding="utf-8",
    )

    rl = ROOT / "lean/Research.lean"
    line = f"import Research.Operators.{lean}.Margin\n"
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
        if imp not in pt:
            pt = "from __future__ import annotations\n" + imp + pt
        pt = re.sub(r"(\n\)\n\n\ndef resolve_profile)", rf"\n    {pkg}_profile,\1", pt, count=1)
        prof.write_text(pt, encoding="utf-8")

    eng = ROOT / "implementation/src/system_b/engines.py"
    et = eng.read_text(encoding="utf-8")
    if f"claim_is_{pkg}_margin" not in et:
        et = et.replace(
            "from operators.argmax.verify import claim_is_argmax_margin, verify_margin_theorem\n",
            "from operators.argmax.verify import claim_is_argmax_margin, verify_margin_theorem\n"
            f"        from operators.{pkg}.verify import claim_is_{pkg}_margin, verify_{pkg}_margin\n",
        )
        block = f'''
        if claim_is_{pkg}_margin(claim):
            vr = verify_{pkg}_margin(claim)
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
        # Append before closing of _ACCEPTED (robust to extra trailing entries).
        if f'("{oid}", "{thm_id}"' not in rt:
            rt = re.sub(
                r"(_ACCEPTED = \(\n(?:.*\n)*?)(\)\n)",
                rf'\1    ("{oid}", "{thm_id}", {pkg}_profile),\n\2',
                rt,
                count=1,
            )
        rs.write_text(rt, encoding="utf-8")

    print({"operator": oid, "pkg": pkg, "lean": lean})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
