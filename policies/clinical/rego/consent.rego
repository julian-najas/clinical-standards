package clinical.consent

# P0: cualquier evento "treatment" requiere consentimiento activo
deny[msg] {
  input.consent.scope == "treatment"
  input.consent.status != "active"
  msg := sprintf("P0: consent must be active for treatment (got %v)", [input.consent.status])
}

# P1: effective_to no puede ser anterior a effective_from (si existe)
warn[msg] {
  input.consent.effective_to
  input.consent.effective_to < input.consent.effective_from
  msg := "P1: consent.effective_to is earlier than consent.effective_from"
}
