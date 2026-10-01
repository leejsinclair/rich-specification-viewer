---

description: "Task list template for feature implementation"
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

# Tasks: Reading-order navigation for story documents

**Input**: Design documents from `/specs/002-reading-order-navigation/`

**Prerequisites**: plan.md (required), spec.md (the AI Specification), research.md, quickstart.md. There is no data-model.md and no contracts/ (the design adds no data and no interface).

**Tests**: The AI Specification's Testing Requirements (AIS-043 to AIS-047) ask for unit and integration tests, so test tasks are included.

**Organization**: Tasks are grouped by use case: US1 is UC-001 (read a story in order), US2 is UC-002 (find a nested document, with the aliases, links and path safety that go with it), US3 is UC-003 (a document directly under `specs/` gets nothing).

## Format: `[ID] [P?] [Story] Description (traces: AIS-###)`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)
- Include exact file paths in descriptions
- End every task with `(traces: AIS-###)`

## Phase 1: Setup (Shared Infrastructure)

- [X] T001 Run `python3 -m unittest discover -s tests` from the repository root and confirm the 74 existing tests pass before any change (traces: AIS-072, AIS-046)
- [X] T002 Read `Viewer._markdown_files`, `Viewer._render_document`, `PathGuard.resolve`, `ALIAS_NAMES`, `doc_url`, `esc`, the inline `CSS` in `specview.py`, and the server start in `tests/integration/support.py`, so the new code reuses them (traces: AIS-034, AIS-035, AIS-036, AIS-073)

## Phase 2: Foundational (Blocking Prerequisites)

- [X] T003 In `specview.py` add the pure helpers `stage_of(file_name)`, `natural_key(text)` and `reading_order_key(parts, staged)`: a stage is `s`, exactly two digits, a hyphen and a name; names compare with `casefold`, digit runs by value, ties by exact characters; the key has a folder part per folder then a document part, staged before unstaged within a folder (traces: AIS-041, AIS-019, AIS-026, AIS-063, ART-008)
- [X] T004 In `specview.py` add `Viewer.reading_order(story, current_rel)` returning the section HTML as a stateless function of names and resolved paths, depending only on `Viewer._markdown_files`, `PathGuard.resolve`, `doc_url` and `esc`; it returns an empty string for a story with no listed document (traces: AIS-041, AIS-031, AIS-032, AIS-015, ART-008)
- [X] T005 In `specview.py` change only `Viewer._render_document` to append the result of `reading_order` after the rendered body of a document inside a story folder; leave the request handler, the path guard, `navigation_page`, `search` and `page_html` unchanged (traces: AIS-023, AIS-033, AIS-037, AIS-059, ART-008)
- [X] T006 [P] In `specview.py` add the `.reading-order` rules to the inline `CSS`: links keep the existing underlined style and colour, the current entry is bold, not underlined, in the text colour, with no external file (traces: AIS-039, AIS-028, AIS-064)

**Checkpoint**: the viewer starts and shows the section on every story document; existing tests still pass.

## Phase 3: User Story 1 - Read a story from start to finish (Priority: P1) 🎯 MVP

**Goal**: each document of a story ends with the "Documents in reading order" section, listing the story's documents in stage order with the current one marked.

**Independent Test**: start the viewer on a temporary story with `s00` to `s10` documents and open one; the section lists them in numeric stage order, the opened one is plain bold text with `aria-current="page"`, and every other entry is a working link.

- [X] T007 [P] [US1] Create `tests/unit/test_reading_order.py` with tests for `stage_of` and the labels (`s1-x.md`, `s100-x.md`, `S01-x.md`, `s01_x.md`, `s01.md` have no stage) and for the sort key (`s00` to `s10`, case, numbers inside names, the same order for any creation order) (traces: AIS-043, AIS-019, AIS-007, AIS-063)
- [X] T008 [P] [US1] Create `tests/integration/test_reading_order.py` that starts the real server on a temporary story folder as `tests/integration/support.py` does and checks the region's accessible name, the `<ol>` list, the order of the entries, exactly one `aria-current="page"` as plain text inside the section (not the breadcrumbs) and links on every other entry (traces: AIS-044, AIS-040, AIS-002, AIS-010, AIS-011, AIS-073)
- [X] T009 [US1] In `specview.py` produce the entry labels: the path relative to the story folder without the extension, `[stage NN: <name>]` for a staged document and `<path> [ref doc: <name>]` for an unstaged one, with every name escaped by `esc` (traces: AIS-003, AIS-004, AIS-005, AIS-036, AIS-049)
- [X] T010 [US1] In `specview.py` write the section markup: `<nav class="reading-order" aria-label="Documents in reading order">` with a visible `<h2>` of the same text and an `<ol>` of `<li>` entries, a link entry as `<a href>` built with `doc_url`, the current entry as `<span aria-current="page">` (traces: AIS-028, AIS-001, AIS-002, AIS-010, AIS-011, AIS-027)
- [X] T011 [US1] In `specview.py` order the entries by sorting the whole list once with `reading_order_key` and mark the current entry as the one whose path is the path being viewed (traces: AIS-007, AIS-026, AIS-027, DEC-005)
- [X] T012 [US1] In `tests/integration/test_reading_order.py` add a test for a story with one document (the only entry, marked current) (traces: AIS-052, AIS-010)
- [X] T013 [P] [US1] In `tests/unit/test_reading_order.py` add a contrast test that computes the ratio of the link colour and the text colour against the background from the `CSS` values and requires at least 4.5:1 (traces: AIS-045, AIS-064)

**Checkpoint**: User Story 1 works and is tested on its own.

## Phase 4: User Story 2 - Find a nested document (Priority: P2)

**Goal**: documents in nested folders are listed after the folder's own documents, aliases are folded into their source entries, and only reachable documents are listed.

**Independent Test**: start the viewer on a story with nested folders, an alias, a link into another story and a link to a file outside `specs/`; the nested documents follow the parent folder's documents, the alias shows in round brackets, the other story's document is listed under the link's path, and the outside file is not listed.

- [X] T014 [P] [US2] In `tests/unit/test_reading_order.py` add tests, on temporary folders with real symbolic links, for sibling folders, a folder's documents before a nested folder's, staged before unstaged within a folder, and alias recognition (a regular `plan.md`, a link to an unstaged document, a link into another story, a link to a missing target, two aliases of one document) (traces: AIS-043, AIS-008, AIS-009, AIS-020, AIS-021)
- [X] T015 [P] [US2] In `tests/integration/test_reading_order.py` add tests for nested story order, an alias shown in round brackets with its source current, two stories not listing each other, an empty folder adding nothing, a symbolic link into another story listed and linked to its real path, and a link to a file outside `specs/` not listed (traces: AIS-044, AIS-006, AIS-013, AIS-014, AIS-015, AIS-050, AIS-051, AIS-057)
- [X] T016 [US2] In `specview.py` take the story's documents only from `Viewer._markdown_files(<story folder>)` and never open a document to build the section (traces: AIS-024, AIS-034, AIS-014, AIS-022, AIS-048, AIS-038)
- [X] T017 [US2] In `specview.py` recognise an alias only when its name is in `ALIAS_NAMES`, it is itself a symbolic link, and its fully resolved target is a staged document of the same story that has an entry; fold it into the source entry as round-bracket file names in alphanumeric order, and list any other such file as an ordinary document (traces: AIS-006, AIS-021, AIS-025, AIS-035, AIS-055, AIS-062)
- [X] T018 [US2] In `specview.py` link an entry whose symbolic link resolves into another story to the target's real path, labelled by the link's path, and list nothing that `PathGuard.resolve` places outside `specs/` (traces: AIS-013, AIS-027, AIS-050, AIS-057, AIS-048)
- [X] T019 [US2] In `specview.py` add a document viewed through a symbolic link to a folder as the current entry under its own path, placed and labelled by the same rules, and list no other file of that linked folder (traces: AIS-054, AIS-024)
- [X] T020 [US2] In `specview.py` label a file named exactly `.md` as `[ref doc: blank]` after its folder path (traces: AIS-053, AIS-005)
- [X] T021 [US2] In `tests/unit/test_reading_order.py` and `tests/integration/test_reading_order.py` add tests for the `.md` file label, the document viewed through a symbolic link to a folder, a listed document removed after the render (its link gives the existing not-found page), and a file or folder name holding `<`, `&`, a quote or a space (traces: AIS-053, AIS-054, AIS-056, AIS-049)

**Checkpoint**: User Stories 1 and 2 both work and are tested.

## Phase 5: User Story 3 - Read a document directly under specs (Priority: P3)

**Goal**: documents directly under `specs/`, the folder navigation page and the search results get no section.

**Independent Test**: open a Markdown document directly under `specs/`, the folder navigation page and a search result; none has the section.

- [X] T022 [P] [US3] In `tests/integration/test_reading_order.py` add tests that a document directly under `specs/` has no section and that the folder navigation page and a search result have none (traces: AIS-044, AIS-012, AIS-017, AIS-060)
- [X] T023 [US3] In `specview.py` make `Viewer._render_document` add the section only for a document that lies inside a story folder, so a document directly under `specs/`, the navigation page and the search results are unchanged (traces: AIS-018, AIS-012, AIS-017, AIS-023, AIS-060)

**Checkpoint**: all three use cases work.

## Phase 6: Polish & Cross-Cutting Concerns

- [X] T024 Run `python3 -m unittest discover -s tests` and confirm the 74 existing tests and the new ones all pass, which shows tooltips, error marking, search, folder navigation, breadcrumbs and diagrams are unchanged (traces: AIS-046, AIS-016, AIS-061, AIS-072)
- [X] T025 [P] Check that the change adds no dependency, route, endpoint or script, and that only `Viewer._render_document`, the inline `CSS` and the new helpers changed in `specview.py` (traces: AIS-058, AIS-059, AIS-030, AIS-033, AIS-065)
- [X] T026 [P] Run the quickstart validation in `specs/002-reading-order-navigation/quickstart.md` against the running viewer (traces: AIS-047, AIS-052)

## Dependencies and execution order

- Phase 1, then Phase 2, which blocks the three stories.
- US1 (T007 to T013) comes first and is the MVP. US2 (T014 to T021) and US3 (T022, T023) change the same function `reading_order` and `_render_document` in `specview.py`, so their `specview.py` tasks run one after another; the test tasks marked [P] are in separate files or sections and can be written in parallel.
- Phase 6 follows all the stories.

## Not applicable

<!-- Sections removed from this document, each with its reason. -->

## Challenges

<!-- Recorded by `eil challenge`. -->

## Overrides

<!-- Recorded by `eil override`, each naming who, what and why. -->

## Change Log (traces: DEC-001)

<!-- eil:begin changelog -->
<!-- eil:end changelog -->

## Record (traces: DEC-001)

<!-- eil:begin provenance -->
```json
{
  "version": 1,
  "blocks": {
    "#f52d711103d5": {
      "hash": "sha256:f52d711103d50a437830c6fbcd04fb4bab49a0f82f6d26d1c791c6e8488dd090",
      "class": "inferred",
      "reviewed": {
        "by": "Lee Sinclair",
        "at": "2026-10-01T13:36:24Z",
        "list": "RVW-009",
        "reply": "Ok"
      }
    },
    "#2cf5717e5d14": {
      "hash": "sha256:2cf5717e5d14288202df5613edf212e42618ba7e9f8bd855a74bb75cd8230860",
      "class": "inferred",
      "reviewed": {
        "by": "Lee Sinclair",
        "at": "2026-10-01T13:36:24Z",
        "list": "RVW-009",
        "reply": "Ok"
      }
    },
    "Tasks: Reading-order navigation for story documents#766685533721": {
      "hash": "sha256:76668553372157d9a9128be091ec525f0e7ead574c4395f4b80b4113bc40d789",
      "class": "inferred",
      "adds": "Adds the grouping, goal, test criteria or ordering that organises the tasks, which the AI Specification does not state.",
      "reviewed": {
        "by": "Lee Sinclair",
        "at": "2026-10-01T13:36:24Z",
        "list": "RVW-009",
        "reply": "Ok"
      }
    },
    "Tasks: Reading-order navigation for story documents#2654923f9d33": {
      "hash": "sha256:2654923f9d3305a4235f9c72ec790d40648d0f4fdf31c552b2c50ba53fc0ba61",
      "class": "inferred",
      "adds": "Adds the grouping, goal, test criteria or ordering that organises the tasks, which the AI Specification does not state.",
      "reviewed": {
        "by": "Lee Sinclair",
        "at": "2026-10-01T13:36:24Z",
        "list": "RVW-009",
        "reply": "Ok"
      }
    },
    "Tasks: Reading-order navigation for story documents#74d454cbf32e": {
      "hash": "sha256:74d454cbf32e95104d8974a0a756d0614e8fd76041633f3b5c91bb2b3f73d2e3",
      "class": "inferred",
      "adds": "Adds the grouping, goal, test criteria or ordering that organises the tasks, which the AI Specification does not state.",
      "reviewed": {
        "by": "Lee Sinclair",
        "at": "2026-10-01T13:36:24Z",
        "list": "RVW-009",
        "reply": "Ok"
      }
    },
    "Tasks: Reading-order navigation for story documents#47963b2f5376": {
      "hash": "sha256:47963b2f53761ceaa92f68329a0b2c1d1a2d21a9d0f22daeaec5013dde583893",
      "class": "inferred",
      "adds": "Adds the grouping, goal, test criteria or ordering that organises the tasks, which the AI Specification does not state.",
      "reviewed": {
        "by": "Lee Sinclair",
        "at": "2026-10-01T13:36:24Z",
        "list": "RVW-009",
        "reply": "Ok"
      }
    },
    "§Format: `[ID] [P?] [Story] Description `": {
      "hash": "sha256:78ecff41c1b9dbf4c7a3caffaf8d3df65f3a498a6db05a25bb4b8e93ae5f0f99",
      "class": "inferred",
      "reviewed": {
        "by": "Lee Sinclair",
        "at": "2026-10-01T13:36:24Z",
        "list": "RVW-009",
        "reply": "Ok"
      }
    },
    "T001": {
      "hash": "sha256:24e8969252488b642972e523f9bc2cb3b9d4eb9f67615be8957719a1e757a879",
      "class": "restated",
      "cites": {
        "AIS-072": "sha256:0bf9e4d35bb7db4ce08bc326a291c9f80c1fce8aa4ceca7880769384588e0e7d",
        "AIS-046": "sha256:4792cd0d137f7703b41afb02fef701d595b090df0d8ca64756f18f64a6c3256a"
      },
      "completed_against": {
        "AIS-046": "sha256:4792cd0d137f7703b41afb02fef701d595b090df0d8ca64756f18f64a6c3256a",
        "AIS-072": "sha256:0bf9e4d35bb7db4ce08bc326a291c9f80c1fce8aa4ceca7880769384588e0e7d",
        "DEC-007": "sha256:c092606ae0d1acdb955329fb0999903f6b0219c952e9d0bbaa51fa3ef1b8ce76",
        "FR-016": "sha256:ea3570068dfeaaa7dda913bd48c48be6dd4a84a8b69fe0e06859657edfaeb67d",
        "NFR-002": "sha256:b6d43217718ec3585d21c7e35c03545369d59141a6cd7f07acb47100eef1826b",
        "NFR-003": "sha256:38473b65fca10e09faa1982b8eee81daace9150eebf3baefbaa5e7209036eabf",
        "REQ-005": "sha256:05e5b7ff7f62222173552749b93cd16789de08c57b13afb8171919152c976b57",
        "REQ-009": "sha256:726e06a357ca16e93d7ddde707c7d9b1a7a0d583ae14dfc677a33b7b0efa370c",
        "REQ-010": "sha256:aeba84bc66554b71b5aa5286cde9cbe4906cc3b0b502f744baa1561c4f22890a"
      },
      "blocked_at_completion": false
    },
    "T002": {
      "hash": "sha256:0a0a1828b0d200b5935a2ea9236e296ad192bbbdd4466395f6e7b38e2bc2e935",
      "class": "inferred",
      "adds": "Adds the instruction to read the existing code before changing it.",
      "reviewed": {
        "by": "Lee Sinclair",
        "at": "2026-10-01T13:36:24Z",
        "list": "RVW-009",
        "reply": "Ok"
      },
      "sources": {
        "AIS-034": "sha256:78bddaf7b4901a446ac1c0da1b283fa70f1452351fb39a34a5545c5e3dc4045c",
        "AIS-035": "sha256:36f2adb477c1ed19b889389cd562597743c5e0fec1c126b5b37be07fa564cde8",
        "AIS-036": "sha256:a550507c3cd8f3326ff97eeb9c0622d5da8ba74ee1dfb197ddd296e56da8e1e5",
        "AIS-073": "sha256:339a23541e50e8ae1a51f34e0731075e73ce78d34235127ca88ec96786c9ca58"
      },
      "completed_against": {
        "AIS-034": "sha256:78bddaf7b4901a446ac1c0da1b283fa70f1452351fb39a34a5545c5e3dc4045c",
        "AIS-035": "sha256:36f2adb477c1ed19b889389cd562597743c5e0fec1c126b5b37be07fa564cde8",
        "AIS-036": "sha256:a550507c3cd8f3326ff97eeb9c0622d5da8ba74ee1dfb197ddd296e56da8e1e5",
        "AIS-073": "sha256:339a23541e50e8ae1a51f34e0731075e73ce78d34235127ca88ec96786c9ca58",
        "DEC-002": "sha256:e5e293b732dc3070124d2538a452ac15b148fb9937d58da144d4ee8d004b2032",
        "DEC-003": "sha256:36efe9d2ce0818895e0200cf12258c73ee561dcb82dbf2c4a1723d203a605105",
        "DEC-006": "sha256:39b03e67818d400e49ee296e2e3c28ac91daeaa69b23d14ab9a0ae88a080b5de",
        "DEC-007": "sha256:c092606ae0d1acdb955329fb0999903f6b0219c952e9d0bbaa51fa3ef1b8ce76",
        "FR-001": "sha256:9b8829cba27184e4e9004fc0ba4af995bb30d52c81be952f804b2817d4ed7a36",
        "FR-002": "sha256:32dc804048b7e426e532d1b98c0fc50d4ebdb1ebea550a3caa6e72002e6f2e6f",
        "FR-006": "sha256:3e514e8dfd04bc478e405c56c902c4d400ee8620a0edc9f5da1d311dea49978d",
        "FR-010": "sha256:8aa5f448ddb370a99dcbb5281add4a0106cbb03152c32325dd17c921f07fe781",
        "FR-011": "sha256:0ca8c3df85b82bec17637d1f09bab4668b4bd26b3337664b6990b103bab3b0ec",
        "FR-014": "sha256:ad118cfdcba914b6dcced02aeaa12e219170b3d9b9b64e1cb3ae800f2cf133cd",
        "FR-015": "sha256:f1d6d8705d95ac71564ee91d3882b78a9adc9ded77660d8d1531a57c74db3bb0",
        "FR-016": "sha256:ea3570068dfeaaa7dda913bd48c48be6dd4a84a8b69fe0e06859657edfaeb67d",
        "NFR-002": "sha256:b6d43217718ec3585d21c7e35c03545369d59141a6cd7f07acb47100eef1826b",
        "NFR-003": "sha256:38473b65fca10e09faa1982b8eee81daace9150eebf3baefbaa5e7209036eabf",
        "REQ-001": "sha256:256ed10c2afe9e022501c4f25204361be56ca8ebe3e3b4e74b6738c84ce8c568",
        "REQ-004": "sha256:b52a4907c94a13f2f9fa348ca1da6350f4504b1786482733a63bf8784b4b091f",
        "REQ-005": "sha256:05e5b7ff7f62222173552749b93cd16789de08c57b13afb8171919152c976b57",
        "REQ-007": "sha256:bb73c59fe2c6e1a8dc4e62a7718608d9cc9c9b2c1ca3dc4e1b8d91b8ace51041",
        "REQ-008": "sha256:f70bd5a6e36b3acdc1e0ef4100073132fb4a46ffcc099383dc4bc14f247254fe",
        "REQ-009": "sha256:726e06a357ca16e93d7ddde707c7d9b1a7a0d583ae14dfc677a33b7b0efa370c",
        "REQ-010": "sha256:aeba84bc66554b71b5aa5286cde9cbe4906cc3b0b502f744baa1561c4f22890a",
        "REQ-011": "sha256:ef32b333ad49ed6d560a3000ff6018a61fc3b9c3c62c7ff1d361ca6da28ef3b6",
        "UC-001": "sha256:39bc034f14596d29449003ea963e3a0b3f51215ee9e15e11c5fef4ae2aaed9ab",
        "UC-002": "sha256:98a48e376358abb62b44feb49ed89036461de691abb57208c9127ef4e0918d00"
      },
      "blocked_at_completion": false
    },
    "T003": {
      "hash": "sha256:00f3571f5073f932a340249c4daf09f8e593a0d4c64149028c048c7439ca2442",
      "class": "restated",
      "cites": {
        "AIS-041": "sha256:950b583b5ce9974d7997eb650727f9c9e6b030de2e4db703f07b7f4bed46a3fc",
        "AIS-019": "sha256:a997103070992e4c060534caba5663d24445fe04793930c80f13b655fe2ba3d7",
        "AIS-026": "sha256:fb41e3346fa2320682eaa6c062601114552d60ebb273a6e385bebbfced0034ec",
        "AIS-063": "sha256:9f81319bfeb664e3fd3502379d744995dd2ed0514c9d81352c8a6aa5aa66297d",
        "ART-008": "sha256:f6fef5898a572d62890e617df6b3c58cd89f75af3a3f1c891255b59bd498b730"
      },
      "completed_against": {
        "AIS-019": "sha256:a997103070992e4c060534caba5663d24445fe04793930c80f13b655fe2ba3d7",
        "AIS-026": "sha256:fb41e3346fa2320682eaa6c062601114552d60ebb273a6e385bebbfced0034ec",
        "AIS-041": "sha256:950b583b5ce9974d7997eb650727f9c9e6b030de2e4db703f07b7f4bed46a3fc",
        "AIS-063": "sha256:9f81319bfeb664e3fd3502379d744995dd2ed0514c9d81352c8a6aa5aa66297d",
        "ART-008": "sha256:f6fef5898a572d62890e617df6b3c58cd89f75af3a3f1c891255b59bd498b730",
        "DEC-001": "sha256:bb921b2401109f1ece0e7a13243eaba9121b572231d2c6402f21a46830d083aa",
        "DEC-002": "sha256:e5e293b732dc3070124d2538a452ac15b148fb9937d58da144d4ee8d004b2032",
        "DEC-004": "sha256:7b10b4a428165cd28fee8fa2619828a86dc5bbf81c06f10415da597c69d300d7",
        "DEC-005": "sha256:141ce780db6dcb541ca4b1c2e4792550978c143cbd5eea57838c9736579db7be",
        "FR-001": "sha256:9b8829cba27184e4e9004fc0ba4af995bb30d52c81be952f804b2817d4ed7a36",
        "FR-004": "sha256:9351afecec6d138f345d4b8a50128f10215e41705620c6441d15ebeb92e564a8",
        "FR-005": "sha256:65cffe4e76d287540239f49d99854034164b552e04e3a5f968efbc820d0fc590",
        "FR-006": "sha256:3e514e8dfd04bc478e405c56c902c4d400ee8620a0edc9f5da1d311dea49978d",
        "FR-007": "sha256:7bcffe16420753854d6ef411e7c3099f58fe40bf91b17e707680884c894d989d",
        "FR-008": "sha256:1efd77e47f9d55a3f735dac2b82d9d1534cd786f60fffcd8463bf2a28f8da6c6",
        "FR-009": "sha256:ac1727d2ea6122e201b9f35a77530ece91dba013c30ac656bc80c791a5884aa5",
        "FR-010": "sha256:8aa5f448ddb370a99dcbb5281add4a0106cbb03152c32325dd17c921f07fe781",
        "FR-011": "sha256:0ca8c3df85b82bec17637d1f09bab4668b4bd26b3337664b6990b103bab3b0ec",
        "FR-013": "sha256:38d94ad5c0f0b784877847af344fd77e14f9941ad73bbc98a535b7942b21e73a",
        "FR-014": "sha256:ad118cfdcba914b6dcced02aeaa12e219170b3d9b9b64e1cb3ae800f2cf133cd",
        "FR-015": "sha256:f1d6d8705d95ac71564ee91d3882b78a9adc9ded77660d8d1531a57c74db3bb0",
        "FR-016": "sha256:ea3570068dfeaaa7dda913bd48c48be6dd4a84a8b69fe0e06859657edfaeb67d",
        "FR-017": "sha256:1dd105d6d7f7eac38abd4ce9c97be3e06a173c742a3cb34e6d0bcf1e15376376",
        "NFR-001": "sha256:df17800aee3588d157d4116760d6c0ac8b1aaaf338acd002ab064f7c755650e9",
        "REQ-001": "sha256:256ed10c2afe9e022501c4f25204361be56ca8ebe3e3b4e74b6738c84ce8c568",
        "REQ-003": "sha256:aedb4376fbb5fa1aa745d236c36bf0e638196fe7604260ebfc5adba12d358b9e",
        "REQ-004": "sha256:b52a4907c94a13f2f9fa348ca1da6350f4504b1786482733a63bf8784b4b091f",
        "REQ-005": "sha256:05e5b7ff7f62222173552749b93cd16789de08c57b13afb8171919152c976b57",
        "REQ-006": "sha256:e517cbec32193438afe0b76b99eb5cc9d95f0fce65987fc63aa5d8ee7f783a47",
        "REQ-007": "sha256:bb73c59fe2c6e1a8dc4e62a7718608d9cc9c9b2c1ca3dc4e1b8d91b8ace51041",
        "REQ-008": "sha256:f70bd5a6e36b3acdc1e0ef4100073132fb4a46ffcc099383dc4bc14f247254fe",
        "REQ-009": "sha256:726e06a357ca16e93d7ddde707c7d9b1a7a0d583ae14dfc677a33b7b0efa370c",
        "REQ-011": "sha256:ef32b333ad49ed6d560a3000ff6018a61fc3b9c3c62c7ff1d361ca6da28ef3b6",
        "REQ-012": "sha256:41c59c37940929ef97e7946344ce85005618b1123b73e752b8750066f6ee568d",
        "UC-001": "sha256:39bc034f14596d29449003ea963e3a0b3f51215ee9e15e11c5fef4ae2aaed9ab",
        "UC-002": "sha256:98a48e376358abb62b44feb49ed89036461de691abb57208c9127ef4e0918d00"
      },
      "blocked_at_completion": false
    },
    "T004": {
      "hash": "sha256:9fcb793e920311ecba93c00e94ce3f457e4923abf11860b28cddef8d0ea9169a",
      "class": "restated",
      "cites": {
        "AIS-041": "sha256:950b583b5ce9974d7997eb650727f9c9e6b030de2e4db703f07b7f4bed46a3fc",
        "AIS-031": "sha256:6591d4b6a388c08e9447c97cae6a6479374087c10fa73ff0b34c853c9f53bbcc",
        "AIS-032": "sha256:42f55118f599932cdb6870ba5de41307bf89222be427097fa315daa98882e0da",
        "AIS-015": "sha256:04a4bcfcfbe3b003ff1f953449e83f69bb14f8d5255add3bd21134a93d020b09",
        "ART-008": "sha256:f6fef5898a572d62890e617df6b3c58cd89f75af3a3f1c891255b59bd498b730"
      },
      "completed_against": {
        "AIS-015": "sha256:04a4bcfcfbe3b003ff1f953449e83f69bb14f8d5255add3bd21134a93d020b09",
        "AIS-031": "sha256:6591d4b6a388c08e9447c97cae6a6479374087c10fa73ff0b34c853c9f53bbcc",
        "AIS-032": "sha256:42f55118f599932cdb6870ba5de41307bf89222be427097fa315daa98882e0da",
        "AIS-041": "sha256:950b583b5ce9974d7997eb650727f9c9e6b030de2e4db703f07b7f4bed46a3fc",
        "ART-008": "sha256:f6fef5898a572d62890e617df6b3c58cd89f75af3a3f1c891255b59bd498b730",
        "DEC-001": "sha256:bb921b2401109f1ece0e7a13243eaba9121b572231d2c6402f21a46830d083aa",
        "DEC-002": "sha256:e5e293b732dc3070124d2538a452ac15b148fb9937d58da144d4ee8d004b2032",
        "DEC-004": "sha256:7b10b4a428165cd28fee8fa2619828a86dc5bbf81c06f10415da597c69d300d7",
        "DEC-005": "sha256:141ce780db6dcb541ca4b1c2e4792550978c143cbd5eea57838c9736579db7be",
        "FR-001": "sha256:9b8829cba27184e4e9004fc0ba4af995bb30d52c81be952f804b2817d4ed7a36",
        "FR-006": "sha256:3e514e8dfd04bc478e405c56c902c4d400ee8620a0edc9f5da1d311dea49978d",
        "FR-007": "sha256:7bcffe16420753854d6ef411e7c3099f58fe40bf91b17e707680884c894d989d",
        "FR-008": "sha256:1efd77e47f9d55a3f735dac2b82d9d1534cd786f60fffcd8463bf2a28f8da6c6",
        "FR-009": "sha256:ac1727d2ea6122e201b9f35a77530ece91dba013c30ac656bc80c791a5884aa5",
        "FR-010": "sha256:8aa5f448ddb370a99dcbb5281add4a0106cbb03152c32325dd17c921f07fe781",
        "FR-011": "sha256:0ca8c3df85b82bec17637d1f09bab4668b4bd26b3337664b6990b103bab3b0ec",
        "FR-013": "sha256:38d94ad5c0f0b784877847af344fd77e14f9941ad73bbc98a535b7942b21e73a",
        "FR-014": "sha256:ad118cfdcba914b6dcced02aeaa12e219170b3d9b9b64e1cb3ae800f2cf133cd",
        "FR-015": "sha256:f1d6d8705d95ac71564ee91d3882b78a9adc9ded77660d8d1531a57c74db3bb0",
        "FR-016": "sha256:ea3570068dfeaaa7dda913bd48c48be6dd4a84a8b69fe0e06859657edfaeb67d",
        "FR-017": "sha256:1dd105d6d7f7eac38abd4ce9c97be3e06a173c742a3cb34e6d0bcf1e15376376",
        "NFR-001": "sha256:df17800aee3588d157d4116760d6c0ac8b1aaaf338acd002ab064f7c755650e9",
        "REQ-001": "sha256:256ed10c2afe9e022501c4f25204361be56ca8ebe3e3b4e74b6738c84ce8c568",
        "REQ-003": "sha256:aedb4376fbb5fa1aa745d236c36bf0e638196fe7604260ebfc5adba12d358b9e",
        "REQ-004": "sha256:b52a4907c94a13f2f9fa348ca1da6350f4504b1786482733a63bf8784b4b091f",
        "REQ-005": "sha256:05e5b7ff7f62222173552749b93cd16789de08c57b13afb8171919152c976b57",
        "REQ-006": "sha256:e517cbec32193438afe0b76b99eb5cc9d95f0fce65987fc63aa5d8ee7f783a47",
        "REQ-007": "sha256:bb73c59fe2c6e1a8dc4e62a7718608d9cc9c9b2c1ca3dc4e1b8d91b8ace51041",
        "REQ-008": "sha256:f70bd5a6e36b3acdc1e0ef4100073132fb4a46ffcc099383dc4bc14f247254fe",
        "REQ-009": "sha256:726e06a357ca16e93d7ddde707c7d9b1a7a0d583ae14dfc677a33b7b0efa370c",
        "REQ-011": "sha256:ef32b333ad49ed6d560a3000ff6018a61fc3b9c3c62c7ff1d361ca6da28ef3b6",
        "UC-001": "sha256:39bc034f14596d29449003ea963e3a0b3f51215ee9e15e11c5fef4ae2aaed9ab",
        "UC-002": "sha256:98a48e376358abb62b44feb49ed89036461de691abb57208c9127ef4e0918d00"
      },
      "blocked_at_completion": false
    },
    "T005": {
      "hash": "sha256:f9e6361741c593e0b85cc8f7a7b6135e3a5f6bddeb8cef80ba9b3d08a1043b58",
      "class": "restated",
      "cites": {
        "AIS-023": "sha256:6644b93f8f8e69eb7e83d12643e22e6e83e44cefa9cb5a084ea219723345591c",
        "AIS-033": "sha256:4d0d690106232bcac25a8dc35253845b7d23ae80f1a5bd59f3f1d0de01a8f365",
        "AIS-037": "sha256:a31c9ae82c6ba4d575326b3d37805d76fc703a2edd8ea312feddd78e6b20f5c3",
        "AIS-059": "sha256:980c28303da1bead8671df27d5a416e946d3bc28609c246558b51026f89adba6",
        "ART-008": "sha256:f6fef5898a572d62890e617df6b3c58cd89f75af3a3f1c891255b59bd498b730"
      },
      "completed_against": {
        "AIS-023": "sha256:6644b93f8f8e69eb7e83d12643e22e6e83e44cefa9cb5a084ea219723345591c",
        "AIS-033": "sha256:4d0d690106232bcac25a8dc35253845b7d23ae80f1a5bd59f3f1d0de01a8f365",
        "AIS-037": "sha256:a31c9ae82c6ba4d575326b3d37805d76fc703a2edd8ea312feddd78e6b20f5c3",
        "AIS-059": "sha256:980c28303da1bead8671df27d5a416e946d3bc28609c246558b51026f89adba6",
        "ART-008": "sha256:f6fef5898a572d62890e617df6b3c58cd89f75af3a3f1c891255b59bd498b730",
        "DEC-001": "sha256:bb921b2401109f1ece0e7a13243eaba9121b572231d2c6402f21a46830d083aa",
        "DEC-002": "sha256:e5e293b732dc3070124d2538a452ac15b148fb9937d58da144d4ee8d004b2032",
        "DEC-005": "sha256:141ce780db6dcb541ca4b1c2e4792550978c143cbd5eea57838c9736579db7be",
        "FR-001": "sha256:9b8829cba27184e4e9004fc0ba4af995bb30d52c81be952f804b2817d4ed7a36",
        "FR-006": "sha256:3e514e8dfd04bc478e405c56c902c4d400ee8620a0edc9f5da1d311dea49978d",
        "FR-010": "sha256:8aa5f448ddb370a99dcbb5281add4a0106cbb03152c32325dd17c921f07fe781",
        "FR-011": "sha256:0ca8c3df85b82bec17637d1f09bab4668b4bd26b3337664b6990b103bab3b0ec",
        "FR-013": "sha256:38d94ad5c0f0b784877847af344fd77e14f9941ad73bbc98a535b7942b21e73a",
        "FR-014": "sha256:ad118cfdcba914b6dcced02aeaa12e219170b3d9b9b64e1cb3ae800f2cf133cd",
        "FR-015": "sha256:f1d6d8705d95ac71564ee91d3882b78a9adc9ded77660d8d1531a57c74db3bb0",
        "FR-016": "sha256:ea3570068dfeaaa7dda913bd48c48be6dd4a84a8b69fe0e06859657edfaeb67d",
        "FR-017": "sha256:1dd105d6d7f7eac38abd4ce9c97be3e06a173c742a3cb34e6d0bcf1e15376376",
        "REQ-001": "sha256:256ed10c2afe9e022501c4f25204361be56ca8ebe3e3b4e74b6738c84ce8c568",
        "REQ-004": "sha256:b52a4907c94a13f2f9fa348ca1da6350f4504b1786482733a63bf8784b4b091f",
        "REQ-005": "sha256:05e5b7ff7f62222173552749b93cd16789de08c57b13afb8171919152c976b57",
        "REQ-006": "sha256:e517cbec32193438afe0b76b99eb5cc9d95f0fce65987fc63aa5d8ee7f783a47",
        "REQ-007": "sha256:bb73c59fe2c6e1a8dc4e62a7718608d9cc9c9b2c1ca3dc4e1b8d91b8ace51041",
        "REQ-008": "sha256:f70bd5a6e36b3acdc1e0ef4100073132fb4a46ffcc099383dc4bc14f247254fe",
        "REQ-009": "sha256:726e06a357ca16e93d7ddde707c7d9b1a7a0d583ae14dfc677a33b7b0efa370c",
        "REQ-011": "sha256:ef32b333ad49ed6d560a3000ff6018a61fc3b9c3c62c7ff1d361ca6da28ef3b6",
        "UC-001": "sha256:39bc034f14596d29449003ea963e3a0b3f51215ee9e15e11c5fef4ae2aaed9ab",
        "UC-002": "sha256:98a48e376358abb62b44feb49ed89036461de691abb57208c9127ef4e0918d00"
      },
      "blocked_at_completion": false
    },
    "T006": {
      "hash": "sha256:96b0e7d80cc5498cf70cae027f27c41f462605b3d81b328da1781365963b606a",
      "class": "restated",
      "cites": {
        "AIS-039": "sha256:ad883fe95ed533f35a62281366d369cc0dc5c866a542dc3ca2d00247901050be",
        "AIS-028": "sha256:f23788fe05415553188b54763ee5135117d61b2507b290f16d7efb9f0b7530c6",
        "AIS-064": "sha256:3cdad1b135aa83d533900483967d0038eb5757e96280afad24c7c1ce2dc0953c"
      },
      "completed_against": {
        "AIS-028": "sha256:f23788fe05415553188b54763ee5135117d61b2507b290f16d7efb9f0b7530c6",
        "AIS-039": "sha256:ad883fe95ed533f35a62281366d369cc0dc5c866a542dc3ca2d00247901050be",
        "AIS-064": "sha256:3cdad1b135aa83d533900483967d0038eb5757e96280afad24c7c1ce2dc0953c",
        "DEC-006": "sha256:39b03e67818d400e49ee296e2e3c28ac91daeaa69b23d14ab9a0ae88a080b5de",
        "FR-002": "sha256:32dc804048b7e426e532d1b98c0fc50d4ebdb1ebea550a3caa6e72002e6f2e6f",
        "FR-010": "sha256:8aa5f448ddb370a99dcbb5281add4a0106cbb03152c32325dd17c921f07fe781",
        "FR-011": "sha256:0ca8c3df85b82bec17637d1f09bab4668b4bd26b3337664b6990b103bab3b0ec",
        "NFR-002": "sha256:b6d43217718ec3585d21c7e35c03545369d59141a6cd7f07acb47100eef1826b",
        "REQ-001": "sha256:256ed10c2afe9e022501c4f25204361be56ca8ebe3e3b4e74b6738c84ce8c568",
        "REQ-004": "sha256:b52a4907c94a13f2f9fa348ca1da6350f4504b1786482733a63bf8784b4b091f",
        "REQ-005": "sha256:05e5b7ff7f62222173552749b93cd16789de08c57b13afb8171919152c976b57",
        "REQ-011": "sha256:ef32b333ad49ed6d560a3000ff6018a61fc3b9c3c62c7ff1d361ca6da28ef3b6",
        "UC-001": "sha256:39bc034f14596d29449003ea963e3a0b3f51215ee9e15e11c5fef4ae2aaed9ab",
        "UC-002": "sha256:98a48e376358abb62b44feb49ed89036461de691abb57208c9127ef4e0918d00"
      },
      "blocked_at_completion": false
    },
    "Phase 2: Foundational (Blocking Prerequisites)#93cca68b24f6": {
      "hash": "sha256:93cca68b24f6c5203993e3ae6e86a35c53be45183c7afd0c7321acb77ec28319",
      "class": "inferred",
      "adds": "Adds the grouping, goal, test criteria or ordering that organises the tasks, which the AI Specification does not state.",
      "reviewed": {
        "by": "Lee Sinclair",
        "at": "2026-10-01T13:36:24Z",
        "list": "RVW-009",
        "reply": "Ok"
      }
    },
    "Phase 3: User Story 1 - Read a story from start to finish (Priority: P1) 🎯 MVP#2ef46a5aea8b": {
      "hash": "sha256:2ef46a5aea8b59df8052eca1fee9a67ac03a6364135da1011de8a42f4a20cba3",
      "class": "inferred",
      "adds": "Adds the grouping, goal, test criteria or ordering that organises the tasks, which the AI Specification does not state.",
      "reviewed": {
        "by": "Lee Sinclair",
        "at": "2026-10-01T13:36:24Z",
        "list": "RVW-009",
        "reply": "Ok"
      }
    },
    "Phase 3: User Story 1 - Read a story from start to finish (Priority: P1) 🎯 MVP#18ec2909f385": {
      "hash": "sha256:18ec2909f38542bd2793f1fb00bf71a870afdc07d1d4c8790789877b10a94c62",
      "class": "inferred",
      "adds": "Adds the grouping, goal, test criteria or ordering that organises the tasks, which the AI Specification does not state.",
      "reviewed": {
        "by": "Lee Sinclair",
        "at": "2026-10-01T13:36:24Z",
        "list": "RVW-009",
        "reply": "Ok"
      }
    },
    "T007": {
      "hash": "sha256:b20aa9e1ded57407af0f1e38cda732b8e0aa70c7fe1cd6d689d56d7749b1e211",
      "class": "restated",
      "cites": {
        "AIS-043": "sha256:ecbd7b859a28e78c8fb5102a68f8a73ac13df9e8c1862fda89e5240b590b68f0",
        "AIS-019": "sha256:a997103070992e4c060534caba5663d24445fe04793930c80f13b655fe2ba3d7",
        "AIS-007": "sha256:852b862cde2ffbc3856bf05a919a51e86888254ded48dd7e8b37ddd3058e9f8f",
        "AIS-063": "sha256:9f81319bfeb664e3fd3502379d744995dd2ed0514c9d81352c8a6aa5aa66297d"
      },
      "completed_against": {
        "AIS-007": "sha256:852b862cde2ffbc3856bf05a919a51e86888254ded48dd7e8b37ddd3058e9f8f",
        "AIS-019": "sha256:a997103070992e4c060534caba5663d24445fe04793930c80f13b655fe2ba3d7",
        "AIS-043": "sha256:ecbd7b859a28e78c8fb5102a68f8a73ac13df9e8c1862fda89e5240b590b68f0",
        "AIS-063": "sha256:9f81319bfeb664e3fd3502379d744995dd2ed0514c9d81352c8a6aa5aa66297d",
        "DEC-004": "sha256:7b10b4a428165cd28fee8fa2619828a86dc5bbf81c06f10415da597c69d300d7",
        "DEC-007": "sha256:c092606ae0d1acdb955329fb0999903f6b0219c952e9d0bbaa51fa3ef1b8ce76",
        "FR-004": "sha256:9351afecec6d138f345d4b8a50128f10215e41705620c6441d15ebeb92e564a8",
        "FR-005": "sha256:65cffe4e76d287540239f49d99854034164b552e04e3a5f968efbc820d0fc590",
        "FR-006": "sha256:3e514e8dfd04bc478e405c56c902c4d400ee8620a0edc9f5da1d311dea49978d",
        "FR-007": "sha256:7bcffe16420753854d6ef411e7c3099f58fe40bf91b17e707680884c894d989d",
        "FR-008": "sha256:1efd77e47f9d55a3f735dac2b82d9d1534cd786f60fffcd8463bf2a28f8da6c6",
        "FR-009": "sha256:ac1727d2ea6122e201b9f35a77530ece91dba013c30ac656bc80c791a5884aa5",
        "FR-016": "sha256:ea3570068dfeaaa7dda913bd48c48be6dd4a84a8b69fe0e06859657edfaeb67d",
        "NFR-001": "sha256:df17800aee3588d157d4116760d6c0ac8b1aaaf338acd002ab064f7c755650e9",
        "NFR-002": "sha256:b6d43217718ec3585d21c7e35c03545369d59141a6cd7f07acb47100eef1826b",
        "NFR-003": "sha256:38473b65fca10e09faa1982b8eee81daace9150eebf3baefbaa5e7209036eabf",
        "REQ-003": "sha256:aedb4376fbb5fa1aa745d236c36bf0e638196fe7604260ebfc5adba12d358b9e",
        "REQ-005": "sha256:05e5b7ff7f62222173552749b93cd16789de08c57b13afb8171919152c976b57",
        "REQ-009": "sha256:726e06a357ca16e93d7ddde707c7d9b1a7a0d583ae14dfc677a33b7b0efa370c",
        "REQ-010": "sha256:aeba84bc66554b71b5aa5286cde9cbe4906cc3b0b502f744baa1561c4f22890a",
        "REQ-011": "sha256:ef32b333ad49ed6d560a3000ff6018a61fc3b9c3c62c7ff1d361ca6da28ef3b6",
        "REQ-012": "sha256:41c59c37940929ef97e7946344ce85005618b1123b73e752b8750066f6ee568d",
        "UC-002": "sha256:98a48e376358abb62b44feb49ed89036461de691abb57208c9127ef4e0918d00"
      },
      "blocked_at_completion": false
    },
    "T008": {
      "hash": "sha256:bbc8612c1b66cbe467cf80a16e89863c00898f3fef2edc9c2992e314e9017930",
      "class": "restated",
      "cites": {
        "AIS-044": "sha256:50a4a6ae4576b654b7ac1578481d148899518955f15500b3d709f8c107cbd983",
        "AIS-040": "sha256:593a84b3698508d760d5c5a181b96836d01b867fc566cb39f88f0edd9922ea95",
        "AIS-002": "sha256:35ecb780bd8181dbfa7fc004c93f08cf48306642484514ae5cb8c443562d9beb",
        "AIS-010": "sha256:9f67f5f2fa3c62011554348671067d4429d372c85c25c1c2fb4a5f75e9f1c69f",
        "AIS-011": "sha256:c61dfa8f0d5ecf2716ab632ff7adf1e72c1a6949ea7f3a929fd37d8471306e6a",
        "AIS-073": "sha256:339a23541e50e8ae1a51f34e0731075e73ce78d34235127ca88ec96786c9ca58"
      },
      "completed_against": {
        "AIS-002": "sha256:35ecb780bd8181dbfa7fc004c93f08cf48306642484514ae5cb8c443562d9beb",
        "AIS-010": "sha256:9f67f5f2fa3c62011554348671067d4429d372c85c25c1c2fb4a5f75e9f1c69f",
        "AIS-011": "sha256:c61dfa8f0d5ecf2716ab632ff7adf1e72c1a6949ea7f3a929fd37d8471306e6a",
        "AIS-040": "sha256:593a84b3698508d760d5c5a181b96836d01b867fc566cb39f88f0edd9922ea95",
        "AIS-044": "sha256:50a4a6ae4576b654b7ac1578481d148899518955f15500b3d709f8c107cbd983",
        "AIS-073": "sha256:339a23541e50e8ae1a51f34e0731075e73ce78d34235127ca88ec96786c9ca58",
        "DEC-006": "sha256:39b03e67818d400e49ee296e2e3c28ac91daeaa69b23d14ab9a0ae88a080b5de",
        "DEC-007": "sha256:c092606ae0d1acdb955329fb0999903f6b0219c952e9d0bbaa51fa3ef1b8ce76",
        "FR-001": "sha256:9b8829cba27184e4e9004fc0ba4af995bb30d52c81be952f804b2817d4ed7a36",
        "FR-002": "sha256:32dc804048b7e426e532d1b98c0fc50d4ebdb1ebea550a3caa6e72002e6f2e6f",
        "FR-010": "sha256:8aa5f448ddb370a99dcbb5281add4a0106cbb03152c32325dd17c921f07fe781",
        "FR-011": "sha256:0ca8c3df85b82bec17637d1f09bab4668b4bd26b3337664b6990b103bab3b0ec",
        "FR-012": "sha256:c398b73a4cbf412ded409ed8f094ae59ed47616c7a4bca37420906c7d2f7291c",
        "FR-013": "sha256:38d94ad5c0f0b784877847af344fd77e14f9941ad73bbc98a535b7942b21e73a",
        "FR-014": "sha256:ad118cfdcba914b6dcced02aeaa12e219170b3d9b9b64e1cb3ae800f2cf133cd",
        "FR-015": "sha256:f1d6d8705d95ac71564ee91d3882b78a9adc9ded77660d8d1531a57c74db3bb0",
        "FR-016": "sha256:ea3570068dfeaaa7dda913bd48c48be6dd4a84a8b69fe0e06859657edfaeb67d",
        "FR-017": "sha256:1dd105d6d7f7eac38abd4ce9c97be3e06a173c742a3cb34e6d0bcf1e15376376",
        "NFR-002": "sha256:b6d43217718ec3585d21c7e35c03545369d59141a6cd7f07acb47100eef1826b",
        "NFR-003": "sha256:38473b65fca10e09faa1982b8eee81daace9150eebf3baefbaa5e7209036eabf",
        "REQ-001": "sha256:256ed10c2afe9e022501c4f25204361be56ca8ebe3e3b4e74b6738c84ce8c568",
        "REQ-004": "sha256:b52a4907c94a13f2f9fa348ca1da6350f4504b1786482733a63bf8784b4b091f",
        "REQ-005": "sha256:05e5b7ff7f62222173552749b93cd16789de08c57b13afb8171919152c976b57",
        "REQ-006": "sha256:e517cbec32193438afe0b76b99eb5cc9d95f0fce65987fc63aa5d8ee7f783a47",
        "REQ-007": "sha256:bb73c59fe2c6e1a8dc4e62a7718608d9cc9c9b2c1ca3dc4e1b8d91b8ace51041",
        "REQ-008": "sha256:f70bd5a6e36b3acdc1e0ef4100073132fb4a46ffcc099383dc4bc14f247254fe",
        "REQ-009": "sha256:726e06a357ca16e93d7ddde707c7d9b1a7a0d583ae14dfc677a33b7b0efa370c",
        "REQ-010": "sha256:aeba84bc66554b71b5aa5286cde9cbe4906cc3b0b502f744baa1561c4f22890a",
        "REQ-011": "sha256:ef32b333ad49ed6d560a3000ff6018a61fc3b9c3c62c7ff1d361ca6da28ef3b6",
        "UC-001": "sha256:39bc034f14596d29449003ea963e3a0b3f51215ee9e15e11c5fef4ae2aaed9ab",
        "UC-002": "sha256:98a48e376358abb62b44feb49ed89036461de691abb57208c9127ef4e0918d00",
        "UC-003": "sha256:e47e99898085ee543414e29d1821cf2de70b134f24d206a2cd379c24a9e577c6"
      },
      "blocked_at_completion": false
    },
    "T009": {
      "hash": "sha256:7e538a4d617d207e20b5a0692c672d8e5c2e055c605a324ada62e8d96751f9c3",
      "class": "restated",
      "cites": {
        "AIS-003": "sha256:61c489ff9eeee1832f21b88e834333b1c3e6ad34b12d9dff3aac3399c0f4b36e",
        "AIS-004": "sha256:e065331d34cf6e63b623a6c46d64e211944d9457578a6f4fe2b3005f65baab08",
        "AIS-005": "sha256:7b3efe32a84407449feb6f0e6e2b14b6872e5a1bcefcaac8963c2aa6217bf1b4",
        "AIS-036": "sha256:a550507c3cd8f3326ff97eeb9c0622d5da8ba74ee1dfb197ddd296e56da8e1e5",
        "AIS-049": "sha256:5f71e91094328301a8d34c12620a403975b866de38b82b0d469c277af597a0d8"
      },
      "completed_against": {
        "AIS-003": "sha256:61c489ff9eeee1832f21b88e834333b1c3e6ad34b12d9dff3aac3399c0f4b36e",
        "AIS-004": "sha256:e065331d34cf6e63b623a6c46d64e211944d9457578a6f4fe2b3005f65baab08",
        "AIS-005": "sha256:7b3efe32a84407449feb6f0e6e2b14b6872e5a1bcefcaac8963c2aa6217bf1b4",
        "AIS-036": "sha256:a550507c3cd8f3326ff97eeb9c0622d5da8ba74ee1dfb197ddd296e56da8e1e5",
        "AIS-049": "sha256:5f71e91094328301a8d34c12620a403975b866de38b82b0d469c277af597a0d8",
        "DEC-006": "sha256:39b03e67818d400e49ee296e2e3c28ac91daeaa69b23d14ab9a0ae88a080b5de",
        "FR-002": "sha256:32dc804048b7e426e532d1b98c0fc50d4ebdb1ebea550a3caa6e72002e6f2e6f",
        "FR-003": "sha256:197f0e7bf32d3fffc1d86caf9e93b21576f2146c4b96744d98b9195835da670b",
        "FR-004": "sha256:9351afecec6d138f345d4b8a50128f10215e41705620c6441d15ebeb92e564a8",
        "FR-005": "sha256:65cffe4e76d287540239f49d99854034164b552e04e3a5f968efbc820d0fc590",
        "FR-010": "sha256:8aa5f448ddb370a99dcbb5281add4a0106cbb03152c32325dd17c921f07fe781",
        "FR-011": "sha256:0ca8c3df85b82bec17637d1f09bab4668b4bd26b3337664b6990b103bab3b0ec",
        "FR-014": "sha256:ad118cfdcba914b6dcced02aeaa12e219170b3d9b9b64e1cb3ae800f2cf133cd",
        "NFR-002": "sha256:b6d43217718ec3585d21c7e35c03545369d59141a6cd7f07acb47100eef1826b",
        "REQ-001": "sha256:256ed10c2afe9e022501c4f25204361be56ca8ebe3e3b4e74b6738c84ce8c568",
        "REQ-002": "sha256:7b9a9aeadce291263cd1c8f6106926ef0868c72ad872a99beac7bbbb688fb049",
        "REQ-004": "sha256:b52a4907c94a13f2f9fa348ca1da6350f4504b1786482733a63bf8784b4b091f",
        "REQ-005": "sha256:05e5b7ff7f62222173552749b93cd16789de08c57b13afb8171919152c976b57",
        "REQ-007": "sha256:bb73c59fe2c6e1a8dc4e62a7718608d9cc9c9b2c1ca3dc4e1b8d91b8ace51041",
        "REQ-011": "sha256:ef32b333ad49ed6d560a3000ff6018a61fc3b9c3c62c7ff1d361ca6da28ef3b6",
        "REQ-012": "sha256:41c59c37940929ef97e7946344ce85005618b1123b73e752b8750066f6ee568d",
        "UC-001": "sha256:39bc034f14596d29449003ea963e3a0b3f51215ee9e15e11c5fef4ae2aaed9ab",
        "UC-002": "sha256:98a48e376358abb62b44feb49ed89036461de691abb57208c9127ef4e0918d00"
      },
      "blocked_at_completion": false
    },
    "T010": {
      "hash": "sha256:f2ae2acfc4756a3594e761bd52f95df4a5259e806824c0f0f7c6ccf293014f78",
      "class": "restated",
      "cites": {
        "AIS-028": "sha256:f23788fe05415553188b54763ee5135117d61b2507b290f16d7efb9f0b7530c6",
        "AIS-001": "sha256:d157fbcce84c54aa24e00f7ae8e8ae0cdbb649c7b07153e755835040d5e200bf",
        "AIS-002": "sha256:35ecb780bd8181dbfa7fc004c93f08cf48306642484514ae5cb8c443562d9beb",
        "AIS-010": "sha256:9f67f5f2fa3c62011554348671067d4429d372c85c25c1c2fb4a5f75e9f1c69f",
        "AIS-011": "sha256:c61dfa8f0d5ecf2716ab632ff7adf1e72c1a6949ea7f3a929fd37d8471306e6a",
        "AIS-027": "sha256:a9f6fde904cd4b9b50af42f8df0504ff65dee864f66e6603a578d45e5c5f124b"
      },
      "completed_against": {
        "AIS-001": "sha256:d157fbcce84c54aa24e00f7ae8e8ae0cdbb649c7b07153e755835040d5e200bf",
        "AIS-002": "sha256:35ecb780bd8181dbfa7fc004c93f08cf48306642484514ae5cb8c443562d9beb",
        "AIS-010": "sha256:9f67f5f2fa3c62011554348671067d4429d372c85c25c1c2fb4a5f75e9f1c69f",
        "AIS-011": "sha256:c61dfa8f0d5ecf2716ab632ff7adf1e72c1a6949ea7f3a929fd37d8471306e6a",
        "AIS-027": "sha256:a9f6fde904cd4b9b50af42f8df0504ff65dee864f66e6603a578d45e5c5f124b",
        "AIS-028": "sha256:f23788fe05415553188b54763ee5135117d61b2507b290f16d7efb9f0b7530c6",
        "DEC-005": "sha256:141ce780db6dcb541ca4b1c2e4792550978c143cbd5eea57838c9736579db7be",
        "DEC-006": "sha256:39b03e67818d400e49ee296e2e3c28ac91daeaa69b23d14ab9a0ae88a080b5de",
        "FR-001": "sha256:9b8829cba27184e4e9004fc0ba4af995bb30d52c81be952f804b2817d4ed7a36",
        "FR-002": "sha256:32dc804048b7e426e532d1b98c0fc50d4ebdb1ebea550a3caa6e72002e6f2e6f",
        "FR-010": "sha256:8aa5f448ddb370a99dcbb5281add4a0106cbb03152c32325dd17c921f07fe781",
        "FR-011": "sha256:0ca8c3df85b82bec17637d1f09bab4668b4bd26b3337664b6990b103bab3b0ec",
        "FR-013": "sha256:38d94ad5c0f0b784877847af344fd77e14f9941ad73bbc98a535b7942b21e73a",
        "NFR-002": "sha256:b6d43217718ec3585d21c7e35c03545369d59141a6cd7f07acb47100eef1826b",
        "REQ-001": "sha256:256ed10c2afe9e022501c4f25204361be56ca8ebe3e3b4e74b6738c84ce8c568",
        "REQ-004": "sha256:b52a4907c94a13f2f9fa348ca1da6350f4504b1786482733a63bf8784b4b091f",
        "REQ-005": "sha256:05e5b7ff7f62222173552749b93cd16789de08c57b13afb8171919152c976b57",
        "REQ-006": "sha256:e517cbec32193438afe0b76b99eb5cc9d95f0fce65987fc63aa5d8ee7f783a47",
        "REQ-011": "sha256:ef32b333ad49ed6d560a3000ff6018a61fc3b9c3c62c7ff1d361ca6da28ef3b6",
        "UC-001": "sha256:39bc034f14596d29449003ea963e3a0b3f51215ee9e15e11c5fef4ae2aaed9ab",
        "UC-002": "sha256:98a48e376358abb62b44feb49ed89036461de691abb57208c9127ef4e0918d00"
      },
      "blocked_at_completion": false
    },
    "T011": {
      "hash": "sha256:514e96d512316d8835751e3eb9c5e78d220b461ab5f0928a3e966f1c0e591214",
      "class": "restated",
      "cites": {
        "AIS-007": "sha256:852b862cde2ffbc3856bf05a919a51e86888254ded48dd7e8b37ddd3058e9f8f",
        "AIS-026": "sha256:fb41e3346fa2320682eaa6c062601114552d60ebb273a6e385bebbfced0034ec",
        "AIS-027": "sha256:a9f6fde904cd4b9b50af42f8df0504ff65dee864f66e6603a578d45e5c5f124b",
        "DEC-005": "sha256:141ce780db6dcb541ca4b1c2e4792550978c143cbd5eea57838c9736579db7be"
      },
      "completed_against": {
        "AIS-007": "sha256:852b862cde2ffbc3856bf05a919a51e86888254ded48dd7e8b37ddd3058e9f8f",
        "AIS-026": "sha256:fb41e3346fa2320682eaa6c062601114552d60ebb273a6e385bebbfced0034ec",
        "AIS-027": "sha256:a9f6fde904cd4b9b50af42f8df0504ff65dee864f66e6603a578d45e5c5f124b",
        "DEC-004": "sha256:7b10b4a428165cd28fee8fa2619828a86dc5bbf81c06f10415da597c69d300d7",
        "DEC-005": "sha256:141ce780db6dcb541ca4b1c2e4792550978c143cbd5eea57838c9736579db7be",
        "FR-007": "sha256:7bcffe16420753854d6ef411e7c3099f58fe40bf91b17e707680884c894d989d",
        "FR-008": "sha256:1efd77e47f9d55a3f735dac2b82d9d1534cd786f60fffcd8463bf2a28f8da6c6",
        "FR-009": "sha256:ac1727d2ea6122e201b9f35a77530ece91dba013c30ac656bc80c791a5884aa5",
        "FR-010": "sha256:8aa5f448ddb370a99dcbb5281add4a0106cbb03152c32325dd17c921f07fe781",
        "FR-011": "sha256:0ca8c3df85b82bec17637d1f09bab4668b4bd26b3337664b6990b103bab3b0ec",
        "FR-013": "sha256:38d94ad5c0f0b784877847af344fd77e14f9941ad73bbc98a535b7942b21e73a",
        "NFR-001": "sha256:df17800aee3588d157d4116760d6c0ac8b1aaaf338acd002ab064f7c755650e9",
        "REQ-001": "sha256:256ed10c2afe9e022501c4f25204361be56ca8ebe3e3b4e74b6738c84ce8c568",
        "REQ-003": "sha256:aedb4376fbb5fa1aa745d236c36bf0e638196fe7604260ebfc5adba12d358b9e",
        "REQ-004": "sha256:b52a4907c94a13f2f9fa348ca1da6350f4504b1786482733a63bf8784b4b091f",
        "REQ-005": "sha256:05e5b7ff7f62222173552749b93cd16789de08c57b13afb8171919152c976b57",
        "REQ-006": "sha256:e517cbec32193438afe0b76b99eb5cc9d95f0fce65987fc63aa5d8ee7f783a47",
        "REQ-011": "sha256:ef32b333ad49ed6d560a3000ff6018a61fc3b9c3c62c7ff1d361ca6da28ef3b6",
        "UC-001": "sha256:39bc034f14596d29449003ea963e3a0b3f51215ee9e15e11c5fef4ae2aaed9ab",
        "UC-002": "sha256:98a48e376358abb62b44feb49ed89036461de691abb57208c9127ef4e0918d00"
      },
      "blocked_at_completion": false
    },
    "T012": {
      "hash": "sha256:d92f1eda26fc9db16fa58ca32ba8d3927809ff5c8a26d302f0c90cffc5abbcb8",
      "class": "restated",
      "cites": {
        "AIS-052": "sha256:76fca578e34b38ea8bc39a80729fcc493c169028c447bbeaaf0d590f3184a0a3",
        "AIS-010": "sha256:9f67f5f2fa3c62011554348671067d4429d372c85c25c1c2fb4a5f75e9f1c69f"
      },
      "completed_against": {
        "AIS-010": "sha256:9f67f5f2fa3c62011554348671067d4429d372c85c25c1c2fb4a5f75e9f1c69f",
        "AIS-052": "sha256:76fca578e34b38ea8bc39a80729fcc493c169028c447bbeaaf0d590f3184a0a3",
        "FR-010": "sha256:8aa5f448ddb370a99dcbb5281add4a0106cbb03152c32325dd17c921f07fe781",
        "REQ-004": "sha256:b52a4907c94a13f2f9fa348ca1da6350f4504b1786482733a63bf8784b4b091f",
        "REQ-005": "sha256:05e5b7ff7f62222173552749b93cd16789de08c57b13afb8171919152c976b57",
        "REQ-011": "sha256:ef32b333ad49ed6d560a3000ff6018a61fc3b9c3c62c7ff1d361ca6da28ef3b6",
        "UC-001": "sha256:39bc034f14596d29449003ea963e3a0b3f51215ee9e15e11c5fef4ae2aaed9ab"
      },
      "blocked_at_completion": false
    },
    "T013": {
      "hash": "sha256:eeb82632c10f0d5355622007099a5af7ad68de2ba9311945740232e38988bae7",
      "class": "restated",
      "cites": {
        "AIS-045": "sha256:e42a3ac6a992fe9a3a24deead6ecc93c3b1da3e78be7c23ede5257aa6c1ae9ea",
        "AIS-064": "sha256:3cdad1b135aa83d533900483967d0038eb5757e96280afad24c7c1ce2dc0953c"
      },
      "completed_against": {
        "AIS-045": "sha256:e42a3ac6a992fe9a3a24deead6ecc93c3b1da3e78be7c23ede5257aa6c1ae9ea",
        "AIS-064": "sha256:3cdad1b135aa83d533900483967d0038eb5757e96280afad24c7c1ce2dc0953c",
        "DEC-006": "sha256:39b03e67818d400e49ee296e2e3c28ac91daeaa69b23d14ab9a0ae88a080b5de",
        "DEC-007": "sha256:c092606ae0d1acdb955329fb0999903f6b0219c952e9d0bbaa51fa3ef1b8ce76",
        "FR-002": "sha256:32dc804048b7e426e532d1b98c0fc50d4ebdb1ebea550a3caa6e72002e6f2e6f",
        "FR-010": "sha256:8aa5f448ddb370a99dcbb5281add4a0106cbb03152c32325dd17c921f07fe781",
        "FR-011": "sha256:0ca8c3df85b82bec17637d1f09bab4668b4bd26b3337664b6990b103bab3b0ec",
        "FR-016": "sha256:ea3570068dfeaaa7dda913bd48c48be6dd4a84a8b69fe0e06859657edfaeb67d",
        "NFR-002": "sha256:b6d43217718ec3585d21c7e35c03545369d59141a6cd7f07acb47100eef1826b",
        "NFR-003": "sha256:38473b65fca10e09faa1982b8eee81daace9150eebf3baefbaa5e7209036eabf",
        "REQ-001": "sha256:256ed10c2afe9e022501c4f25204361be56ca8ebe3e3b4e74b6738c84ce8c568",
        "REQ-004": "sha256:b52a4907c94a13f2f9fa348ca1da6350f4504b1786482733a63bf8784b4b091f",
        "REQ-005": "sha256:05e5b7ff7f62222173552749b93cd16789de08c57b13afb8171919152c976b57",
        "REQ-009": "sha256:726e06a357ca16e93d7ddde707c7d9b1a7a0d583ae14dfc677a33b7b0efa370c",
        "REQ-010": "sha256:aeba84bc66554b71b5aa5286cde9cbe4906cc3b0b502f744baa1561c4f22890a",
        "REQ-011": "sha256:ef32b333ad49ed6d560a3000ff6018a61fc3b9c3c62c7ff1d361ca6da28ef3b6",
        "UC-001": "sha256:39bc034f14596d29449003ea963e3a0b3f51215ee9e15e11c5fef4ae2aaed9ab",
        "UC-002": "sha256:98a48e376358abb62b44feb49ed89036461de691abb57208c9127ef4e0918d00"
      },
      "blocked_at_completion": false
    },
    "Phase 3: User Story 1 - Read a story from start to finish (Priority: P1) 🎯 MVP#81d3aab60764": {
      "hash": "sha256:81d3aab6076464404e82fb7673828939f35344495aeff4fbdc3c8c016b4d0205",
      "class": "inferred",
      "adds": "Adds the grouping, goal, test criteria or ordering that organises the tasks, which the AI Specification does not state.",
      "reviewed": {
        "by": "Lee Sinclair",
        "at": "2026-10-01T13:36:24Z",
        "list": "RVW-009",
        "reply": "Ok"
      }
    },
    "Phase 4: User Story 2 - Find a nested document (Priority: P2)#1ecc365024fd": {
      "hash": "sha256:1ecc365024fd086f1238d06c0fe7c962d43a46d17ecebffa56d335690537f65f",
      "class": "inferred",
      "adds": "Adds the grouping, goal, test criteria or ordering that organises the tasks, which the AI Specification does not state.",
      "reviewed": {
        "by": "Lee Sinclair",
        "at": "2026-10-01T13:36:24Z",
        "list": "RVW-009",
        "reply": "Ok"
      }
    },
    "Phase 4: User Story 2 - Find a nested document (Priority: P2)#75b1c9d1c2bc": {
      "hash": "sha256:75b1c9d1c2bc68aecb345f7db5950ce4628c2d36558d5ddfda09e8e9eaa5e97c",
      "class": "inferred",
      "adds": "Adds the grouping, goal, test criteria or ordering that organises the tasks, which the AI Specification does not state.",
      "reviewed": {
        "by": "Lee Sinclair",
        "at": "2026-10-01T13:36:24Z",
        "list": "RVW-009",
        "reply": "Ok"
      }
    },
    "T014": {
      "hash": "sha256:bc35fec36186a58970d5507c038c7fa13f254ff6d9ccb909b6b0a30b1d20e7c4",
      "class": "restated",
      "cites": {
        "AIS-043": "sha256:ecbd7b859a28e78c8fb5102a68f8a73ac13df9e8c1862fda89e5240b590b68f0",
        "AIS-008": "sha256:ae0244647a8219ec8f3cd692a80d70c59679bc0502fada26aec39a85c98a61a7",
        "AIS-009": "sha256:ca8faee8ca35286fad97ea40959e30bb078badade6d67c8dccdd9cff915f73f7",
        "AIS-020": "sha256:a4a3c69d47e31fa59042fbcc5d4992379696223e9ccdf5a8de3800aaaacc30ed",
        "AIS-021": "sha256:635c20f5f43fc191ccdea31f97c26bfbbb66d4456df7d66c5a4253117b55e035"
      },
      "completed_against": {
        "AIS-008": "sha256:ae0244647a8219ec8f3cd692a80d70c59679bc0502fada26aec39a85c98a61a7",
        "AIS-009": "sha256:ca8faee8ca35286fad97ea40959e30bb078badade6d67c8dccdd9cff915f73f7",
        "AIS-020": "sha256:a4a3c69d47e31fa59042fbcc5d4992379696223e9ccdf5a8de3800aaaacc30ed",
        "AIS-021": "sha256:635c20f5f43fc191ccdea31f97c26bfbbb66d4456df7d66c5a4253117b55e035",
        "AIS-043": "sha256:ecbd7b859a28e78c8fb5102a68f8a73ac13df9e8c1862fda89e5240b590b68f0",
        "DEC-007": "sha256:c092606ae0d1acdb955329fb0999903f6b0219c952e9d0bbaa51fa3ef1b8ce76",
        "FR-004": "sha256:9351afecec6d138f345d4b8a50128f10215e41705620c6441d15ebeb92e564a8",
        "FR-005": "sha256:65cffe4e76d287540239f49d99854034164b552e04e3a5f968efbc820d0fc590",
        "FR-006": "sha256:3e514e8dfd04bc478e405c56c902c4d400ee8620a0edc9f5da1d311dea49978d",
        "FR-007": "sha256:7bcffe16420753854d6ef411e7c3099f58fe40bf91b17e707680884c894d989d",
        "FR-008": "sha256:1efd77e47f9d55a3f735dac2b82d9d1534cd786f60fffcd8463bf2a28f8da6c6",
        "FR-009": "sha256:ac1727d2ea6122e201b9f35a77530ece91dba013c30ac656bc80c791a5884aa5",
        "FR-016": "sha256:ea3570068dfeaaa7dda913bd48c48be6dd4a84a8b69fe0e06859657edfaeb67d",
        "NFR-001": "sha256:df17800aee3588d157d4116760d6c0ac8b1aaaf338acd002ab064f7c755650e9",
        "NFR-002": "sha256:b6d43217718ec3585d21c7e35c03545369d59141a6cd7f07acb47100eef1826b",
        "NFR-003": "sha256:38473b65fca10e09faa1982b8eee81daace9150eebf3baefbaa5e7209036eabf",
        "REQ-003": "sha256:aedb4376fbb5fa1aa745d236c36bf0e638196fe7604260ebfc5adba12d358b9e",
        "REQ-005": "sha256:05e5b7ff7f62222173552749b93cd16789de08c57b13afb8171919152c976b57",
        "REQ-009": "sha256:726e06a357ca16e93d7ddde707c7d9b1a7a0d583ae14dfc677a33b7b0efa370c",
        "REQ-010": "sha256:aeba84bc66554b71b5aa5286cde9cbe4906cc3b0b502f744baa1561c4f22890a",
        "REQ-011": "sha256:ef32b333ad49ed6d560a3000ff6018a61fc3b9c3c62c7ff1d361ca6da28ef3b6",
        "REQ-012": "sha256:41c59c37940929ef97e7946344ce85005618b1123b73e752b8750066f6ee568d",
        "UC-002": "sha256:98a48e376358abb62b44feb49ed89036461de691abb57208c9127ef4e0918d00"
      },
      "blocked_at_completion": false
    },
    "T015": {
      "hash": "sha256:61a6b95f5616a9fbfbc39ac38ad74e6bb79f17f073b53ef8539b62659c0be243",
      "class": "restated",
      "cites": {
        "AIS-044": "sha256:50a4a6ae4576b654b7ac1578481d148899518955f15500b3d709f8c107cbd983",
        "AIS-006": "sha256:54e23a48faf12e83c12c8f4538e2532f9ed4cebc29b900f82752975ca73a130b",
        "AIS-013": "sha256:3a67ab57e283b333f166a1ffee484866594a8f199e200c2be907ebdc19a8eb7b",
        "AIS-014": "sha256:63501bcbe2699b95976faa6310fc67bcc0a812aa72a0cbbe5827fe33f3e87b66",
        "AIS-015": "sha256:04a4bcfcfbe3b003ff1f953449e83f69bb14f8d5255add3bd21134a93d020b09",
        "AIS-050": "sha256:61ffe257563f058d194c7a2b53f194c7214e6bf8d8bc6da4fb12868459ee68be",
        "AIS-051": "sha256:e5f372d0f875d229848dba789a21a65c62debd127131a4ac1696bbc41a36bd62",
        "AIS-057": "sha256:8676693afdc4b17e371018536f85159d37c6ed8161a1223016b4c0a9fd45be97"
      },
      "completed_against": {
        "AIS-006": "sha256:54e23a48faf12e83c12c8f4538e2532f9ed4cebc29b900f82752975ca73a130b",
        "AIS-013": "sha256:3a67ab57e283b333f166a1ffee484866594a8f199e200c2be907ebdc19a8eb7b",
        "AIS-014": "sha256:63501bcbe2699b95976faa6310fc67bcc0a812aa72a0cbbe5827fe33f3e87b66",
        "AIS-015": "sha256:04a4bcfcfbe3b003ff1f953449e83f69bb14f8d5255add3bd21134a93d020b09",
        "AIS-044": "sha256:50a4a6ae4576b654b7ac1578481d148899518955f15500b3d709f8c107cbd983",
        "AIS-050": "sha256:61ffe257563f058d194c7a2b53f194c7214e6bf8d8bc6da4fb12868459ee68be",
        "AIS-051": "sha256:e5f372d0f875d229848dba789a21a65c62debd127131a4ac1696bbc41a36bd62",
        "AIS-057": "sha256:8676693afdc4b17e371018536f85159d37c6ed8161a1223016b4c0a9fd45be97",
        "DEC-005": "sha256:141ce780db6dcb541ca4b1c2e4792550978c143cbd5eea57838c9736579db7be",
        "DEC-007": "sha256:c092606ae0d1acdb955329fb0999903f6b0219c952e9d0bbaa51fa3ef1b8ce76",
        "FR-001": "sha256:9b8829cba27184e4e9004fc0ba4af995bb30d52c81be952f804b2817d4ed7a36",
        "FR-002": "sha256:32dc804048b7e426e532d1b98c0fc50d4ebdb1ebea550a3caa6e72002e6f2e6f",
        "FR-006": "sha256:3e514e8dfd04bc478e405c56c902c4d400ee8620a0edc9f5da1d311dea49978d",
        "FR-010": "sha256:8aa5f448ddb370a99dcbb5281add4a0106cbb03152c32325dd17c921f07fe781",
        "FR-011": "sha256:0ca8c3df85b82bec17637d1f09bab4668b4bd26b3337664b6990b103bab3b0ec",
        "FR-012": "sha256:c398b73a4cbf412ded409ed8f094ae59ed47616c7a4bca37420906c7d2f7291c",
        "FR-013": "sha256:38d94ad5c0f0b784877847af344fd77e14f9941ad73bbc98a535b7942b21e73a",
        "FR-014": "sha256:ad118cfdcba914b6dcced02aeaa12e219170b3d9b9b64e1cb3ae800f2cf133cd",
        "FR-015": "sha256:f1d6d8705d95ac71564ee91d3882b78a9adc9ded77660d8d1531a57c74db3bb0",
        "FR-016": "sha256:ea3570068dfeaaa7dda913bd48c48be6dd4a84a8b69fe0e06859657edfaeb67d",
        "FR-017": "sha256:1dd105d6d7f7eac38abd4ce9c97be3e06a173c742a3cb34e6d0bcf1e15376376",
        "NFR-002": "sha256:b6d43217718ec3585d21c7e35c03545369d59141a6cd7f07acb47100eef1826b",
        "NFR-003": "sha256:38473b65fca10e09faa1982b8eee81daace9150eebf3baefbaa5e7209036eabf",
        "REQ-001": "sha256:256ed10c2afe9e022501c4f25204361be56ca8ebe3e3b4e74b6738c84ce8c568",
        "REQ-004": "sha256:b52a4907c94a13f2f9fa348ca1da6350f4504b1786482733a63bf8784b4b091f",
        "REQ-005": "sha256:05e5b7ff7f62222173552749b93cd16789de08c57b13afb8171919152c976b57",
        "REQ-006": "sha256:e517cbec32193438afe0b76b99eb5cc9d95f0fce65987fc63aa5d8ee7f783a47",
        "REQ-007": "sha256:bb73c59fe2c6e1a8dc4e62a7718608d9cc9c9b2c1ca3dc4e1b8d91b8ace51041",
        "REQ-008": "sha256:f70bd5a6e36b3acdc1e0ef4100073132fb4a46ffcc099383dc4bc14f247254fe",
        "REQ-009": "sha256:726e06a357ca16e93d7ddde707c7d9b1a7a0d583ae14dfc677a33b7b0efa370c",
        "REQ-010": "sha256:aeba84bc66554b71b5aa5286cde9cbe4906cc3b0b502f744baa1561c4f22890a",
        "REQ-011": "sha256:ef32b333ad49ed6d560a3000ff6018a61fc3b9c3c62c7ff1d361ca6da28ef3b6",
        "UC-001": "sha256:39bc034f14596d29449003ea963e3a0b3f51215ee9e15e11c5fef4ae2aaed9ab",
        "UC-002": "sha256:98a48e376358abb62b44feb49ed89036461de691abb57208c9127ef4e0918d00",
        "UC-003": "sha256:e47e99898085ee543414e29d1821cf2de70b134f24d206a2cd379c24a9e577c6"
      },
      "blocked_at_completion": false
    },
    "T016": {
      "hash": "sha256:9709b05696ad2c43abc382c71003fc619ed9aa37a3a7f5950a903585de4fc919",
      "class": "restated",
      "cites": {
        "AIS-024": "sha256:3f7c205c5d9ce8b91e3549e8711d2e35bcd942ce700b387a39a5225d3b7fd017",
        "AIS-034": "sha256:78bddaf7b4901a446ac1c0da1b283fa70f1452351fb39a34a5545c5e3dc4045c",
        "AIS-014": "sha256:63501bcbe2699b95976faa6310fc67bcc0a812aa72a0cbbe5827fe33f3e87b66",
        "AIS-022": "sha256:55edcfd29969634bfdf1c81455cbf667576f9a63480b72acfc324ed8cd6e0769",
        "AIS-048": "sha256:f7558a2888e61d956d25926606b4453d188b26a00d183fb0d1d92784835552a7",
        "AIS-038": "sha256:ba473fccf4a4206208df9e0d0a9296d04740897cb107d829fbfe14b6d9f3e1f8"
      },
      "completed_against": {
        "AIS-014": "sha256:63501bcbe2699b95976faa6310fc67bcc0a812aa72a0cbbe5827fe33f3e87b66",
        "AIS-022": "sha256:55edcfd29969634bfdf1c81455cbf667576f9a63480b72acfc324ed8cd6e0769",
        "AIS-024": "sha256:3f7c205c5d9ce8b91e3549e8711d2e35bcd942ce700b387a39a5225d3b7fd017",
        "AIS-034": "sha256:78bddaf7b4901a446ac1c0da1b283fa70f1452351fb39a34a5545c5e3dc4045c",
        "AIS-038": "sha256:ba473fccf4a4206208df9e0d0a9296d04740897cb107d829fbfe14b6d9f3e1f8",
        "AIS-048": "sha256:f7558a2888e61d956d25926606b4453d188b26a00d183fb0d1d92784835552a7",
        "DEC-002": "sha256:e5e293b732dc3070124d2538a452ac15b148fb9937d58da144d4ee8d004b2032",
        "FR-001": "sha256:9b8829cba27184e4e9004fc0ba4af995bb30d52c81be952f804b2817d4ed7a36",
        "FR-006": "sha256:3e514e8dfd04bc478e405c56c902c4d400ee8620a0edc9f5da1d311dea49978d",
        "FR-014": "sha256:ad118cfdcba914b6dcced02aeaa12e219170b3d9b9b64e1cb3ae800f2cf133cd",
        "FR-015": "sha256:f1d6d8705d95ac71564ee91d3882b78a9adc9ded77660d8d1531a57c74db3bb0",
        "REQ-001": "sha256:256ed10c2afe9e022501c4f25204361be56ca8ebe3e3b4e74b6738c84ce8c568",
        "REQ-007": "sha256:bb73c59fe2c6e1a8dc4e62a7718608d9cc9c9b2c1ca3dc4e1b8d91b8ace51041",
        "REQ-008": "sha256:f70bd5a6e36b3acdc1e0ef4100073132fb4a46ffcc099383dc4bc14f247254fe",
        "REQ-011": "sha256:ef32b333ad49ed6d560a3000ff6018a61fc3b9c3c62c7ff1d361ca6da28ef3b6",
        "UC-001": "sha256:39bc034f14596d29449003ea963e3a0b3f51215ee9e15e11c5fef4ae2aaed9ab",
        "UC-002": "sha256:98a48e376358abb62b44feb49ed89036461de691abb57208c9127ef4e0918d00"
      },
      "blocked_at_completion": false
    },
    "T017": {
      "hash": "sha256:b43a8a2f0a27f4178f06e0cfaa42cc317190354ac87af5033b262ff944a27fdd",
      "class": "restated",
      "cites": {
        "AIS-006": "sha256:54e23a48faf12e83c12c8f4538e2532f9ed4cebc29b900f82752975ca73a130b",
        "AIS-021": "sha256:635c20f5f43fc191ccdea31f97c26bfbbb66d4456df7d66c5a4253117b55e035",
        "AIS-025": "sha256:c2bdca8fedfad8142d89052404b3d2ea44ac83970c8de11130fbf87af4d57794",
        "AIS-035": "sha256:36f2adb477c1ed19b889389cd562597743c5e0fec1c126b5b37be07fa564cde8",
        "AIS-055": "sha256:98bfdbf9348e859ca1304c5b69a29c498cf4ec9f2d44244cfc810b4f26316bfe",
        "AIS-062": "sha256:80cd3c27482939fb3730e0c8c7334e3fb9fb389cdad56cd2848b63088b2b9334"
      },
      "completed_against": {
        "AIS-006": "sha256:54e23a48faf12e83c12c8f4538e2532f9ed4cebc29b900f82752975ca73a130b",
        "AIS-021": "sha256:635c20f5f43fc191ccdea31f97c26bfbbb66d4456df7d66c5a4253117b55e035",
        "AIS-025": "sha256:c2bdca8fedfad8142d89052404b3d2ea44ac83970c8de11130fbf87af4d57794",
        "AIS-035": "sha256:36f2adb477c1ed19b889389cd562597743c5e0fec1c126b5b37be07fa564cde8",
        "AIS-055": "sha256:98bfdbf9348e859ca1304c5b69a29c498cf4ec9f2d44244cfc810b4f26316bfe",
        "AIS-062": "sha256:80cd3c27482939fb3730e0c8c7334e3fb9fb389cdad56cd2848b63088b2b9334",
        "DEC-002": "sha256:e5e293b732dc3070124d2538a452ac15b148fb9937d58da144d4ee8d004b2032",
        "DEC-003": "sha256:36efe9d2ce0818895e0200cf12258c73ee561dcb82dbf2c4a1723d203a605105",
        "FR-001": "sha256:9b8829cba27184e4e9004fc0ba4af995bb30d52c81be952f804b2817d4ed7a36",
        "FR-006": "sha256:3e514e8dfd04bc478e405c56c902c4d400ee8620a0edc9f5da1d311dea49978d",
        "FR-010": "sha256:8aa5f448ddb370a99dcbb5281add4a0106cbb03152c32325dd17c921f07fe781",
        "FR-014": "sha256:ad118cfdcba914b6dcced02aeaa12e219170b3d9b9b64e1cb3ae800f2cf133cd",
        "FR-015": "sha256:f1d6d8705d95ac71564ee91d3882b78a9adc9ded77660d8d1531a57c74db3bb0",
        "REQ-001": "sha256:256ed10c2afe9e022501c4f25204361be56ca8ebe3e3b4e74b6738c84ce8c568",
        "REQ-004": "sha256:b52a4907c94a13f2f9fa348ca1da6350f4504b1786482733a63bf8784b4b091f",
        "REQ-005": "sha256:05e5b7ff7f62222173552749b93cd16789de08c57b13afb8171919152c976b57",
        "REQ-007": "sha256:bb73c59fe2c6e1a8dc4e62a7718608d9cc9c9b2c1ca3dc4e1b8d91b8ace51041",
        "REQ-008": "sha256:f70bd5a6e36b3acdc1e0ef4100073132fb4a46ffcc099383dc4bc14f247254fe",
        "REQ-011": "sha256:ef32b333ad49ed6d560a3000ff6018a61fc3b9c3c62c7ff1d361ca6da28ef3b6",
        "UC-001": "sha256:39bc034f14596d29449003ea963e3a0b3f51215ee9e15e11c5fef4ae2aaed9ab",
        "UC-002": "sha256:98a48e376358abb62b44feb49ed89036461de691abb57208c9127ef4e0918d00"
      },
      "blocked_at_completion": false
    },
    "T018": {
      "hash": "sha256:848eb63f4ec135c9c98d3987721294808e3d3817f8eb584b423c4f26731f253f",
      "class": "restated",
      "cites": {
        "AIS-013": "sha256:3a67ab57e283b333f166a1ffee484866594a8f199e200c2be907ebdc19a8eb7b",
        "AIS-027": "sha256:a9f6fde904cd4b9b50af42f8df0504ff65dee864f66e6603a578d45e5c5f124b",
        "AIS-050": "sha256:61ffe257563f058d194c7a2b53f194c7214e6bf8d8bc6da4fb12868459ee68be",
        "AIS-057": "sha256:8676693afdc4b17e371018536f85159d37c6ed8161a1223016b4c0a9fd45be97",
        "AIS-048": "sha256:f7558a2888e61d956d25926606b4453d188b26a00d183fb0d1d92784835552a7"
      },
      "completed_against": {
        "AIS-013": "sha256:3a67ab57e283b333f166a1ffee484866594a8f199e200c2be907ebdc19a8eb7b",
        "AIS-027": "sha256:a9f6fde904cd4b9b50af42f8df0504ff65dee864f66e6603a578d45e5c5f124b",
        "AIS-048": "sha256:f7558a2888e61d956d25926606b4453d188b26a00d183fb0d1d92784835552a7",
        "AIS-050": "sha256:61ffe257563f058d194c7a2b53f194c7214e6bf8d8bc6da4fb12868459ee68be",
        "AIS-057": "sha256:8676693afdc4b17e371018536f85159d37c6ed8161a1223016b4c0a9fd45be97",
        "DEC-002": "sha256:e5e293b732dc3070124d2538a452ac15b148fb9937d58da144d4ee8d004b2032",
        "DEC-005": "sha256:141ce780db6dcb541ca4b1c2e4792550978c143cbd5eea57838c9736579db7be",
        "FR-001": "sha256:9b8829cba27184e4e9004fc0ba4af995bb30d52c81be952f804b2817d4ed7a36",
        "FR-006": "sha256:3e514e8dfd04bc478e405c56c902c4d400ee8620a0edc9f5da1d311dea49978d",
        "FR-010": "sha256:8aa5f448ddb370a99dcbb5281add4a0106cbb03152c32325dd17c921f07fe781",
        "FR-011": "sha256:0ca8c3df85b82bec17637d1f09bab4668b4bd26b3337664b6990b103bab3b0ec",
        "FR-013": "sha256:38d94ad5c0f0b784877847af344fd77e14f9941ad73bbc98a535b7942b21e73a",
        "FR-014": "sha256:ad118cfdcba914b6dcced02aeaa12e219170b3d9b9b64e1cb3ae800f2cf133cd",
        "FR-015": "sha256:f1d6d8705d95ac71564ee91d3882b78a9adc9ded77660d8d1531a57c74db3bb0",
        "REQ-001": "sha256:256ed10c2afe9e022501c4f25204361be56ca8ebe3e3b4e74b6738c84ce8c568",
        "REQ-004": "sha256:b52a4907c94a13f2f9fa348ca1da6350f4504b1786482733a63bf8784b4b091f",
        "REQ-005": "sha256:05e5b7ff7f62222173552749b93cd16789de08c57b13afb8171919152c976b57",
        "REQ-006": "sha256:e517cbec32193438afe0b76b99eb5cc9d95f0fce65987fc63aa5d8ee7f783a47",
        "REQ-007": "sha256:bb73c59fe2c6e1a8dc4e62a7718608d9cc9c9b2c1ca3dc4e1b8d91b8ace51041",
        "REQ-008": "sha256:f70bd5a6e36b3acdc1e0ef4100073132fb4a46ffcc099383dc4bc14f247254fe",
        "REQ-011": "sha256:ef32b333ad49ed6d560a3000ff6018a61fc3b9c3c62c7ff1d361ca6da28ef3b6",
        "UC-001": "sha256:39bc034f14596d29449003ea963e3a0b3f51215ee9e15e11c5fef4ae2aaed9ab",
        "UC-002": "sha256:98a48e376358abb62b44feb49ed89036461de691abb57208c9127ef4e0918d00"
      },
      "blocked_at_completion": false
    },
    "T019": {
      "hash": "sha256:15507c2d93848b7d24b22f03553ea80a7cbdeabc81465d1384dff945cdbcb793",
      "class": "restated",
      "cites": {
        "AIS-054": "sha256:7a39487f01f3a80c3ee002b024dabd3721110513298b128067743627c1b79aa3",
        "AIS-024": "sha256:3f7c205c5d9ce8b91e3549e8711d2e35bcd942ce700b387a39a5225d3b7fd017"
      },
      "completed_against": {
        "AIS-024": "sha256:3f7c205c5d9ce8b91e3549e8711d2e35bcd942ce700b387a39a5225d3b7fd017",
        "AIS-054": "sha256:7a39487f01f3a80c3ee002b024dabd3721110513298b128067743627c1b79aa3",
        "DEC-002": "sha256:e5e293b732dc3070124d2538a452ac15b148fb9937d58da144d4ee8d004b2032",
        "FR-001": "sha256:9b8829cba27184e4e9004fc0ba4af995bb30d52c81be952f804b2817d4ed7a36",
        "FR-006": "sha256:3e514e8dfd04bc478e405c56c902c4d400ee8620a0edc9f5da1d311dea49978d",
        "FR-010": "sha256:8aa5f448ddb370a99dcbb5281add4a0106cbb03152c32325dd17c921f07fe781",
        "FR-014": "sha256:ad118cfdcba914b6dcced02aeaa12e219170b3d9b9b64e1cb3ae800f2cf133cd",
        "FR-015": "sha256:f1d6d8705d95ac71564ee91d3882b78a9adc9ded77660d8d1531a57c74db3bb0",
        "REQ-001": "sha256:256ed10c2afe9e022501c4f25204361be56ca8ebe3e3b4e74b6738c84ce8c568",
        "REQ-004": "sha256:b52a4907c94a13f2f9fa348ca1da6350f4504b1786482733a63bf8784b4b091f",
        "REQ-005": "sha256:05e5b7ff7f62222173552749b93cd16789de08c57b13afb8171919152c976b57",
        "REQ-007": "sha256:bb73c59fe2c6e1a8dc4e62a7718608d9cc9c9b2c1ca3dc4e1b8d91b8ace51041",
        "REQ-008": "sha256:f70bd5a6e36b3acdc1e0ef4100073132fb4a46ffcc099383dc4bc14f247254fe",
        "REQ-011": "sha256:ef32b333ad49ed6d560a3000ff6018a61fc3b9c3c62c7ff1d361ca6da28ef3b6",
        "UC-001": "sha256:39bc034f14596d29449003ea963e3a0b3f51215ee9e15e11c5fef4ae2aaed9ab",
        "UC-002": "sha256:98a48e376358abb62b44feb49ed89036461de691abb57208c9127ef4e0918d00"
      },
      "blocked_at_completion": false
    },
    "T020": {
      "hash": "sha256:408b5d4fead7c45cf1935ec1f26882ab0eff2051e444059f135929c0f537ca43",
      "class": "restated",
      "cites": {
        "AIS-053": "sha256:43784ea41393117378d068f0daba401fd45776c5a9f855a78b939b5d523777df",
        "AIS-005": "sha256:7b3efe32a84407449feb6f0e6e2b14b6872e5a1bcefcaac8963c2aa6217bf1b4"
      },
      "completed_against": {
        "AIS-005": "sha256:7b3efe32a84407449feb6f0e6e2b14b6872e5a1bcefcaac8963c2aa6217bf1b4",
        "AIS-053": "sha256:43784ea41393117378d068f0daba401fd45776c5a9f855a78b939b5d523777df",
        "FR-003": "sha256:197f0e7bf32d3fffc1d86caf9e93b21576f2146c4b96744d98b9195835da670b",
        "FR-005": "sha256:65cffe4e76d287540239f49d99854034164b552e04e3a5f968efbc820d0fc590",
        "REQ-002": "sha256:7b9a9aeadce291263cd1c8f6106926ef0868c72ad872a99beac7bbbb688fb049",
        "REQ-012": "sha256:41c59c37940929ef97e7946344ce85005618b1123b73e752b8750066f6ee568d",
        "UC-002": "sha256:98a48e376358abb62b44feb49ed89036461de691abb57208c9127ef4e0918d00"
      },
      "blocked_at_completion": false
    },
    "T021": {
      "hash": "sha256:650f8e9ccf1b4882162d232971c1d6ccae9559d91842f96cc454a7cb6f5aa3ca",
      "class": "restated",
      "cites": {
        "AIS-053": "sha256:43784ea41393117378d068f0daba401fd45776c5a9f855a78b939b5d523777df",
        "AIS-054": "sha256:7a39487f01f3a80c3ee002b024dabd3721110513298b128067743627c1b79aa3",
        "AIS-056": "sha256:7318ba523083068f8e195f78ec77a7c0b642b9f52f7a863dafa8c421ceeb7a7f",
        "AIS-049": "sha256:5f71e91094328301a8d34c12620a403975b866de38b82b0d469c277af597a0d8"
      },
      "completed_against": {
        "AIS-049": "sha256:5f71e91094328301a8d34c12620a403975b866de38b82b0d469c277af597a0d8",
        "AIS-053": "sha256:43784ea41393117378d068f0daba401fd45776c5a9f855a78b939b5d523777df",
        "AIS-054": "sha256:7a39487f01f3a80c3ee002b024dabd3721110513298b128067743627c1b79aa3",
        "AIS-056": "sha256:7318ba523083068f8e195f78ec77a7c0b642b9f52f7a863dafa8c421ceeb7a7f",
        "DEC-001": "sha256:bb921b2401109f1ece0e7a13243eaba9121b572231d2c6402f21a46830d083aa",
        "DEC-002": "sha256:e5e293b732dc3070124d2538a452ac15b148fb9937d58da144d4ee8d004b2032",
        "DEC-006": "sha256:39b03e67818d400e49ee296e2e3c28ac91daeaa69b23d14ab9a0ae88a080b5de",
        "FR-001": "sha256:9b8829cba27184e4e9004fc0ba4af995bb30d52c81be952f804b2817d4ed7a36",
        "FR-002": "sha256:32dc804048b7e426e532d1b98c0fc50d4ebdb1ebea550a3caa6e72002e6f2e6f",
        "FR-003": "sha256:197f0e7bf32d3fffc1d86caf9e93b21576f2146c4b96744d98b9195835da670b",
        "FR-005": "sha256:65cffe4e76d287540239f49d99854034164b552e04e3a5f968efbc820d0fc590",
        "FR-006": "sha256:3e514e8dfd04bc478e405c56c902c4d400ee8620a0edc9f5da1d311dea49978d",
        "FR-010": "sha256:8aa5f448ddb370a99dcbb5281add4a0106cbb03152c32325dd17c921f07fe781",
        "FR-011": "sha256:0ca8c3df85b82bec17637d1f09bab4668b4bd26b3337664b6990b103bab3b0ec",
        "FR-014": "sha256:ad118cfdcba914b6dcced02aeaa12e219170b3d9b9b64e1cb3ae800f2cf133cd",
        "FR-015": "sha256:f1d6d8705d95ac71564ee91d3882b78a9adc9ded77660d8d1531a57c74db3bb0",
        "FR-016": "sha256:ea3570068dfeaaa7dda913bd48c48be6dd4a84a8b69fe0e06859657edfaeb67d",
        "FR-017": "sha256:1dd105d6d7f7eac38abd4ce9c97be3e06a173c742a3cb34e6d0bcf1e15376376",
        "NFR-002": "sha256:b6d43217718ec3585d21c7e35c03545369d59141a6cd7f07acb47100eef1826b",
        "REQ-001": "sha256:256ed10c2afe9e022501c4f25204361be56ca8ebe3e3b4e74b6738c84ce8c568",
        "REQ-002": "sha256:7b9a9aeadce291263cd1c8f6106926ef0868c72ad872a99beac7bbbb688fb049",
        "REQ-004": "sha256:b52a4907c94a13f2f9fa348ca1da6350f4504b1786482733a63bf8784b4b091f",
        "REQ-005": "sha256:05e5b7ff7f62222173552749b93cd16789de08c57b13afb8171919152c976b57",
        "REQ-007": "sha256:bb73c59fe2c6e1a8dc4e62a7718608d9cc9c9b2c1ca3dc4e1b8d91b8ace51041",
        "REQ-008": "sha256:f70bd5a6e36b3acdc1e0ef4100073132fb4a46ffcc099383dc4bc14f247254fe",
        "REQ-009": "sha256:726e06a357ca16e93d7ddde707c7d9b1a7a0d583ae14dfc677a33b7b0efa370c",
        "REQ-011": "sha256:ef32b333ad49ed6d560a3000ff6018a61fc3b9c3c62c7ff1d361ca6da28ef3b6",
        "REQ-012": "sha256:41c59c37940929ef97e7946344ce85005618b1123b73e752b8750066f6ee568d",
        "UC-001": "sha256:39bc034f14596d29449003ea963e3a0b3f51215ee9e15e11c5fef4ae2aaed9ab",
        "UC-002": "sha256:98a48e376358abb62b44feb49ed89036461de691abb57208c9127ef4e0918d00"
      },
      "blocked_at_completion": false
    },
    "Phase 4: User Story 2 - Find a nested document (Priority: P2)#e1eb391e989b": {
      "hash": "sha256:e1eb391e989b92bf324ce4eafb59740e14e2fbfa79a5c4aa045d773947b4f363",
      "class": "inferred",
      "adds": "Adds the grouping, goal, test criteria or ordering that organises the tasks, which the AI Specification does not state.",
      "reviewed": {
        "by": "Lee Sinclair",
        "at": "2026-10-01T13:36:24Z",
        "list": "RVW-009",
        "reply": "Ok"
      }
    },
    "Phase 5: User Story 3 - Read a document directly under specs (Priority: P3)#5a450a8bc11b": {
      "hash": "sha256:5a450a8bc11b65d3fab7fb9f8cf9d24d4d1edc8f925702f79e7a50eef8088522",
      "class": "inferred",
      "adds": "Adds the grouping, goal, test criteria or ordering that organises the tasks, which the AI Specification does not state.",
      "reviewed": {
        "by": "Lee Sinclair",
        "at": "2026-10-01T13:36:24Z",
        "list": "RVW-009",
        "reply": "Ok"
      }
    },
    "Phase 5: User Story 3 - Read a document directly under specs (Priority: P3)#dd9a56661728": {
      "hash": "sha256:dd9a56661728055985f3c08c0b99b9081a800c68781f4589f0d4f38ca0fb24b5",
      "class": "inferred",
      "adds": "Adds the grouping, goal, test criteria or ordering that organises the tasks, which the AI Specification does not state.",
      "reviewed": {
        "by": "Lee Sinclair",
        "at": "2026-10-01T13:36:24Z",
        "list": "RVW-009",
        "reply": "Ok"
      }
    },
    "T022": {
      "hash": "sha256:a9aea9561e6874979d41efee6fe691b96ebcbb3f8f0350d6bffc51a2ae752d16",
      "class": "restated",
      "cites": {
        "AIS-044": "sha256:50a4a6ae4576b654b7ac1578481d148899518955f15500b3d709f8c107cbd983",
        "AIS-012": "sha256:5bc6336c1bd0f8671de8ae8806beb0553d90203d3b451bb782bd67da09492001",
        "AIS-017": "sha256:c917cf5df2dff0aba7c55da433e076853b08bdb67c203676b492393593e0fa7f",
        "AIS-060": "sha256:e9ac7c0cdaf9029090ee28b5d46e6691d0f80829449612677ebd0656896c53dc"
      },
      "completed_against": {
        "AIS-012": "sha256:5bc6336c1bd0f8671de8ae8806beb0553d90203d3b451bb782bd67da09492001",
        "AIS-017": "sha256:c917cf5df2dff0aba7c55da433e076853b08bdb67c203676b492393593e0fa7f",
        "AIS-044": "sha256:50a4a6ae4576b654b7ac1578481d148899518955f15500b3d709f8c107cbd983",
        "AIS-060": "sha256:e9ac7c0cdaf9029090ee28b5d46e6691d0f80829449612677ebd0656896c53dc",
        "DEC-007": "sha256:c092606ae0d1acdb955329fb0999903f6b0219c952e9d0bbaa51fa3ef1b8ce76",
        "FR-001": "sha256:9b8829cba27184e4e9004fc0ba4af995bb30d52c81be952f804b2817d4ed7a36",
        "FR-002": "sha256:32dc804048b7e426e532d1b98c0fc50d4ebdb1ebea550a3caa6e72002e6f2e6f",
        "FR-010": "sha256:8aa5f448ddb370a99dcbb5281add4a0106cbb03152c32325dd17c921f07fe781",
        "FR-012": "sha256:c398b73a4cbf412ded409ed8f094ae59ed47616c7a4bca37420906c7d2f7291c",
        "FR-013": "sha256:38d94ad5c0f0b784877847af344fd77e14f9941ad73bbc98a535b7942b21e73a",
        "FR-014": "sha256:ad118cfdcba914b6dcced02aeaa12e219170b3d9b9b64e1cb3ae800f2cf133cd",
        "FR-015": "sha256:f1d6d8705d95ac71564ee91d3882b78a9adc9ded77660d8d1531a57c74db3bb0",
        "FR-016": "sha256:ea3570068dfeaaa7dda913bd48c48be6dd4a84a8b69fe0e06859657edfaeb67d",
        "FR-017": "sha256:1dd105d6d7f7eac38abd4ce9c97be3e06a173c742a3cb34e6d0bcf1e15376376",
        "NFR-002": "sha256:b6d43217718ec3585d21c7e35c03545369d59141a6cd7f07acb47100eef1826b",
        "NFR-003": "sha256:38473b65fca10e09faa1982b8eee81daace9150eebf3baefbaa5e7209036eabf",
        "REQ-001": "sha256:256ed10c2afe9e022501c4f25204361be56ca8ebe3e3b4e74b6738c84ce8c568",
        "REQ-004": "sha256:b52a4907c94a13f2f9fa348ca1da6350f4504b1786482733a63bf8784b4b091f",
        "REQ-005": "sha256:05e5b7ff7f62222173552749b93cd16789de08c57b13afb8171919152c976b57",
        "REQ-006": "sha256:e517cbec32193438afe0b76b99eb5cc9d95f0fce65987fc63aa5d8ee7f783a47",
        "REQ-007": "sha256:bb73c59fe2c6e1a8dc4e62a7718608d9cc9c9b2c1ca3dc4e1b8d91b8ace51041",
        "REQ-008": "sha256:f70bd5a6e36b3acdc1e0ef4100073132fb4a46ffcc099383dc4bc14f247254fe",
        "REQ-009": "sha256:726e06a357ca16e93d7ddde707c7d9b1a7a0d583ae14dfc677a33b7b0efa370c",
        "REQ-010": "sha256:aeba84bc66554b71b5aa5286cde9cbe4906cc3b0b502f744baa1561c4f22890a",
        "REQ-011": "sha256:ef32b333ad49ed6d560a3000ff6018a61fc3b9c3c62c7ff1d361ca6da28ef3b6",
        "UC-001": "sha256:39bc034f14596d29449003ea963e3a0b3f51215ee9e15e11c5fef4ae2aaed9ab",
        "UC-002": "sha256:98a48e376358abb62b44feb49ed89036461de691abb57208c9127ef4e0918d00",
        "UC-003": "sha256:e47e99898085ee543414e29d1821cf2de70b134f24d206a2cd379c24a9e577c6"
      },
      "blocked_at_completion": false
    },
    "T023": {
      "hash": "sha256:392962397c4d41a989e7c1f7a2835397f99c78304775127a8e1834475d5bdcb0",
      "class": "restated",
      "cites": {
        "AIS-018": "sha256:de11e45b65e87fd463a911bef1475c1eaf39b9973938c7d144cbe5bd8e9917a6",
        "AIS-012": "sha256:5bc6336c1bd0f8671de8ae8806beb0553d90203d3b451bb782bd67da09492001",
        "AIS-017": "sha256:c917cf5df2dff0aba7c55da433e076853b08bdb67c203676b492393593e0fa7f",
        "AIS-023": "sha256:6644b93f8f8e69eb7e83d12643e22e6e83e44cefa9cb5a084ea219723345591c",
        "AIS-060": "sha256:e9ac7c0cdaf9029090ee28b5d46e6691d0f80829449612677ebd0656896c53dc"
      },
      "completed_against": {
        "AIS-012": "sha256:5bc6336c1bd0f8671de8ae8806beb0553d90203d3b451bb782bd67da09492001",
        "AIS-017": "sha256:c917cf5df2dff0aba7c55da433e076853b08bdb67c203676b492393593e0fa7f",
        "AIS-018": "sha256:de11e45b65e87fd463a911bef1475c1eaf39b9973938c7d144cbe5bd8e9917a6",
        "AIS-023": "sha256:6644b93f8f8e69eb7e83d12643e22e6e83e44cefa9cb5a084ea219723345591c",
        "AIS-060": "sha256:e9ac7c0cdaf9029090ee28b5d46e6691d0f80829449612677ebd0656896c53dc",
        "DEC-001": "sha256:bb921b2401109f1ece0e7a13243eaba9121b572231d2c6402f21a46830d083aa",
        "FR-001": "sha256:9b8829cba27184e4e9004fc0ba4af995bb30d52c81be952f804b2817d4ed7a36",
        "FR-012": "sha256:c398b73a4cbf412ded409ed8f094ae59ed47616c7a4bca37420906c7d2f7291c",
        "FR-016": "sha256:ea3570068dfeaaa7dda913bd48c48be6dd4a84a8b69fe0e06859657edfaeb67d",
        "FR-017": "sha256:1dd105d6d7f7eac38abd4ce9c97be3e06a173c742a3cb34e6d0bcf1e15376376",
        "REQ-001": "sha256:256ed10c2afe9e022501c4f25204361be56ca8ebe3e3b4e74b6738c84ce8c568",
        "REQ-006": "sha256:e517cbec32193438afe0b76b99eb5cc9d95f0fce65987fc63aa5d8ee7f783a47",
        "REQ-009": "sha256:726e06a357ca16e93d7ddde707c7d9b1a7a0d583ae14dfc677a33b7b0efa370c",
        "UC-001": "sha256:39bc034f14596d29449003ea963e3a0b3f51215ee9e15e11c5fef4ae2aaed9ab",
        "UC-002": "sha256:98a48e376358abb62b44feb49ed89036461de691abb57208c9127ef4e0918d00",
        "UC-003": "sha256:e47e99898085ee543414e29d1821cf2de70b134f24d206a2cd379c24a9e577c6"
      },
      "blocked_at_completion": false
    },
    "Phase 5: User Story 3 - Read a document directly under specs (Priority: P3)#751a994c52dc": {
      "hash": "sha256:751a994c52dc9d50a6589d163b640a803716cea9652c075659597b3f3744edbc",
      "class": "inferred",
      "adds": "Adds the grouping, goal, test criteria or ordering that organises the tasks, which the AI Specification does not state.",
      "reviewed": {
        "by": "Lee Sinclair",
        "at": "2026-10-01T13:36:24Z",
        "list": "RVW-009",
        "reply": "Ok"
      }
    },
    "T024": {
      "hash": "sha256:46ce876d58cebc1364a84c5d820db7dfba6e41aeeba45e2f8369105fc4e46ed1",
      "class": "restated",
      "cites": {
        "AIS-046": "sha256:4792cd0d137f7703b41afb02fef701d595b090df0d8ca64756f18f64a6c3256a",
        "AIS-016": "sha256:ab023f06526e4601e7e4f6a76b3f05c41396747454b74be9fa4aae10707987e0",
        "AIS-061": "sha256:28096f8adbffe497dfb993efa0b188bc016240654b224714b46bf13bbe144abb",
        "AIS-072": "sha256:0bf9e4d35bb7db4ce08bc326a291c9f80c1fce8aa4ceca7880769384588e0e7d"
      },
      "completed_against": {
        "AIS-016": "sha256:ab023f06526e4601e7e4f6a76b3f05c41396747454b74be9fa4aae10707987e0",
        "AIS-046": "sha256:4792cd0d137f7703b41afb02fef701d595b090df0d8ca64756f18f64a6c3256a",
        "AIS-061": "sha256:28096f8adbffe497dfb993efa0b188bc016240654b224714b46bf13bbe144abb",
        "AIS-072": "sha256:0bf9e4d35bb7db4ce08bc326a291c9f80c1fce8aa4ceca7880769384588e0e7d",
        "DEC-007": "sha256:c092606ae0d1acdb955329fb0999903f6b0219c952e9d0bbaa51fa3ef1b8ce76",
        "FR-016": "sha256:ea3570068dfeaaa7dda913bd48c48be6dd4a84a8b69fe0e06859657edfaeb67d",
        "NFR-002": "sha256:b6d43217718ec3585d21c7e35c03545369d59141a6cd7f07acb47100eef1826b",
        "NFR-003": "sha256:38473b65fca10e09faa1982b8eee81daace9150eebf3baefbaa5e7209036eabf",
        "REQ-005": "sha256:05e5b7ff7f62222173552749b93cd16789de08c57b13afb8171919152c976b57",
        "REQ-009": "sha256:726e06a357ca16e93d7ddde707c7d9b1a7a0d583ae14dfc677a33b7b0efa370c",
        "REQ-010": "sha256:aeba84bc66554b71b5aa5286cde9cbe4906cc3b0b502f744baa1561c4f22890a"
      },
      "blocked_at_completion": false
    },
    "T025": {
      "hash": "sha256:febc3922bcb086abfaf3c328a9d7a1db54a4e47b69ba016a4a085c333af1e5bb",
      "class": "inferred",
      "adds": "Adds a final review step that checks no dependency, route or extra change was introduced.",
      "reviewed": {
        "by": "Lee Sinclair",
        "at": "2026-10-01T13:36:24Z",
        "list": "RVW-009",
        "reply": "Ok"
      },
      "sources": {
        "AIS-058": "sha256:31f0a466e2d5a2de65bf3281a01357947b596fe09b91be59b86926900d117152",
        "AIS-059": "sha256:980c28303da1bead8671df27d5a416e946d3bc28609c246558b51026f89adba6",
        "AIS-030": "sha256:e57d7d30152612780d8e18253036a07ff2c04f1462133d3e4a696d3afdcc4aa0",
        "AIS-033": "sha256:4d0d690106232bcac25a8dc35253845b7d23ae80f1a5bd59f3f1d0de01a8f365",
        "AIS-065": "sha256:128abb124e342a32b0a9722b3ab6ef7d20ec160ddd2951c3d5d7e70e816784ad"
      },
      "completed_against": {
        "AIS-030": "sha256:e57d7d30152612780d8e18253036a07ff2c04f1462133d3e4a696d3afdcc4aa0",
        "AIS-033": "sha256:4d0d690106232bcac25a8dc35253845b7d23ae80f1a5bd59f3f1d0de01a8f365",
        "AIS-058": "sha256:31f0a466e2d5a2de65bf3281a01357947b596fe09b91be59b86926900d117152",
        "AIS-059": "sha256:980c28303da1bead8671df27d5a416e946d3bc28609c246558b51026f89adba6",
        "AIS-065": "sha256:128abb124e342a32b0a9722b3ab6ef7d20ec160ddd2951c3d5d7e70e816784ad",
        "ART-007": "sha256:084128aeb0d17c901971f78251314276ef4c4b2cc3d9bb09ed723e078fc5eeb9",
        "ART-008": "sha256:f6fef5898a572d62890e617df6b3c58cd89f75af3a3f1c891255b59bd498b730",
        "DEC-001": "sha256:bb921b2401109f1ece0e7a13243eaba9121b572231d2c6402f21a46830d083aa",
        "DEC-002": "sha256:e5e293b732dc3070124d2538a452ac15b148fb9937d58da144d4ee8d004b2032",
        "DEC-005": "sha256:141ce780db6dcb541ca4b1c2e4792550978c143cbd5eea57838c9736579db7be",
        "DEC-007": "sha256:c092606ae0d1acdb955329fb0999903f6b0219c952e9d0bbaa51fa3ef1b8ce76",
        "FR-001": "sha256:9b8829cba27184e4e9004fc0ba4af995bb30d52c81be952f804b2817d4ed7a36",
        "FR-006": "sha256:3e514e8dfd04bc478e405c56c902c4d400ee8620a0edc9f5da1d311dea49978d",
        "FR-010": "sha256:8aa5f448ddb370a99dcbb5281add4a0106cbb03152c32325dd17c921f07fe781",
        "FR-011": "sha256:0ca8c3df85b82bec17637d1f09bab4668b4bd26b3337664b6990b103bab3b0ec",
        "FR-013": "sha256:38d94ad5c0f0b784877847af344fd77e14f9941ad73bbc98a535b7942b21e73a",
        "FR-014": "sha256:ad118cfdcba914b6dcced02aeaa12e219170b3d9b9b64e1cb3ae800f2cf133cd",
        "FR-015": "sha256:f1d6d8705d95ac71564ee91d3882b78a9adc9ded77660d8d1531a57c74db3bb0",
        "FR-016": "sha256:ea3570068dfeaaa7dda913bd48c48be6dd4a84a8b69fe0e06859657edfaeb67d",
        "FR-017": "sha256:1dd105d6d7f7eac38abd4ce9c97be3e06a173c742a3cb34e6d0bcf1e15376376",
        "NFR-002": "sha256:b6d43217718ec3585d21c7e35c03545369d59141a6cd7f07acb47100eef1826b",
        "NFR-003": "sha256:38473b65fca10e09faa1982b8eee81daace9150eebf3baefbaa5e7209036eabf",
        "REQ-001": "sha256:256ed10c2afe9e022501c4f25204361be56ca8ebe3e3b4e74b6738c84ce8c568",
        "REQ-004": "sha256:b52a4907c94a13f2f9fa348ca1da6350f4504b1786482733a63bf8784b4b091f",
        "REQ-005": "sha256:05e5b7ff7f62222173552749b93cd16789de08c57b13afb8171919152c976b57",
        "REQ-006": "sha256:e517cbec32193438afe0b76b99eb5cc9d95f0fce65987fc63aa5d8ee7f783a47",
        "REQ-007": "sha256:bb73c59fe2c6e1a8dc4e62a7718608d9cc9c9b2c1ca3dc4e1b8d91b8ace51041",
        "REQ-008": "sha256:f70bd5a6e36b3acdc1e0ef4100073132fb4a46ffcc099383dc4bc14f247254fe",
        "REQ-009": "sha256:726e06a357ca16e93d7ddde707c7d9b1a7a0d583ae14dfc677a33b7b0efa370c",
        "REQ-010": "sha256:aeba84bc66554b71b5aa5286cde9cbe4906cc3b0b502f744baa1561c4f22890a",
        "REQ-011": "sha256:ef32b333ad49ed6d560a3000ff6018a61fc3b9c3c62c7ff1d361ca6da28ef3b6",
        "UC-001": "sha256:39bc034f14596d29449003ea963e3a0b3f51215ee9e15e11c5fef4ae2aaed9ab",
        "UC-002": "sha256:98a48e376358abb62b44feb49ed89036461de691abb57208c9127ef4e0918d00"
      },
      "blocked_at_completion": false
    },
    "T026": {
      "hash": "sha256:245a9cfdbfcb02577ca1d266f2264709f920250688da1d1b1b59c4e3c6b64e94",
      "class": "inferred",
      "adds": "Adds running the quickstart as a final validation step.",
      "reviewed": {
        "by": "Lee Sinclair",
        "at": "2026-10-01T13:36:24Z",
        "list": "RVW-009",
        "reply": "Ok"
      },
      "sources": {
        "AIS-047": "sha256:d00cae3fd57ea3b2f433c6b5fff99fa07d2841409c68b29065dbd30ec0ac64a4",
        "AIS-052": "sha256:76fca578e34b38ea8bc39a80729fcc493c169028c447bbeaaf0d590f3184a0a3"
      },
      "completed_against": {
        "AIS-047": "sha256:d00cae3fd57ea3b2f433c6b5fff99fa07d2841409c68b29065dbd30ec0ac64a4",
        "AIS-052": "sha256:76fca578e34b38ea8bc39a80729fcc493c169028c447bbeaaf0d590f3184a0a3",
        "FR-010": "sha256:8aa5f448ddb370a99dcbb5281add4a0106cbb03152c32325dd17c921f07fe781",
        "NFR-003": "sha256:38473b65fca10e09faa1982b8eee81daace9150eebf3baefbaa5e7209036eabf",
        "REQ-004": "sha256:b52a4907c94a13f2f9fa348ca1da6350f4504b1786482733a63bf8784b4b091f",
        "REQ-005": "sha256:05e5b7ff7f62222173552749b93cd16789de08c57b13afb8171919152c976b57",
        "REQ-009": "sha256:726e06a357ca16e93d7ddde707c7d9b1a7a0d583ae14dfc677a33b7b0efa370c",
        "REQ-010": "sha256:aeba84bc66554b71b5aa5286cde9cbe4906cc3b0b502f744baa1561c4f22890a",
        "REQ-011": "sha256:ef32b333ad49ed6d560a3000ff6018a61fc3b9c3c62c7ff1d361ca6da28ef3b6",
        "UC-001": "sha256:39bc034f14596d29449003ea963e3a0b3f51215ee9e15e11c5fef4ae2aaed9ab"
      },
      "blocked_at_completion": false
    },
    "Dependencies and execution order#134ed95f7c9d": {
      "hash": "sha256:134ed95f7c9db99889ad32f13214128c29895c0d3c6741a2031be6f569b6199c",
      "class": "inferred",
      "adds": "Adds the grouping, goal, test criteria or ordering that organises the tasks, which the AI Specification does not state.",
      "reviewed": {
        "by": "Lee Sinclair",
        "at": "2026-10-01T13:36:24Z",
        "list": "RVW-009",
        "reply": "Ok"
      }
    },
    "§Change Log": {
      "hash": "sha256:c8125cc9f94594e60a2e0d68b05f7bf53fc6deba1c17335ae3424c261ec5500a",
      "class": "restated",
      "cites": {
        "DEC-001": "sha256:bb921b2401109f1ece0e7a13243eaba9121b572231d2c6402f21a46830d083aa"
      }
    },
    "§Record": {
      "hash": "sha256:23b35fe72a02d11c538eeb2fbd5432f29891c68fd3042803822d4ae37373734d",
      "class": "restated",
      "cites": {
        "DEC-001": "sha256:bb921b2401109f1ece0e7a13243eaba9121b572231d2c6402f21a46830d083aa"
      }
    }
  },
  "acceptances": [
    {
      "id": "RVW-009",
      "stage": "tasks",
      "kind": "inferred",
      "digest": "sha256:a40e249e736736bbe04a3ce16130d6c0cdc033240a56c3b4a9a2ea7da22dc04c",
      "by": "Lee Sinclair",
      "at": "2026-10-01T13:36:24Z",
      "reply": "Ok",
      "accepted": [
        "#f52d711103d5",
        "#2cf5717e5d14",
        "Tasks: Reading-order navigation for story documents#766685533721",
        "Tasks: Reading-order navigation for story documents#2654923f9d33",
        "Tasks: Reading-order navigation for story documents#74d454cbf32e",
        "Tasks: Reading-order navigation for story documents#47963b2f5376",
        "§Format: `[ID] [P?] [Story] Description `",
        "T002",
        "Phase 2: Foundational (Blocking Prerequisites)#93cca68b24f6",
        "Phase 3: User Story 1 - Read a story from start to finish (Priority: P1) 🎯 MVP#2ef46a5aea8b",
        "Phase 3: User Story 1 - Read a story from start to finish (Priority: P1) 🎯 MVP#18ec2909f385",
        "Phase 3: User Story 1 - Read a story from start to finish (Priority: P1) 🎯 MVP#81d3aab60764",
        "Phase 4: User Story 2 - Find a nested document (Priority: P2)#1ecc365024fd",
        "Phase 4: User Story 2 - Find a nested document (Priority: P2)#75b1c9d1c2bc",
        "Phase 4: User Story 2 - Find a nested document (Priority: P2)#e1eb391e989b",
        "Phase 5: User Story 3 - Read a document directly under specs (Priority: P3)#5a450a8bc11b",
        "Phase 5: User Story 3 - Read a document directly under specs (Priority: P3)#dd9a56661728",
        "Phase 5: User Story 3 - Read a document directly under specs (Priority: P3)#751a994c52dc",
        "T025",
        "T026",
        "Dependencies and execution order#134ed95f7c9d"
      ],
      "except": [],
      "questioned": [],
      "reopened": [],
      "reason": null,
      "hashes": {
        "#f52d711103d5": "sha256:f52d711103d50a437830c6fbcd04fb4bab49a0f82f6d26d1c791c6e8488dd090",
        "#2cf5717e5d14": "sha256:2cf5717e5d14288202df5613edf212e42618ba7e9f8bd855a74bb75cd8230860",
        "Tasks: Reading-order navigation for story documents#766685533721": "sha256:76668553372157d9a9128be091ec525f0e7ead574c4395f4b80b4113bc40d789",
        "Tasks: Reading-order navigation for story documents#2654923f9d33": "sha256:2654923f9d3305a4235f9c72ec790d40648d0f4fdf31c552b2c50ba53fc0ba61",
        "Tasks: Reading-order navigation for story documents#74d454cbf32e": "sha256:74d454cbf32e95104d8974a0a756d0614e8fd76041633f3b5c91bb2b3f73d2e3",
        "Tasks: Reading-order navigation for story documents#47963b2f5376": "sha256:47963b2f53761ceaa92f68329a0b2c1d1a2d21a9d0f22daeaec5013dde583893",
        "§Format: `[ID] [P?] [Story] Description `": "sha256:78ecff41c1b9dbf4c7a3caffaf8d3df65f3a498a6db05a25bb4b8e93ae5f0f99",
        "T002": "sha256:0a0a1828b0d200b5935a2ea9236e296ad192bbbdd4466395f6e7b38e2bc2e935",
        "Phase 2: Foundational (Blocking Prerequisites)#93cca68b24f6": "sha256:93cca68b24f6c5203993e3ae6e86a35c53be45183c7afd0c7321acb77ec28319",
        "Phase 3: User Story 1 - Read a story from start to finish (Priority: P1) 🎯 MVP#2ef46a5aea8b": "sha256:2ef46a5aea8b59df8052eca1fee9a67ac03a6364135da1011de8a42f4a20cba3",
        "Phase 3: User Story 1 - Read a story from start to finish (Priority: P1) 🎯 MVP#18ec2909f385": "sha256:18ec2909f38542bd2793f1fb00bf71a870afdc07d1d4c8790789877b10a94c62",
        "Phase 3: User Story 1 - Read a story from start to finish (Priority: P1) 🎯 MVP#81d3aab60764": "sha256:81d3aab6076464404e82fb7673828939f35344495aeff4fbdc3c8c016b4d0205",
        "Phase 4: User Story 2 - Find a nested document (Priority: P2)#1ecc365024fd": "sha256:1ecc365024fd086f1238d06c0fe7c962d43a46d17ecebffa56d335690537f65f",
        "Phase 4: User Story 2 - Find a nested document (Priority: P2)#75b1c9d1c2bc": "sha256:75b1c9d1c2bc68aecb345f7db5950ce4628c2d36558d5ddfda09e8e9eaa5e97c",
        "Phase 4: User Story 2 - Find a nested document (Priority: P2)#e1eb391e989b": "sha256:e1eb391e989b92bf324ce4eafb59740e14e2fbfa79a5c4aa045d773947b4f363",
        "Phase 5: User Story 3 - Read a document directly under specs (Priority: P3)#5a450a8bc11b": "sha256:5a450a8bc11b65d3fab7fb9f8cf9d24d4d1edc8f925702f79e7a50eef8088522",
        "Phase 5: User Story 3 - Read a document directly under specs (Priority: P3)#dd9a56661728": "sha256:dd9a56661728055985f3c08c0b99b9081a800c68781f4589f0d4f38ca0fb24b5",
        "Phase 5: User Story 3 - Read a document directly under specs (Priority: P3)#751a994c52dc": "sha256:751a994c52dc9d50a6589d163b640a803716cea9652c075659597b3f3744edbc",
        "T025": "sha256:febc3922bcb086abfaf3c328a9d7a1db54a4e47b69ba016a4a085c333af1e5bb",
        "T026": "sha256:245a9cfdbfcb02577ca1d266f2264709f920250688da1d1b1b59c4e3c6b64e94",
        "Dependencies and execution order#134ed95f7c9d": "sha256:134ed95f7c9db99889ad32f13214128c29895c0d3c6741a2031be6f569b6199c"
      }
    }
  ]
}
```
<!-- eil:end provenance -->

## Quality Assessment

<!-- eil:begin assessment -->
```json
{
  "stage": "tasks",
  "evaluated_at": "2026-10-01T13:42:17Z",
  "fingerprint": "sha256:d9b1d94dc0de186963419472f88a019b059bbc0029ecd9922c1f6567db7f09fc",
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
      "reason": "AI assessment: Every task carries out an AIS item (restating DEC-001 to DEC-007): edits to Viewer._render_document, the new helpers and builder inside specview.py, inline CSS and two test files; no new component, route, store or dependency.",
      "basis": "sha256:d9b1d94dc0de186963419472f88a019b059bbc0029ecd9922c1f6567db7f09fc"
    }
  ],
  "assessment": {
    "ambiguity": [],
    "missing": [],
    "contradictions": [],
    "unsupported_assumptions": [],
    "untestable": []
  },
  "findings": []
}
```
<!-- eil:end assessment -->
