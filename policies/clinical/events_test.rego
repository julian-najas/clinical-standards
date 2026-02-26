package clinical.events

# Import the rules from events.rego via same package.
# Tests validate deny list behavior deterministically.

test_allow_non_pii_event {
  denies := data.clinical.events.deny with input as {
    "ts_unix": 1.0,
    "run_id": "r1",
    "actor": "orchestrator",
    "kind": "emit",
    "cid": "c1",
    "payload": {"patient_ref": "p_123", "invoice_ref": "inv_456"}
  }
  count(denies) == 0
}

test_deny_email_key {
  denies := data.clinical.events.deny with input as {
    "ts_unix": 1.0,
    "run_id": "r2",
    "actor": "tool:notify",
    "kind": "emit",
    "cid": "c2",
    "payload": {"email": "test@example.com"}
  }
  count(denies) > 0
}

test_deny_at_symbol_in_payload_string {
  denies := data.clinical.events.deny with input as {
    "ts_unix": 1.0,
    "run_id": "r3",
    "actor": "tool:notify",
    "kind": "emit",
    "cid": "c3",
    "payload": {"note": "contact me at x@y.com"}
  }
  count(denies) > 0
}

test_deny_dni_like_pattern {
  denies := data.clinical.events.deny with input as {
    "ts_unix": 1.0,
    "run_id": "r4",
    "actor": "tool:notify",
    "kind": "emit",
    "cid": "c4",
    "payload": {"note": "DNI 12345678Z"}
  }
  count(denies) > 0
}
