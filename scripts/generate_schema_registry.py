from __future__ import annotations
import hashlib
import json
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "mcp" / "schemas"
REGISTRY = SCHEMAS / "registry.json"

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()

def main() -> None:
    v1 = SCHEMAS / "v1"

    event = v1 / "event.schema.json"
    run = v1 / "run.schema.json"

    registry = {
        "registry_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "schemas": {
            "v1": {
                "event": {
                    "path": str(event.relative_to(ROOT)),
                    "sha256": sha256_file(event),
                },
                "run": {
                    "path": str(run.relative_to(ROOT)),
                    "sha256": sha256_file(run),
                },
            }
        },
    }

    REGISTRY.write_text(json.dumps(registry, indent=2), encoding="utf-8")
    print("Registry updated:", REGISTRY)

if __name__ == "__main__":
    main()
