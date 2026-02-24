package clinical.docker_compose

# Stub mínimo funcional para desarrollo colaborativo
default allow = true
package clinical.docker_compose

# Minimal baseline:
# - deny privileged
# - deny docker.sock mount
# - deny exposed ports on DB/Redis services (when applicable)

deny[msg] {
  service(name, svc)
  object.get(svc, "privileged", false) == true
  msg := sprintf("service %q: privileged=true no permitido", [name])
}

deny[msg] {
  service(name, svc)
  vol := object.get(svc, "volumes", [])[_]
  mounts_docker_sock(vol)
  msg := sprintf("service %q: montaje de /var/run/docker.sock no permitido", [name])
}

deny[msg] {
  service(name, svc)
  is_db_or_redis_service(name, svc)
  has_published_ports(svc)
  msg := sprintf("service %q: no exponer puertos de DB/Redis", [name])
}

# Helpers

service(name, svc) {
  services := object.get(input, "services", {})
  svc := services[name]
}

is_db_or_redis_service(name, svc) {
  _ := object.get(svc, "image", "")
  contains(lower(name), "postgres")
}

is_db_or_redis_service(name, svc) {
  _ := object.get(svc, "image", "")
  contains(lower(name), "redis")
}

is_db_or_redis_service(name, svc) {
  image := lower(object.get(svc, "image", ""))
  contains(image, "postgres")
}

is_db_or_redis_service(name, svc) {
  image := lower(object.get(svc, "image", ""))
  contains(image, "redis")
}

has_published_ports(svc) {
  ports := object.get(svc, "ports", [])
  count(ports) > 0
}

mounts_docker_sock(vol) {
  is_string(vol)
  contains(lower(vol), "/var/run/docker.sock")
}

mounts_docker_sock(vol) {
  is_object(vol)
  source := lower(object.get(vol, "source", ""))
  source == "/var/run/docker.sock"
}

mounts_docker_sock(vol) {
  is_object(vol)
  target := lower(object.get(vol, "target", ""))
  target == "/var/run/docker.sock"
}
