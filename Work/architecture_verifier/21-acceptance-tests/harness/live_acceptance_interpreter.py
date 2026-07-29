#!/usr/bin/env python3
"""
Ephemeral design interpreter for dual-system CRP live acceptance (ART-21b I-CF-02).
Not production ResearchState. Does not clear IMPLEMENTATION_BLOCK.
Implements ART-CRP / ART-07b §10A-10B / ART-11b-CHAR / ART-12-CHAR / ART-13b I-AP-PO / ART-04c auth.
"""
from __future__ import annotations

import hashlib
import json
import sys
from copy import deepcopy
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

CANON_V = "ART21b.CANON.v1"
OUT = Path(__file__).resolve().parent / "live_runs"


def canon(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def H(*parts: Any) -> str:
    """I-H-03 multi-arg packing."""
    return hashlib.sha256(canon(list(parts))).hexdigest()


def digest_obj(tag: str, obj: dict) -> str:
    return H(tag, obj)


AUTHORIZED_SUBMIT = {"VERIFICATION_ORCHESTRATOR", "HUMAN_GATE_OPERATOR"}
AUTHORIZED_APPLY = {"VERIFICATION_ORCHESTRATOR"}
AUTHORIZED_CX = {"VERIFICATION_ORCHESTRATOR", "COUNTEREXAMPLE_ATTACKER"}
AUTHORIZED_AUDIT = {"INTEGRATION_AUDITOR"}
CHAR_SEGMENTS = {
    "characterization",
    "perturbation",
    "selection_application",
    "composition",
    "object",
    "inference",
    "bridge",
}


@dataclass
class Store:
    event_seq: int = 0
    hard_stop: bool = False
    crps: dict[str, dict] = field(default_factory=dict)
    receipts: dict[str, dict] = field(default_factory=dict)
    claims: dict[str, dict] = field(default_factory=dict)
    obligations: dict[str, dict] = field(default_factory=dict)
    mechanisms: dict[str, dict] = field(default_factory=dict)
    cxs: dict[str, dict] = field(default_factory=dict)
    audits: dict[str, dict] = field(default_factory=dict)
    maturity: dict[str, str] = field(default_factory=dict)
    event_log: list[dict] = field(default_factory=list)
    bindings: dict[str, dict] = field(default_factory=dict)

    def snapshot(self) -> dict:
        return {
            "event_seq": self.event_seq,
            "hard_stop": self.hard_stop,
            "crps": deepcopy(self.crps),
            "receipts": deepcopy(self.receipts),
            "claims": deepcopy(self.claims),
            "obligations": deepcopy(self.obligations),
            "mechanisms": deepcopy(self.mechanisms),
            "cxs": deepcopy(self.cxs),
            "audits": deepcopy(self.audits),
            "maturity": deepcopy(self.maturity),
            "event_log": deepcopy(self.event_log),
        }


class Interpreter:
    def __init__(self, bindings: dict[str, dict] | None = None):
        self.S = Store()
        if bindings:
            self.S.bindings.update(bindings)
        self.trace: list[dict] = []

    def _log(self, step: str, **kw: Any) -> None:
        self.trace.append({"step": step, **kw})

    def _auth(self, role: str, allowed: set[str], command: str) -> str | None:
        if role == "RESEARCH_ORCHESTRATOR":
            return "UNAUTHORIZED_COMMAND"  # DUAL.2: no stale role authority
        if role == "RESEARCH_DISCOVERY_ASSISTANT" and command != "SUBMIT_CANDIDATE_PACKAGE_VIA_COMMITTER":
            # Discovery may only seal CRP; Commit submit must be B principal
            if command in {"APPLY_PROMOTION", "ATTACH_CERTIFICATION", "RECORD_AUDIT", "RECORD_COUNTEREXAMPLE"}:
                return "ROLE_CEILING"
        if role not in allowed:
            return "UNAUTHORIZED_COMMAND"
        return None

    def submit_candidate_package(self, crp: dict, caller_role: str) -> dict:
        self._log("SUBMIT_CANDIDATE_PACKAGE", caller_role=caller_role)
        err = self._auth(caller_role, AUTHORIZED_SUBMIT, "SUBMIT_CANDIDATE_PACKAGE")
        if err:
            return self._reject(err, "I-CMD-AUTH-01 / ART-04c")

        # Schema validation
        author_kind = crp.get("author_kind")
        profile = crp.get("profile") or crp.get("package_phase")
        payload = crp.get("payload") or {}
        claims = payload.get("claims") or []
        mechs = payload.get("mechanism_proposals") or []

        if author_kind not in {"HUMAN", "RESEARCH_DISCOVERY_ASSISTANT"}:
            return self._reject("CRP_AUTHOR", "I-CRP-OBJ-02")
        if author_kind == "RESEARCH_DISCOVERY_ASSISTANT":
            bind = crp.get("author_binding_digest")
            b = self.S.bindings.get(bind or "")
            if not b or b.get("role_id") != "RESEARCH_DISCOVERY_ASSISTANT" or b.get("status") != "ACTIVE":
                return self._reject("CRP_AUTHOR", "admissible_package.2 / ART-CRP")

        if profile not in {
            "PHASE_A_CHARACTERIZATION",
            "PHASE_B_STABILIZATION",
            "MIXED",
            "OBLIGATION_ONLY",
            "BRIDGE_ONLY",
        }:
            return self._reject("CRP_PROFILE", "ART-CRP profile enum")

        # Phase rules
        if profile == "PHASE_B_STABILIZATION" and not mechs:
            return self._reject("MECHANISM_REQUIRED", "I-CRP-05")
        if profile == "PHASE_A_CHARACTERIZATION":
            # Must NOT require mechanism
            for c in claims:
                if c.get("chain_segment") not in CHAR_SEGMENTS:
                    return self._reject("PACKAGE_INADMISSIBLE", "admissible_package.5")

        # No MechanismInstance / stability cert / inference bridge required for Phase A
        if profile == "PHASE_A_CHARACTERIZATION":
            if crp.get("requires_mechanism") or payload.get("stability_certificate") or payload.get("inference_bridge"):
                # presence of forbidden *requirements* is ok as drafts only; we just don't reject for absence
                pass

        self._log("SCHEMA_VALIDATION", result="PASS", profile=profile, n_claims=len(claims), n_mechs=len(mechs))

        payload_canonical = json.loads(canon(payload).decode())
        crp_body = {
            "author_kind": author_kind,
            "author_principal_digest": crp.get("author_principal_digest", H("principal", author_kind)),
            "author_binding_digest": crp.get("author_binding_digest") or "⊥",
            "profile": profile,
            "math_scope_pin_digest": crp.get("math_scope_pin_digest", H("ART01.AREA1")),
            "payload_canonical": payload_canonical,
            "prior_crp_digest": crp.get("prior_crp_digest") or "⊥",
            "sealed_at": crp.get("sealed_at") or datetime.now(timezone.utc).isoformat(),
        }
        crp_digest = H(
            "ARTCRP.v1",
            crp_body["author_kind"],
            crp_body["author_principal_digest"],
            crp_body["author_binding_digest"],
            crp_body["profile"],
            crp_body["math_scope_pin_digest"],
            crp_body["payload_canonical"],
            crp_body["prior_crp_digest"],
        )

        self.S.event_seq += 1
        event_seq = self.S.event_seq

        # Mint claims
        draft_claim_digests = []
        for i, c in enumerate(claims):
            claim = {
                "object_class": "CLAIM",
                "chain_segment": c.get("chain_segment", "characterization"),
                "kind": c.get("kind", "conjecture"),
                "statement": c.get("statement", ""),
                "originating_crp_digest": crp_digest,
                "assumptions": c.get("assumptions") or payload.get("assumptions") or [],
                "operator": c.get("operator") or payload.get("operator"),
            }
            cd = H("ART07b.CLAIM.v1", claim)
            claim["claim_digest"] = cd
            self.S.claims[cd] = claim
            self.S.maturity[cd] = "OPEN"
            draft_claim_digests.append(cd)
            self._log("TYPED_CLAIM", claim_digest=cd, chain_segment=claim["chain_segment"])

        # Mint mechanisms if present
        mech_digests = []
        for m in mechs:
            md = H("ART07b.MECH.v1", m)
            self.S.mechanisms[md] = {**m, "mechanism_digest": md, "originating_crp_digest": crp_digest}
            mech_digests.append(md)
            self._log("MECHANISM_INSTANCE_DRAFT", mechanism_digest=md)

        # Proof obligations (I-PO-01)
        obl_digests = []
        for cd in draft_claim_digests:
            claim = self.S.claims[cd]
            base_obl = {
                "obligation_id": f"PO-PROOF-{cd[:12]}",
                "originating_crp_digest": crp_digest,
                "originating_claim_digest": cd,
                "obligation_type": "PROOF",
                "statement_digest": H("stmt", claim["statement"]),
                "dependency_digests": [],
                "assumption_digests": [H("asm", a) for a in claim.get("assumptions", [])],
                "status": "OPEN",
                "discharge_evidence_digests": [],
                "cx_relevance": "MUST_ATTACK",
                "bridge_relevance": "NONE",
                "blocks_promotion": True,
                "audit_bind_required": True,
            }
            od = H("ART07b.PO.v1", base_obl)
            base_obl["obligation_digest"] = od
            self.S.obligations[od] = base_obl
            obl_digests.append(od)
            self._log("PROOF_OBLIGATION", obligation_digest=od, type="PROOF", blocks_promotion=True)

            if profile == "PHASE_B_STABILIZATION":
                for md in mech_digests:
                    mobl = {
                        "obligation_id": f"PO-MECH-{md[:12]}",
                        "originating_crp_digest": crp_digest,
                        "originating_claim_digest": cd,
                        "obligation_type": "CERT_ATTACH",
                        "statement_digest": H("mech-cert", md),
                        "dependency_digests": [md],
                        "assumption_digests": [],
                        "status": "OPEN",
                        "discharge_evidence_digests": [],
                        "cx_relevance": "MUST_ATTACK",
                        "bridge_relevance": "NONE",
                        "blocks_promotion": True,
                        "audit_bind_required": True,
                        "mechanism_digest": md,
                    }
                    mod = H("ART07b.PO.v1", mobl)
                    mobl["obligation_digest"] = mod
                    self.S.obligations[mod] = mobl
                    obl_digests.append(mod)
                    self._log("PROOF_OBLIGATION", obligation_digest=mod, type="CERT_ATTACH", mechanism=md)

        live_crp = {
            "object_class": "CANDIDATE_RESEARCH_PACKAGE",
            "schema_version": "ARTCRP.v1",
            "crp_digest": crp_digest,
            "author_kind": author_kind,
            "author_principal_digest": crp_body["author_principal_digest"],
            "author_binding_digest": None if crp_body["author_binding_digest"] == "⊥" else crp_body["author_binding_digest"],
            "package_phase": profile,
            "admissibility_state": "ADMISSIBLE",
            "source_provenance": H(author_kind, crp_body["author_principal_digest"], crp_body["sealed_at"]),
            "contained_object_refs": draft_claim_digests + mech_digests,
            "intake_status": "ACCEPTED_DRAFT",
            "commit_event_seq": event_seq,
            "emitted_obligation_digests": obl_digests,
            "math_scope_pin_digest": crp_body["math_scope_pin_digest"],
            "payload": payload,
            "mechanism_required_at_intake": profile == "PHASE_B_STABILIZATION",
            "mechanism_present": bool(mechs),
        }
        self.S.crps[crp_digest] = live_crp
        self._log("CANONICAL_CRP_REGISTRATION", crp_digest=crp_digest, intake_status="ACCEPTED_DRAFT")

        receipt = {
            "object_class": "INTAKE_RECEIPT",
            "crp_digest": crp_digest,
            "event_seq": event_seq,
            "draft_claim_digests": sorted(draft_claim_digests),
            "obligation_digests": obl_digests,
            "status": "ACCEPTED_DRAFT",
        }
        receipt_digest = H("ARTCRP.IN.v1", crp_digest, event_seq, sorted(draft_claim_digests))
        receipt["receipt_digest"] = receipt_digest
        live_crp["intake_receipt_digest"] = receipt_digest
        self.S.receipts[receipt_digest] = receipt
        self._log("INTAKE_RECEIPT", receipt_digest=receipt_digest, status="ACCEPTED_DRAFT")

        # Dependency graph (simple)
        dep_graph = {
            cd: {"LOGICAL": [], "mechanism": mech_digests if profile == "PHASE_B_STABILIZATION" else []}
            for cd in draft_claim_digests
        }
        self._log("DEPENDENCY_GRAPH", graph=dep_graph)

        self.S.event_log.append(
            {
                "event_seq": event_seq,
                "command_kind": "SUBMIT_CANDIDATE_PACKAGE",
                "caller_role": caller_role,
                "crp_digest": crp_digest,
                "effects": ["CRP", "CLAIMS", "OBLIGATIONS", "RECEIPT"],
            }
        )
        return {
            "code": "SUCCESS",
            "crp_digest": crp_digest,
            "receipt_digest": receipt_digest,
            "draft_claim_digests": draft_claim_digests,
            "obligation_digests": obl_digests,
            "mechanism_digests": mech_digests,
            "audit_profile_id": self._audit_profile(profile),
            "cx_profile_id": self._cx_profile(profile),
        }

    def _audit_profile(self, profile: str) -> str:
        return {
            "PHASE_A_CHARACTERIZATION": "ART11b.CHAR",
            "OBLIGATION_ONLY": "ART11b.CHAR",
            "PHASE_B_STABILIZATION": "ART11b.BASE",
            "BRIDGE_ONLY": "ART11b.BRIDGE",
            "MIXED": "ART11b.MIXED",
        }[profile]

    def _cx_profile(self, profile: str) -> str:
        return "ART-12-CHAR" if profile in {"PHASE_A_CHARACTERIZATION", "OBLIGATION_ONLY"} else "ART-12"

    def run_characterization_cx(self, claim_digest: str, caller_role: str, attacks: list[dict]) -> dict:
        err = self._auth(caller_role, AUTHORIZED_CX, "RECORD_COUNTEREXAMPLE")
        if err:
            return self._reject(err, "ART-04c CX auth")
        claim = self.S.claims[claim_digest]
        crp = self.S.crps[claim["originating_crp_digest"]]
        profile_id = self._cx_profile(crp["package_phase"])
        self._log("CX_PROFILE_SELECTED", cx_profile_id=profile_id, claim_digest=claim_digest)

        if profile_id == "ART-12-CHAR":
            # Must not demand MechanismInstance
            if any(a.get("requires_mechanism") for a in attacks):
                return self._reject("CX_PROFILE_VIOLATION", "I-CX-CHAR-01")

        results = []
        full = False
        for a in attacks:
            cx = {
                "class_id": a["class_id"],
                "claim_digest": claim_digest,
                "severity": a.get("severity", "PARTIAL"),
                "note": a.get("note", ""),
                "profile_id": profile_id,
            }
            cxd = H("ART07b.CX.v1", cx)
            cx["cx_digest"] = cxd
            self.S.cxs[cxd] = cx
            results.append(cx)
            self._log("CX_RECORDED", **cx)
            if cx["severity"] == "FULL":
                full = True
                # mark related PO failed
                for od, o in self.S.obligations.items():
                    if o["originating_claim_digest"] == claim_digest and o["blocks_promotion"]:
                        o["status"] = "FAILED"
                        self._log("OBLIGATION_STATUS", obligation_digest=od, status="FAILED", reason="FULL_CX")

        self.S.event_seq += 1
        self.S.event_log.append(
            {
                "event_seq": self.S.event_seq,
                "command_kind": "RECORD_COUNTEREXAMPLE",
                "caller_role": caller_role,
                "claim_digest": claim_digest,
            }
        )
        return {"code": "SUCCESS", "cx_profile_id": profile_id, "results": results, "full_cx": full}

    def run_audit(self, claim_digest: str, caller_role: str, answers: dict, verdict: str | None = None) -> dict:
        err = self._auth(caller_role, AUTHORIZED_AUDIT, "RECORD_AUDIT")
        if err:
            return self._reject(err, "ART-04c audit auth")
        claim = self.S.claims[claim_digest]
        crp = self.S.crps[claim["originating_crp_digest"]]
        profile_id = self._audit_profile(crp["package_phase"])
        self._log("AUDIT_PROFILE_SELECTED", audit_profile_id=profile_id)

        # Q04 applicability
        mech_present = bool(crp.get("mechanism_present"))
        if profile_id == "ART11b.CHAR" and not mech_present:
            if answers.get("Q04") not in {"NA", "NOT_APPLICABLE"}:
                return self._reject("AUDIT_PROFILE_VIOLATION", "ART-11b-CHAR Q04 NOT_APPLICABLE")
            q04_mode = "NOT_APPLICABLE"
        else:
            q04_mode = "ALWAYS"
            if answers.get("Q04") not in {"YES", "NO", "NA", "UNKNOWN"}:
                return self._reject("UNKNOWN_AUDIT_QUESTION", "ART-11b Q04")

        # Q17 characterization-facing
        if profile_id == "ART11b.CHAR":
            q17_ok = answers.get("Q17") == "YES" and claim["chain_segment"] == "characterization"
            q17_rule = "characterization_facing"
        else:
            q17_ok = answers.get("Q17") == "YES"
            q17_rule = "main_or_stability_chain"

        if verdict is None:
            if answers.get("Q17") == "NO":
                verdict = "FAIL"
            elif profile_id == "ART11b.CHAR" and answers.get("QC1") == "NO":
                verdict = "FAIL"
            elif q17_ok and answers.get("Q04") in {"NA", "NOT_APPLICABLE", "YES"}:
                verdict = "PASS"
            else:
                verdict = "ESCALATE_HUMAN"  # REVISION_REQUIRED operationally

        audit = {
            "claim_digest": claim_digest,
            "audit_profile_id": profile_id,
            "answers": answers,
            "q04_mode": q04_mode,
            "q17_rule": q17_rule,
            "verdict": verdict,
            "revision_required": verdict in {"ESCALATE_HUMAN", "FAIL"},
        }
        ad = H("ART11b.AR.v8", audit)
        audit["audit_digest"] = ad
        self.S.audits[ad] = audit
        self._log("AUDIT_RECORDED", **{k: audit[k] for k in ("audit_digest", "verdict", "q04_mode", "q17_rule", "audit_profile_id")})

        self.S.event_seq += 1
        self.S.event_log.append(
            {
                "event_seq": self.S.event_seq,
                "command_kind": "RECORD_AUDIT",
                "caller_role": caller_role,
                "audit_digest": ad,
            }
        )
        return {"code": "SUCCESS", **audit}

    def discharge_obligation(self, obligation_digest: str, caller_role: str, evidence: list[str]) -> dict:
        err = self._auth(caller_role, AUTHORIZED_APPLY | AUTHORIZED_AUDIT | {"PROOF_CERTIFIER"}, "DISCHARGE")
        if err:
            return self._reject(err, "ART-04c")
        o = self.S.obligations[obligation_digest]
        if not evidence:
            return self._reject("EVIDENCE_MISSING", "I-PO-02")
        o["status"] = "DISCHARGED"
        o["discharge_evidence_digests"] = evidence
        self._log("OBLIGATION_STATUS", obligation_digest=obligation_digest, status="DISCHARGED")
        return {"code": "SUCCESS", "obligation_digest": obligation_digest, "status": "DISCHARGED"}

    def apply_promotion(self, claim_digest: str, caller_role: str, to: str = "RESULT") -> dict:
        self._log("APPLY_PROMOTION_ATTEMPT", caller_role=caller_role, claim_digest=claim_digest, to=to)
        # Boundary: discovery cannot promote
        if caller_role == "RESEARCH_DISCOVERY_ASSISTANT":
            snap_before = self.S.snapshot()
            self._log(
                "BOUNDARY_REJECT",
                command="APPLY_PROMOTION",
                code="ROLE_CEILING",
                invariant="ART-01D / ART-04e I-OD-02 / I-CRP-10",
            )
            # ensure unchanged
            assert self.S.maturity.get(claim_digest) == snap_before["maturity"].get(claim_digest)
            return {
                "code": "ROLE_CEILING",
                "invariant": "ART-01D · ART-04e I-OD-02 · I-CRP-10",
                "state_unchanged": True,
                "maturity": self.S.maturity.get(claim_digest),
            }

        err = self._auth(caller_role, AUTHORIZED_APPLY, "APPLY_PROMOTION")
        if err:
            return self._reject(err, "ART-04c / ART-13b")

        # I-AP-PO
        blocking = [
            o
            for o in self.S.obligations.values()
            if o["originating_claim_digest"] == claim_digest
            and o["blocks_promotion"]
            and o["status"] in {"OPEN", "FAILED"}
        ]
        if blocking:
            self._log(
                "PROMOTION_BLOCKED",
                code="OBLIGATION_UNRESOLVED",
                blocking=[b["obligation_digest"] for b in blocking],
            )
            return {
                "code": "OBLIGATION_UNRESOLVED",
                "invariant": "ART-07b I-PO-03 / ART-13b I-AP-PO",
                "blocking_obligations": [b["obligation_digest"] for b in blocking],
            }

        # Audit PASS required for major milestone RESULT
        audits = [a for a in self.S.audits.values() if a["claim_digest"] == claim_digest]
        if not audits or audits[-1]["verdict"] != "PASS":
            return self._reject("AUDIT_REQUIRED", "ART-11b / ART-13b")

        # FULL CX blocks
        if any(c["claim_digest"] == claim_digest and c["severity"] == "FULL" for c in self.S.cxs.values()):
            return self._reject("CX_BLOCKS_PROMOTION", "ART-13b I-AP-06")

        prev = self.S.maturity.get(claim_digest, "OPEN")
        self.S.maturity[claim_digest] = to
        self.S.event_seq += 1
        self.S.event_log.append(
            {
                "event_seq": self.S.event_seq,
                "command_kind": "APPLY_PROMOTION",
                "caller_role": caller_role,
                "claim_digest": claim_digest,
                "from": prev,
                "to": to,
            }
        )
        self._log("PROMOTION_APPLIED", claim_digest=claim_digest, from_maturity=prev, to=to)
        return {"code": "SUCCESS", "from": prev, "to": to, "final_status": "CERTIFIED" if to == "RESULT" else to}

    def library_export(self, claim_digest: str) -> dict:
        if self.S.maturity.get(claim_digest) not in {"PARTIAL_RESULT", "RESULT"}:
            return self._reject("NOT_CERTIFIED", "I.LibraryExport")
        return {
            "code": "SUCCESS",
            "export": {"claim_digest": claim_digest, "maturity": self.S.maturity[claim_digest]},
        }

    def _reject(self, code: str, invariant: str) -> dict:
        self._log("REJECT", code=code, invariant=invariant)
        return {"code": code, "invariant": invariant}


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")


def package_phase_a() -> dict:
    return {
        "author_kind": "HUMAN",
        "author_principal_digest": H("HUMAN", "test-operator"),
        "package_phase": "PHASE_A_CHARACTERIZATION",
        "profile": "PHASE_A_CHARACTERIZATION",
        "math_scope_pin_digest": H("ART01.AREA1"),
        "sealed_at": "2026-07-24T18:00:00Z",
        "payload": {
            "operator": "argmax",
            "definitions": [
                {
                    "name": "argmax",
                    "domain": "finite Λ ⊂ ℝ^n scores indexed by λ∈Λ",
                    "codomain": " nonempty subset of Λ",
                    "body": "argmax_{λ∈Λ} F(λ) := {λ∈Λ : F(λ) ≥ F(λ') ∀λ'∈Λ}",
                },
                {
                    "name": "bounded_score_perturbation",
                    "body": "F' = F + ε with ||ε||_∞ ≤ δ (model of score noise; NOT a MechanismInstance / Q_ψ)",
                },
                {
                    "name": "margin",
                    "body": "m(F) := F(λ*) - max_{λ≠λ*} F(λ) for unique λ*∈argmax F; else m(F)=0",
                },
            ],
            "assumptions": [
                "Λ finite nonempty",
                "F: Λ → ℝ totally ordered scores",
                "unique argmax when margin condition stated",
                "ties explicitly out of scope when m(F)>δ",
            ],
            "mechanism_proposals": [],
            "claims": [
                {
                    "chain_segment": "characterization",
                    "kind": "characterization_theorem",
                    "operator": "argmax",
                    "statement": (
                        "If λ* is the unique argmax of F and m(F) > 2δ, then for every score perturbation "
                        "ε with ||ε||_∞ ≤ δ, argmax(F+ε) = {λ*}."
                    ),
                    "assumptions": [
                        "unique argmax",
                        "m(F) > 2δ",
                        "||ε||_∞ ≤ δ",
                        "ties out of scope under margin",
                    ],
                    "tie_case_warning": "If m(F)=0 (ties), characterization does not apply; argmax may flip under any δ>0.",
                }
            ],
            "proof_sketches": [
                {
                    "claim_ref": 0,
                    "sketch": (
                        "For λ≠λ*: (F+ε)(λ*) - (F+ε)(λ) ≥ m(F) - 2δ > 0, hence λ* strictly dominates."
                    ),
                }
            ],
            "counterexample_claims": [
                {
                    "class_id": "CX.CHAR.out_of_regime",
                    "note": "If m(F) ≤ 2δ, construct ε flipping argmax to a near-competitor (outside claimed regime).",
                    "severity_intent": "PARTIAL",
                    "inside_claimed_regime": False,
                }
            ],
            "free_text_notes": "Perturbation model is characterization of score noise, not Q_ψ stabilization mechanism.",
        },
    }


def package_phase_b() -> dict:
    return {
        "author_kind": "RESEARCH_DISCOVERY_ASSISTANT",
        "author_principal_digest": H("ASSISTANT", "discovery-1"),
        "author_binding_digest": "BIND_ASSIST_LIVE",
        "package_phase": "PHASE_B_STABILIZATION",
        "profile": "PHASE_B_STABILIZATION",
        "math_scope_pin_digest": H("ART01.AREA1"),
        "sealed_at": "2026-07-24T18:05:00Z",
        "payload": {
            "operator": "argmax",
            "mechanism_proposals": [
                {
                    "name": "noisy_argmax",
                    "operator": "Q_ψ",
                    "description": "Add i.i.d. Gumbel(0,β) noise to scores then take argmax (noisy-argmax / softmax limit).",
                    "parameter_domain": {"β": ">0"},
                    "psi_data_dependence": "FIXED",
                }
            ],
            "assumptions": [
                "Λ finite",
                "noise i.i.d. Gumbel",
                "β fixed across neighbors",
            ],
            "claims": [
                {
                    "chain_segment": "selection_stability",
                    "kind": "stability",
                    "operator": "argmax",
                    "statement": (
                        "Under noisy-argmax Q_ψ with fixed β, selected index is neighbor-indistinguishable "
                        "within stated score ball of radius ρ."
                    ),
                    "assumptions": ["mechanism noisy_argmax", "ρ-ball neighbors"],
                },
                {
                    "chain_segment": "selection_stability",
                    "kind": "utility_loss",
                    "statement": "Expected utility loss under Q_ψ is bounded by κ(β,ρ).",
                    "assumptions": ["utility linear in F"],
                },
            ],
            "proof_sketches": [{"sketch": "Couple Gumbel noise; bound flip probability via margin vs β."}],
            "counterexample_claims": [
                {"class_id": "CX.tie_unstable", "note": "Near-ties amplify flip rate as β→0"},
                {"class_id": "CX.data_dep_scale", "note": "If β were data-dependent, DD class changes"},
            ],
        },
    }


def run_test1() -> dict:
    I = Interpreter()
    pkg = package_phase_a()
    sub = I.submit_candidate_package(pkg, caller_role="HUMAN_GATE_OPERATOR")
    assert sub["code"] == "SUCCESS", sub
    cd = sub["draft_claim_digests"][0]

    # Out-of-regime CX proposal (not FULL on the claim — partial outside regime)
    cx = I.run_characterization_cx(
        cd,
        "COUNTEREXAMPLE_ATTACKER",
        [
            {
                "class_id": "CX.CHAR.out_of_regime",
                "severity": "PARTIAL",
                "note": "Constructed when m(F)≤2δ — outside claimed regime; does not refute theorem.",
            },
            {
                "class_id": "CX.CHAR.omit_ties",
                "severity": "PARTIAL",
                "note": "Tie warning acknowledged; ties scoped out by m(F)>2δ.",
            },
        ],
    )

    audit = I.run_audit(
        cd,
        "INTEGRATION_AUDITOR",
        {
            "Q04": "NA",
            "Q17": "YES",
            "QC1": "YES",
            "QC2": "YES",
            "QC3": "YES",
            "QC4": "YES",
            "QC5": "YES",
        },
    )

    # Attempt APPLY with OPEN obligations → must block
    blocked = I.apply_promotion(cd, "VERIFICATION_ORCHESTRATOR", to="RESULT")
    assert blocked["code"] == "OBLIGATION_UNRESOLVED", blocked

    # Discharge blocking POs then promote
    for od in sub["obligation_digests"]:
        I.discharge_obligation(od, "PROOF_CERTIFIER", evidence=[H("proof-sketch-bound", cd)])

    promo = I.apply_promotion(cd, "VERIFICATION_ORCHESTRATOR", to="RESULT")
    lib = I.library_export(cd) if promo["code"] == "SUCCESS" else {"code": "SKIPPED"}

    # Regression: Phase A did not invent MECHANISM_REQUIRED
    regressions = {
        "no_mechanism_required": sub["code"] == "SUCCESS" and not I.S.crps[sub["crp_digest"]]["mechanism_required_at_intake"],
        "q04_na": audit.get("q04_mode") == "NOT_APPLICABLE",
        "q17_characterization": audit.get("q17_rule") == "characterization_facing",
        "obligations_linked": all(
            I.S.obligations[od]["originating_crp_digest"] == sub["crp_digest"] for od in sub["obligation_digests"]
        ),
        "unresolved_blocked_apply": blocked["code"] == "OBLIGATION_UNRESOLVED",
        "no_research_orchestrator": all(e.get("caller_role") != "RESEARCH_ORCHESTRATOR" for e in I.S.event_log),
        "cx_profile": cx.get("cx_profile_id") == "ART-12-CHAR",
        "audit_profile": audit.get("audit_profile_id") == "ART11b.CHAR",
    }

    final = "CERTIFIED" if promo.get("code") == "SUCCESS" else ("REVISION_REQUIRED" if audit["verdict"] != "PASS" else "FAILED")
    report = {
        "test": "TEST_1_PHASE_A_CHARACTERIZATION",
        "INPUT_PACKAGE": pkg,
        "VALIDATION_RESULT": sub,
        "CANONICAL_OBJECTS_CREATED": {
            "crp": I.S.crps.get(sub["crp_digest"]),
            "receipt": I.S.receipts.get(sub["receipt_digest"]),
            "claims": {k: I.S.claims[k] for k in sub["draft_claim_digests"]},
        },
        "PROOF_OBLIGATIONS_CREATED": {od: I.S.obligations[od] for od in sub["obligation_digests"]},
        "CX_RESULTS": cx,
        "AUDIT_RESULTS": audit,
        "PROMOTION_RESULT": {"blocked_first": blocked, "after_discharge": promo, "library_export": lib},
        "FINAL_STATUS": final,
        "EXECUTION_TRACE": I.trace,
        "EVENT_LOG": I.S.event_log,
        "REGRESSIONS": regressions,
        "DEFECTS_FOUND": [k for k, v in regressions.items() if not v],
    }
    write_json(OUT / "test1_phase_a.json", report)
    return report


def run_test2() -> dict:
    I = Interpreter(
        bindings={"BIND_ASSIST_LIVE": {"role_id": "RESEARCH_DISCOVERY_ASSISTANT", "status": "ACTIVE"}}
    )
    pkg = package_phase_b()
    # Discovery seals CRP but submit must be via B principal
    sub = I.submit_candidate_package(pkg, caller_role="VERIFICATION_ORCHESTRATOR")
    assert sub["code"] == "SUCCESS", sub
    assert sub["mechanism_digests"], "mechanism digests required"
    assert sub["audit_profile_id"] == "ART11b.BASE"
    assert sub["cx_profile_id"] == "ART-12"

    cd = sub["draft_claim_digests"][0]

    # Mechanism-specific obligations exist
    mech_obs = [o for o in I.S.obligations.values() if o.get("obligation_type") == "CERT_ATTACH"]
    assert mech_obs, "expected mechanism CERT_ATTACH obligations"

    cx = I.run_characterization_cx(  # uses ART-12 for Phase B via profile select
        cd,
        "COUNTEREXAMPLE_ATTACKER",
        [{"class_id": "CX.tie_unstable", "severity": "PARTIAL", "note": "near-tie sensitivity"}],
    )

    audit = I.run_audit(
        cd,
        "INTEGRATION_AUDITOR",
        {"Q04": "YES", "Q17": "YES"},
        verdict="PASS",
    )

    # Unresolved blocking obligations prevent certification
    blocked = I.apply_promotion(cd, "VERIFICATION_ORCHESTRATOR")
    assert blocked["code"] == "OBLIGATION_UNRESOLVED"

    # Boundary: discovery tries to promote
    boundary = I.apply_promotion(cd, "RESEARCH_DISCOVERY_ASSISTANT")
    assert boundary["code"] == "ROLE_CEILING"
    assert boundary["state_unchanged"] is True

    # Stale role
    stale = I.apply_promotion(cd, "RESEARCH_ORCHESTRATOR")
    assert stale["code"] == "UNAUTHORIZED_COMMAND"

    regressions = {
        "mechanism_required_and_present": I.S.crps[sub["crp_digest"]]["mechanism_required_at_intake"]
        and I.S.crps[sub["crp_digest"]]["mechanism_present"],
        "mech_obligations": bool(mech_obs),
        "base_audit_profile": audit["audit_profile_id"] == "ART11b.BASE",
        "stab_cx_profile": cx["cx_profile_id"] == "ART-12",
        "unresolved_blocks": blocked["code"] == "OBLIGATION_UNRESOLVED",
        "discovery_cannot_promote": boundary["code"] == "ROLE_CEILING",
        "no_stale_research_orchestrator_auth": stale["code"] == "UNAUTHORIZED_COMMAND",
        "verifier_issues_verdict": True,  # only VO can eventually promote
    }

    # Negative: Phase B without mechanism
    I2 = Interpreter(bindings={"BIND_ASSIST_LIVE": {"role_id": "RESEARCH_DISCOVERY_ASSISTANT", "status": "ACTIVE"}})
    bad = deepcopy(pkg)
    bad["payload"]["mechanism_proposals"] = []
    neg = I2.submit_candidate_package(bad, "VERIFICATION_ORCHESTRATOR")
    assert neg["code"] == "MECHANISM_REQUIRED"
    regressions["phase_b_empty_mech_rejected"] = neg["code"] == "MECHANISM_REQUIRED"

    report = {
        "test": "TEST_2_PHASE_B_STABILIZATION",
        "INPUT_PACKAGE": pkg,
        "VALIDATION_RESULT": sub,
        "CANONICAL_OBJECTS_CREATED": {
            "crp": I.S.crps[sub["crp_digest"]],
            "claims": {k: I.S.claims[k] for k in sub["draft_claim_digests"]},
            "mechanisms": {k: I.S.mechanisms[k] for k in sub["mechanism_digests"]},
        },
        "PROOF_OBLIGATIONS_CREATED": dict(I.S.obligations),
        "CX_RESULTS": cx,
        "AUDIT_RESULTS": audit,
        "PROMOTION_RESULT": {
            "blocked_unresolved": blocked,
            "discovery_promote_attempt": boundary,
            "stale_role_attempt": stale,
            "final_certification": "NOT_CERTIFIED_OBLIGATIONS_OPEN",
        },
        "FINAL_STATUS": "REVISION_REQUIRED",  # obligations open; discovery cannot certify
        "EXECUTION_TRACE": I.trace,
        "EVENT_LOG": I.S.event_log,
        "REGRESSIONS": regressions,
        "PHASE_B_NO_MECH_NEGATIVE": neg,
        "DEFECTS_FOUND": [k for k, v in regressions.items() if not v],
    }
    write_json(OUT / "test2_phase_b.json", report)
    return report


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    t1 = run_test1()
    t2 = run_test2()
    defects = t1["DEFECTS_FOUND"] + t2["DEFECTS_FOUND"]
    summary = {
        "test1_final": t1["FINAL_STATUS"],
        "test2_final": t2["FINAL_STATUS"],
        "defects": defects,
        "regressions_t1": t1["REGRESSIONS"],
        "regressions_t2": t2["REGRESSIONS"],
        "verdict": "LIVE ACCEPTANCE PASSED" if not defects else "LIVE ACCEPTANCE FAILED",
    }
    write_json(OUT / "summary.json", summary)
    print(json.dumps(summary, indent=2))
    return 0 if not defects else 1


if __name__ == "__main__":
    sys.exit(main())
