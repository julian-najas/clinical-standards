from __future__ import annotations
import re
from typing import Any, Mapping

# Minimal guardrails: block obvious identifiers in logs/events.
_PATTERNS = [
    re.compile(r"\b\d{8}[A-Z]\b"),                # DNI (naive)
    re.compile(r"\b\d{3}[- ]?\d{2}[- ]?\d{4}\b"), # SSN-like (naive)
    re.compile(r"\b\d{9}\b"),                     # phone-ish (naive)
    re.compile(r"@"),                                # emails (very strict)
]

def assert_no_pii(obj: Any) -> None:
    s = str(obj)
    for p in _PATTERNS:
        if p.search(s):
            raise ValueError("PII detected in payload/log. Refuse to emit.")

def sanitize_mapping(m: Mapping[str, Any]) -> dict[str, Any]:
    # Refuse to emit if any PII-like content is present.
    assert_no_pii(m)
    return dict(m)
