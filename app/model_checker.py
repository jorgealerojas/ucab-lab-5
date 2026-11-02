"""Clasificador didáctico basado en evidencia explícita de arquitectura."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence


NIST_MODELS = {"publica", "privada", "hibrida", "comunitaria"}


@dataclass(frozen=True)
class Classification:
    model: str
    multicloud: bool
    evidence: tuple[str, ...]


def classify(manifest: dict[str, Any]) -> Classification:
    organizations = manifest.get("organizations", [])
    infrastructures = manifest.get("infrastructures", [])
    providers = {
        item.get("provider")
        for item in infrastructures
        if item.get("provider")
        and item.get("counts_for_multicloud", item.get("deployment") == "publica")
    }
    deployments = {item.get("deployment") for item in infrastructures}
    integrated = bool(manifest.get("integrated"))
    common_governance = bool(manifest.get("common_governance"))
    community_exclusive = bool(manifest.get("community_exclusive"))
    exclusive_organization = bool(manifest.get("exclusive_organization"))
    evidence: list[str] = []

    if not organizations:
        raise ValueError("se requiere al menos una organización")
    if not infrastructures:
        raise ValueError("se requiere al menos una infraestructura")
    if not deployments <= {"publica", "privada", "comunitaria"}:
        raise ValueError("deployment solo admite publica, privada o comunitaria")

    if len(infrastructures) >= 2 and len(deployments) >= 2 and integrated:
        model = "hibrida"
        evidence.append("combina infraestructuras cloud distintas con integración")
    elif (
        len(organizations) >= 2
        and common_governance
        and community_exclusive
        and deployments == {"comunitaria"}
    ):
        model = "comunitaria"
        evidence.append("infraestructura exclusiva para una comunidad con gobierno común")
    elif deployments == {"privada"} and exclusive_organization and len(organizations) == 1:
        model = "privada"
        evidence.append("uso exclusivo de una organización sobre una nube privada")
    elif deployments == {"publica"}:
        model = "publica"
        evidence.append("capacidades consumidas de uno o más proveedores de nube pública")
    else:
        raise ValueError("la evidencia no permite una clasificación NIST consistente")

    multicloud = len(providers) >= 2
    provider_names = ", ".join(sorted(providers)) if providers else "ninguno"
    evidence.append(
        f"{len(providers)} proveedor(es) público(s) externo(s) "
        f"considerado(s) para multinube: {provider_names}"
    )
    return Classification(model, multicloud, tuple(evidence))


def evaluate(manifest: dict[str, Any]) -> dict[str, Any]:
    result = classify(manifest)
    claimed_model = manifest.get("claimed_model")
    claimed_multicloud = manifest.get("claimed_multicloud")
    errors: list[str] = []
    if claimed_model not in NIST_MODELS:
        errors.append("claimed_model debe ser publica, privada, hibrida o comunitaria")
    elif claimed_model != result.model:
        errors.append(
            f"el modelo declarado ({claimed_model}) no coincide con la evidencia ({result.model})"
        )
    if not isinstance(claimed_multicloud, bool):
        errors.append("claimed_multicloud debe ser verdadero o falso")
    elif claimed_multicloud != result.multicloud:
        errors.append(
            "la estrategia multinube declarada no coincide con la cantidad de proveedores"
        )
    return {
        "id": manifest.get("id", "sin-id"),
        "model": result.model,
        "multicloud": result.multicloud,
        "evidence": list(result.evidence),
        "valid": not errors,
        "errors": errors,
    }


def load_manifest(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: el manifiesto debe ser un objeto JSON")
    return value


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args(argv)
    exit_code = 0
    for path in args.paths:
        try:
            result = evaluate(load_manifest(path))
        except (OSError, ValueError, json.JSONDecodeError) as error:
            result = {"id": path.stem, "valid": False, "errors": [str(error)]}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        if not result.get("valid"):
            exit_code = 1
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
