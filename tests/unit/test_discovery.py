"""Story 003: prefix discovery and the definitions it adds (US1, FR-001 to FR-005)."""

import unittest

import specview


class DiscoverPrefixesTest(unittest.TestCase):
    def test_heading_introduces_a_prefix(self):
        self.assertEqual(specview.discover_prefixes("## VO-001 Voice\n"), {"VO"})

    def test_bullet_introduces_a_prefix_plain_or_bold(self):
        text = "- QZ-001 plain\n- **PX-002**: bold\n  - NS-3 nested\n"
        self.assertEqual(specview.discover_prefixes(text), {"QZ", "PX", "NS"})

    def test_table_row_with_a_description_introduces_a_prefix(self):
        text = "| Code | Meaning |\n|---|---|\n| TB-001 | A thing |\n"
        self.assertEqual(specview.discover_prefixes(text), {"TB"})

    def test_back_reference_table_introduces_nothing(self):
        text = "| Item | Covers |\n|---|---|\n| ZZ-001 | VO-001, QZ-002 |\n| ZZ-002 | VO-001 and QZ-002 |\n"
        self.assertEqual(specview.discover_prefixes(text), set())

    def test_a_code_in_running_text_or_code_introduces_nothing(self):
        text = "See VO-001 for more.\n\n```\n- QZ-001 in a fence\n```\n"
        self.assertEqual(specview.discover_prefixes(text), set())

    def test_single_letter_prefix_is_not_a_form(self):
        self.assertEqual(specview.discover_prefixes("- A-001 one letter\n"), set())


class CodesTest(unittest.TestCase):
    def test_fixed_prefixes_are_not_replaced(self):
        codes = specview.Codes({"FR", "VO"})
        self.assertEqual(codes.prefixes, ("VO",))
        self.assertTrue(codes.code_re.fullmatch("FR-001"))
        self.assertIsNone(codes.code_re.fullmatch("FR-1"))
        self.assertTrue(codes.code_re.fullmatch("VO-1"))

    def test_without_prefixes_it_is_the_fixed_list(self):
        self.assertIsNone(specview.Codes().code_re.fullmatch("VO-001"))


class DiscoveredDefinitionsTest(unittest.TestCase):
    codes = specview.Codes({"VO", "QZ", "TB"})

    def defs(self, text):
        return {(d.code, d.kind) for d in specview.find_definitions(text, "x/d.md", self.codes)}

    def test_heading_bullet_and_row_define(self):
        text = "## VO-001 Voice\n\n- QZ-001 item\n\n| Code | Meaning |\n|---|---|\n| TB-001 | A thing |\n"
        self.assertEqual(self.defs(text), {("VO-001", "heading"), ("QZ-001", "item"), ("TB-001", "row")})

    def test_back_reference_row_does_not_define(self):
        text = "| Item | Covers |\n|---|---|\n| VO-001 | QZ-001 |\n"
        self.assertEqual(self.defs(text), set())

    def test_row_section_is_the_row_with_its_header(self):
        text = "| Code | Meaning |\n|---|---|\n| TB-001 | A thing |\n| TB-002 | Another |\n"
        row = [d for d in specview.find_definitions(text, "x/d.md", self.codes) if d.code == "TB-001"][0]
        self.assertIn("A thing", row.section_html)
        self.assertNotIn("Another", row.section_html)

    def test_fixed_codes_behave_as_before(self):
        text = "**FR-001**: shall\n\n- VO-9 plain\n"
        self.assertEqual({d.code for d in specview.find_definitions(text, "x/d.md")}, {"FR-001"})
