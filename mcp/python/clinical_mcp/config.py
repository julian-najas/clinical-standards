from __future__ import annotations
from dataclasses import dataclass
import os

@dataclass(frozen=True)
class MCPConfig:
    service_name: str = os.getenv("MCP_SERVICE_NAME", "clinical-mcp")
    environment: str = os.getenv("MCP_ENV", "dev")
    eventlog_path: str = os.getenv("MCP_EVENTLOG_PATH", "artifacts/mcp/events.jsonl")
    trace_exporter: str = os.getenv("MCP_TRACE_EXPORTER", "otlp")  # otlp|console|none
    otlp_endpoint: str = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317")
    run_id: str = os.getenv("MCP_RUN_ID", "")
