#!/usr/bin/env bash

set -euo pipefail
# shellcheck source=scripts/common.sh
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/common.sh"

require_tool aws
require_ohio
curated_bucket="$(stack_output CuratedBucketName)"

set +e
output="$(aws s3api head-object \
  --bucket "${curated_bucket}" \
  --key approved/approved_records.json \
  --no-sign-request \
  --region "${REGION}" 2>&1)"
status=$?
set -e

if [[ ${status} -eq 0 ]]; then
  fail "El objeto aceptó una solicitud anónima; revisa Block Public Access."
fi
if [[ "${output}" != *"403"* && "${output}" != *"Forbidden"* ]]; then
  fail "La solicitud falló por una razón inesperada: ${output}"
fi
printf 'RESULTADO ESPERADO: acceso anónimo rechazado con HTTP 403.\n'
printf 'El recurso no es público, pero permanece dentro de la nube pública de AWS.\n'
