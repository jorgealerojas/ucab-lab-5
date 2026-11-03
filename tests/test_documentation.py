import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class DocumentationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.guide = (ROOT / "LAB_GUIDE.md").read_text(encoding="utf-8")

    def test_all_guide_images_exist(self):
        references = re.findall(r"!\[[^]]*\]\(([^)]+)\)", self.guide)
        self.assertEqual(3, len(references))
        for reference in references:
            with self.subTest(reference=reference):
                self.assertTrue((ROOT / reference).is_file())

    def test_guide_states_simulation_limits(self):
        self.assertIn("Alcance y límites de la simulación", self.guide)
        self.assertIn("no una implementación completa", self.guide)
        self.assertIn("nube pública de AWS", self.guide)


if __name__ == "__main__":
    unittest.main()
