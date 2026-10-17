# Quickstart: checking reading-order navigation

Prerequisites: Python 3.11 or later, the repository root as the working directory, and the change implemented.

1. Run the tests: `python3 -m unittest discover -s tests`. The 74 existing tests and the new `tests/unit/test_reading_order.py` and `tests/integration/test_reading_order.py` pass.
2. Start the viewer: `python3 specview.py`, and open a document of a story, for example `specs/002-reading-order-navigation/s03-technical-spec.md`.
3. At the bottom of the page there is a "Documents in reading order" section. Its entries are in stage order (`s00`, `s01`, ..., `s10`), documents of the story folder before documents of nested folders, and the document you are viewing is bold, not underlined, and is not a link.
4. Follow another entry: that page shows the same section with its own entry as the current one.
5. Open a document directly under `specs/` (not in a story folder), the folder navigation page and a search result page: none of them has the section.
