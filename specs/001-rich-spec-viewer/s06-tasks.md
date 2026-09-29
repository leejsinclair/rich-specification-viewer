---

description: "Task list for the rich specification viewer"
---

<!--
  STAGE 6 OF THE DEFINITION PIPELINE: What work is required?

  This document is `tasks.md` as Spec Kit sees it (an alias of this file).

  - Every task line ends with `(traces: AIS-###)`, the item of the AI Specification it carries out
    (or an approved decision, `DEC-###`). A task with no source is flagged.
  - A task that builds a screen, a schema or a technical flow also cites the artefact it implements,
    for example `(traces: AIS-014, ART-007)`. Every wireframe, ER diagram and technical sequence
    diagram listed in the AI Specification must be reached by at least one task.
  - A task must not introduce architecture that the approved design does not contain. Raise it as a
    challenge instead.
  - Gate: TSK-G01 to TSK-G03 (`eil check --stage tasks`). The task list is not approved by a person.
  - Keep the sections below the last phase (Not applicable, Challenges, Overrides, Quality Assessment).
-->

# Tasks: Rich specification viewer

**Input**: Design documents from `specs/001-rich-spec-viewer/`

**Prerequisites**: plan.md, spec.md (the AI Specification), research.md, data-model.md, contracts/http.md, contracts/cli.md, quickstart.md

**Tests**: Included, because the AI Specification's Testing Requirements (AIS-051 to AIS-054) ask for unit tests, integration tests and manual browser checks.

**Organization**: Tasks are grouped by user story. US1 = UC-002 (find and read a document), US2 = UC-001 and UC-004 (references explained and followed), US3 = UC-003 (diagrams).

## Format: `[ID] [P?] [Story] Description (traces: AIS-###)`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)
- Everything in the viewer lives in one file, `specview.py` (AIS-038), so implementation tasks on it run in sequence; test and fixture files can be written in parallel.

## Phase 1: Setup (Shared Infrastructure)

- [X] T001 Create `specview.py` at the repository root with a module docstring, a `main()` entry point, a Python 3.11 version check that exits with a message on older versions, and standard-library imports only (traces: AIS-034, AIS-038, AIS-073) (code: 2cceacc)
- [X] T002 [P] Create `tests/__init__.py`, `tests/unit/__init__.py` and `tests/integration/__init__.py` so `python3 -m unittest discover -s tests` finds both suites (traces: AIS-051, AIS-052) (code: 2cceacc)
- [X] T003 [P] Create the fixture project `tests/fixtures/project/specs/` with a story `001-demo/` holding `s01-requirements.md`, `s02-functional-spec.md` (codes referencing s01, an unresolved code, a code defined twice, a challenge block, HTML comments, `eil:` regions, Mermaid blocks of several types including one invalid), a `spec.md` symbolic link and a `plan.md` identical copy of other documents, a `checklists/requirements.md` defining a code, a second story `002-other/` defining a code also used in `001-demo`, and a `specs/README.md` containing codes (traces: AIS-051, AIS-052, AIS-088, AIS-089) (code: 2cceacc)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: the server skeleton, the security checks and the Markdown renderer every story needs.

- [X] T004 Write unit tests for the Path guard (`..`, absolute paths, a symbolic link resolving outside `specs/`, a path inside) in `tests/unit/test_path_guard.py` (traces: AIS-051, AIS-056, AIS-066) (code: 2cceacc)
- [X] T005 [P] Write unit tests for the Host check (`localhost`, `127.0.0.1`, either with any port, a foreign host, a missing header) in `tests/unit/test_host_check.py` (traces: AIS-051, AIS-055) (code: 2cceacc)
- [X] T006 [P] Write unit tests for container detection and bind-address choice, including `--host` override, in `tests/unit/test_startup.py` (traces: AIS-051, AIS-036) (code: 2cceacc)
- [X] T007 [P] Write unit tests for the Markdown renderer covering every construct in FR-004, HTML escaping of text and raw HTML, and the dropping of HTML comments, `eil:` blocks and the assessment, comprehension and approval regions, in `tests/unit/test_markdown.py` (traces: AIS-004, AIS-019, AIS-051, AIS-058) (code: 2cceacc)
- [X] T008 Implement the Path guard in `specview.py`: resolve with `Path.resolve()` and accept only paths that are relative to `<start>/specs`; all file opens go through it, read-only (traces: AIS-018, AIS-041, AIS-056, AIS-057, AIS-066) (code: 2cceacc)
- [X] T009 Implement the Host check in `specview.py`: strip any port and accept only `localhost` and `127.0.0.1`, otherwise `403` (traces: AIS-055) (code: 2cceacc)
- [X] T010 Implement start-up in `specview.py` per `contracts/cli.md`: container detection, bind to `0.0.0.0` or `127.0.0.1`, optional `--host` and `--port`, first free port from 8000 to 8019, start-up lines, `webbrowser.open`, a message and exit when all ports are busy, clean Ctrl+C (traces: AIS-017, AIS-035, AIS-036, AIS-065, AIS-075) (code: 2cceacc)
- [X] T011 Implement the Request handler in `specview.py` on `http.server.ThreadingHTTPServer`: Host check first, route table per `contracts/http.md`, `403`, `404` and `500` pages, per-request log lines and rendering tracebacks to the terminal (traces: AIS-029, AIS-043, AIS-044, AIS-046, AIS-074, AIS-075) (code: 2cceacc)
- [X] T012 Implement the Markdown renderer's block parser in `specview.py`: headings with stable anchors, paragraphs, ordered, unordered and nested lists, task-list items, tables, block quotes, fenced code blocks; drop HTML comments, `eil:` blocks and the assessment, comprehension and approval regions; show anything it cannot interpret as escaped plain text (traces: AIS-004, AIS-019, AIS-030) (code: 2cceacc)
- [X] T013 Implement the renderer's inline pass in `specview.py`: HTML-escape first, then emphasis, inline code and links (traces: AIS-004, AIS-030, AIS-058) (code: 2cceacc)
- [X] T014 Implement the Page template in `specview.py`: inline stylesheet meeting the readability checklist (reading width, clear fonts, spacing, scannable headings and lists), breadcrumbs, the search box, the body slot and the script slots (traces: AIS-005, AIS-020, AIS-038) (code: 2cceacc)

**Checkpoint**: `python3 specview.py` starts, refuses foreign hosts and paths outside `specs/`, and T004 to T007 pass.

---

## Phase 3: User Story 1 - Find and read a document (Priority: P1) 🎯 MVP

**Goal**: the developer navigates or searches `specs/` and reads any document as a formatted HTML page (UC-002).

**Independent Test**: start the viewer on the fixture project; the navigation view lists the stories; `*/s01-*` finds the Requirements document; opening it shows formatted content with breadcrumbs; a folder with no `specs/` shows "No specs folder found".

- [X] T015 [P] [US1] Write unit tests for glob search (plain word wrapped as `*word*`, wildcards, case-insensitivity, sort order, empty pattern, no `specs/`) in `tests/unit/test_search.py` (traces: AIS-051, AIS-033, AIS-061) (code: 2cceacc)
- [X] T016 [P] [US1] Write integration tests that start the server on a free port against the fixture project and check the navigation view, search JSON, a rendered document page, breadcrumbs, `403` for a path above the start folder and a foreign Host header, and "No specs folder found" from a folder without `specs/`, in `tests/integration/test_navigation_and_search.py` (traces: AIS-052, AIS-053, AIS-060) (code: 2cceacc)
- [X] T017 [US1] Implement the navigation view in `specview.py`: list folders and `.md` documents of `specs/` or a subfolder at request time, with breadcrumbs and "No specs folder found" under the search box when `specs/` is missing (traces: AIS-001, AIS-007, AIS-020, AIS-043, AIS-060) (code: 2cceacc)
- [X] T018 [US1] Implement Search and `GET /api/search` in `specview.py` per `contracts/http.md`: walk `specs/` on each request, `fnmatch` on lower-cased relative paths, wrap a pattern with no wildcard as `*pattern*`, sort by path, report `specs: false` when missing (traces: AIS-002, AIS-033, AIS-045, AIS-061, ART-016) (code: 2cceacc)
- [X] T019 [US1] Implement the Search box script embedded in `specview.py`: call `/api/search`, list results as links, show "no matches" or "No specs folder found" underneath the box, leave the navigation view for an empty pattern (traces: AIS-002, AIS-040, AIS-060, AIS-061, ART-016) (code: 2cceacc)
- [X] T020 [US1] Implement the document page route in `specview.py`: render the requested `.md` through the Path guard and renderer into the Page template, returning `404` with a message for a document removed or renamed since it was listed (traces: AIS-003, AIS-044, AIS-063) (code: 2cceacc)

**Checkpoint**: US1 is usable on its own: every document can be found and read.

---

## Phase 4: User Story 2 - References explained and followed (Priority: P2)

**Goal**: every reference code is marked; hovering shows its whole defining section from the same story, and clicking goes there; broken codes are highlighted (UC-001, UC-004).

**Independent Test**: in the fixture story, hovering a code from `s01` in `s02` shows its section and source; clicking opens it; the unresolved and twice-defined codes show a red error with an icon; `AIS` codes on `spec.md` show no error; codes on `specs/README.md` are plain text; a code defined only in `002-other` is not resolved in `001-demo`.

- [X] T021 [P] [US2] Write unit tests for the Story index and reference rules (code forms, definition forms including tasks and challenge blocks, section boundaries, codes in code are not references, story scope, nested documents, link and copy aliases counted once, unresolved and ambiguous, documents directly in `specs/`) in `tests/unit/test_story_index.py` (traces: AIS-024, AIS-025, AIS-026, AIS-027, AIS-028, AIS-051, AIS-088, AIS-089) (code: 2cceacc)
- [X] T022 [P] [US2] Write integration tests for embedded tooltip JSON, reference links and error spans, JSON escaping, and a tooltip updating after another story document changes, in `tests/integration/test_references.py` (traces: AIS-052, AIS-053, AIS-059) (code: 2cceacc)
- [X] T023 [US2] Implement the Story index in `specview.py` per `data-model.md`: walk the story at every depth through the Path guard, detect link and identical-copy aliases, collect definitions (items, headings, tasks, `eil:challenge` blocks with their answers) with their defining-section HTML, and build no index for documents directly in `specs/` (traces: AIS-009, AIS-022, AIS-024, AIS-025, AIS-026, AIS-048, AIS-069, AIS-088, AIS-089) (code: 2cceacc)
- [X] T024 [US2] Implement the story-wide render cache in `specview.py`: key on every document's relative path, `mtime_ns` and size, guarded by a lock, so any change in the story re-renders its pages on the next request (traces: AIS-006, AIS-029, AIS-050) (code: 2cceacc)
- [X] T025 [US2] Implement the Reference marker in `specview.py`: mark each code outside code, as a link to its defining anchor when resolved, or a red `<span>` with an error icon when unresolved or ambiguous; leave codes unmarked on documents directly in `specs/` (traces: AIS-008, AIS-012, AIS-013, AIS-027, AIS-028, AIS-064, ART-015, ART-018) (code: 2cceacc)
- [X] T026 [US2] Embed the tooltip JSON for the codes each page uses in `specview.py`, with `<`, `>` and `&` escaped, replacing diagrams in sections with a note (traces: AIS-010, AIS-023, AIS-032, AIS-049, AIS-059, ART-015) (code: 2cceacc)
- [X] T027 [US2] Implement the Tooltip controller script embedded in `specview.py`: on hover show the section and document name, capped in size and scrolling inside; explain unresolved and ambiguous codes; show challenge text, target, status and answer; open no tooltip for codes inside a tooltip; hide when the pointer leaves code and tooltip (traces: AIS-010, AIS-011, AIS-021, AIS-022, AIS-040, ART-015) (code: 2cceacc)
- [X] T028 [US2] Implement reference following in `specview.py`: resolved codes link to `/specs/<path>#<anchor>` (the Challenges section for a challenge code), scroll within the same document, and error codes do not navigate (traces: AIS-012, AIS-022, AIS-064, ART-018) (code: 2cceacc)

**Checkpoint**: US1 and US2 both work independently.

---

## Phase 5: User Story 3 - Diagrams (Priority: P3)

**Goal**: every valid Mermaid diagram is drawn; one that cannot be drawn shows an error while the rest of the page works (UC-003).

**Independent Test**: the fixture `s02` page draws each valid diagram, including C4 and ER; the invalid block shows an error; with the network off every diagram shows an error while text and tooltips still work.

- [X] T029 [P] [US3] Write an integration test that Mermaid blocks are emitted as escaped `<pre class="mermaid-src">` elements and that the page imports only the pinned-major Mermaid URL as outside script, in `tests/integration/test_diagrams.py` (traces: AIS-031, AIS-042, AIS-047, AIS-052) (code: 2cceacc)
- [X] T030 [US3] Emit each fenced `mermaid` block from the renderer in `specview.py` as `<pre class="mermaid-src">` with its source escaped (traces: AIS-014, AIS-030) (code: 2cceacc)
- [X] T031 [US3] Implement the Diagram loader module script embedded in `specview.py`: import `mermaid@11` from jsDelivr, `initialize({startOnLoad: false})`, render each block with `mermaid.render()` in `try`/`catch`, replace a failed block with an error message, and every block when the import fails (traces: AIS-014, AIS-015, AIS-016, AIS-031, AIS-047, AIS-062, ART-017) (code: 2cceacc)

**Checkpoint**: all three stories work independently.

---

## Phase 6: Polish & Cross-Cutting Concerns

- [X] T032 Run `python3 -m unittest discover -s tests` and fix any failure in `specview.py` (traces: AIS-051, AIS-052, AIS-053) (code: 2cceacc)
- [X] T033 Walk the browser scenarios of `specs/001-rich-spec-viewer/quickstart.md` (tooltips, scrolling, no nested tooltips, every diagram type, offline and invalid diagrams, readability) and fix what fails in `specview.py` (traces: AIS-054, AIS-005) (code: 2cceacc)
- [X] T034 [P] Confirm by review that `specview.py` imports only the standard library, writes no file, and makes no outside request from the server (traces: AIS-042, AIS-057, AIS-072, AIS-073) (code: 2cceacc)

---

## Dependencies & Execution Order

- **Setup (T001 to T003)** first; T002 and T003 in parallel with T001.
- **Foundational (T004 to T014)** blocks every story. The test files T004 to T007 run in parallel; T008 to T014 are sequential edits to `specview.py`.
- **US1 (T015 to T020)** needs Foundational. **US2 (T021 to T028)** needs Foundational and T020 (the document page). **US3 (T029 to T031)** needs Foundational and T020.
- US2 and US3 do not depend on each other; with one file, implement them one after the other.
- **Polish (T032 to T034)** last.

## Parallel Examples

- Foundational: T004, T005, T006 and T007 (four test files) together.
- US1: T015 and T016 together, before T017.
- US2: T021 and T022 together, before T023.

## Implementation Strategy

1. **MVP**: Setup, Foundational and US1: a viewer that finds and renders every document safely. Validate with quickstart scenarios 1 to 3, 11 to 13.
2. **Add US2**: tooltips, following and error highlighting. Validate scenarios 4 to 7 and 10.
3. **Add US3**: diagrams. Validate scenarios 8 and 9.
4. **Polish**: full test run and browser walk-through, including readability (scenario 14).

## Not applicable

- Wireframes (ART-006 to ART-011): waived by OVR-001 and not listed in the AI Specification, so no task implements a wireframe export.
- ER diagrams: the Technical Specification records that no persistent data is added, so there is no schema task.

## Challenges

<!-- Recorded by `eil challenge`. -->

## Overrides

<!-- Recorded by `eil override`, each naming who, what and why. -->

## Quality Assessment

<!-- eil:begin assessment -->
```json
{
  "stage": "tasks",
  "evaluated_at": "2026-09-29T11:30:36Z",
  "fingerprint": "sha256:95f3b5d6051704e0580cf86b7d638a74119a812ce13f717de602a9096670de7d",
  "criteria": [
    {
      "id": "TSK-G01",
      "kind": "traceability",
      "status": "met",
      "reason": ""
    },
    {
      "id": "TSK-G02",
      "kind": "traceability",
      "status": "met",
      "reason": ""
    },
    {
      "id": "TSK-G03",
      "kind": "judgment",
      "status": "met",
      "reason": "AI assessment: Every implementation task builds a component named in ART-013 or ART-014 inside the single approved script, and the tests and fixture follow the approved Testing Strategy; no task adds a container, store, dependency or integration."
    }
  ],
  "assessment": {
    "ambiguity": [],
    "missing": [],
    "contradictions": [],
    "unsupported_assumptions": [
      "T001's version check that exits on Python older than 3.11 and T010's explicit --port failing when busy come from contracts/cli.md, not from an approved stage",
      "The readability values in research.md R-10 guide T014 but are not stated in any approved stage"
    ],
    "untestable": []
  },
  "findings": []
}
```
<!-- eil:end assessment -->
