"""CLI para aplicar la política local y producir artefactos auditables."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from app.data_policy import apply_policy, checksum


def promote(input_path: Path, output_path: Path, report_path: Path) -> dict[str, object]:
    records = json.loads(input_path.read_text(encoding="utf-8"))
    accepted, rejected = apply_policy(records)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(accepted, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    report = {
        "input_count": len(records),
        "accepted_count": len(accepted),
        "rejected_count": len(rejected),
        "accepted_ids": [record["id"] for record in accepted],
        "rejected": rejected,
        "input_checksum": checksum(records),
        "approved_checksum": checksum(accepted),
    }
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--report", required=True, type=Path)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    report = promote(args.input, args.output, args.report)
    print(
        "Política aplicada: "
        f"{report['accepted_count']} aceptados, "
        f"{report['rejected_count']} rechazados"
    )
    print(f"Checksum aprobado: {report['approved_checksum']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
