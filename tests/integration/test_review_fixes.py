"""Story 003: behaviour raised in review of the discovery, board and refresh code."""

import os
import shutil
import tempfile
import unittest
from pathlib import Path

import specview


class ReviewFixesTest(unittest.TestCase):
    def setUp(self):
        self.dir = Path(tempfile.mkdtemp())
        self.story = self.dir / "specs" / "001-x"
        self.story.mkdir(parents=True)
        self.viewer = specview.Viewer(self.dir)

    def tearDown(self):
        shutil.rmtree(self.dir)

    def page(self, rel):
        return self.viewer.document_page(self.dir / "specs" / rel)

    def test_back_reference_row_to_an_undiscovered_prefix_defines_nothing(self):
        codes = specview.Codes({"TB"})
        self.assertIsNone(codes.row_definition(["TB-001", "ZZ-001"]))
        self.assertEqual(codes.row_definition(["TB-001", "ZZ-001 and a real description"]), "TB-001")

    def test_in_progress_and_blocked_tasks_still_define_their_code(self):
        (self.story / "tasks.md").write_text("- [~] T001 a\n- [!] T002 b\n- [X] T003 c\n")
        (self.story / "refs.md").write_text("See T001, T002 and T003.\n")
        refs = self.viewer.story_index("001-x")
        for code in ("T001", "T002", "T003"):
            self.assertEqual(refs.state(code), "resolved", code)
        self.assertIn('<li id="t001"', self.page("001-x/tasks.md"))

    def test_longer_fence_is_not_closed_by_a_shorter_one(self):
        text = "````\n```\n- [ ] T001 inside\n```\n````\n- [ ] T002 real\n"
        self.assertEqual([c.task for c in specview.parse_tasks(text)], ["T002"])

    def test_closing_fence_with_text_does_not_close(self):
        text = "```\n- [ ] T001 inside\n``` trailing\n- [ ] T002 still inside\n```\n- [ ] T003 real\n"
        self.assertEqual([c.task for c in specview.parse_tasks(text)], ["T003"])

    def test_prefixes_are_discovered_on_every_request(self):
        (self.story / "a.md").write_text("- QZ-001 thing\n")
        calls = []
        original = specview.discover_prefixes
        specview.discover_prefixes = lambda text: calls.append(1) or original(text)
        try:
            self.page("001-x/a.md")
            first = len(calls)
            self.page("001-x/a.md")
        finally:
            specview.discover_prefixes = original
        self.assertGreater(len(calls), first)

    def test_symlinked_folder_document_is_re_rendered_when_it_changes(self):
        outside = self.dir / "specs" / "002-y"
        outside.mkdir()
        target = outside / "doc.md"
        target.write_text("# One\n")
        os.symlink(outside, self.story / "linked")
        before = self.page("001-x/linked/doc.md")
        target.write_text("# Two\n")
        os.utime(target, (target.stat().st_atime + 5, target.stat().st_mtime + 5))
        self.assertIn("Two", self.page("001-x/linked/doc.md"))
        self.assertNotEqual(before, self.page("001-x/linked/doc.md"))

    def test_unreadable_file_has_a_null_stamp_and_an_unreadable_board_is_empty(self):
        tasks = self.story / "tasks.md"
        tasks.write_text("- [ ] T001 a\n")
        self.assertEqual([c.task for c in self.viewer.board("001-x")], ["T001"])
        tasks.chmod(0)
        try:
            if os.access(tasks, os.R_OK):
                self.skipTest("permissions are not enforced for this user")
            self.assertIsNone(self.viewer.stamp("001-x/tasks.md"))
            self.assertEqual(self.viewer.board("001-x"), [])
        finally:
            tasks.chmod(0o644)
        self.assertEqual([c.task for c in self.viewer.board("001-x")], ["T001"])

    def test_nested_folder_pages_carry_the_story_menu(self):
        (self.story / "checklists").mkdir()
        (self.story / "checklists" / "r.md").write_text("# R\n")
        page = self.viewer.navigation_page(self.story / "checklists")
        self.assertIn('href="/specs/001-x/kanban"', page)


if __name__ == "__main__":
    unittest.main()
