#!/usr/bin/env bash

set -euo pipefail

readonly REGION="us-east-2"
readonly STACK_NAME="ucab-lab-5"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
readonly REPO_ROOT
# shellcheck disable=SC2034
readonly GENERATED_DIR="${REPO_ROOT}/generated"

fail() {
  printf 'ERROR: %s\n' "$*" >&2
  exit 1
}

require_tool() {
  command -v "$1" >/dev/null 2>&1 || fail "No se encontró la herramienta requerida: $1"
}

effective_region() {
  if [[ -n "${AWS_REGION:-}" ]]; then
    printf '%s\n' "${AWS_REGION}"
  elif [[ -n "${AWS_DEFAULT_REGION:-}" ]]; then
    printf '%s\n' "${AWS_DEFAULT_REGION}"
  else
    aws configure get region 2>/dev/null || true
  fi
}

require_ohio() {
  local configured
  configured="$(effective_region)"
  [[ "${configured}" == "${REGION}" ]] || fail \
    "La región efectiva es '${configured:-sin configurar}'. Debe ser ${REGION} (Ohio)."
  [[ -z "${AWS_REGION:-}" || "${AWS_REGION}" == "${REGION}" ]] || fail \
    "AWS_REGION debe ser ${REGION}."
  [[ -z "${AWS_DEFAULT_REGION:-}" || "${AWS_DEFAULT_REGION}" == "${REGION}" ]] || fail \
    "AWS_DEFAULT_REGION debe ser ${REGION}."
}

stack_output() {
  local output_key="$1"
  aws cloudformation describe-stacks \
    --stack-name "${STACK_NAME}" \
    --query "Stacks[0].Outputs[?OutputKey=='${output_key}'].OutputValue | [0]" \
    --output text \
    --region "${REGION}"
}
