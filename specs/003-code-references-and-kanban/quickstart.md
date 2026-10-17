# Quickstart: validating cross-reference codes and the kanban view

Interfaces are in [contracts/http.md](contracts/http.md).

## Prerequisites

- Python 3.11 or later; nothing to install.
- A browser.

## Run the automated tests

```bash
python3 -m unittest discover -s tests
```

Expected: all unit, integration and end to end tests pass.

## Run the viewer

```bash
python3 specview.py
```

## Validation scenarios

| # | Do | Expect | Covers |
|---|---|---|---|
| 1 | Open a story document that references a code introduced in another document of the same story under a prefix not in the fixed list | The code is marked, with hover and click to its definition | FR-001, FR-003 |
| 2 | Open a document of another story using that prefix | The code is not marked | FR-005 |
| 3 | Reference a discovered-form code with no definition, or two | The error is shown | FR-004 |
| 4 | Open `/specs/<story>/kanban` for a story with tasks | Four columns of cards grouped by phase | FR-006, FR-007, FR-011 |
| 5 | Open it with `?group=story` | Cards grouped by user story; untagged tasks under Unallocated | FR-007 |
| 6 | Mark tasks `[~]`, `[!]`, `(blocked)`; one with both in progress and blocked | They land in in progress and blocked; the tie goes to blocked | FR-008 |
| 7 | Open the board for a story with no or an empty `tasks.md` | The "no tasks found" message | FR-010 |
| 8 | Check `tasks.md` after viewing the board | Unchanged | FR-009 |
| 9 | Edit an open document, scrolled part way down | Within about 10 seconds the page shows the new content at the same scroll position | FR-012 |
| 10 | Edit `tasks.md` while the board is open on `?group=story` | Within about 10 seconds the board updates and keeps its grouping | FR-012, NFR-001 |
| 11 | Delete the shown file | The page keeps its last content | FR-012 |
| 12 | Request `/api/stamp` with a path outside `specs/` or a wrong `Host` | `403` | DEC-004 |
