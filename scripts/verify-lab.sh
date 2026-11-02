#!/usr/bin/env bash

set -euo pipefail
# shellcheck source=scripts/common.sh
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/common.sh"

require_tool aws
require_tool python3
require_ohio

status="$(aws cloudformation describe-stacks --stack-name "${STACK_NAME}" --query 'Stacks[0].StackStatus' --output text --region "${REGION}")"
[[ "${status}" == *_COMPLETE ]] || fail "El stack no está completo: ${status}"
printf 'OK  Stack completo: %s\n' "${status}"

intake_bucket="$(stack_output IntakeBucketName)"
curated_bucket="$(stack_output CuratedBucketName)"
for bucket in "${intake_bucket}" "${curated_bucket}"; do
  versioning="$(aws s3api get-bucket-versioning --bucket "${bucket}" --query Status --output text --region "${REGION}")"
  [[ "${versioning}" == "Enabled" ]] || fail "Versionado no habilitado en ${bucket}."
  public_flags="$(aws s3api get-public-access-block --bucket "${bucket}" --query 'PublicAccessBlockConfiguration.*' --output text --region "${REGION}")"
  [[ "${public_flags}" == $'True\tTrue\tTrue\tTrue' ]] || fail "Block Public Access incompleto en ${bucket}."
  printf 'OK  Controles activos: %s\n' "${bucket}"
done

aws s3api head-object \
  --bucket "${intake_bucket}" \
  --key incoming/mixed_records.json \
  --region "${REGION}" \
  >/dev/null
printf 'OK  Datos originales presentes.\n'

aws s3api head-object \
  --bucket "${curated_bucket}" \
  --key approved/approved_records.json \
  --region "${REGION}" \
  >/dev/null
printf 'OK  Datos aprobados presentes.\n'

mkdir -p "${GENERATED_DIR}"
cd "${REPO_ROOT}"
python3 -m app.inventory --stack-name "${STACK_NAME}" --output "${GENERATED_DIR}/inventory.json" >/dev/null
python3 -m app.model_checker scenarios/*.json >/dev/null
python3 -m unittest discover -s tests -q
printf 'VERIFICACIÓN INTEGRAL APROBADA\n'
