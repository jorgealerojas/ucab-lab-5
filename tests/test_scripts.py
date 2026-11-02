import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ScriptContractTests(unittest.TestCase):
    def test_presigned_url_uses_ohio_endpoint(self):
        script = (ROOT / "scripts/create-temporary-link.sh").read_text(encoding="utf-8")
        self.assertIn('--endpoint-url "https://s3.${REGION}.amazonaws.com"', script)

    def test_all_aws_mutation_scripts_load_region_guard(self):
        names = [
            "cleanup-lab.sh",
            "create-temporary-link.sh",
            "deploy-lab.sh",
            "run-experiment.sh",
            "test-anonymous-access.sh",
        ]
        for name in names:
            with self.subTest(name=name):
                script = (ROOT / "scripts" / name).read_text(encoding="utf-8")
                self.assertIn("require_ohio", script)


if __name__ == "__main__":
    unittest.main()
