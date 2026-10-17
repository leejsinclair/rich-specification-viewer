"""Story 003: the stamp route and the page refresher (US3, FR-012, DEC-004)."""

import json
import os
import re
import shutil
import tempfile
import unittest
from pathlib import Path

import specview

from .support import ServerTestCase


class StampRouteTest(ServerTestCase):
    def stamp(self, path, **kw):
        status, body = self.get("/api/stamp?path=" + path, **kw)
        return status, json.loads(body) if status == 200 else None

    def test_returns_the_modified_time(self):
        status, data = self.stamp("012-board/tasks.md")
        self.assertEqual(status, 200)
        self.assertEqual(data, {"stamp": (self.start / "specs" / "012-board" / "tasks.md").stat().st_mtime})

    def test_returns_null_for_an_unreadable_file(self):
        status, data = self.stamp("014-none/tasks.md")
        self.assertEqual((status, data), (200, {"stamp": None}))

    def test_refuses_a_path_outside_specs(self):
        for path in ("../README.md", "%2e%2e/%2e%2e/etc/passwd", ""):
            status, _ = self.stamp(path)
            self.assertEqual(status, 403, path)

    def test_refuses_a_wrong_host(self):
        status, _ = self.stamp("012-board/tasks.md", host="evil.example")
        self.assertEqual(status, 403)

    def test_pages_carry_the_refresher_with_a_ten_second_interval(self):
        for path in ("/specs/001-demo/s01-requirements.md", "/specs/012-board/kanban", "/specs/012-board/kanban?group=story"):
            _, page = self.get(path)
            self.assertIn('id="stamp"', page, path)
            self.assertIn("setInterval", page, path)
            self.assertIn("}, 10000);", page, path)
            self.assertIn("/api/stamp?path=", page, path)

    def test_page_stamp_names_the_shown_file_and_its_time(self):
        _, page = self.get("/specs/012-board/kanban")
        data = json.loads(re.search(r'<script type="application/json" id="stamp">(.*?)</script>', page, re.S).group(1))
        self.assertEqual(data["path"], "012-board/tasks.md")
        self.assertEqual(data["stamp"], (self.start / "specs" / "012-board" / "tasks.md").stat().st_mtime)

    def test_refresher_keeps_scroll_and_the_address(self):
        _, page = self.get("/specs/012-board/kanban?group=story")
        self.assertIn("window.scrollY", page)
        self.assertIn("location.search", page)
        self.assertIn("location.reload()", page)
        self.assertIn("d.stamp === null", page)


class ChangeTest(unittest.TestCase):
    """A changed file gives a new stamp and new content; an unchanged board is not parsed again."""

    def setUp(self):
        self.dir = Path(tempfile.mkdtemp())
        story = self.dir / "specs" / "001-x"
        story.mkdir(parents=True)
        self.tasks = story / "tasks.md"
        self.tasks.write_text("- [ ] T001 first\n")
        self.viewer = specview.Viewer(self.dir)

    def tearDown(self):
        shutil.rmtree(self.dir)

    def test_changed_file_gives_a_new_stamp_and_board(self):
        before = self.viewer.stamp("001-x/tasks.md")
        self.assertEqual([c.task for c in self.viewer.board("001-x")], ["T001"])
        self.tasks.write_text("- [ ] T001 first\n- [X] T002 second\n")
        os.utime(self.tasks, (before + 5, before + 5))
        self.assertNotEqual(self.viewer.stamp("001-x/tasks.md"), before)
        self.assertEqual([c.task for c in self.viewer.board("001-x")], ["T001", "T002"])

    def test_unchanged_board_is_not_parsed_again(self):
        calls = []
        original = specview.parse_tasks
        specview.parse_tasks = lambda text: calls.append(1) or original(text)
        try:
            self.viewer.board("001-x")
            self.viewer.board("001-x")
        finally:
            specview.parse_tasks = original
        self.assertEqual(len(calls), 1)

    def test_removed_file_gives_a_null_stamp_and_an_empty_board(self):
        self.viewer.board("001-x")
        self.tasks.unlink()
        self.assertIsNone(self.viewer.stamp("001-x/tasks.md"))
        self.assertEqual(self.viewer.board("001-x"), [])
