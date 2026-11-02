import json
import tempfile
import unittest
from pathlib import Path

from app.promote_data import promote


class PromoteDataTests(unittest.TestCase):
    def test_writes_approved_data_and_report(self):
        records = [
            {"id": "ok", "category": "temp", "value": 20, "timestamp": "2026"},
            {
                "id": "no",
                "category": "temp",
                "value": 21,
                "timestamp": "2026",
                "correo": "x@example.invalid",
            },
        ]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source.json"
            output = root / "nested" / "approved.json"
            report_path = root / "nested" / "report.json"
            source.write_text(json.dumps(records), encoding="utf-8")
            report = promote(source, output, report_path)
            self.assertEqual(1, report["accepted_count"])
            self.assertEqual("ok", json.loads(output.read_text(encoding="utf-8"))[0]["id"])
            self.assertEqual(report, json.loads(report_path.read_text(encoding="utf-8")))


if __name__ == "__main__":
    unittest.main()
