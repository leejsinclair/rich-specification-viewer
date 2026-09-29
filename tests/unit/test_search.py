"""T015: glob search (DEC-005, FR-002)."""

import tempfile
import unittest
from pathlib import Path

import specview

FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "project"


def files(result):
    return [(r["story"] or "") + "/" + r["file"] for r in result["results"]]


class SearchTest(unittest.TestCase):
    def setUp(self):
        self.viewer = specview.Viewer(FIXTURE)

    def test_glob_pattern_matches_paths(self):
        self.assertEqual(files(self.viewer.search("*/s01-*")), ["001-demo/s01-requirements.md", "002-other/s01-requirements.md"])

    def test_plain_word_is_a_contains_match(self):
        self.assertIn("001-demo/checklists/requirements.md", files(self.viewer.search("checklists")))

    def test_matching_ignores_case(self):
        self.assertEqual(files(self.viewer.search("*/S01-*")), files(self.viewer.search("*/s01-*")))

    def test_results_are_sorted_by_path(self):
        found = files(self.viewer.search("*.md"))
        self.assertEqual(found, sorted(found, key=str.lower))
        self.assertIn("/README.md", found)  # a file directly in specs/ has no story

    def test_no_match_and_empty_pattern(self):
        self.assertEqual(self.viewer.search("zzz-nothing")["results"], [])
        self.assertEqual(self.viewer.search("   ")["results"], [])
        self.assertTrue(self.viewer.search("")["specs"])

    def test_no_specs_folder(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(specview.Viewer(Path(tmp)).search("x"), {"specs": False, "results": []})

    def test_hrefs_point_at_document_pages(self):
        result = self.viewer.search("*/s02-*")["results"][0]
        self.assertEqual(result["href"], "/specs/001-demo/s02-functional-spec.md")


if __name__ == "__main__":
    unittest.main()
