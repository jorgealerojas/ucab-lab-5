"""Genera un inventario reproducible del stack y sus controles S3."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any, Callable, Sequence


REGION = "us-east-2"
Runner = Callable[[list[str]], Any]


def run_aws(arguments: list[str]) -> Any:
    command = ["aws", *arguments, "--region", REGION, "--output", "json"]
    completed = subprocess.run(command, check=True, capture_output=True, text=True)
    return json.loads(completed.stdout or "{}")


def _outputs(stack: dict[str, Any]) -> dict[str, str]:
    stacks = stack.get("Stacks", [])
    if len(stacks) != 1:
        raise ValueError("no se encontró exactamente un stack")
    return {
        item["OutputKey"]: item["OutputValue"]
        for item in stacks[0].get("Outputs", [])
    }


def collect_inventory(stack_name: str, runner: Runner = run_aws) -> dict[str, Any]:
    identity = runner(["sts", "get-caller-identity"])
    stack = runner(["cloudformation", "describe-stacks", "--stack-name", stack_name])
    outputs = _outputs(stack)
    buckets = []
    for purpose, key in (("recepcion", "IntakeBucketName"), ("aprobados", "CuratedBucketName")):
        name = outputs[key]
        location = runner(["s3api", "get-bucket-location", "--bucket", name])
        encryption = runner(["s3api", "get-bucket-encryption", "--bucket", name])
        public_access = runner(["s3api", "get-public-access-block", "--bucket", name])
        versioning = runner(["s3api", "get-bucket-versioning", "--bucket", name])
        buckets.append(
            {
                "name": name,
                "purpose": purpose,
                "region": location.get("LocationConstraint") or "us-east-1",
                "versioning": versioning.get("Status"),
                "encryption": encryption["ServerSideEncryptionConfiguration"]["Rules"][0][
                    "ApplyServerSideEncryptionByDefault"
                ]["SSEAlgorithm"],
                "block_public_access": public_access["PublicAccessBlockConfiguration"],
            }
        )
    return {
        "account": identity["Account"],
        "principal_arn": identity["Arn"],
        "provider": "aws",
        "deployment_model": "publica",
        "region": REGION,
        "stack": stack_name,
        "buckets": buckets,
        "observations": [
            "Los recursos sin acceso público continúan dentro de la nube pública de AWS.",
            "Dos buckets del mismo proveedor no constituyen multinube.",
            "Separar datos en dos buckets del mismo entorno no constituye nube híbrida.",
        ],
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stack-name", default="ucab-lab-5")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    inventory = collect_inventory(args.stack_name)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(inventory, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(inventory, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
