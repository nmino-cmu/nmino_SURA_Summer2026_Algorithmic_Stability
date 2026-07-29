#!/usr/bin/env python3
"""Ship an OrderStat-Ranking alias operator end-to-end (files → e2e → PDF → registry).

Usage (from repo root, on a clean operator/<id> branch from main):
  python3 scripts/ship_orderstat_alias.py --id median --lean Median --display Median \\
    --sequence 7 --description "..."
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(cmd: list[str], **kw) -> None:
    print("+", " ".join(cmd))
    subprocess.check_call(cmd, cwd=ROOT, **kw)


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).lstrip("\n"), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--id", required=True)
    ap.add_argument("--lean", required=True)
    ap.add_argument("--display", required=True)
    ap.add_argument("--sequence", type=int, required=True)
    ap.add_argument("--description", required=True)
    ap.add_argument("--family", default="scalar_selection")
    args = ap.parse_args()

    oid = args.id
    pkg = oid.replace("-", "_")
    lean = args.lean
    thm_id = f"{oid}-margin"
    eval_m = f"{oid.upper().replace('-', '_')}_MARGIN_COMPUTATIONAL_V1"
    prop = f"{lean}MarginInvarianceProp"
    sharp = f"{lean}MarginSharpnessProp"
    thm = f"{pkg}_margin_invariance"
    thm_s = f"{pkg}_margin_sharpness"

    stmt = (
        f"Let n≥2, s∈ℤ^n, ε≥0. If every pairwise gap exceeds 2ε and ‖δ‖_∞≤ε, then for all "
        f"indices i,j: s_i < s_j iff (s+δ)_i < (s+δ)_j. ({args.display} uses this ranking core.)"
    )
    sharp_stmt = (
        "If some pair i≠j has |s_i−s_j|≤2ε, there exists ‖δ‖_∞≤ε forcing a value collision "
        "(ranking sharpness)."
    )
    formal = {
        "selection": "full_pairwise_ranking",
        "perturbation": "linf_ball",
        "gap_condition": "all_pairwise_gaps > 2*epsilon",
    }

    # Copy quantile Python and rewrite identifiers
    src = ROOT / "implementation/src/operators/quantile"
    dst = ROOT / f"implementation/src/operators/{pkg}"
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
    for p in dst.rglob("*.py"):
        t = p.read_text(encoding="utf-8")
        t = t.replace("quantile", pkg)
        t = t.replace("QUANTILE", oid.upper().replace("-", "_"))
        t = t.replace('"quantile"', f'"{oid}"')
        t = t.replace("quantile-margin", thm_id)
        t = t.replace("Quantile", lean)
        # Fix statement strings by rewriting math.py fully below
        p.write_text(t, encoding="utf-8")

    write(
        dst / "math.py",
        f'''
        """{args.display} — unique strict k-th order statistic (Mathlib R)."""

        from __future__ import annotations

        from operators.quantile.math import  # ranking ops reuse gap helpers (
            adversarial_tie,
            all_gaps_exceed,
            count_lt,
            invariance_holds,
            is_strict_kth,
            min_pairwise_gap,
            quantile_index,
        )

        OPERATOR = "{oid}"
        THEOREM_ID = "{thm_id}"
        EVALUATION_METHOD = "{eval_m}"
        THEOREM_STATEMENT = ({stmt!r})
        SHARPNESS_STATEMENT = ({sharp_stmt!r})

        __all__ = [
            "OPERATOR", "THEOREM_ID", "EVALUATION_METHOD", "THEOREM_STATEMENT", "SHARPNESS_STATEMENT",
            "is_strict_kth", "invariance_holds", "adversarial_tie", "all_gaps_exceed",
            "min_pairwise_gap", "count_lt", "quantile_index",
        ]
        ''',
    )
    # Fix verify/discovery/lean_profile/workflow/__init__ imports (already renamed by replace)
    for name in ("verify.py", "discovery.py", "lean_profile.py", "workflow.py", "__init__.py"):
        p = dst / name
        t = p.read_text(encoding="utf-8")
        t = t.replace("claim_is_quantile_margin", f"claim_is_{pkg}_margin")
        t = t.replace("verify_quantile_margin", f"verify_{pkg}_margin")
        t = t.replace("discover_quantile", f"discover_{pkg}")
        t = t.replace("run_quantile_margin_workflow", f"run_{pkg}_margin_workflow")
        t = t.replace("QUANTILE_MARGIN_COMPUTATIONAL_V1", eval_m)
        t = t.replace(f'THEOREM_STATEMENT = ({stmt!r})', "")  # noop
        # lean profile targets
        t = t.replace("QuantileMarginInvarianceProp", prop)
        t = t.replace("QuantileMarginSharpnessProp", sharp)
        t = t.replace("quantile_margin_invariance", thm)
        t = t.replace("quantile_margin_sharpness", thm_s)
        t = t.replace("Research/Operators/Quantile/Preservation.lean", f"Research/Operators/{lean}/Preservation.lean")
        t = t.replace("Research.Operators.Quantile.Preservation", f"Research.Operators.{lean}.Preservation")
        t = t.replace(f"operators/{pkg}/math.py", f"implementation/src/operators/{pkg}/math.py")
        t = t.replace('ARTLEAN.CONCL.quantile_margin.v1', f'ARTLEAN.CONCL.{pkg}_margin.v1')
        t = t.replace('"quantile"', f'"{oid}"')
        t = t.replace("quantile-margin", thm_id)
        p.write_text(t, encoding="utf-8")

    # discovery formal + claim statement from math
    disc = (dst / "discovery.py").read_text(encoding="utf-8")
    # ensure formal dict matches
    (dst / "discovery.py").write_text(disc, encoding="utf-8")

    write(
        ROOT / f"lean/Research/Operators/{lean}/Preservation.lean",
        f'''
        import Research.Operators.OrderStat.Ranking

        namespace Research.Operators.{lean}.Preservation

        open Research.Operators.OrderStat.Ranking

        /- STATEMENT_BEGIN -/
        def {prop} : Prop := RankingInvarianceProp
        def {sharp} : Prop := RankingSharpnessProp
        /- STATEMENT_END -/

        theorem {thm} : {prop} := ranking_invariance
        theorem {thm_s} : {sharp} := ranking_sharpness

        end Research.Operators.{lean}.Preservation
        ''',
    )

    # tests
    write(
        ROOT / f"implementation/tests/test_{pkg}_operator.py",
        f'''
        from operators.{pkg}.math import EVALUATION_METHOD, OPERATOR, SHARPNESS_STATEMENT, THEOREM_ID, THEOREM_STATEMENT, invariance_holds, is_strict_kth
        from operators.{pkg}.verify import verify_{pkg}_margin

        def test_strict_kth():
            scores = (1.0, 5.0, 3.0)
            assert is_strict_kth(scores, 1, 2)
            assert invariance_holds(scores, 1, 2, 0.9)

        def test_verifier():
            claim = {{
                "operator": OPERATOR, "theorem_id": THEOREM_ID, "evaluation": EVALUATION_METHOD,
                "statement": THEOREM_STATEMENT, "sharpness_statement": SHARPNESS_STATEMENT,
            }}
            vr = verify_{pkg}_margin(claim)
            assert vr.ok, (vr.detail, vr.counterexamples)
        ''',
    )
    write(
        ROOT / f"implementation/tests/lean/test_{pkg}_e2e.py",
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
        ''',
    )
    write(
        ROOT / f"implementation/docs/operators/{oid}.md",
        f"# {args.display}\\n\\nOrderStat kth-margin alias. Lean: `Research.Operators.{lean}.Preservation`.\\n",
    )

    # Wire Research.lean
    rl = ROOT / "lean/Research.lean"
    line = f"import Research.Operators.{lean}.Preservation\n"
    txt = rl.read_text(encoding="utf-8")
    if line not in txt:
        rl.write_text(txt.rstrip() + "\n" + line, encoding="utf-8")

    # Wire profiles
    prof = ROOT / "implementation/src/system_b/lean/profiles.py"
    pt = prof.read_text(encoding="utf-8")
    imp = f"from operators.{pkg} import lean_profile as {pkg}_profile\n"
    if imp not in pt:
        pt = pt.replace(
            "from operators.quantile import lean_profile as quantile_profile\n",
            "from operators.quantile import lean_profile as quantile_profile\n" + imp,
        )
        pt = pt.replace(
            "    median_profile,\n)",
            f"    median_profile,\n    {pkg}_profile,\n)",
        )
        if f"{pkg}_profile,\n" not in pt.split("_PROFILES")[1]:
            # append before closing paren of _PROFILES
            import re
            pt2 = re.sub(
                r"(_PROFILES: tuple\[ModuleType, ...\] = \(\n(?:.+\n)*?)(\))",
                rf"\1    {pkg}_profile,\n\2",
                pt,
                count=1,
            )
            if f"{pkg}_profile" in pt2:
                pt = pt2
        prof.write_text(pt, encoding="utf-8")

    # Wire engines eval + limitations
    eng = ROOT / "implementation/src/system_b/engines.py"
    et = eng.read_text(encoding="utf-8")
    if f"claim_is_{pkg}_margin" not in et:
        et = et.replace(
            "from operators.quantile.verify import claim_is_quantile_margin, verify_quantile_margin\n",
            "from operators.quantile.verify import claim_is_quantile_margin, verify_quantile_margin\n"
            f"        from operators.{pkg}.verify import claim_is_{pkg}_margin, verify_{pkg}_margin\n",
        )
        et = et.replace(
            "        if claim_is_quantile_margin(claim):\n"
            "            vr = verify_quantile_margin(claim)\n"
            "            if vr.ok:\n"
            "                return ObligationStatus.DISCHARGED, OutcomeKind.PROOF_SUCCESS, vr.detail\n"
            "            if vr.counterexamples:\n"
            "                return ObligationStatus.FAILED, OutcomeKind.COUNTEREXAMPLE, vr.detail\n"
            "            return ObligationStatus.OPEN, OutcomeKind.PROOF_INCOMPLETE, vr.detail\n",
            "        if claim_is_quantile_margin(claim):\n"
            "            vr = verify_quantile_margin(claim)\n"
            "            if vr.ok:\n"
            "                return ObligationStatus.DISCHARGED, OutcomeKind.PROOF_SUCCESS, vr.detail\n"
            "            if vr.counterexamples:\n"
            "                return ObligationStatus.FAILED, OutcomeKind.COUNTEREXAMPLE, vr.detail\n"
            "            return ObligationStatus.OPEN, OutcomeKind.PROOF_INCOMPLETE, vr.detail\n\n"
            f"        if claim_is_{pkg}_margin(claim):\n"
            f"            vr = verify_{pkg}_margin(claim)\n"
            "            if vr.ok:\n"
            "                return ObligationStatus.DISCHARGED, OutcomeKind.PROOF_SUCCESS, vr.detail\n"
            "            if vr.counterexamples:\n"
            "                return ObligationStatus.FAILED, OutcomeKind.COUNTEREXAMPLE, vr.detail\n"
            "            return ObligationStatus.OPEN, OutcomeKind.PROOF_INCOMPLETE, vr.detail\n",
        )
        marker = '                    "QUANTILE_MARGIN_COMPUTATIONAL_V1",\n                ):\n                    if lim not in run.limitations:\n                        run.limitations.append(lim)\n'
        insert = marker + f'''
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
        if f'claim.get("operator") == "{oid}"' not in et:
            et = et.replace(marker, insert)
        eng.write_text(et, encoding="utf-8")

    # Wire recompute_status
    rs = ROOT / "lean/scripts/recompute_status.py"
    rt = rs.read_text(encoding="utf-8")
    if f"{pkg}_profile" not in rt:
        rt = rt.replace(
            "from operators.quantile import lean_profile as quantile_profile  # noqa: E402\n",
            "from operators.quantile import lean_profile as quantile_profile  # noqa: E402\n"
            f"from operators.{pkg} import lean_profile as {pkg}_profile  # noqa: E402\n",
        )
        rt = rt.replace(
            '    ("quantile", "quantile-margin", quantile_profile),\n)',
            f'    ("quantile", "quantile-margin", quantile_profile),\n'
            f'    ("{oid}", "{thm_id}", {pkg}_profile),\n)',
        )
        rs.write_text(rt, encoding="utf-8")

    # Fix lean_profile EXPECTED_FORMAL and statement by rewriting key parts
    lp = dst / "lean_profile.py"
    write(
        lp,
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
                "prop_fully_qualified": "Research.Operators.{lean}.Preservation.{prop}",
                "theorem_name": "{thm}",
                "lemma_deps": [],
            }},
            {{
                "target_id": "sharpness",
                "prop_fully_qualified": "Research.Operators.{lean}.Preservation.{sharp}",
                "theorem_name": "{thm_s}",
                "lemma_deps": [],
            }},
        ]
        KNOWN_GAPS = ["DEFINITION_PINS_SURROGATE"]
        LEAN_NAMESPACE = "Research.Operators.{lean}.Preservation"
        PROP_RELATIVE = Path("Research/Operators/{lean}/Preservation.lean")
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
            Path("Research/Operators/{lean}/Preservation.lean"),
            Path("Research/Operators/OrderStat/Ranking.lean"),
            Path("Research/Operators/OrderStat/KthMargin.lean"),
            Path("Research/Operators/OrderStat/Basic.lean"),
            Path("Research/Operators/Argmax/Basic.lean"),
        )

        def claim_matches_profile(claim: dict[str, Any]) -> bool:
            return (
                claim.get("operator") == OPERATOR
                and claim.get("theorem_id") == THEOREM_ID
                and claim.get("evaluation") == EVALUATION_METHOD
                and str(claim.get("statement", "")).strip() == THEOREM_STATEMENT.strip()
            )

        def formal_matches(claim: dict[str, Any]) -> bool:
            formal = claim.get("formal") or {{}}
            return all(formal.get(k) == v for k, v in EXPECTED_FORMAL.items())
        ''',
    )
    write(
        dst / "discovery.py",
        f'''
        from __future__ import annotations
        from typing import Any
        from operators.{pkg}.math import EVALUATION_METHOD, OPERATOR, SHARPNESS_STATEMENT, THEOREM_ID, THEOREM_STATEMENT
        from system_a import engines as a_engines
        from system_a.ir import DiscoveryIR
        from system_a.ownership import CLASS_OWNER

        def discover_{pkg}(ir: DiscoveryIR) -> dict[str, Any]:
            op = a_engines.run_operator_analyzer(ir, {{"name": OPERATOR, "form": "{args.display} as strict kth", "reduction": "order_stat_ranking"}})
            instab = a_engines.run_instability_characterization(ir, op.version_ids[0])
            qty = a_engines.run_structural_quantity(ir, op.version_ids[0])
            mech = a_engines.run_mechanism(ir, qty.version_ids[0])
            psi = a_engines.run_psi_construction(ir, mech.version_ids[0])
            assum = a_engines.run_assumptions(ir, "Finite n≥2; unique strict kth; pairwise gaps; ℓ∞ perturbations.")
            claim = {{
                "statement": THEOREM_STATEMENT,
                "chain_segment": "inference",
                "operator": OPERATOR,
                "theorem_id": THEOREM_ID,
                "evaluation": EVALUATION_METHOD,
                "sharpness_statement": SHARPNESS_STATEMENT,
                "formal": {formal!r},
            }}
            tip = ir.mint(artifact_class="TheoremCandidate", caller_module=CLASS_OWNER["TheoremCandidate"], payload=claim).version_id
            sketch = a_engines.run_proof_strategy(ir, tip)
            bridge = a_engines.run_bridge(ir, tip, qty.version_ids[0])
            util = a_engines.run_utility_tradeoff(ir, [tip])
            open_q = a_engines.run_open_questions(ir, "Composition with masks.")
            cex = a_engines.run_conjecture(ir, "Pairwise gap margin is sharp via tie adversary.")
            soft = a_engines.run_soft_attack(ir, tip)
            port = a_engines.run_pareto_portfolio(ir, [tip])
            return {{
                "operator": op.version_ids[0], "instability": instab.version_ids[0], "quantity": qty.version_ids[0],
                "mechanism": mech.version_ids[0], "psi": psi.version_ids[0], "assumptions": assum.version_ids[0],
                "theorem": tip, "proof_sketch": sketch.version_ids[0], "bridge": bridge.version_ids[0],
                "utility": util.version_ids[0], "open_questions": open_q.version_ids[0],
                "sharpness_conjecture": cex.version_ids[0], "soft_attack": soft.version_ids,
                "portfolio": port.version_ids[0], "claim_payload": claim,
            }}
        ''',
    )
    write(
        dst / "verify.py",
        f'''
        from __future__ import annotations
        import random
        from dataclasses import dataclass
        from typing import Any
        from operators.{pkg}.math import (
            EVALUATION_METHOD, OPERATOR, SHARPNESS_STATEMENT, THEOREM_ID, THEOREM_STATEMENT,
            adversarial_tie, invariance_holds, is_strict_kth,
        )

        @dataclass(frozen=True)
        class VerifyResult:
            ok: bool
            detail: str
            counterexamples: tuple[dict[str, Any], ...] = ()
            limitations: tuple[str, ...] = ("COMPUTATIONAL_VERIFICATION_NOT_LEAN",)

        def claim_is_{pkg}_margin(claim: dict[str, Any]) -> bool:
            return (
                claim.get("operator") == OPERATOR
                and claim.get("theorem_id") == THEOREM_ID
                and claim.get("evaluation") == EVALUATION_METHOD
            )

        def verify_{pkg}_margin(claim: dict[str, Any]) -> VerifyResult:
            if not claim_is_{pkg}_margin(claim):
                return VerifyResult(False, "claim_mismatch")
            if str(claim.get("statement", "")).strip() != THEOREM_STATEMENT.strip():
                return VerifyResult(False, "statement_mismatch")
            if str(claim.get("sharpness_statement", "")).strip() != SHARPNESS_STATEMENT.strip():
                return VerifyResult(False, "sharpness_mismatch")
            rng = random.Random(17)
            failures: list[dict[str, Any]] = []
            for _ in range(300):
                n = rng.randint(2, 7)
                base = sorted(rng.sample(range(-20, 21), n))
                scores = tuple(float(v) for v in base)
                k = rng.randint(0, n - 1)
                order = sorted(range(n), key=lambda i: scores[i])
                i = order[k]
                assert is_strict_kth(scores, k, i)
                gap = min(abs(scores[a] - scores[b]) for a in range(n) for b in range(a + 1, n))
                eps_ok = gap / 2 - 1e-9
                if eps_ok >= 0 and not invariance_holds(scores, k, i, max(0.0, eps_ok)):
                    failures.append({{"kind": "invariance"}})
                j = order[0] if k > 0 else order[1]
                eps = abs(scores[i] - scores[j]) / 2
                br = adversarial_tie(scores, i, j, eps)
                if br is None:
                    failures.append({{"kind": "missing_break"}})
                    continue
                news = tuple(scores[t] + br[t] for t in range(n))
                if is_strict_kth(news, k, i):
                    failures.append({{"kind": "break_failed"}})
            if failures:
                return VerifyResult(False, f"failures:{{len(failures)}}", tuple(failures[:8]))
            return VerifyResult(True, "ok")
        ''',
    )
    write(
        dst / "workflow.py",
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
            session_id: str
            theorem_version_id: str
            sealed_digest: str
            crp_digest: str
            intake_status: str
            audit_verdict: str | None
            limitations: tuple[str, ...]
            obligation_statuses: tuple[str, ...]
            unresolved: tuple[str, ...]
            close_reason: str | None
            lean_bundle_path: str | None = None

        def run_{pkg}_margin_workflow(*, export_lean_bundle: bool = False) -> ResearchResult:
            orch = DiscoveryOrchestrator.create()
            orch.scope_pin = SCOPE
            orch.principal = PRINCIPAL
            for s in (State.DS01, State.DS02, State.DS03):
                orch.advance(s)
            tips = discover_{pkg}(orch.ir)
            th = tips["theorem"]
            orch.advance(State.DS05)
            orch.ir.upsert_branch("{oid}", [th])
            orch.ir.add_dep(th, tips["assumptions"], "depends")
            orch.ir.add_dep(th, tips["proof_sketch"], "depends")
            orch.advance(State.DS07); orch.advance(State.DS08)
            vid = orch.compile_portfolio_member("{oid}", "PHASE_A_CHARACTERIZATION", "{thm_id}")
            orch.advance(State.DS09)
            orch.apply_gate3(GateDecision.APPROVE, seal_set=[vid])
            snap = orch.seal_authorized(vid)
            b = VerificationIntake(SCOPE)
            out = b.submit_sealed(snap)
            eng = VerificationEngine()
            run = eng.run_from_package(crp=snap.crp, receipt=out.receipt, obligations=out.obligations)
            export = eng.export(out.receipt, out.obligations, run)
            lean_bundle_path = None
            if export_lean_bundle and out.status == IntakeStatus.ACCEPTED_DRAFT:
                bundle = export_bundle(
                    crp=snap.crp, receipt=out.receipt, run_id=run.run_id,
                    results=verification_run_to_dicts(run),
                    audit_verdict=run.audit_verdict.value if run.audit_verdict else None,
                    limitations=list(run.limitations), counterexamples=list(run.counterexamples),
                    feedback_export_digest=export.export_digest,
                )
                dest = Path(__file__).resolve().parents[3] / "artifacts" / "lean" / "bundles" / snap.crp.crp_digest / f"{{run.run_id}}.json"
                write_bundle(bundle, dest)
                lean_bundle_path = str(dest)
            orch.start_submission_batch()
            orch.record_intake(snap.sealed_digest, out.status, out.receipt.receipt_digest)
            if out.status == IntakeStatus.ACCEPTED_DRAFT:
                orch.advance(State.DS12); orch.import_feedback(export); orch.close_from_batch_outcome()
            unresolved = tuple(r.obligation_digest for r in run.results if r.status.value == "OPEN")
            return ResearchResult(
                orch.session.session_id, th, snap.sealed_digest, snap.crp.crp_digest, out.status.value,
                run.audit_verdict.value if run.audit_verdict else None, tuple(run.limitations),
                tuple(r.status.value for r in run.results), unresolved, orch.session.close_reason, lean_bundle_path,
            )
        ''',
    )
    write(
        dst / "__init__.py",
        f'''
        from operators.{pkg}.math import EVALUATION_METHOD, OPERATOR, THEOREM_ID, THEOREM_STATEMENT
        from operators.{pkg}.verify import claim_is_{pkg}_margin, verify_{pkg}_margin
        from operators.{pkg}.workflow import run_{pkg}_margin_workflow
        __all__ = ["EVALUATION_METHOD", "OPERATOR", "THEOREM_ID", "THEOREM_STATEMENT",
                   "claim_is_{pkg}_margin", "verify_{pkg}_margin", "run_{pkg}_margin_workflow"]
        ''',
    )

    print(json.dumps({"operator": oid, "pkg": pkg, "lean": lean, "theorem_id": thm_id}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
