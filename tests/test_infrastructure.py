import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class InfrastructureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.template = (ROOT / "infra/lab-stack.yaml").read_text(encoding="utf-8")

    def test_restricts_deployment_to_ohio(self):
        self.assertIn('!Equals [!Ref "AWS::Region", us-east-2]', self.template)

    def test_defines_exactly_two_buckets(self):
        self.assertEqual(2, self.template.count("Type: AWS::S3::Bucket"))

    def test_declares_required_bucket_controls(self):
        self.assertEqual(2, self.template.count("ObjectOwnership: BucketOwnerEnforced"))
        self.assertEqual(2, self.template.count("BlockPublicAcls: true"))
        self.assertEqual(2, self.template.count("RestrictPublicBuckets: true"))
        self.assertEqual(2, self.template.count("SSEAlgorithm: AES256"))
        self.assertEqual(
            2,
            self.template.count("VersioningConfiguration:\n        Status: Enabled"),
        )


if __name__ == "__main__":
    unittest.main()
