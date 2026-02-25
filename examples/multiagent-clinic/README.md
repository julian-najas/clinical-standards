# Ejemplo: Orquestador Multiagente (clinical-mcp)

Este ejemplo muestra cómo orquestar agentes clínicos usando el runtime `clinical_mcp`.
Incluye:
- Orquestador minimal
- Dos agentes simulados ("triage" y "treatment")
- Trazabilidad y eventlog

## Estructura
- `orchestrator.py`: Orquestador principal
- `agents.py`: Lógica de agentes simulados
- `run.sh`: Ejecución rápida
- `eventlog/`: Salida de eventos

## Uso rápido
```sh
python orchestrator.py
```

Verifica el eventlog generado en `eventlog/` y la salida de consola para trazabilidad.