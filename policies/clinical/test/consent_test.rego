package clinical.consent_test

import data.clinical.consent.deny
import data.clinical.consent.warn

test_valid_treatment_has_no_denies {
  input := json.unmarshal(file("policies/clinical/test/fixtures/valid_treatment.json"))
  count(deny with input as input) == 0
}

test_revoked_treatment_is_denied {
  input := json.unmarshal(file("policies/clinical/test/fixtures/revoked_treatment.json"))
  count(deny with input as input) == 1
}

test_bad_dates_warn {
  input := json.unmarshal(file("policies/clinical/test/fixtures/bad_dates.json"))
  some i
  warn[i] == "P1: consent.effective_to is earlier than consent.effective_from"
}
