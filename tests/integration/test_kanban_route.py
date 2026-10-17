"""Story 003: the kanban route over HTTP (US2, FR-006 to FR-011, DEC-002)."""

import hashlib
import re

from .support import FIXTURE, ServerTestCase


def lane(page, name):
    match = re.search(r'<section class="lane"><h2>%s</h2>(.*?</section>)</div></section>' % re.escape(name), page, re.S)
    return match.group(1) if match else ""


def column(page, lane_name, col):
    html = lane(page, lane_name)
    match = re.search(r'<section class="col col-%s">(.*?)</section>' % col, html, re.S)
    return match.group(1) if match else ""


class KanbanRouteTest(ServerTestCase):
    def test_board_groups_by_phase_by_default(self):
        status, page = self.get("/specs/012-board/kanban")
        self.assertEqual(status, 200)
        for name in ("Phase 1: Setup", "Phase 2: Build", "Unallocated"):
            self.assertIn("<h2>%s</h2>" % name, page)
        self.assertIn("T003", column(page, "Phase 1: Setup", "done"))
        self.assertIn("T004", column(page, "Phase 1: Setup", "in-progress"))
        self.assertIn("T005", column(page, "Phase 1: Setup", "blocked"))
        self.assertIn("T002", column(page, "Phase 1: Setup", "backlog"))
        self.assertIn("T008", column(page, "Phase 1: Setup", "blocked"))
        self.assertNotIn("T008", column(page, "Phase 1: Setup", "in-progress"))
        self.assertIn("T001", column(page, "Unallocated", "backlog"))

    def test_card_shows_id_label_and_description(self):
        _, page = self.get("/specs/012-board/kanban")
        self.assertIn('<span class="card-id">T003</span> <span class="card-story">US1</span> <span class="card-text">Done task</span>', page)

    def test_group_by_story(self):
        _, page = self.get("/specs/012-board/kanban?group=story")
        for name in ("US1", "US2", "Unallocated"):
            self.assertIn("<h2>%s</h2>" % name, page)
        self.assertIn("T009", column(page, "Unallocated", "backlog"))
        self.assertIn("Grouped by user story", page)

    def test_unknown_group_falls_back_to_phase(self):
        _, page = self.get("/specs/012-board/kanban?group=nonsense")
        self.assertIn("<h2>Phase 1: Setup</h2>", page)

    def test_descriptions_are_escaped(self):
        _, page = self.get("/specs/012-board/kanban")
        self.assertIn("&amp; &lt;b&gt;escaped&lt;/b&gt;", page)
        self.assertNotIn("<b>escaped</b>", page)

    def test_empty_tasks_file_shows_the_message(self):
        status, page = self.get("/specs/013-empty/kanban")
        self.assertEqual(status, 200)
        self.assertIn("No tasks were found", page)
        self.assertNotIn('class="lane"', page)

    def test_missing_tasks_file_shows_the_message(self):
        status, page = self.get("/specs/014-none/kanban")
        self.assertEqual(status, 200)
        self.assertIn("No tasks were found", page)

    def test_tasks_file_is_unchanged(self):
        path = FIXTURE / "specs" / "012-board" / "tasks.md"
        before = (hashlib.sha256(path.read_bytes()).hexdigest(), path.stat().st_mtime_ns)
        self.get("/specs/012-board/kanban")
        self.get("/specs/012-board/kanban?group=story")
        self.assertEqual((hashlib.sha256(path.read_bytes()).hexdigest(), path.stat().st_mtime_ns), before)

    def test_wrong_host_is_refused(self):
        status, _ = self.get("/specs/012-board/kanban", host="evil.example")
        self.assertEqual(status, 403)

    def test_path_outside_specs_is_refused(self):
        status, _ = self.get("/specs/%2e%2e/kanban")
        self.assertEqual(status, 403)

    def test_unknown_story_is_not_found(self):
        status, _ = self.get("/specs/999-nothing/kanban")
        self.assertEqual(status, 404)

    def test_story_pages_link_to_the_board(self):
        for path in ("/specs/001-demo/s01-requirements.md", "/specs/001-demo/"):
            _, page = self.get(path)
            self.assertIn('<nav class="story-menu"', page, path)
            self.assertIn('href="/specs/001-demo/kanban"', page, path)
        _, page = self.get("/specs/012-board/kanban")
        self.assertIn('href="/specs/012-board/kanban"', page)
