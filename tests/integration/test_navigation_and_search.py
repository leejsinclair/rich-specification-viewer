"""T016: navigation, search, document pages and refusals over HTTP (AC-1 to AC-3, AC-10, AC-13, AC-14, AC-17)."""

import json
import tempfile
import unittest
from pathlib import Path

import specview

from .support import ServerTestCase


class NavigationAndSearchTest(ServerTestCase):
    def test_navigation_lists_stories(self):  # AC-1
        status, page = self.get("/")
        self.assertEqual(status, 200)
        self.assertIn('href="/specs/001-demo/"', page)
        self.assertIn('href="/specs/002-other/"', page)
        self.assertIn('href="/specs/README.md"', page)

    def test_folder_view_has_breadcrumbs(self):  # AC-13
        status, page = self.get("/specs/001-demo/checklists/")
        self.assertEqual(status, 200)
        self.assertIn('<a href="/">specs</a> / <a href="/specs/001-demo/">001-demo</a> / <a href="/specs/001-demo/checklists/">checklists</a>', page)
        self.assertIn('href="/specs/001-demo/checklists/requirements.md"', page)

    def test_search_api(self):  # AC-2
        status, body = self.get("/api/search?q=%2A%2Fs01-%2A")
        self.assertEqual(status, 200)
        data = json.loads(body)
        self.assertTrue(data["specs"])
        self.assertEqual([r["story"] for r in data["results"]], ["001-demo", "002-other"])
        self.assertEqual(json.loads(self.get("/api/search?q=zzz")[1])["results"], [])

    def test_document_page_is_formatted(self):  # AC-3, AC-14
        status, page = self.get("/specs/001-demo/s01-requirements.md")
        self.assertEqual(status, 200)
        self.assertIn('<h1 id="requirements-demo">Requirements: Demo</h1>', page)
        self.assertIn("<li><strong>Trigger</strong>: the developer opens a page.</li>", page)
        self.assertNotIn("Guidance comment", page)
        self.assertNotIn("SECRET-APPROVAL-TEXT", page)
        self.assertIn('<span aria-current="page">s01-requirements.md</span>', page)

    def test_path_above_start_folder_is_refused(self):  # AC-10
        status, page = self.get("/specs/../README.md")
        self.assertEqual(status, 403)
        self.assertIn("outside the viewer", page)
        status, _ = self.get("/specs/001-demo/../../../etc/passwd")
        self.assertEqual(status, 403)

    def test_foreign_host_is_refused(self):  # CH-016
        status, page = self.get("/", host="evil.example")
        self.assertEqual(status, 403)
        self.assertNotIn("001-demo", page)

    def test_missing_document_is_not_found(self):
        self.assertEqual(self.get("/specs/001-demo/nothing.md")[0], 404)
        self.assertEqual(self.get("/elsewhere")[0], 404)


class NoSpecsFolderTest(ServerTestCase):  # AC-17
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.start = Path(cls.tmp.name)
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.tmp.cleanup()

    def test_message_under_the_search_box(self):
        status, page = self.get("/")
        self.assertEqual(status, 200)
        self.assertIn('<p id="search-msg" class="search-msg">%s</p>' % specview.NO_SPECS, page)
        self.assertFalse(json.loads(self.get("/api/search?q=x")[1])["specs"])


if __name__ == "__main__":
    unittest.main()
