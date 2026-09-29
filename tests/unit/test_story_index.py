"""T021: the Story index and reference rules (BR-1 to BR-6, FR-009, FR-022, FR-024, FR-025)."""

import unittest
from pathlib import Path

import specview

FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "project"


class CodeFormTest(unittest.TestCase):
    def test_spec_kit_code_forms_are_codes(self):
        for code in ("REQ-001", "UC-004", "OQ-018", "ART-012", "CH-007", "FR-025", "NFR-003", "SC-001", "DEC-008", "AIS-089", "EVD-001", "D-01", "T001"):
            with self.subTest(code=code):
                self.assertTrue(specview.CODE_RE.fullmatch(code))

    def test_other_forms_are_not_codes(self):
        for text in ("CHK-001", "BR-1", "AC-17", "OVR-001", "UTF-8", "IDEC-001"):
            with self.subTest(text=text):
                self.assertIsNone(specview.CODE_RE.search(text))

    def test_nfr_is_not_read_as_fr(self):
        self.assertEqual(specview.CODE_RE.findall("see NFR-001"), ["NFR-001"])


class DefinitionTest(unittest.TestCase):
    def defs(self, text):
        return {d.code: d for d in specview.find_definitions(text, "001-x/doc.md")}

    def test_item_heading_task_and_challenge_definitions(self):
        text = (
            "**REQ-001**: first\n\n- **FR-002**: in a list\n\n### UC-001: A heading\n\nBody.\n\n"
            "- [ ] T001 a task\n\n"
            '```eil:challenge\n{"id": "CH-001", "text": "gap", "target": "FR-002", "status": "open"}\n```\n'
        )
        defs = self.defs(text)
        self.assertEqual({k: d.kind for k, d in defs.items()}, {"REQ-001": "item", "FR-002": "item", "UC-001": "heading", "T001": "task", "CH-001": "challenge"})
        self.assertEqual(defs["CH-001"].anchor, "challenges")
        self.assertIn("gap", defs["CH-001"].section_html)

    def test_mentions_are_not_definitions(self):
        self.assertEqual(self.defs("This mentions REQ-001 and **FR-002** without a colon.\n"), {})

    def test_section_runs_to_next_definition_or_heading(self):
        defs = self.defs("## A\n\n**FR-001**: one\nmore of one\n\n**FR-002**: two\n\nstill two\n\n## B\n\nnot two\n")
        self.assertIn("more of one", defs["FR-001"].section_html)
        self.assertNotIn("two", defs["FR-001"].section_html)
        self.assertIn("still two", defs["FR-002"].section_html)
        self.assertNotIn("not two", defs["FR-002"].section_html)

    def test_heading_section_runs_to_next_heading_of_same_level(self):
        defs = self.defs("### UC-001: Reads\n\n#### Detail\n\ninside\n\n### Next\n\noutside\n")
        self.assertIn("inside", defs["UC-001"].section_html)
        self.assertNotIn("outside", defs["UC-001"].section_html)

    def test_codes_in_code_define_nothing(self):
        self.assertEqual(self.defs("```\n**REQ-001**: in code\n```\n\n`**REQ-002**: inline`\n"), {})


class StoryIndexTest(unittest.TestCase):
    def setUp(self):
        self.viewer = specview.Viewer(FIXTURE)
        self.index = self.viewer.story_index("001-demo")

    def test_nested_documents_belong_to_the_story(self):  # FR-025
        self.assertEqual(self.index.state("SC-001"), "resolved")
        self.assertEqual(self.index.definitions["SC-001"][0].document, "001-demo/checklists/requirements.md")

    def test_link_and_copy_aliases_count_once(self):  # FR-024
        self.assertEqual(self.index.state("AIS-001"), "resolved")
        self.assertEqual(self.index.aliases, {"001-demo/plan.md": "001-demo/s04-ai-spec.md", "001-demo/spec.md": "001-demo/s04-ai-spec.md"})

    def test_unresolved_and_ambiguous(self):  # BR-5
        self.assertEqual(self.index.state("FR-777"), "unresolved")
        self.assertEqual(self.index.state("UC-050"), "ambiguous")

    def test_story_scope(self):  # FR-009, BR-4
        self.assertEqual(self.index.state("REQ-900"), "unresolved")
        self.assertEqual(self.viewer.story_index("002-other").state("REQ-900"), "resolved")

    def test_comment_and_code_block_codes_are_not_definitions(self):
        self.assertNotIn("REQ-999", self.index.definitions)


class MarkingTest(unittest.TestCase):
    def setUp(self):
        self.viewer = specview.Viewer(FIXTURE)

    def page(self, rel):
        return self.viewer.document_page(FIXTURE / "specs" / rel)

    def test_references_are_links_and_errors_are_spans(self):
        page = self.page("001-demo/s02-functional-spec.md")
        self.assertIn('<a class="ref" data-code="REQ-002" href="/specs/001-demo/s01-requirements.md#req-002">REQ-002</a>', page)
        self.assertIn('<span class="ref ref-error" data-code="FR-777" title="Not defined in this story">⚠ FR-777</span>', page)
        self.assertIn('data-code="UC-050" title="Defined in more than one document"', page)

    def test_codes_in_code_and_on_their_own_definition_are_plain(self):
        page = self.page("001-demo/s02-functional-spec.md")
        self.assertIn("<code>REQ-001</code>", page)
        self.assertIn('<p id="fr-001"><strong>FR-001</strong>:', page)
        self.assertIn("print(&quot;REQ-001 inside a code block&quot;)", page)

    def test_document_directly_in_specs_is_not_marked(self):  # FR-009 (CH-019)
        page = self.page("README.md")
        self.assertIn("mentions REQ-001 and FR-001", page)
        self.assertNotIn('class="ref', page)


if __name__ == "__main__":
    unittest.main()
