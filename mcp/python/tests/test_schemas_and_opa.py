from __future__ import annotations
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]  # repo root when run via `pytest -c ...`
FIX = ROOT / "mcp" / "fixtures"

def run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

def test_schema_validation_pass(tmp_path: Path) -> None:
    # copy fixtures into expected artifacts locations
    artifacts = tmp_path / "artifacts" / "mcp"
    artifacts.mkdir(parents=True, exist_ok=True)
    (artifacts / "events.jsonl").write_text((FIX / "events.pass.jsonl").read_text(), encoding="utf-8")
    (artifacts / "run.json").write_text((FIX / "run.pass.json").read_text(), encoding="utf-8")

    # run validator from tmp cwd
    p = run(["python", str(ROOT / "mcp/python/clinical_mcp/validate_artifacts.py")])
    # validate_artifacts.py expects artifacts/mcp/... relative to cwd
    # so run with cwd=tmp_path by invoking through shell
    p = subprocess.run(
        ["python", str(ROOT / "mcp/python/clinical_mcp/validate_artifacts.py")],
        cwd=str(tmp_path),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    assert p.returncode == 0, p.stderr

def test_opa_denies_pii(tmp_path: Path) -> None:
    artifacts = tmp_path / "artifacts" / "mcp"
    artifacts.mkdir(parents=True, exist_ok=True)
    (artifacts / "events.jsonl").write_text((FIX / "events.fail_pii.jsonl").read_text(), encoding="utf-8")
    # OPA runner only reads events.jsonl; run.json not required for this test.

    p = subprocess.run(
        ["python", str(ROOT / "mcp/python/clinical_mcp/opa_eval_events.py")],
        cwd=str(tmp_path),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    assert p.returncode != 0
    assert "OPA denied" in (p.stderr + p.stdout)
