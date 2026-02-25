from __future__ import annotations
import uuid
from typing import Callable, Dict, Any

from opentelemetry import trace
from .config import MCPConfig
from .eventlog import EventLog
from .guardrails import sanitize_payload

StepFn = Callable[[Dict[str, Any]], Dict[str, Any]]

class MCPRunner:
    def __init__(self, cfg: MCPConfig) -> None:
        self.cfg = cfg
        self.run_id = cfg.run_id or str(uuid.uuid4())
        self.log = EventLog(cfg.eventlog_path)
        self.tracer = trace.get_tracer(cfg.service_name)

    def run(self, plan: Dict[str, StepFn], initial: Dict[str, Any]) -> Dict[str, Any]:
        self.log.emit(self.run_id, "orchestrator", "started", self.run_id, {"plan": list(plan.keys())})
        state = dict(initial)

        for step_name, fn in plan.items():
            with self.tracer.start_as_current_span(f"step:{step_name}") as span:
                cid = span.get_span_context().span_id
                self.log.emit(self.run_id, "orchestrator", "step", str(cid), sanitize_payload({"step": step_name}))
                try:
                    out = fn(state)
                    state.update(out)
                except Exception as e:
                    self.log.emit(
                        self.run_id,
                        "orchestrator",
                        "error",
                        str(cid),
                        sanitize_payload({"step": step_name, "error": type(e).__name__, "msg": str(e)[:200]}),
                    )
                    raise

        self.log.emit(self.run_id, "orchestrator", "completed", self.run_id, {"keys": sorted(state.keys())})
        return state
