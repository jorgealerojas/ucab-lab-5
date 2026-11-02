import os
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMMON = ROOT / "scripts/common.sh"


class RegionGuardTests(unittest.TestCase):
    def run_guard(self, region):
        environment = dict(os.environ)
        environment["AWS_REGION"] = region
        environment["AWS_DEFAULT_REGION"] = region
        return subprocess.run(
            ["bash", "-c", f"source '{COMMON}'; require_ohio"],
            text=True,
            capture_output=True,
            env=environment,
        )

    def test_accepts_ohio(self):
        self.assertEqual(0, self.run_guard("us-east-2").returncode)

    def test_rejects_other_region(self):
        result = self.run_guard("us-east-1")
        self.assertNotEqual(0, result.returncode)
        self.assertIn("Debe ser us-east-2", result.stderr)


if __name__ == "__main__":
    unittest.main()
