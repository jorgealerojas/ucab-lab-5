#!/usr/bin/env bash

set -euo pipefail
# shellcheck source=scripts/common.sh
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/common.sh"

require_tool aws
require_tool python3
require_ohio
mkdir -p "${GENERATED_DIR}"

intake_bucket="$(stack_output IntakeBucketName)"
curated_bucket="$(stack_output CuratedBucketName)"

printf '1/4 Cargando datos ficticios en el bucket de recepción...\n'
aws s3 cp \
  "${REPO_ROOT}/data/mixed_records.json" \
  "s3://${intake_bucket}/incoming/mixed_records.json" \
  --region "${REGION}" \
  --only-show-errors

printf '2/4 Aplicando la política local de publicación...\n'
cd "${REPO_ROOT}"
python3 -m app.promote_data \
  --input "data/mixed_records.json" \
  --output "generated/approved_records.json" \
  --report "generated/policy_report.json"

printf '3/4 Cargando solamente los registros aprobados...\n'
aws s3 cp \
  "${GENERATED_DIR}/approved_records.json" \
  "s3://${curated_bucket}/approved/approved_records.json" \
  --region "${REGION}" \
  --only-show-errors

printf '4/4 Guardando el reporte auditable junto a los datos aprobados...\n'
aws s3 cp \
  "${GENERATED_DIR}/policy_report.json" \
  "s3://${curated_bucket}/reports/policy_report.json" \
  --region "${REGION}" \
  --only-show-errors

printf 'EXPERIMENTO COMPLETADO\n'
python3 -m json.tool "${GENERATED_DIR}/policy_report.json"
