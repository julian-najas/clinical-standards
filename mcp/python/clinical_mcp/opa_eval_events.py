from __future__ import annotations
import json
import subprocess
import sys
from pathlib import Path

POLICY = Path("policies/clinical/events.rego")

def die(msg: str) -> None:
    print(msg, file=sys.stderr)
    sys.exit(1)

def opa_eval(event: dict) -> list[str]:
    # Evaluate: data.clinical.events.deny
    p = subprocess.run(
        ["opa", "eval", "-f", "json", "-d", str(POLICY), "data.clinical.events.deny"],
        input=json.dumps(event).encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if p.returncode != 0:
        die(f"opa eval failed: {p.stderr.decode('utf-8', errors='ignore')[:500]}")
    out = json.loads(p.stdout.decode("utf-8"))
    # result[0].expressions[0].value is the deny array
    try:
        return out["result"][0]["expressions"][0]["value"]
    except Exception:
        return []

def main() -> None:
    events_path = Path("artifacts/mcp/events.jsonl")
    if not events_path.exists():
        die("missing artifacts/mcp/events.jsonl")

    if not POLICY.exists():
        die("missing policies/clinical/events.rego")

    denied = 0
    for i, line in enumerate(events_path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        event = json.loads(line)
        denies = opa_eval(event)
        if denies:
            denied += 1
            print(f"[DENY] line={i} run_id={event.get('run_id')} kind={event.get('kind')} -> {denies}")

    if denied:
        die(f"OPA denied {denied} event(s).")
    print("OK: OPA policies passed for all events.")

if __name__ == "__main__":
    main()
