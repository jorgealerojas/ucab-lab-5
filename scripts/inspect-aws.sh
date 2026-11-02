#!/usr/bin/env bash

set -euo pipefail
# shellcheck source=scripts/common.sh
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/common.sh"

require_tool aws
require_tool python3
require_ohio
mkdir -p "${GENERATED_DIR}"

cd "${REPO_ROOT}"
python3 -m app.inventory \
  --stack-name "${STACK_NAME}" \
  --output "${GENERATED_DIR}/inventory.json"
printf 'Inventario guardado en generated/inventory.json\n'
