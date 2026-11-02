#!/usr/bin/env bash

set -euo pipefail
# shellcheck source=scripts/common.sh
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/common.sh"

require_tool aws
require_tool python3
require_ohio

if ! aws cloudformation describe-stacks --stack-name "${STACK_NAME}" --region "${REGION}" >/dev/null 2>&1; then
  printf 'No existe el stack %s en Ohio. No hay recursos del laboratorio que eliminar.\n' "${STACK_NAME}"
  exit 0
fi

intake_bucket="$(stack_output IntakeBucketName)"
curated_bucket="$(stack_output CuratedBucketName)"
cd "${REPO_ROOT}"
python3 -m app.cleanup_bucket --bucket "${intake_bucket}"
python3 -m app.cleanup_bucket --bucket "${curated_bucket}"

printf 'Eliminando el stack %s...\n' "${STACK_NAME}"
aws cloudformation delete-stack --stack-name "${STACK_NAME}" --region "${REGION}"
aws cloudformation wait stack-delete-complete --stack-name "${STACK_NAME}" --region "${REGION}"
printf 'LIMPIEZA COMPLETADA: el stack ya no existe en Ohio.\n'
