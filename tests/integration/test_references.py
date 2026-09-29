"""T022: tooltip data, reference following and freshness over HTTP (AC-4 to AC-6, AC-9, AC-11, AC-15, AC-18, CH-015)."""

import os
import shutil
import tempfile
import time
import unittest
from pathlib import Path

from .support import FIXTURE, ServerTestCase


class ReferencesTest(ServerTestCase):
    def test_tooltip_carries_the_whole_defining_section(self):  # AC-4, AC-11
        _, page = self.get("/specs/001-demo/s02-functional-spec.md")
        refs = self.refs(page)
        self.assertEqual(refs["REQ-002"]["state"], "resolved")
        self.assertEqual(refs["REQ-002"]["doc"], "s01-requirements.md")
        self.assertIn("Hovering a code shows its definition.", refs["REQ-002"]["html"])
        self.assertIn("the developer opens a page", refs["UC-001"]["html"])  # a heading's whole section
        self.assertEqual(refs["REQ-900"], {"state": "unresolved"})  # defined only in another story

    def test_errors_and_same_document_codes(self):  # AC-6, FR-011
        refs = self.refs(self.get("/specs/001-demo/s02-functional-spec.md")[1])
        self.assertEqual(refs["FR-777"], {"state": "unresolved"})
        self.assertEqual(refs["UC-050"], {"state": "ambiguous", "documents": ["notes.md", "s03-technical-spec.md"]})
        self.assertEqual(refs["NFR-001"]["href"], "/specs/001-demo/s02-functional-spec.md#nfr-001")

    def test_following_a_reference_opens_its_anchor(self):  # AC-5
        href = self.refs(self.get("/specs/001-demo/s02-functional-spec.md")[1])["REQ-001"]["href"]
        path, anchor = href.split("#")
        status, page = self.get(path)
        self.assertEqual(status, 200)
        self.assertIn('id="%s"' % anchor, page)

    def test_challenge_code(self):  # AC-15, FR-022
        ref = self.refs(self.get("/specs/001-demo/s02-functional-spec.md")[1])["CH-001"]
        self.assertEqual(ref["href"], "/specs/001-demo/s02-functional-spec.md#challenges")
        for text in ("FR-002 does not say what a tooltip holds.", "FR-002", "accepted", "Lee Sinclair", "the whole section"):
            self.assertIn(text, ref["html"])

    def test_alias_page_shows_no_ambiguity(self):  # AC-18
        for alias in ("spec.md", "plan.md"):
            with self.subTest(alias=alias):
                status, page = self.get("/specs/001-demo/" + alias)
                self.assertEqual(status, 200)
                self.assertNotIn('class="ref ref-error"', page)

    def test_tooltip_sections_have_no_marked_codes_or_diagrams(self):  # FR-021, FR-023
        refs = self.refs(self.get("/specs/001-demo/spec.md")[1])
        self.assertIn("REQ-002, UC-001", refs["FR-002"]["html"])  # codes shown as plain text
        self.assertNotIn('class="ref', refs["FR-002"]["html"])

    def test_embedded_json_cannot_close_the_script(self):  # DEC-004
        _, page = self.get("/specs/001-demo/s02-functional-spec.md")
        start = page.index('id="refs">')
        self.assertNotIn("<", page[start + len('id="refs">') : page.index("</script>", start)])


class FreshnessTest(ServerTestCase):  # AC-9, CH-015
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.start = Path(cls.tmp.name) / "project"
        shutil.copytree(FIXTURE, cls.start, symlinks=True)
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.tmp.cleanup()

    def test_changing_another_document_updates_the_tooltip(self):
        page = "/specs/001-demo/s02-functional-spec.md"
        self.assertIn("Hovering a code shows its definition.", self.refs(self.get(page)[1])["REQ-002"]["html"])
        source = self.start / "specs" / "001-demo" / "s01-requirements.md"
        text = source.read_text().replace("Hovering a code shows its definition.", "Hovering shows the NEW text.")
        source.write_text(text)
        later = time.time_ns() + 5_000_000_000
        os.utime(source, ns=(later, later))  # be sure the timestamp moves on coarse file systems
        self.assertIn("Hovering shows the NEW text.", self.refs(self.get(page)[1])["REQ-002"]["html"])


if __name__ == "__main__":
    unittest.main()
