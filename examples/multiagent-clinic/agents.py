from typing import Dict, Any

def triage_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    # Simula decisión de triage
    patient = state.get("patient", {})
    if patient.get("symptom") == "dolor_pecho":
        return {"triage": "urgente"}
    return {"triage": "no_urgente"}

def treatment_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    # Simula decisión de tratamiento
    if state.get("triage") == "urgente":
        return {"treatment": "derivar_urgencias"}
    return {"treatment": "reposo"}
