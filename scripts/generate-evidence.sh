#!/usr/bin/env bash

set -euo pipefail
# shellcheck source=scripts/common.sh
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/common.sh"

require_tool python3
[[ -f "${GENERATED_DIR}/inventory.json" ]] || fail "Falta generated/inventory.json. Ejecuta inspect-aws.sh."
[[ -f "${GENERATED_DIR}/policy_report.json" ]] || fail "Falta generated/policy_report.json. Ejecuta run-experiment.sh."

cd "${REPO_ROOT}"
python3 -m app.evidence \
  --inventory "generated/inventory.json" \
  --policy-report "generated/policy_report.json" \
  --scenarios "scenarios" \
  --output "generated/technical-summary.md"
