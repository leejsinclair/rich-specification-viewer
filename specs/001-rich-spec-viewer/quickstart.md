# Quickstart: validating the rich specification viewer

A run-and-check guide. Interfaces are in [contracts/http.md](contracts/http.md) and [contracts/cli.md](contracts/cli.md); structures in [data-model.md](data-model.md).

## Prerequisites

- Python 3.11 or later; nothing to install.
- A browser. Internet access for diagrams (Mermaid is loaded from jsDelivr).

## Run the automated tests

```bash
python3 -m unittest discover -s tests
```

Expected: all unit and integration tests pass. The integration tests start the server on a free port against `tests/fixtures/project`.

## Run the viewer on this repository

```bash
cd /path/to/rich-specification-viewer
python3 specview.py
```

Expected: the start-up lines from `contracts/cli.md`, and the browser opens the navigation view showing `001-rich-spec-viewer`.

## Validation scenarios

| # | Do | Expect | Covers |
|---|---|---|---|
| 1 | Open `/` | Story folders under `specs/`; breadcrumbs; search box | AC-1, AC-13 |
| 2 | Search `*/s01-*`, then `zzz` | The Requirements document of each story; then "no matches" | AC-2 |
| 3 | Open `s01-requirements.md` | Headings, lists, tables and code blocks formatted; no HTML comments or `eil:` blocks | AC-3, AC-14 |
| 4 | In `s02-functional-spec.md`, hover `REQ-001`; click it | Tooltip with the whole REQ-001 item from `s01-requirements.md`, naming it; the click opens `s01` at REQ-001 | AC-4, AC-5 |
| 5 | Hover a code inside that tooltip; hover a long section | No nested tooltip; the long one scrolls inside a capped tooltip | AC-12 |
| 6 | Hover `CH-007` | Challenge text, target, status and answer; the click opens the Challenges section of `s02` | AC-15 |
| 7 | Open `spec.md` and hover any `AIS` code | Its section, and no ambiguous error | AC-18 |
| 8 | Open a page with Mermaid blocks | Every diagram drawn, including C4 and ER; a tooltip for a section with a diagram shows a note instead | AC-7, AC-16 |
| 9 | Turn off the network and refresh | Each diagram shows an error message; text, tables and tooltips still work | AC-8 |
| 10 | Edit `s01-requirements.md`, save, refresh an `s02` page | The tooltip for the edited REQ shows the new text | AC-9, CH-015 |
| 11 | Request `/specs/../README.md` | `403` with the outside-the-folder message | AC-10 |
| 12 | `curl -H 'Host: evil.example' http://127.0.0.1:8000/` | `403` | CH-016 |
| 13 | Run from a folder with no `specs/` | "No specs folder found" under the search box | AC-17 |
| 14 | Judge readability of a long document | Fixed reading width, clear fonts, spacing between elements, easy to scan | NFR-001 |

Scenarios 5 to 9 and 14 are browser checks; the rest are also covered by the integration tests.
