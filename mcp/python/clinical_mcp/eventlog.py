from __future__ import annotations
import json
import os
import time
from dataclasses import asdict, dataclass
from typing import Any, Dict, Optional

@dataclass
class MCPEvent:
    ts_unix: float
    run_id: str
    actor: str                 # agent/orchestrator/tool
    action: str                # started|step|decision|tool_call|completed|error
    correlation_id: str        # trace/span correlation or internal id
    payload: Dict[str, Any]    # structured, NO PII

class EventLog:
    def __init__(self, path: str) -> None:
        self.path = path
        os.makedirs(os.path.dirname(path), exist_ok=True)

    def emit(
        self,
        run_id: str,
        actor: str,
        action: str,
        correlation_id: str,
        payload: Dict[str, Any],
        ts_unix: Optional[float] = None,
    ) -> None:
        ev = MCPEvent(
            ts_unix=ts_unix if ts_unix is not None else time.time(),
            run_id=run_id,
            actor=actor,
            action=action,
            correlation_id=correlation_id,
            payload=payload,
        )
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(ev), ensure_ascii=False) + "\n")
