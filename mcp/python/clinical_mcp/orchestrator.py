from __future__ import annotations
import os
import uuid
from typing import Callable, Any, Dict, Mapping

from opentelemetry import trace

from .config import MCPConfig
from .eventlog import JsonlEventLog
from .outbox import Outbox
from .bus import OutboxBus
from .runbook import Runbook, write_runbook, now

StepFn = Callable[[Dict[str, Any]], Dict[str, Any]]

class HybridOrchestrator:
    """
    Orchestrator-centric hybrid:
    - deterministic sync pipeline executes steps in order (truth)
    - emits structured events to JSONL
    - enqueues async side-effects to outbox (notifications, reporting, sync)
    """
    def __init__(self, cfg: MCPConfig) -> None:
        self.cfg = cfg
        self.run_id = str(uuid.uuid4())
        os.makedirs(cfg.artifacts_dir, exist_ok=True)

        self.log = JsonlEventLog(cfg.eventlog_path)
        self.outbox = Outbox(cfg.outbox_db_path)
        self.bus = OutboxBus(self.outbox, poll_interval_s=cfg.outbox_poll_interval_s)

        self.tracer = trace.get_tracer(cfg.service_name)

    def start_workers(self) -> None:
        self.bus.start()

    def stop_workers(self) -> None:
        self.bus.stop()

    def run(self, plan: Mapping[str, StepFn], initial: Mapping[str, Any]) -> Dict[str, Any]:
        plan_names = list(plan.keys())
        write_runbook(
            self.cfg.runbook_path,
            Runbook(
                run_id=self.run_id,
                started_ts_unix=now(),
                service_name=self.cfg.service_name,
                environment=self.cfg.environment,
                plan=plan_names,
                result_keys=[],
                status="started",
            ),
        )

        self.log.emit(
            run_id=self.run_id,
            actor="orchestrator",
            kind="started",
            cid=self.run_id,
            payload={"plan": plan_names},
        )

        state: Dict[str, Any] = dict(initial)

        try:
            for step_name, fn in plan.items():
                with self.tracer.start_as_current_span(f"step:{step_name}") as span:
                    cid = str(span.get_span_context().span_id)
                    self.log.emit(
                        run_id=self.run_id,
                        actor="orchestrator",
                        kind="step",
                        cid=cid,
                        payload={"step": step_name},
                    )

                    out = fn(state)
                    state.update(out)

                    # Deterministic event for step result keys only (no values)
                    self.log.emit(
                        run_id=self.run_id,
                        actor=f"agent:{step_name}",
                        kind="decision",
                        cid=cid,
                        payload={"produced_keys": sorted(out.keys())},
                    )

            self.log.emit(
                run_id=self.run_id,
                actor="orchestrator",
                kind="completed",
                cid=self.run_id,
                payload={"result_keys": sorted(state.keys())},
            )

            write_runbook(
                self.cfg.runbook_path,
                Runbook(
                    run_id=self.run_id,
                    started_ts_unix=now(),
                    service_name=self.cfg.service_name,
                    environment=self.cfg.environment,
                    plan=plan_names,
                    result_keys=sorted(state.keys()),
                    status="completed",
                ),
            )
            return state

        except Exception as e:
            self.log.emit(
                run_id=self.run_id,
                actor="orchestrator",
                kind="error",
                cid=self.run_id,
                payload={"error": type(e).__name__, "msg": str(e)[:200], "at": "run"},
            )
            write_runbook(
                self.cfg.runbook_path,
                Runbook(
                    run_id=self.run_id,
                    started_ts_unix=now(),
                    service_name=self.cfg.service_name,
                    environment=self.cfg.environment,
                    plan=plan_names,
                    result_keys=sorted(state.keys()),
                    status="failed",
                ),
            )
            raise
