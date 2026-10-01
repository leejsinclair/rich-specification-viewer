"""Story 002: the "Documents in reading order" section over HTTP (US1 to US3, DEC-007)."""

import html
import os
import re
import shutil
import tempfile
import unittest
from pathlib import Path
from urllib.parse import quote

from .support import ServerTestCase


def section(page: str) -> str:
    match = re.search(r'<nav class="reading-order".*?</nav>', page, re.S)
    return match.group(0) if match else ""


def build(start: Path) -> None:
    specs = start / "specs"
    files = {
        "001-a/s00-intro.md": "# Intro\n",
        "001-a/s01-req.md": "# Req\n",
        "001-a/s02-func.md": "# Func\n",
        "001-a/s10-late.md": "# Late\n",
        "001-a/notes.md": "# Notes\n",
        "001-a/sub/s01-inner.md": "# Inner\n",
        "001-a/sub/readme.md": "# Readme\n",
        "001-a/sub/deeper/z.md": "# Z\n",
        "001-a/empty/keep.txt": "not markdown\n",
        "001-a/a<b>&\"c'd e.md": "# Odd\n",
        "002-b/s01-only.md": "# Only\n",
        "003-solo/s01-solo.md": "# Solo\n",
        "root.md": "# Root\n",
    }
    for name, text in files.items():
        path = specs / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
    (start / "secret.md").write_text("# Secret\n")
    if hasattr(os, "symlink"):
        (specs / "001-a" / "spec.md").symlink_to("s01-req.md")
        (specs / "001-a" / "to-b.md").symlink_to("../002-b/s01-only.md")
        (specs / "001-a" / "escape.md").symlink_to("../../secret.md")
        (specs / "001-a" / "linked").symlink_to("../002-b", target_is_directory=True)


class ReadingOrderTest(ServerTestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.start = Path(cls.tmp.name) / "project"
        build(cls.start)
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.tmp.cleanup()

    def page(self, path: str) -> str:
        status, body = self.get("/specs/" + quote(path))
        self.assertEqual(status, 200, path)
        return body

    def items(self, path: str) -> list[str]:
        return re.findall(r"<li>(.*?)</li>", section(self.page(path)))

    def test_region_name_heading_and_ordered_list(self):  # US1
        nav = section(self.page("001-a/s01-req.md"))
        self.assertIn('aria-label="Documents in reading order"', nav)
        self.assertIn("<h2>Documents in reading order</h2>", nav)
        self.assertIn("<ol>", nav)
        self.assertEqual(self.page("001-a/s01-req.md").count('class="reading-order"'), 1)

    def test_section_comes_after_the_document_body(self):
        page = self.page("001-a/s01-req.md")
        self.assertLess(page.index("Req</h1>"), page.index('class="reading-order"'))

    def test_order_is_natural_and_folders_follow_their_parents(self):  # FR-007 to FR-009
        labels = [re.sub(r"<.*?>", "", item) for item in self.items("001-a/s00-intro.md")]
        stripped = [re.sub(r" \(.*?\)$", "", label) for label in labels]
        expected = [
            "[stage 00: intro]",
            "[stage 01: req]",
            "[stage 02: func]",
            "[stage 10: late]",
            "a<b>&\"c'd e [ref doc: a<b>&\"c'd e]",
            "notes [ref doc: notes]",
            "sub/[stage 01: inner]",
            "sub/readme [ref doc: readme]",
            "sub/deeper/z [ref doc: z]",
        ]
        got = [html.unescape(label) for label in stripped]
        self.assertEqual([g for g in got if not g.startswith(("linked/", "to-b", "spec", "escape"))], expected)

    def test_exactly_one_current_entry_in_plain_text(self):  # US1
        for path in ("001-a/s00-intro.md", "001-a/sub/deeper/z.md", "001-a/notes.md"):
            nav = section(self.page(path))
            self.assertEqual(nav.count('aria-current="page"'), 1, path)
        nav = section(self.page("001-a/s02-func.md"))
        self.assertIn('<span aria-current="page">[stage 02: func]</span>', nav)
        self.assertNotIn('<a href="/specs/001-a/s02-func.md"', nav)

    def test_other_entries_are_links_to_their_documents(self):
        nav = section(self.page("001-a/s00-intro.md"))
        self.assertIn('<a href="/specs/001-a/s01-req.md">[stage 01: req]</a>', nav)
        self.assertIn('<a href="/specs/001-a/sub/deeper/z.md">sub/deeper/z [ref doc: z]</a>', nav)

    def test_the_same_list_on_every_document_of_the_story(self):  # NFR-001
        first = [re.sub(r"<.*?>", "", i) for i in self.items("001-a/s00-intro.md")]
        for path in ("001-a/notes.md", "001-a/sub/readme.md", "001-a/s10-late.md"):
            self.assertEqual([re.sub(r"<.*?>", "", i) for i in self.items(path)], first)

    @unittest.skipUnless(hasattr(os, "symlink"), "needs symbolic links")
    def test_alias_is_bracketed_after_its_document(self):  # FR-006
        nav = section(self.page("001-a/s00-intro.md"))
        self.assertIn('<a href="/specs/001-a/s01-req.md">[stage 01: req]</a> (spec.md)</li>', nav)
        self.assertNotIn(">spec [ref doc", nav)

    @unittest.skipUnless(hasattr(os, "symlink"), "needs symbolic links")
    def test_viewing_an_alias_marks_its_document_current(self):
        nav = section(self.page("001-a/spec.md"))
        self.assertIn('<span aria-current="page">[stage 01: req]</span> (spec.md)', nav)
        self.assertEqual(nav.count('aria-current="page"'), 1)

    @unittest.skipUnless(hasattr(os, "symlink"), "needs symbolic links")
    def test_cross_story_link_opens_the_real_path_and_nothing_outside_specs_is_listed(self):
        nav = section(self.page("001-a/s00-intro.md"))
        self.assertIn('<a href="/specs/002-b/s01-only.md">to-b [ref doc: to-b]</a>', nav)
        self.assertNotIn("escape", nav)
        self.assertNotIn("Secret", nav)

    @unittest.skipUnless(hasattr(os, "symlink"), "needs symbolic links")
    def test_document_viewed_through_a_linked_folder_is_current(self):  # CH-009
        nav = section(self.page("001-a/linked/s01-only.md"))
        self.assertEqual(nav.count('aria-current="page"'), 1)
        self.assertIn('<span aria-current="page">linked/[stage 01: only]</span>', nav)

    def test_story_isolation(self):  # US2
        nav = section(self.page("002-b/s01-only.md"))
        self.assertEqual(len(re.findall("<li>", nav)), 1)
        self.assertNotIn("001-a", nav)
        self.assertNotIn("intro", nav)
        solo = section(self.page("003-solo/s01-solo.md"))
        self.assertIn('<span aria-current="page">[stage 01: solo]</span>', solo)
        self.assertEqual(len(re.findall("<li>", solo)), 1)

    def test_a_folder_with_no_markdown_adds_no_entry(self):
        nav = section(self.page("001-a/s00-intro.md"))
        self.assertNotIn("empty", nav)
        self.assertNotIn("keep.txt", nav)

    def test_names_with_markup_characters_are_escaped_and_links_encoded(self):
        nav = section(self.page("001-a/s00-intro.md"))
        self.assertNotIn("<b>", nav)
        self.assertIn("a&lt;b&gt;&amp;&quot;c&#x27;d e [ref doc: a&lt;b&gt;&amp;&quot;c&#x27;d e]", nav)
        self.assertIn(quote("a<b>&\"c'd e.md"), nav)

    def test_document_without_a_section_outside_a_story(self):  # US3
        self.assertEqual(section(self.page("root.md")), "")

    def test_folder_pages_and_search_results_have_no_section(self):  # US3
        for path in ("/specs/", "/specs/001-a", "/specs/001-a/sub"):
            status, body = self.get(path)
            self.assertEqual(status, 200)
            self.assertNotIn('class="reading-order"', body, path)
        status, body = self.get("/api/search?q=%2A")
        self.assertEqual(status, 200)
        self.assertNotIn("reading-order", body)

    def test_path_safety_is_unchanged(self):
        self.assertEqual(self.get("/specs/..%2Fsecret.md")[0], 403)
        self.assertEqual(self.get("/specs/001-a/gone.md")[0], 404)


class RemovedDocumentTest(ServerTestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.start = Path(cls.tmp.name) / "project"
        build(cls.start)
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.tmp.cleanup()

    def test_a_removed_document_leaves_the_list_on_the_next_request(self):
        page = "/specs/001-a/s00-intro.md"
        self.assertIn("[stage 10: late]", section(self.get(page)[1]))
        (self.start / "specs" / "001-a" / "s10-late.md").unlink()
        self.assertNotIn("[stage 10: late]", section(self.get(page)[1]))

    def test_an_empty_story_folder_has_no_documents_to_show(self):
        (self.start / "specs" / "004-empty").mkdir()
        status, body = self.get("/specs/004-empty")
        self.assertEqual(status, 200)
        self.assertNotIn('class="reading-order"', body)


class FileNamedDotMdTest(ServerTestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.start = Path(cls.tmp.name) / "project"
        story = cls.start / "specs" / "001-a"
        story.mkdir(parents=True)
        (story / ".md").write_text("# Dot\n")
        (story / "s01-x.md").write_text("# X\n")
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.tmp.cleanup()

    def test_dot_md_is_labelled_blank(self):  # CH-010
        status, body = self.get("/specs/001-a/s01-x.md")
        self.assertEqual(status, 200)
        self.assertIn("[ref doc: blank]", section(body))


if __name__ == "__main__":
    unittest.main()
