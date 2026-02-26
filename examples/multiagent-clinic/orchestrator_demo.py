from __future__ import annotations

from clinical_mcp.config import MCPConfig
from clinical_mcp.tracing import init_tracing
from clinical_mcp.orchestrator import HybridOrchestrator

def main() -> None:
    cfg = MCPConfig(
        service_name="multiagent-clinic-demo",
        environment="local",
        artifacts_dir="artifacts/mcp",
        eventlog_path="artifacts/mcp/events.jsonl",
        runbook_path="artifacts/mcp/run.json",
        outbox_db_path="artifacts/mcp/outbox.sqlite3",
        trace_exporter="none",
    )
    init_tracing(cfg)

    orch = HybridOrchestrator(cfg)

    # Async handlers: side-effects (reporting, notifications, sync)
    def on_report(msg):
        # Do NOT put PII in payload. Use internal refs.
        print(f"[async] report topic={msg.topic} run_id={msg.run_id} payload={msg.payload}")

    orch.bus.subscribe("report.generated", on_report)
    orch.start_workers()

    # Agents (sync truth)
    def intake(state):
        return {"patient_ref": "p_123", "intake_status": "ok"}

    def billing(state):
        return {"invoice_ref": "inv_456", "billing_status": "queued"}

    def followup(state):
        # publish async side-effect
        orch.bus.publish_async(
            run_id=orch.run_id,
            topic="report.generated",
            payload={"patient_ref": state["patient_ref"], "invoice_ref": state["invoice_ref"]},
        )
        return {"followup_status": "scheduled"}

    plan = {"intake": intake, "billing": billing, "followup": followup}
    result = orch.run(plan, initial={})
    print("[sync result]", result)

    orch.stop_workers()

if __name__ == "__main__":
    main()
