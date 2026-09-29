"""T007: the Markdown renderer (FR-004, FR-019, DEC-002, Security Design)."""

import unittest

import specview


def render(text: str) -> str:
    return specview.render_markdown(text)


class BlockTest(unittest.TestCase):
    def test_headings_have_anchors(self):
        out = render("# Title\n\n## Use Cases\n\n### UC-001: Developer reads\n")
        self.assertIn('<h1 id="title">Title</h1>', out)
        self.assertIn('<h2 id="use-cases">Use Cases</h2>', out)
        self.assertIn('<h3 id="uc-001">', out)

    def test_paragraphs_and_emphasis(self):
        out = render("Some **bold** and *italic* and _under_ text.\nSame paragraph.\n\nNext.")
        self.assertIn("<p>Some <strong>bold</strong> and <em>italic</em> and <em>under</em> text.\nSame paragraph.</p>", out)
        self.assertIn("<p>Next.</p>", out)

    def test_links_and_inline_code(self):
        out = render("See [the plan](plan.md) and `code <x>`.")
        self.assertIn('<a href="plan.md">the plan</a>', out)
        self.assertIn("<code>code &lt;x&gt;</code>", out)

    def test_unsafe_link_scheme_is_neutralised(self):
        self.assertIn('href="#"', render("[x](javascript:alert(1))"))

    def test_unordered_ordered_and_nested_lists(self):
        out = render("- one\n- two\n  - nested\n- three\n\n3. c\n4. d\n")
        self.assertIn("<ul><li>one</li><li>two<ul><li>nested</li></ul></li><li>three</li></ul>", out)
        self.assertIn('<ol start="3"><li>c</li><li>d</li></ol>', out)

    def test_task_list_items(self):
        out = render("- [ ] T001 open\n- [x] T002 done\n")
        self.assertIn('<input type="checkbox" disabled> T001 open', out)
        self.assertIn('<input type="checkbox" disabled checked> T002 done', out)

    def test_tables(self):
        out = render("| A | B |\n|---|---|\n| 1 | `x|y` |\n")
        self.assertIn("<table><thead><tr><th>A</th><th>B</th></tr></thead>", out)
        self.assertIn("<td>1</td>", out)

    def test_block_quotes_and_rules(self):
        out = render("> quoted **text**\n\n---\n")
        self.assertIn("<blockquote><p>quoted <strong>text</strong></p></blockquote>", out)
        self.assertIn("<hr>", out)

    def test_fenced_code_is_escaped(self):
        out = render("```python\nprint('<b>')\n```\n")
        self.assertIn('<pre><code class="language-python">print(&#x27;&lt;b&gt;&#x27;)</code></pre>', out)

    def test_mermaid_block_is_emitted_for_the_page(self):
        out = render("```mermaid\nflowchart LR\n  A --> B\n```\n")
        self.assertIn('<pre class="mermaid-src">flowchart LR\n  A --&gt; B</pre>', out)

    def test_mermaid_in_a_tooltip_becomes_a_note(self):
        out = specview.render_markdown("```mermaid\nflowchart LR\n```\n", specview.RenderContext(tooltip=True))
        self.assertIn("diagram-note", out)
        self.assertNotIn("mermaid-src", out)


class HiddenContentTest(unittest.TestCase):
    def test_html_comments_are_dropped(self):
        out = render("before <!-- hidden --> after\n\n<!--\nmulti\nline\n-->\nshown\n")
        self.assertNotIn("hidden", out)
        self.assertNotIn("multi", out)
        self.assertIn("before  after", out)
        self.assertIn("shown", out)

    def test_eil_regions_and_blocks_are_dropped(self):
        text = (
            "Keep.\n\n<!-- eil:begin approval -->\nAPPROVED-TEXT\n<!-- eil:end approval -->\n\n"
            '```eil:challenge\n{"id": "CH-001"}\n```\n\nAlso keep.\n'
        )
        out = render(text)
        self.assertNotIn("APPROVED-TEXT", out)
        self.assertNotIn("CH-001", out)
        self.assertIn("Keep.", out)
        self.assertIn("Also keep.", out)

    def test_raw_html_is_escaped(self):
        out = render("<script>alert(1)</script>\n")
        self.assertNotIn("<script>", out)
        self.assertIn("&lt;script&gt;", out)

    def test_comment_between_paragraphs_keeps_them_apart(self):
        out = render("First.\n<!-- note -->\nSecond.\n")
        self.assertIn("<p>First.</p>", out)
        self.assertIn("<p>Second.</p>", out)


if __name__ == "__main__":
    unittest.main()
