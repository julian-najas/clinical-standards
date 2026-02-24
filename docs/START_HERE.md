# START HERE

Objetivo: que cualquier persona del equipo encuentre rapido que tocar.

## 1) Si vas a usar standards en otro repo
1. Revisa `README.md` (seccion "Que Usar En Cada Caso").
2. Copia/llama el workflow reutilizable que corresponda.
3. Si es repo nuevo Python, parte de `templates/python/`.

## 2) Si vas a modificar este repo
1. Cambios de CI reusable: `/.github/workflows/`.
2. Cambios de pasos compartidos: `/actions/`.
3. Cambios de politicas infra: `/policies/conftest/`.
4. Cambios de reglas semgrep: `/semgrep/rules/`.
5. Cambios plantilla base: `/templates/python/`.

## 3) Flujo recomendado de cambios
1. Cambia lo minimo necesario.
2. Actualiza docs del bloque tocado.
3. Commit con scope claro (`feat(actions): ...`, `feat(templates): ...`).
4. PR con ejemplos de consumo en repos target.

## 4) Convenciones para no perdernos
- No duplicar logica entre workflows y composite actions.
- Reutilizar acciones antes de crear nuevos scripts.
- Mantener nombres estables para facilitar adopcion en varios repos.
- Dejar siempre un ejemplo de uso cuando se anade algo nuevo.
