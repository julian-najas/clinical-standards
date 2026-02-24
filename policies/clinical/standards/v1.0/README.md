# Clinical Standard v1.0 - Consent

Este estandar define el minimo canonico para declarar el estado de consentimiento de un paciente en procesos clinicos.

## Objetivo
- Determinar si un evento clinico puede ejecutarse en base a consentimiento.
- Ofrecer validacion determinista en CI con OPA (opt-in).

## Inputs esperados (payload)
El motor OPA evalua un `input` JSON con:
- `standard_version`: "v1.0"
- `patient.patient_id`
- `consent.status`: active|revoked|unknown
- `consent.scope`: treatment|research|data_sharing
- `consent.effective_from` (ISO8601)
- `consent.effective_to` (opcional, ISO8601)

## Severidades
- P0: Falta consentimiento activo cuando se requiere (treatment).
- P1: Datos incompletos o inconsistentes (fechas invalidas, scope faltante).

## Validacion
- Schema: `schemas/consent_event.schema.json`
- Politicas: `rego/consent.rego`
- Tests: `opa test policies/clinical -v`
