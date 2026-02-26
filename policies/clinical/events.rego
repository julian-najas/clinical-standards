package clinical.events

default deny := []

# Helpers
lower_str(x) := lower(sprintf("%v", [x]))

# Deny if payload contains "email" key
deny[msg] {
  input.payload.email
  msg := "event payload contains email field (PII)"
}

# Deny if payload contains "phone" key
deny[msg] {
  input.payload.phone
  msg := "event payload contains phone field (PII)"
}

# Deny if payload stringified contains '@' (strict)
deny[msg] {
  contains(lower_str(input.payload), "@")
  msg := "event payload appears to contain an email address"
}

# Deny if payload contains Spanish DNI-like pattern (very naive)
deny[msg] {
  re_match(".*\\b[0-9]{8}[A-Z]\\b.*", sprintf("%v", [input.payload]))
  msg := "event payload appears to contain DNI-like identifier"
}
