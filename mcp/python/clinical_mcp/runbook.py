from __future__ import annotations
import json
import os
import time
from dataclasses import dataclass, asdict
from typing import Any, Mapping

@dataclass(frozen=True)
class Runbook:
    run_id: str
    started_ts_unix: float
    service_name: str
    environment: str
    plan: list[str]
    result_keys: list[str]
    status: str  # started|completed|failed

def write_runbook(path: str, rb: Runbook) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(asdict(rb), f, ensure_ascii=False, indent=2)

def now() -> float:
    return time.time()
