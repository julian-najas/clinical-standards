#!/usr/bin/env bash
set -euo pipefail

OPA_DEFAULT_VERSION="v1.13.2"
OPA_DEFAULT_SHA256="c03641d62f8763295f74509fd1f827df70622d30275e1c75f1055b454b4d7eca"

OPA_VERSION="${OPA_VERSION:-${OPA_DEFAULT_VERSION}}"
OPA_SHA256="${OPA_SHA256:-}"

opa_url="https://openpolicyagent.org/downloads/${OPA_VERSION}/opa_linux_amd64_static"

curl -fsSL --retry 3 --retry-all-errors -o opa "${opa_url}"

if [ -n "${OPA_SHA256}" ]; then
  expected_sha="${OPA_SHA256}"
elif [ "${OPA_VERSION}" = "${OPA_DEFAULT_VERSION}" ]; then
  expected_sha="${OPA_DEFAULT_SHA256}"
else
  curl -fsSL --retry 3 --retry-all-errors -o opa.sha256 "${opa_url}.sha256"
  expected_sha="$(awk '{print $1}' opa.sha256)"
  if [ -z "${expected_sha}" ]; then
    echo "Unable to resolve checksum for OPA ${OPA_VERSION}"
    exit 1
  fi
fi

echo "${expected_sha}  opa" | sha256sum -c -
chmod +x opa
sudo mv opa /usr/local/bin/opa