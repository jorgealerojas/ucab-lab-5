import json
import unittest
from pathlib import Path

from app.evidence import build_summary


ROOT = Path(__file__).resolve().parents[1]


class EvidenceTests(unittest.TestCase):
    def test_builds_summary_with_counts_and_scenarios(self):
        inventory = {
            "account": "123456789012",
            "provider": "aws",
            "region": "us-east-2",
            "deployment_model": "publica",
            "buckets": [{}, {}],
        }
        policy = {
            "input_count": 6,
            "accepted_count": 3,
            "rejected_count": 3,
            "approved_checksum": "abc",
        }
        summary = build_summary(
            inventory,
            policy,
            [ROOT / "scenarios/publica.json", ROOT / "scenarios/multinube.json"],
        )
        self.assertIn("Registros aceptados: `3`", summary)
        self.assertIn("referencia-aws-ohio", summary)
        self.assertIn("comercio-multinube", summary)


if __name__ == "__main__":
    unittest.main()
