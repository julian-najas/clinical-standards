from __future__ import annotations
from .config import MCPConfig

def init_tracing(cfg: MCPConfig) -> None:
    if cfg.trace_exporter == "none":
        return

    from opentelemetry import trace
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

    resource = Resource.create({
        "service.name": cfg.service_name,
        "deployment.environment": cfg.environment,
    })
    provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(provider)

    if cfg.trace_exporter == "console":
        provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
        return

    # OTLP default
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
    exporter = OTLPSpanExporter(endpoint=cfg.otlp_endpoint, insecure=True)
    provider.add_span_processor(BatchSpanProcessor(exporter))
