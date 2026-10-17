"""Story 003: a discovered code is marked wherever it is referenced in its story (US1, FR-003 to FR-005)."""

from .support import ServerTestCase


class DiscoveredReferencesTest(ServerTestCase):
    def page(self, path):
        status, body = self.get("/specs/" + path)
        self.assertEqual(status, 200, path)
        return body

    def test_codes_introduced_elsewhere_are_marked_with_a_link(self):
        page = self.page("010-discovery/refs.md")
        refs = self.refs(page)
        for code in ("VO-001", "QZ-001", "TB-001"):
            self.assertEqual(refs[code]["state"], "resolved", code)
            self.assertIn('<a class="ref" data-code="%s" href="/specs/010-discovery/defs.md#%s">' % (code, code.lower()), page)
            self.assertIn("html", refs[code])

    def test_row_definition_links_to_its_row(self):
        page = self.page("010-discovery/defs.md")
        self.assertIn('<tr id="tb-001">', page)
        self.assertIn('<h2 id="vo-001">', page)
        self.assertIn('<li id="qz-001">', page)

    def test_undefined_discovered_code_shows_the_error(self):
        page = self.page("010-discovery/refs.md")
        self.assertEqual(self.refs(page)["VO-009"]["state"], "unresolved")
        self.assertIn('class="ref ref-error" data-code="VO-009"', page)

    def test_ambiguous_discovered_code_shows_the_error(self):
        page = self.page("010-discovery/refs.md")
        self.assertEqual(self.refs(page)["QZ-002"]["state"], "ambiguous")

    def test_back_reference_tables_introduce_nothing(self):
        page = self.page("010-discovery/refs.md")
        self.assertNotIn("ZZ-001", self.refs(page))
        self.assertNotIn('data-code="ZZ-', page)

    def test_code_in_inline_code_is_not_marked(self):
        page = self.page("010-discovery/refs.md")
        self.assertIn("<code>VO-001</code>", page)

    def test_the_same_code_in_another_story_is_not_marked_as_a_form(self):
        page = self.page("011-other/uses.md")
        self.assertNotIn('data-code="VO-001"', page)
        self.assertEqual(self.refs(page), {})

    def test_the_fixed_list_still_works(self):
        page = self.page("010-discovery/refs.md")
        self.assertEqual(self.refs(page)["REQ-001"]["state"], "unresolved")
        status, demo = self.get("/specs/001-demo/s02-functional-spec.md")
        self.assertEqual(status, 200)
        self.assertTrue(self.refs(demo))
