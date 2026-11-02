"""Construye un resumen reproducible que el estudiante puede anexar a su informe."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Sequence

from app.model_checker import evaluate, load_manifest


def build_summary(
    inventory: dict[str, Any],
    policy_report: dict[str, Any],
    scenario_paths: list[Path],
) -> str:
    lines = [
        "# Resumen técnico generado",
        "",
        "## Arquitectura observada",
        "",
        f"- Cuenta: `{inventory['account']}`",
        f"- Proveedor: `{inventory['provider']}`",
        f"- Región: `{inventory['region']}`",
        f"- Modelo observado: `{inventory['deployment_model']}`",
        f"- Buckets inspeccionados: `{len(inventory['buckets'])}`",
        "",
        "## Política de datos",
        "",
        f"- Registros de entrada: `{policy_report['input_count']}`",
        f"- Registros aceptados: `{policy_report['accepted_count']}`",
        f"- Registros rechazados: `{policy_report['rejected_count']}`",
        f"- Checksum aprobado: `{policy_report['approved_checksum']}`",
        "",
        "## Escenarios",
        "",
        "| Escenario | Modelo NIST | Multinube | Consistente |",
        "|---|---|---:|---:|",
    ]
    for path in sorted(scenario_paths):
        result = evaluate(load_manifest(path))
        lines.append(
            f"| {result['id']} | {result['model']} | "
            f"{'sí' if result['multicloud'] else 'no'} | "
            f"{'sí' if result['valid'] else 'no'} |"
        )
    lines.extend(
        [
            "",
            "> Este resumen registra resultados técnicos. Las explicaciones y respuestas deben redactarse con palabras propias.",
            "",
        ]
    )
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inventory", required=True, type=Path)
    parser.add_argument("--policy-report", required=True, type=Path)
    parser.add_argument("--scenarios", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args(argv)
    inventory = json.loads(args.inventory.read_text(encoding="utf-8"))
    policy_report = json.loads(args.policy_report.read_text(encoding="utf-8"))
    summary = build_summary(inventory, policy_report, list(args.scenarios.glob("*.json")))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(summary, encoding="utf-8")
    print(f"Resumen guardado en {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
