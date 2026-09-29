"""T029: Mermaid blocks reach the page for drawing, and Mermaid is the only outside script (FR-014, DEC-003, NFR-003)."""

import re
import unittest

import specview

from .support import ServerTestCase


class DiagramsTest(ServerTestCase):
    def test_each_mermaid_block_is_emitted_escaped(self):
        _, page = self.get("/specs/001-demo/s02-functional-spec.md")
        blocks = re.findall(r'<pre class="mermaid-src">(.*?)</pre>', page, re.S)
        self.assertEqual(len(blocks), 5)  # flowchart, sequence, C4Context, ER, and the invalid one
        self.assertIn("A --&gt; B", blocks[0])
        self.assertTrue(any(b.startswith("erDiagram") for b in blocks))
        self.assertTrue(any(b.startswith("this is not valid mermaid") for b in blocks))

    def test_c4_container_and_component_blocks_are_emitted(self):
        _, page = self.get("/specs/001-demo/s03-technical-spec.md")
        self.assertIn('<pre class="mermaid-src">C4Container', page)
        self.assertIn('<pre class="mermaid-src">C4Component', page)

    def test_only_outside_script_is_mermaid_11(self):
        _, page = self.get("/specs/001-demo/s02-functional-spec.md")
        outside = set(re.findall(r"https?://[^'\"\s)]+", page))
        self.assertEqual(outside, {specview.MERMAID_URL})
        self.assertIn("/npm/mermaid@11/", specview.MERMAID_URL)
        self.assertNotIn("<script src=", page)

    def test_loader_handles_failures_per_block(self):
        self.assertIn("startOnLoad: false", specview.DIAGRAM_JS)
        self.assertIn("could not be loaded", specview.DIAGRAM_JS)
        self.assertIn("could not be drawn", specview.DIAGRAM_JS)


if __name__ == "__main__":
    unittest.main()
