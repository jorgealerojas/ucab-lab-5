"""Política didáctica para publicar registros de investigación ficticios."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any, Iterable


REQUIRED_FIELDS = {"id", "category", "value", "timestamp"}
RESTRICTED_FIELDS = {
    "cedula",
    "correo",
    "email",
    "nombre",
    "phone",
    "telefono",
}


@dataclass(frozen=True)
class ValidationResult:
    accepted: bool
    reasons: tuple[str, ...]


def _field_names(value: Any) -> Iterable[str]:
    if isinstance(value, dict):
        for key, nested in value.items():
            yield str(key).casefold()
            yield from _field_names(nested)
    elif isinstance(value, list):
        for nested in value:
            yield from _field_names(nested)


def validate_record(record: Any) -> ValidationResult:
    """Valida estructura mínima y ausencia de campos restringidos."""

    reasons: list[str] = []
    if not isinstance(record, dict):
        return ValidationResult(False, ("el registro no es un objeto JSON",))

    missing = sorted(REQUIRED_FIELDS - set(record))
    if missing:
        reasons.append(f"faltan campos obligatorios: {', '.join(missing)}")

    restricted = sorted(set(_field_names(record)) & RESTRICTED_FIELDS)
    if restricted:
        reasons.append(f"contiene campos restringidos: {', '.join(restricted)}")

    if "id" in record and (not isinstance(record["id"], str) or not record["id"].strip()):
        reasons.append("id debe ser un texto no vacío")
    if "value" in record and not isinstance(record["value"], (int, float)):
        reasons.append("value debe ser numérico")

    return ValidationResult(not reasons, tuple(reasons))


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def checksum(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def apply_policy(records: Any) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Separa registros aceptados y rechazados, conservando las razones."""

    if not isinstance(records, list):
        raise ValueError("el documento de entrada debe contener una lista JSON")

    accepted: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    seen_ids: set[str] = set()

    for position, record in enumerate(records):
        result = validate_record(record)
        reasons = list(result.reasons)
        record_id = record.get("id") if isinstance(record, dict) else None
        if isinstance(record_id, str) and record_id in seen_ids:
            reasons.append("id duplicado")

        if reasons:
            rejected.append(
                {
                    "position": position,
                    "id": record_id,
                    "reasons": reasons,
                }
            )
            continue

        seen_ids.add(record_id)
        accepted.append(record)

    return accepted, rejected
