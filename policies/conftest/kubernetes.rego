package clinical.kubernetes

# Stub mínimo funcional para desarrollo colaborativo
default allow = true
package clinical.kubernetes

# Minimal baseline:
# - deny privileged
# - deny hostNetwork
# - deny hostPath
# - warn latest tag (optional; does not fail by default)

deny[msg] {
  pod_spec(spec)
  spec.hostNetwork == true
  msg := sprintf("%s/%s: hostNetwork=true no permitido", [kind_name, resource_name])
}

deny[msg] {
  c := containers[_]
  c.securityContext.privileged == true
  msg := sprintf("%s/%s: container %q privileged=true no permitido", [kind_name, resource_name, container_name(c)])
}

deny[msg] {
  v := volumes[_]
  v.hostPath
  msg := sprintf("%s/%s: volumen hostPath no permitido", [kind_name, resource_name])
}

warn[msg] {
  c := containers[_]
  endswith(lower(c.image), ":latest")
  msg := sprintf("%s/%s: container %q usa tag :latest (opcional: evitar)", [kind_name, resource_name, container_name(c)])
}

# Helpers

kind_name = k {
  k := object.get(input, "kind", "UnknownKind")
}

resource_name = n {
  metadata := object.get(input, "metadata", {})
  n := object.get(metadata, "name", "unknown")
}

container_name(c) = n {
  n := object.get(c, "name", "<unnamed>")
}

pod_spec(spec) {
  input.kind == "Pod"
  spec := object.get(input, "spec", {})
}

pod_spec(spec) {
  spec_obj := object.get(input, "spec", {})
  template := object.get(spec_obj, "template", {})
  spec := object.get(template, "spec", {})
  count(spec) > 0
}

containers[c] {
  pod_spec(spec)
  c := object.get(spec, "containers", [])[_]
}

containers[c] {
  pod_spec(spec)
  c := object.get(spec, "initContainers", [])[_]
}

volumes[v] {
  pod_spec(spec)
  v := object.get(spec, "volumes", [])[_]
}
