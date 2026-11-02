import json
import unittest
from pathlib import Path

from app.model_checker import classify, evaluate, load_manifest


ROOT = Path(__file__).resolve().parents[1]


class ModelCheckerTests(unittest.TestCase):
    def test_repository_scenarios_are_consistent(self):
        results = [evaluate(load_manifest(path)) for path in sorted((ROOT / "scenarios").glob("*.json"))]
        self.assertEqual(5, len(results))
        self.assertTrue(all(result["valid"] for result in results), results)

    def test_two_aws_resources_are_not_multicloud(self):
        manifest = json.loads((ROOT / "scenarios/publica.json").read_text(encoding="utf-8"))
        result = classify(manifest)
        self.assertEqual("publica", result.model)
        self.assertFalse(result.multicloud)

    def test_hybrid_can_also_be_multicloud(self):
        manifest = json.loads((ROOT / "scenarios/hibrida.json").read_text(encoding="utf-8"))
        manifest["infrastructures"].append(
            {
                "id": "analytics-b",
                "provider": "provider-b",
                "deployment": "publica",
            }
        )
        result = classify(manifest)
        self.assertEqual("hibrida", result.model)
        self.assertTrue(result.multicloud)

    def test_shared_public_provider_is_not_community_cloud(self):
        manifest = {
            "organizations": ["a", "b"],
            "infrastructures": [
                {"id": "shared", "provider": "aws", "deployment": "publica"}
            ],
            "integrated": False,
            "common_governance": True,
            "community_exclusive": False,
            "exclusive_organization": False,
        }
        result = classify(manifest)
        self.assertEqual("publica", result.model)

    def test_rejects_ambiguous_evidence(self):
        manifest = {
            "organizations": ["a", "b"],
            "infrastructures": [
                {"id": "x", "provider": "x", "deployment": "comunitaria"}
            ],
            "integrated": False,
            "common_governance": False,
            "community_exclusive": False,
            "exclusive_organization": False,
        }
        with self.assertRaisesRegex(ValueError, "no permite"):
            classify(manifest)

    def test_detects_incorrect_claim(self):
        manifest = json.loads((ROOT / "scenarios/publica.json").read_text(encoding="utf-8"))
        manifest["claimed_model"] = "privada"
        result = evaluate(manifest)
        self.assertFalse(result["valid"])
        self.assertIn("no coincide", result["errors"][0])


if __name__ == "__main__":
    unittest.main()
