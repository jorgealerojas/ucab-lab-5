import unittest

from app.cleanup_bucket import empty_versioned_bucket


class CleanupBucketTests(unittest.TestCase):
    def test_deletes_versions_and_markers_until_empty(self):
        calls = []
        pages = [
            {
                "Versions": [{"Key": "a", "VersionId": "1"}],
                "DeleteMarkers": [{"Key": "b", "VersionId": "2"}],
            },
            {},
        ]

        def runner(arguments):
            calls.append(arguments)
            if arguments[1] == "list-object-versions":
                return pages.pop(0)
            if arguments[1] == "delete-objects":
                return {"Deleted": []}
            raise AssertionError(arguments)

        count = empty_versioned_bucket("bucket", runner)
        self.assertEqual(2, count)
        self.assertEqual(2, sum(call[1] == "list-object-versions" for call in calls))
        self.assertEqual(1, sum(call[1] == "delete-objects" for call in calls))


if __name__ == "__main__":
    unittest.main()
