import sys
import os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "mcp" / "python"))
from clinical_mcp.config import MCPConfig
from clinical_mcp.tracing import init_tracing
from clinical_mcp.runner import MCPRunner
from agents import triage_agent, treatment_agent

def main():
    cfg = MCPConfig(
        eventlog_path="eventlog/events.jsonl",
        run_id="multiagent-demo"
    )
    os.makedirs("eventlog", exist_ok=True)
    init_tracing(cfg)
    runner = MCPRunner(cfg)
    plan = {
        "triage": triage_agent,
        "treatment": treatment_agent,
    }
    initial = {"patient": {"id": "1234", "symptom": "dolor_pecho"}}
    result = runner.run(plan, initial)
    print("\nResultado final:", result)
    print("Eventlog en: eventlog/events.jsonl")

if __name__ == "__main__":
    main()
