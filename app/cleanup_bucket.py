"""Vacía de forma segura un bucket versionado antes de eliminar el stack."""

from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Callable, Sequence


REGION = "us-east-2"
Runner = Callable[[list[str]], Any]


def run_aws(arguments: list[str]) -> Any:
    command = ["aws", *arguments, "--region", REGION, "--output", "json"]
    completed = subprocess.run(command, check=True, capture_output=True, text=True)
    return json.loads(completed.stdout or "{}")


def empty_versioned_bucket(bucket: str, runner: Runner = run_aws) -> int:
    deleted = 0
    while True:
        page = runner(["s3api", "list-object-versions", "--bucket", bucket])
        objects = [
            {"Key": item["Key"], "VersionId": item["VersionId"]}
            for group in ("Versions", "DeleteMarkers")
            for item in page.get(group, [])
        ]
        if not objects:
            return deleted
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".json") as handle:
            json.dump({"Objects": objects, "Quiet": True}, handle)
            handle.flush()
            runner(
                [
                    "s3api",
                    "delete-objects",
                    "--bucket",
                    bucket,
                    "--delete",
                    f"file://{handle.name}",
                ]
            )
        deleted += len(objects)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bucket", required=True)
    args = parser.parse_args(argv)
    count = empty_versioned_bucket(args.bucket)
    print(f"Bucket {args.bucket}: {count} versión(es) eliminada(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
