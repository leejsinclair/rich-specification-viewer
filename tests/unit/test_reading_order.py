"""Story 002: stage detection, labels, the sort key, alias recognition and contrast (DEC-003, DEC-004, DEC-007)."""

import os
import re
import tempfile
import unittest
from pathlib import Path

import specview
from specview import entry_label, natural_key, reading_order_key, stage_of


def order(*paths: str) -> list[str]:
    """Sort slash-separated document paths with the reading-order key."""
    def key(path: str):
        parts = tuple(path.split("/"))
        return reading_order_key(parts, stage_of(parts[-1]) is not None)

    return sorted(paths, key=key)


class StageAndLabelTest(unittest.TestCase):
    def test_stage_prefix(self):
        self.assertEqual(stage_of("s01-requirements.md"), ("01", "requirements"))
        self.assertEqual(stage_of("s10-x.MD"), ("10", "x"))
        self.assertEqual(stage_of("s04-ai-spec.md"), ("04", "ai-spec"))

    def test_names_without_a_stage(self):
        for name in ("s1-x.md", "s100-x.md", "S01-x.md", "s01_x.md", "s01.md", "s01-.md", "notes.md", ".md", "s01-x.txt"):
            self.assertIsNone(stage_of(name), name)

    def test_staged_label(self):
        self.assertEqual(entry_label(("s01-requirements.md",)), "[stage 01: requirements]")
        self.assertEqual(entry_label(("sub", "deeper", "s02-x.md")), "sub/deeper/[stage 02: x]")

    def test_unstaged_label(self):
        self.assertEqual(entry_label(("notes.md",)), "notes [ref doc: notes]")
        self.assertEqual(entry_label(("sub", "notes.MD")), "sub/notes [ref doc: notes]")
        self.assertEqual(entry_label(("s1-x.md",)), "s1-x [ref doc: s1-x]")

    def test_file_named_exactly_dot_md(self):  # CH-010
        self.assertEqual(entry_label((".md",)), "[ref doc: blank]")
        self.assertEqual(entry_label(("sub", ".md")), "sub/[ref doc: blank]")


class SortKeyTest(unittest.TestCase):
    def test_numbers_compare_by_value(self):  # FR-007
        names = ["s%02d-x.md" % n for n in (10, 2, 0, 9, 1)]
        self.assertEqual(order(*names), ["s00-x.md", "s01-x.md", "s02-x.md", "s09-x.md", "s10-x.md"])
        self.assertEqual(order("a10.md", "a2.md", "a1.md"), ["a1.md", "a2.md", "a10.md"])

    def test_case_is_ignored_and_exact_characters_break_ties(self):  # FR-009
        self.assertEqual(order("b.md", "A.md", "a.md", "B.md"), ["A.md", "a.md", "B.md", "b.md"])
        self.assertEqual(order("a1.md", "a01.md"), ["a01.md", "a1.md"])

    def test_staged_before_unstaged_within_a_folder(self):  # FR-009
        self.assertEqual(order("a.md", "s05-x.md", "s01-y.md", "z.md"), ["s01-y.md", "s05-x.md", "a.md", "z.md"])

    def test_a_folders_documents_come_before_its_nested_folders(self):  # FR-008
        got = order("sub/s00-a.md", "z.md", "s09-x.md", "sub/deeper/a.md", "sub/b.md")
        self.assertEqual(got, ["s09-x.md", "z.md", "sub/s00-a.md", "sub/b.md", "sub/deeper/a.md"])

    def test_sibling_folders_use_the_name_comparison(self):  # DEC-004
        got = order("s10-x/a.md", "s02-x/a.md", "Alpha/a.md", "s2-x/a.md")
        self.assertEqual(got, ["Alpha/a.md", "s02-x/a.md", "s2-x/a.md", "s10-x/a.md"])

    def test_the_same_order_for_any_input_order(self):  # NFR-001
        paths = ["b.md", "s01-a.md", "sub/x.md", "A.md", "s10-z.md", "s02-y.md", "sub/s01-q.md"]
        expected = order(*paths)
        for shift in range(len(paths)):
            self.assertEqual(order(*(paths[shift:] + paths[:shift])), expected)
        self.assertEqual(order(*reversed(paths)), expected)

    def test_natural_key_is_comparable_for_mixed_names(self):
        self.assertLess(natural_key("a1b"), natural_key("a1c"))
        self.assertLess(natural_key("1a"), natural_key("a1"))


@unittest.skipUnless(hasattr(os, "symlink"), "needs symbolic links")
class AliasRecognitionTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.start = Path(self.tmp.name) / "project"
        self.specs = self.start / "specs"
        self.story = self.specs / "001-a"
        (self.story / "sub").mkdir(parents=True)
        (self.specs / "002-b").mkdir()
        for path in ("001-a/s04-ai-spec.md", "001-a/notes.md", "001-a/sub/s02-x.md", "002-b/s01-b.md"):
            (self.specs / path).write_text("# T\n")
        self.viewer = specview.Viewer(self.start)

    def tearDown(self):
        self.tmp.cleanup()

    def labels(self, current="001-a/s04-ai-spec.md"):
        html = self.viewer.reading_order("001-a", current)
        return re.findall(r"<li>(.*?)</li>", html)

    def test_symbolic_link_to_a_stage_document_is_an_alias(self):
        (self.story / "spec.md").symlink_to("s04-ai-spec.md")
        self.assertEqual(
            self.labels(),
            [
                '<span aria-current="page">[stage 04: ai-spec]</span> (spec.md)',
                '<a href="/specs/001-a/notes.md">notes [ref doc: notes]</a>',
                '<a href="/specs/001-a/sub/s02-x.md">sub/[stage 02: x]</a>',
            ],
        )

    def test_two_aliases_are_two_bracket_groups_in_order(self):
        (self.story / "tasks.md").symlink_to("s04-ai-spec.md")
        (self.story / "plan.md").symlink_to("s04-ai-spec.md")
        self.assertTrue(self.labels()[0].endswith("[stage 04: ai-spec]</span> (plan.md) (tasks.md)"))

    def test_an_alias_can_point_into_a_nested_folder(self):
        (self.story / "spec.md").symlink_to("sub/s02-x.md")
        self.assertIn("sub/[stage 02: x]</a> (spec.md)", "".join(self.labels()))

    def test_a_chain_of_links_is_followed(self):
        (self.story / "plan.md").symlink_to("s04-ai-spec.md")
        (self.story / "spec.md").symlink_to("plan.md")
        self.assertTrue(self.labels()[0].endswith("(plan.md) (spec.md)"))

    def test_a_regular_file_with_an_alias_name_is_an_ordinary_document(self):
        (self.story / "plan.md").write_text("# plan\n")
        self.assertIn("plan [ref doc: plan]", "".join(self.labels()))

    def test_a_link_to_a_document_without_a_stage_is_ordinary(self):
        (self.story / "plan.md").symlink_to("notes.md")
        self.assertIn("plan [ref doc: plan]", "".join(self.labels()))

    def test_a_link_into_another_story_is_ordinary_and_opens_the_real_path(self):
        (self.story / "spec.md").symlink_to("../002-b/s01-b.md")
        got = "".join(self.labels())
        self.assertIn('<a href="/specs/002-b/s01-b.md">spec [ref doc: spec]</a>', got)

    def test_a_link_with_a_missing_target_is_not_listed(self):
        (self.story / "spec.md").symlink_to("gone.md")
        self.assertNotIn("spec [ref doc", "".join(self.labels()))

    def test_a_link_to_a_file_outside_specs_is_not_listed(self):
        (self.start / "secret.md").write_text("secret\n")
        (self.story / "spec.md").symlink_to("../../secret.md")
        self.assertNotIn("spec [ref doc", "".join(self.labels()))

    def test_viewing_the_alias_makes_its_source_current(self):
        (self.story / "spec.md").symlink_to("s04-ai-spec.md")
        self.assertTrue(self.labels("001-a/spec.md")[0].startswith('<span aria-current="page">'))

    def test_a_document_reached_through_a_linked_folder_is_the_current_entry(self):  # CH-009
        (self.story / "linked").symlink_to("../002-b", target_is_directory=True)
        html = self.viewer.reading_order("001-a", "001-a/linked/s01-b.md")
        self.assertEqual(html.count('aria-current="page"'), 1)
        self.assertIn('<span aria-current="page">linked/[stage 01: b]</span>', html)
        self.assertEqual(len(re.findall("<li>", html)), 4)

    def test_names_are_escaped(self):
        (self.story / "a<b>&\"c'.md").write_text("# T\n")
        html = self.viewer.reading_order("001-a", "001-a/s04-ai-spec.md")
        self.assertNotIn("<b>", html)
        self.assertIn("a&lt;b&gt;&amp;&quot;c&#x27; [ref doc: a&lt;b&gt;&amp;&quot;c&#x27;]", html)

    def test_a_story_with_no_documents_gets_no_section(self):
        self.assertEqual(self.viewer.reading_order("003-none", "003-none/x.md"), "")


class ContrastTest(unittest.TestCase):
    """NFR-002: at least 4.5:1 between the text colours and the background, from the CSS values."""

    @staticmethod
    def luminance(colour: str) -> float:
        digits = colour[1:] if len(colour) == 7 else "".join(c * 2 for c in colour[1:])
        channels = [int(digits[i : i + 2], 16) / 255 for i in (0, 2, 4)]
        lin = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
        return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]

    def ratio(self, one: str, two: str) -> float:
        a, b = sorted((self.luminance(one), self.luminance(two)), reverse=True)
        return (a + 0.05) / (b + 0.05)

    def test_links_and_current_entry_have_enough_contrast(self):
        values = dict(re.findall(r"--(fg|link|bg):\s*(#[0-9a-fA-F]{3,6})", specview.CSS))
        self.assertEqual(set(values), {"fg", "link", "bg"})
        self.assertGreaterEqual(self.ratio(values["link"], values["bg"]), 4.5)
        self.assertGreaterEqual(self.ratio(values["fg"], values["bg"]), 4.5)

    def test_current_entry_is_not_underlined_and_uses_the_text_colour(self):
        rule = re.search(r"\.reading-order \[aria-current=\"page\"\]\s*\{([^}]*)\}", specview.CSS).group(1)
        self.assertIn("font-weight: 700", rule)
        self.assertIn("text-decoration: none", rule)
        self.assertIn("var(--fg)", rule)


if __name__ == "__main__":
    unittest.main()
