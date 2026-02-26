.PHONY: mcp.install mcp.demo mcp.validate mcp.opa mcp.test

mcp.install:
	python -m pip install -U pip
	python -m pip install -e mcp/python[dev]
	python -m pip install jsonschema

mcp.demo:
	python examples/multiagent-clinic/orchestrator_demo.py

mcp.validate:
	python mcp/python/clinical_mcp/validate_artifacts.py

mcp.opa:
	python mcp/python/clinical_mcp/opa_eval_events.py

mcp.test:
	pytest -q mcp/python/tests
