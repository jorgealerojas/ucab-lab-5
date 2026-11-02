import unittest

from app.inventory import collect_inventory


class FakeAws:
    def __call__(self, arguments):
        service, operation = arguments[:2]
        if (service, operation) == ("sts", "get-caller-identity"):
            return {"Account": "123456789012", "Arn": "arn:aws:iam::123456789012:user/test"}
        if (service, operation) == ("cloudformation", "describe-stacks"):
            return {
                "Stacks": [
                    {
                        "Outputs": [
                            {"OutputKey": "IntakeBucketName", "OutputValue": "intake"},
                            {"OutputKey": "CuratedBucketName", "OutputValue": "curated"},
                        ]
                    }
                ]
            }
        if operation == "get-bucket-location":
            return {"LocationConstraint": "us-east-2"}
        if operation == "get-bucket-encryption":
            return {
                "ServerSideEncryptionConfiguration": {
                    "Rules": [
                        {"ApplyServerSideEncryptionByDefault": {"SSEAlgorithm": "AES256"}}
                    ]
                }
            }
        if operation == "get-public-access-block":
            return {
                "PublicAccessBlockConfiguration": {
                    "BlockPublicAcls": True,
                    "IgnorePublicAcls": True,
                    "BlockPublicPolicy": True,
                    "RestrictPublicBuckets": True,
                }
            }
        if operation == "get-bucket-versioning":
            return {"Status": "Enabled"}
        raise AssertionError(arguments)


class InventoryTests(unittest.TestCase):
    def test_collects_two_buckets_and_conceptual_facts(self):
        inventory = collect_inventory("ucab-lab-5", FakeAws())
        self.assertEqual("us-east-2", inventory["region"])
        self.assertEqual("publica", inventory["deployment_model"])
        self.assertEqual(2, len(inventory["buckets"]))
        self.assertTrue(
            all(bucket["versioning"] == "Enabled" for bucket in inventory["buckets"])
        )

    def test_requires_exactly_one_stack(self):
        fake = FakeAws()

        def runner(arguments):
            if arguments[:2] == ["cloudformation", "describe-stacks"]:
                return {"Stacks": []}
            return fake(arguments)

        with self.assertRaisesRegex(ValueError, "exactamente un stack"):
            collect_inventory("missing", runner)


if __name__ == "__main__":
    unittest.main()
