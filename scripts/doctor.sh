#!/usr/bin/env bash

set -euo pipefail
# shellcheck source=scripts/common.sh
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/common.sh"

require_tool aws
require_tool git
require_tool make
require_tool python3
require_ohio

printf 'OK  Región efectiva: %s\n' "$(effective_region)"

account_id="$(aws sts get-caller-identity --query Account --output text --region "${REGION}")"
[[ "${account_id}" =~ ^[0-9]{12}$ ]] || fail "AWS STS no devolvió una cuenta válida."
printf 'OK  Cuenta AWS accesible: %s\n' "${account_id}"

aws cloudformation validate-template \
  --template-body "file://${REPO_ROOT}/infra/lab-stack.yaml" \
  --region "${REGION}" \
  >/dev/null
printf 'OK  Plantilla CloudFormation válida.\n'

python3 -m unittest discover -s "${REPO_ROOT}/tests" -q
printf 'OK  Pruebas locales aprobadas.\n'
printf 'Entorno listo para desplegar en Ohio.\n'
