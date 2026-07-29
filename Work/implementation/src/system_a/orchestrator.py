"""DISCOVERY_ORCHESTRATOR — sole FSM authority; gates; seal; submit bookkeeping."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from art_int.batch import SubmissionAttempt, SubmissionBatch, recompute_batch_status
from art_int.draft import DraftCRPPayload
from art_int.enums import AuthorKind, BatchStatus, IntakeStatus, TransportResult
from art_int.feedback import VerifierFeedbackExport
from art_int.seal import SealedCRPSnapshotPayload, seal_draft
from system_a.fsm import DiscoverySession, IllegalTransition, State, replay_control
from system_a.gates import GateDecision, GateNumber, GateRecord
from system_a.ir import DiscoveryIR
from system_a.packager import compile_branch


@dataclass
class DiscoveryOrchestrator:
    session: DiscoverySession
    ir: DiscoveryIR
    drafts: dict[str, DraftCRPPayload] = field(default_factory=dict)
    seals: dict[str, SealedCRPSnapshotPayload] = field(default_factory=dict)
    seal_version_ids: dict[str, str] = field(default_factory=dict)
    batches: list[SubmissionBatch] = field(default_factory=list)
    attempts: list[SubmissionAttempt] = field(default_factory=list)
    gate_records: list[GateRecord] = field(default_factory=list)
    scope_pin: str = "a" * 64
    principal: str = "b" * 64
    _gate3_policy_version_id: str | None = None
    _seal_wave_key: tuple[str, ...] | None = None
    _batch_for_wave: str | None = None

    @classmethod
    def create(cls, session_id: str | None = None) -> DiscoveryOrchestrator:
        sid = session_id or str(uuid4())
        ir = DiscoveryIR(session_id=sid)
        session = DiscoverySession(session_id=sid)
        session._append("SessionOpened", {"session_id": sid})
        orch = cls(session=session, ir=ir)
        session.bind_owner(orch)
        session._ir_close_hook = ir.close
        return orch

    def advance(self, to: State, **kw: Any):
        return self.session._commit(self, to, **kw)

    def skip_gate(self, gate: int):
        return self.session._skip_gate(self, gate)

    def set_gate1_required(self, required: bool) -> None:
        self.session.gate1_required = required
        if required:
            self.session.gate1_cleared = False

    def set_gate2_required(self, required: bool) -> None:
        self.session.gate2_required = required
        if required:
            self.session.gate2_cleared = False

    def install_gate3_waiver_policy(self, seal_set: list[str]) -> str:
        if self.session.state in (State.DS09, State.DS10, State.DS11, State.DS12) or self.session.is_closed:
            raise RuntimeError("Gate3 waiver SessionPolicy must be installed before DS09")
        av = self.ir.mint(
            artifact_class="SessionPolicy",
            caller_module="DISCOVERY_ORCHESTRATOR",
            payload={
                "session_id": self.session.session_id,
                "approved_before_gate3": True,
                "gate3_waiver_seal_resolver": "DETERMINISTIC_PROFILE",
                "deterministic_seal_rule": {"seal_set": list(seal_set)},
                "allow_same_session_continue_after_ds12": False,
                "unrecoverable_transport_to_ds91": self.session.policy_unrecoverable_transport_to_ds91,
                "created_at": "t0",
                "kind": "gate3_waiver_seal_set",
                "seal_set": list(seal_set),
            },
        )
        self._gate3_policy_version_id = av.version_id
        return av.version_id

    def apply_gate1(self, decision: GateDecision, *, accept_scope_change: bool = True) -> GateRecord:
        if self.session.state != State.DS04:
            raise RuntimeError("Gate 1 only in DS04")
        rec = GateRecord(gate_id=str(uuid4()), gate_number=GateNumber.G1, decision=decision, rationale="gate1")
        self.gate_records.append(rec)
        self.ir.mint(
            artifact_class="GateRecord",
            caller_module="DISCOVERY_ORCHESTRATOR",
            payload={"gate_id": rec.gate_id, "gate": 1, "decision": decision.value},
        )
        self.session._append("GateDecision", {"gate": 1, "decision": decision.value})
        self.session._gate_exit_authorized = True
        if decision in (GateDecision.APPROVE, GateDecision.WAIVE):
            if accept_scope_change or decision == GateDecision.WAIVE:
                self.session.scope_binding_version += 1
                self.ir.mint(
                    artifact_class="ScopeBinding",
                    caller_module="DISCOVERY_ORCHESTRATOR",
                    payload={"version": self.session.scope_binding_version},
                )
            self.session.gate1_required = False
            self.session.gate1_cleared = True
            self.advance(State.DS05, reason="gate1_cleared")
        elif decision == GateDecision.REVISE:
            self.advance(State.DS03, reason="gate1_revise")
        elif decision == GateDecision.REJECT:
            self.advance(State.DS13, reason="gate1_rejected")
        else:
            self.session._gate_exit_authorized = False  # defer
        return rec

    def apply_gate2(self, decision: GateDecision) -> GateRecord:
        if self.session.state != State.DS06:
            raise RuntimeError("Gate 2 only in DS06")
        rec = GateRecord(gate_id=str(uuid4()), gate_number=GateNumber.G2, decision=decision, rationale="gate2")
        self.gate_records.append(rec)
        self.ir.mint(
            artifact_class="GateRecord",
            caller_module="DISCOVERY_ORCHESTRATOR",
            payload={"gate_id": rec.gate_id, "gate": 2, "decision": decision.value},
        )
        self.session._append("GateDecision", {"gate": 2, "decision": decision.value})
        self.session._gate_exit_authorized = True
        if decision in (GateDecision.APPROVE, GateDecision.WAIVE):
            self.session.gate2_required = False
            self.session.gate2_cleared = True
            self.advance(State.DS07, reason="gate2_cleared")
        elif decision == GateDecision.REVISE:
            self.advance(State.DS05, reason="gate2_revise")
        elif decision == GateDecision.REJECT:
            self.advance(State.DS13, reason="gate2_rejected")
        else:
            self.session._gate_exit_authorized = False
        return rec

    def apply_gate3(
        self,
        decision: GateDecision,
        seal_set: list[str] | None = None,
        *,
        revise_target: str = "portfolio",
    ) -> GateRecord:
        if self.session.state != State.DS09:
            raise RuntimeError("Gate 3 only in DS09")
        requested = list(seal_set or [])
        policy_ref = self._gate3_policy_version_id
        if decision == GateDecision.WAIVE and not requested:
            if not policy_ref:
                self.session._append("GateIncomplete", {"gate": 3, "reason": "no_session_policy"})
                rec = GateRecord(
                    gate_id=str(uuid4()),
                    gate_number=GateNumber.G3,
                    decision=decision,
                    seal_set=None,
                    rationale="incomplete_no_policy",
                )
                self.gate_records.append(rec)
                return rec
            pol = self.ir.versions[policy_ref]
            requested = list(pol.payload["seal_set"])

        if len(requested) != len(set(requested)):
            self.session._append("GateIncomplete", {"gate": 3, "reason": "duplicate_seal_set_entries"})
            rec = GateRecord(
                gate_id=str(uuid4()),
                gate_number=GateNumber.G3,
                decision=decision,
                seal_set=None,
                rationale="duplicate_entries",
            )
            self.gate_records.append(rec)
            return rec

        incomplete = False
        ok: list[str] = []
        for d in requested:
            if d not in self.drafts or not self.drafts[d].compile_ok:
                incomplete = True
                break
            av = self.ir.versions.get(d)
            if av is None or av.artifact_class != "DraftCRP":
                incomplete = True
                break
            ok.append(d)

        if decision in (GateDecision.APPROVE, GateDecision.WAIVE):
            if incomplete or not ok or len(ok) != len(requested):
                self.session._append("GateIncomplete", {"gate": 3, "requested": requested})
                rec = GateRecord(
                    gate_id=str(uuid4()),
                    gate_number=GateNumber.G3,
                    decision=decision,
                    seal_set=None,
                    rationale="incomplete_seal_set",
                )
                self.gate_records.append(rec)
                self.ir.mint(
                    artifact_class="GateRecord",
                    caller_module="DISCOVERY_ORCHESTRATOR",
                    payload={
                        "gate_id": rec.gate_id,
                        "gate": 3,
                        "decision": decision.value,
                        "incomplete": True,
                    },
                )
                return rec
            rec = GateRecord(
                gate_id=str(uuid4()),
                gate_number=GateNumber.G3,
                decision=decision,
                seal_set=list(ok),
                rationale="sealable",
            )
            self.gate_records.append(rec)
            payload = {
                "gate_id": rec.gate_id,
                "gate": 3,
                "decision": decision.value,
                "seal_set": ok,
            }
            if decision == GateDecision.WAIVE and policy_ref:
                payload["session_policy_ref"] = policy_ref
            self.ir.mint(
                artifact_class="GateRecord",
                caller_module="DISCOVERY_ORCHESTRATOR",
                payload=payload,
            )
            self.session.seal_set = tuple(ok)
            self.session.sealed_draft_ids = ()
            self._seal_wave_key = tuple(ok)
            self._batch_for_wave = None
            self.session._append("GateDecision", {"gate": 3, "decision": decision.value, "seal_set": ok})
            self.session._gate_exit_authorized = True
            self.advance(State.DS10, reason="gate3_sealable")
            return rec

        rec = GateRecord(gate_id=str(uuid4()), gate_number=GateNumber.G3, decision=decision, seal_set=None)
        self.gate_records.append(rec)
        self.ir.mint(
            artifact_class="GateRecord",
            caller_module="DISCOVERY_ORCHESTRATOR",
            payload={"gate_id": rec.gate_id, "gate": 3, "decision": decision.value},
        )
        self.session._append("GateDecision", {"gate": 3, "decision": decision.value})
        if decision == GateDecision.REJECT:
            self.session._gate_exit_authorized = True
            self.advance(State.DS13, reason="gate3_rejected")
        elif decision == GateDecision.REVISE:
            self.session._gate_exit_authorized = True
            if revise_target == "discovery":
                self.advance(State.DS05, reason="revise_discovery")
            else:
                self.advance(State.DS07, reason="revise_portfolio")
        return rec

    def seal_authorized(
        self,
        draft_version_id: str,
        *,
        author_kind: AuthorKind = AuthorKind.HUMAN,
        binding: str | None = None,
        assistant_live: bool = False,
    ) -> SealedCRPSnapshotPayload:
        if self.session.state != State.DS10:
            raise RuntimeError("seal only in DS10")
        if draft_version_id not in self.session.seal_set:
            raise RuntimeError("draft not in Gate3 seal_set")
        if draft_version_id in self.session.sealed_draft_ids:
            raise RuntimeError("draft already sealed in this wave")
        if draft_version_id not in self.ir.versions:
            raise RuntimeError("draft not in IR")
        gate_id = next(
            (r.gate_id for r in reversed(self.gate_records) if r.gate_number == GateNumber.G3 and r.seal_set),
            None,
        )
        if not gate_id:
            raise RuntimeError("no Gate3 record with seal_set")
        draft = self.drafts[draft_version_id]
        snap = seal_draft(
            draft,
            draft_crp_version_id=draft_version_id,
            gate_record_id=gate_id,
            sealed_at="2026-07-25T12:00:00Z",
            author_kind=author_kind,
            author_principal_digest=self.principal,
            author_binding_digest=binding,
            live_scope_pin=self.scope_pin,
            assistant_binding_live=assistant_live,
        )
        if snap.sealed_digest in self.session.sealed_digests:
            raise RuntimeError("sealed_digest collision in wave; revise draft content before seal")
        self.seals[snap.sealed_digest] = snap
        vid = self.ir.mint(
            artifact_class="SealedCRPSnapshot",
            caller_module="RESEARCH_DISCOVERY_ASSISTANT",
            payload=snap.to_wire(),
        ).version_id
        self.seal_version_ids[draft_version_id] = vid
        self.session.sealed_draft_ids = self.session.sealed_draft_ids + (draft_version_id,)
        self.session.sealed_digests = self.session.sealed_digests + (snap.sealed_digest,)
        self.session.sealed_snapshot_version_ids = self.session.sealed_snapshot_version_ids + (vid,)
        self.session._append("DraftSealed", {"sealed_digest": snap.sealed_digest, "version_id": vid})
        return snap

    def compile_portfolio_member(self, branch_id: str, profile_hint: str, member_id: str) -> str:
        result = compile_branch(
            self.ir,
            branch_id=branch_id,
            profile_hint=profile_hint,
            math_scope_pin_digest=self.scope_pin,
            member_id=member_id,
        )
        if isinstance(result, DraftCRPPayload):
            vid = self.ir.mint(
                artifact_class="DraftCRP",
                caller_module="CRP_PACKAGER",
                payload=result.to_wire(),
            ).version_id
            self.drafts[vid] = result
            self.session.draft_ok_count += 1
            self.session._append("DraftCompiled", {"version_id": vid})
            return vid
        vid = self.ir.mint(
            artifact_class="CompileError",
            caller_module="CRP_PACKAGER",
            payload=result.to_wire(),
        ).version_id
        self.session._append("CompileFailed", {"version_id": vid})
        return vid

    def start_submission_batch(self) -> SubmissionBatch:
        if self.session.state == State.DS10:
            self.advance(State.DS11, reason="begin_submit")
        if self.session.state != State.DS11:
            raise RuntimeError("submission only in DS11")
        if self._batch_for_wave:
            return next(b for b in self.batches if b.batch_id == self._batch_for_wave)
        gate_id = next(
            (r.gate_id for r in reversed(self.gate_records) if r.gate_number == GateNumber.G3 and r.seal_set),
            "g3",
        )
        batch = SubmissionBatch(
            batch_id=str(uuid4()),
            session_id=self.session.session_id,
            gate_record_id=gate_id,
            seal_set=list(self.session.seal_set),
            sealed_snapshot_version_ids=list(self.session.sealed_snapshot_version_ids),
        )
        for dig, svid in zip(self.session.sealed_digests, self.session.sealed_snapshot_version_ids):
            if any(
                a.sealed_digest == dig and a.b_intake_result == IntakeStatus.ACCEPTED_DRAFT for a in self.attempts
            ):
                continue
            att = SubmissionAttempt(
                attempt_id=str(uuid4()),
                batch_id=batch.batch_id,
                session_id=self.session.session_id,
                sealed_snapshot_version_id=svid,
                sealed_digest=dig,
                idempotency_key=dig,
                logical_submission_id=svid,  # unique per sealed snapshot version
                transport_result=TransportResult.OK,
                b_intake_result=IntakeStatus.PENDING,
            )
            self.attempts.append(att)
            batch.member_attempt_ids.append(att.attempt_id)
            self.ir.mint(
                artifact_class="SubmissionAttempt",
                caller_module="DISCOVERY_ORCHESTRATOR",
                payload=att.to_wire(),
            )
            self.session._append("SubmissionAttemptRecorded", {"attempt_id": att.attempt_id})
        self.batches.append(batch)
        self._batch_for_wave = batch.batch_id
        self.ir.mint(
            artifact_class="SubmissionBatch",
            caller_module="DISCOVERY_ORCHESTRATOR",
            payload=batch.to_wire(),
        )
        return batch

    def retry_failed_transport(self, sealed_digest: str) -> SubmissionAttempt:
        if self.session.state != State.DS11:
            raise RuntimeError("retry only in DS11")
        if not self._batch_for_wave:
            raise RuntimeError("no batch")
        if any(
            a.sealed_digest == sealed_digest and a.b_intake_result == IntakeStatus.ACCEPTED_DRAFT
            for a in self.attempts
        ):
            raise RuntimeError("cannot retry ACCEPTED_DRAFT")
        prev = [a for a in self.attempts if a.sealed_digest == sealed_digest]
        if not prev:
            raise RuntimeError("unknown digest")
        last = prev[-1]
        if last.b_intake_result == IntakeStatus.REJECTED:
            raise RuntimeError("cannot retry B intake REJECTED via transport retry")
        if last.transport_result not in (TransportResult.FAILED, TransportResult.EXHAUSTED):
            raise RuntimeError("transport retry only after FAILED/EXHAUSTED")
        att = SubmissionAttempt(
            attempt_id=str(uuid4()),
            batch_id=self._batch_for_wave,
            session_id=self.session.session_id,
            sealed_snapshot_version_id=last.sealed_snapshot_version_id,
            sealed_digest=sealed_digest,
            idempotency_key=sealed_digest,
            logical_submission_id=last.logical_submission_id,
            attempt_number=last.attempt_number + 1,
            transport_result=TransportResult.OK,
            b_intake_result=IntakeStatus.PENDING,
        )
        self.attempts.append(att)
        batch = next(b for b in self.batches if b.batch_id == self._batch_for_wave)
        batch.member_attempt_ids.append(att.attempt_id)
        self.ir.mint(
            artifact_class="SubmissionAttempt",
            caller_module="DISCOVERY_ORCHESTRATOR",
            payload=att.to_wire(),
        )
        self.ir.mint(
            artifact_class="SubmissionBatch",
            caller_module="DISCOVERY_ORCHESTRATOR",
            payload={**batch.to_wire(), "retry_roster_update": True},
        )
        return att

    def record_intake(self, sealed_digest: str, status: IntakeStatus, receipt_ref: str | None = None) -> None:
        for a in self.attempts:
            if a.sealed_digest == sealed_digest and a.b_intake_result == IntakeStatus.PENDING:
                # ponytail: terminal fill on PENDING attempt object; ceiling = memory+event; upgrade = immutable AttemptOutcome IR versions only
                a.b_intake_result = status
                a.receipt_ref = receipt_ref
                if receipt_ref:
                    self.session.receipt_refs = self.session.receipt_refs + (receipt_ref,)
                self.ir.mint(
                    artifact_class="SubmissionAttempt",
                    caller_module="DISCOVERY_ORCHESTRATOR",
                    payload={**a.to_wire(), "outcome_record": True},
                )
                self.session._append(
                    "SubmissionAttemptOutcome",
                    {"attempt_id": a.attempt_id, "status": status.value, "receipt_ref": receipt_ref},
                )
                break
        if self.batches:
            self.batches[-1].batch_status = recompute_batch_status(
                [a for a in self.attempts if a.batch_id == self.batches[-1].batch_id]
            )
            self.ir.mint(
                artifact_class="SubmissionBatch",
                caller_module="DISCOVERY_ORCHESTRATOR",
                payload={**self.batches[-1].to_wire(), "status_snapshot": True},
            )

    def attest_foreign_seal(self, source_session_id: str, sealed_digest: str) -> None:
        self.session.attested_foreign_seals = self.session.attested_foreign_seals + (
            (source_session_id, sealed_digest),
        )

    def import_feedback(
        self,
        export: VerifierFeedbackExport,
        *,
        active: bool = True,
        authorized_import: bool = False,
        source_session_id: str | None = None,
    ) -> dict[str, Any]:
        prior = self.session._mint_verifier_prior(
            self,
            export,
            active=active,
            authorized_import=authorized_import,
            source_session_id=source_session_id,
        )
        if prior["active"]:
            self.ir.mint(
                artifact_class="VerifierPrior",
                caller_module="DISCOVERY_ORCHESTRATOR",
                payload=prior,
            )
        return prior

    def _assert_batch_closable(self) -> None:
        if self.batches and self.batches[-1].batch_status == BatchStatus.OPEN:
            raise IllegalTransition("cannot close while batch has pending members")

    def close_from_batch_outcome(self) -> None:
        self._assert_batch_closable()
        if not self.batches:
            self.advance(State.DS13, reason="completed_without_submission")
            return
        st = self.batches[-1].batch_status
        if st == BatchStatus.COMPLETED_ALL_ACCEPTED:
            reason = "completed_submitted"
        elif st == BatchStatus.COMPLETED_ALL_REJECTED:
            reason = "completed_b_intake_rejected"
        elif st == BatchStatus.COMPLETED_MIXED:
            reason = "completed_mixed_outcomes"
        else:
            reason = "completed_without_submission"
        if self.session.state == State.DS11:
            self.advance(State.DS12, reason="feedback_optional")
        if self.session.state == State.DS12:
            self.advance(State.DS13, reason=reason)
        elif not self.session.is_closed:
            self.advance(State.DS13, reason=reason)

    def close(self, reason: str = "completed_without_submission") -> None:
        self._assert_batch_closable()
        if not self.session.is_closed:
            self.advance(State.DS13, reason=reason)

    def replay_state(self) -> State:
        return replay_control(self.session.events)
