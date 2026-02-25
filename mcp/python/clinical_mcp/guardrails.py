from __future__ import annotations
import re
from typing import Any, Dict

PII_PATTERNS = [
    re.compile(r"\b\d{8}[A-Z]\b"),                  # DNI (simplificado)
    re.compile(r"\b\d{3}[- ]?\d{2}[- ]?\d{4}\b"),   # SSN-like
    re.compile(r"\b\d{9}\b"),                       # phone-ish naive
]

def assert_no_pii(obj: Any) -> None:
    s = str(obj)
    for p in PII_PATTERNS:
        if p.search(s):
            raise ValueError("PII detected in payload/log. Refuse to emit.")

def sanitize_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    # Minimal: enforce no PII. (If you need redaction, implement here.)
    assert_no_pii(payload)
    return payload
