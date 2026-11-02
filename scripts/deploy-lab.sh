#!/usr/bin/env bash

set -euo pipefail
# shellcheck source=scripts/common.sh
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/common.sh"

require_tool aws
require_ohio

printf 'Creando o actualizando el stack %s en %s...\n' "${STACK_NAME}" "${REGION}"
aws cloudformation deploy \
  --stack-name "${STACK_NAME}" \
  --template-file "${REPO_ROOT}/infra/lab-stack.yaml" \
  --no-fail-on-empty-changeset \
  --tags Course=UCAB-Cloud Lab=5 \
  --region "${REGION}"

intake_bucket="$(stack_output IntakeBucketName)"
curated_bucket="$(stack_output CuratedBucketName)"
printf 'LABORATORIO LISTO\n'
printf 'Stack: %s\n' "${STACK_NAME}"
printf 'Bucket de recepción: %s\n' "${intake_bucket}"
printf 'Bucket de aprobados: %s\n' "${curated_bucket}"
