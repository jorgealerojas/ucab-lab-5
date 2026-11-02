#!/usr/bin/env bash

set -euo pipefail
# shellcheck source=scripts/common.sh
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/common.sh"

require_tool python3
cd "${REPO_ROOT}"
python3 -m app.model_checker scenarios/*.json
