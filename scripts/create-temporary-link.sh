#!/usr/bin/env bash

set -euo pipefail
# shellcheck source=scripts/common.sh
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/common.sh"

require_tool aws
require_ohio
curated_bucket="$(stack_output CuratedBucketName)"

printf 'URL temporal válida durante 120 segundos:\n'
aws s3 presign \
  "s3://${curated_bucket}/approved/approved_records.json" \
  --expires-in 120 \
  --endpoint-url "https://s3.${REGION}.amazonaws.com" \
  --region "${REGION}"
printf 'No incluyas una URL todavía vigente en el informe.\n'
