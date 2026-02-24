# Conftest Policies

Politicas baseline para repos de infraestructura/GitOps.

## Kubernetes (`kubernetes.rego`)
- `deny`: `hostNetwork=true`
- `deny`: `securityContext.privileged=true` en containers/initContainers
- `deny`: uso de `hostPath`
- `warn`: imagen con tag `:latest` (opcional)

## Docker Compose (`docker-compose.rego`)
- `deny`: `privileged=true`
- `deny`: montaje de `/var/run/docker.sock`
- `deny`: puertos expuestos en servicios DB/Redis

## Uso rapido
```bash
conftest test k8s/**/*.yaml -p policies/conftest
conftest test docker-compose*.yml -p policies/conftest
```
