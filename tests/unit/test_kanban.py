"""Story 003: the kanban parser and the grouping (US2, FR-006 to FR-008, DEC-003)."""

import unittest
from pathlib import Path

import specview

FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "project" / "specs" / "012-board" / "tasks.md"


def columns(text):
    return {c.task: c.column for c in specview.parse_tasks(text)}


class ParseTasksTest(unittest.TestCase):
    def test_each_marker_picks_a_column(self):
        text = "- [ ] T001 a\n- [X] T002 b\n- [x] T003 c\n- [~] T004 d\n- [!] T005 e\n"
        self.assertEqual(
            columns(text),
            {"T001": "backlog", "T002": "done", "T003": "done", "T004": "in-progress", "T005": "blocked"},
        )

    def test_tags_pick_a_column(self):
        text = "- [ ] T001 a (in progress)\n- [ ] T002 b (Blocked)\n"
        self.assertEqual(columns(text), {"T001": "in-progress", "T002": "blocked"})

    def test_blocked_wins_over_in_progress(self):
        text = "- [~] T001 a (blocked)\n- [!] T002 b (in progress)\n- [ ] T003 c (in progress) (blocked)\n"
        self.assertEqual(columns(text), {"T001": "blocked", "T002": "blocked", "T003": "blocked"})

    def test_done_task_stays_done(self):
        self.assertEqual(columns("- [X] T001 a (blocked)\n"), {"T001": "done"})

    def test_phase_story_label_and_description(self):
        cards = specview.parse_tasks("## Phase 1\n\n- [ ] T001 [P] [US2] Do the thing\n")
        self.assertEqual(
            cards, [specview.Card("T001", "US2", "[P] Do the thing", "Phase 1", "backlog")]
        )

    def test_task_before_any_phase_has_no_phase(self):
        cards = specview.parse_tasks("- [ ] T001 a\n\n## P\n\n- [ ] T002 b\n")
        self.assertEqual([c.phase for c in cards], [None, "P"])

    def test_malformed_lines_are_ignored(self):
        text = "- [ ] T001 a\nnot a task\n- [Q] T002 odd mark\n- [ ] no id\n- [ ] T003 b\n"
        self.assertEqual([c.task for c in specview.parse_tasks(text)], ["T001", "T003"])

    def test_fenced_lines_are_ignored(self):
        self.assertEqual(specview.parse_tasks("```\n- [ ] T001 a\n```\n- [ ] T002 b\n")[0].task, "T002")

    def test_empty_file_has_no_cards(self):
        self.assertEqual(specview.parse_tasks(""), [])

    def test_fixture_covers_every_column(self):
        cards = specview.parse_tasks(FIXTURE.read_text())
        self.assertEqual({c.column for c in cards}, {"backlog", "in-progress", "blocked", "done"})
        self.assertEqual(len(cards), 10)


class GroupingTest(unittest.TestCase):
    cards = specview.parse_tasks(FIXTURE.read_text())

    def test_group_by_phase_puts_unphased_tasks_in_unallocated_last(self):
        names = [n for n, _ in specview.group_cards(self.cards, "phase")]
        self.assertEqual(names, ["Phase 1: Setup", "Phase 2: Build", "Unallocated"])

    def test_group_by_story_puts_untagged_tasks_in_unallocated_last(self):
        groups = dict(specview.group_cards(self.cards, "story"))
        self.assertEqual(list(groups), ["US1", "US2", "Unallocated"])
        self.assertIn("T001", [c.task for c in groups["Unallocated"]])
        self.assertIn("T009", [c.task for c in groups["Unallocated"]])

    def test_every_card_is_in_exactly_one_group(self):
        for by in ("phase", "story"):
            total = sum(len(g) for _, g in specview.group_cards(self.cards, by))
            self.assertEqual(total, len(self.cards))


if __name__ == "__main__":
    unittest.main()
