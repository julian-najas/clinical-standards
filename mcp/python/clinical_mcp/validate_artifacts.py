from __future__ import annotations
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]  # .../mcp/python/clinical_mcp -> .../mcp
SCHEMAS = ROOT / "schemas" / "v1"
EVENT_SCHEMA = json.loads((SCHEMAS / "event.schema.json").read_text(encoding="utf-8"))
RUN_SCHEMA = json.loads((SCHEMAS / "run.schema.json").read_text(encoding="utf-8"))

event_validator = Draft202012Validator(EVENT_SCHEMA)
run_validator = Draft202012Validator(RUN_SCHEMA)

def die(msg: str) -> None:
    print(msg, file=sys.stderr)
    sys.exit(1)

def validate_events_jsonl(path: Path) -> None:
    if not path.exists():
        die(f"missing events file: {path}")
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            obj = json.loads(line)
        except Exception as e:
            die(f"events.jsonl invalid JSON at line {i}: {e}")
        errors = sorted(event_validator.iter_errors(obj), key=lambda e: e.path)
        if errors:
            die(f"events.jsonl schema error at line {i}: {errors[0].message}")

def validate_run_json(path: Path) -> None:
    if not path.exists():
        die(f"missing run file: {path}")
    try:
        obj = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        die(f"run.json invalid JSON: {e}")
    errors = sorted(run_validator.iter_errors(obj), key=lambda e: e.path)
    if errors:
        die(f"run.json schema error: {errors[0].message}")

def main() -> None:
    # Paths relative to repo root when CI runs from checkout root
    events = Path("artifacts/mcp/events.jsonl")
    run = Path("artifacts/mcp/run.json")
    validate_events_jsonl(events)
    validate_run_json(run)
    print("OK: MCP artifacts validated against JSON Schemas.")

if __name__ == "__main__":
    main()
