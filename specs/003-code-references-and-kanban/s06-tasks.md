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

# Tasks: Cross-reference codes and tasks kanban view

**Input**: Design documents from `/specs/003-code-references-and-kanban/`

**Prerequisites**: plan.md (required), spec.md (the AI Specification), contracts/http.md, quickstart.md

**Tests**: Test tasks are included because the AI Specification's Testing Requirements ask for them.

**Organization**: Tasks are grouped by user story: US1 is following a newly introduced code (UC-001), US2 is the kanban view (UC-002), and US3 is the automatic refresh of open pages (REQ-012).

## Format: `[ID] [P?] [Story] Description (traces: AIS-###)`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)
- Include exact file paths in descriptions
- End every task with `(traces: AIS-###)`

## Phase 1: Setup (Shared Infrastructure)

- [X] T001 Add a fixture story `tests/fixtures/project/specs/010-discovery/` whose documents introduce the prefix `VO` in a heading, `QZ` in a bullet and `TB` in a qualifying table row, reference them from another document, and hold a back-reference table that introduces nothing, plus a second story `011-other/` that uses `VO-001` without defining it (traces: AIS-030, AIS-031, AIS-005)
- [X] T002 [P] Add a fixture story `tests/fixtures/project/specs/012-board/` with a `tasks.md` covering every marker (`[ ]`, `[X]`, `[~]`, `[!]`), the `(in progress)` and `(blocked)` tags, a task with both, tasks under two `## ` phases, two `[USn]` tags, a task before any phase heading, a task with no `[USn]` tag and a malformed line, and stories `013-empty/` with an empty `tasks.md` and `014-none/` with none (traces: AIS-032, AIS-009, AIS-014, AIS-027, AIS-037, AIS-038)

## Phase 2: Foundational (Blocking Prerequisites)

- [X] T003 Add a story-page menu listing the story's documents and the kanban board to the page template in `specview.py`, shown on every page of a story, with the board link pointing at `/specs/<story>/kanban` (traces: AIS-028, AIS-008, AIS-021)

## Phase 3: User Story 1 - Follow a newly introduced code (Priority: P1) 🎯 MVP

**Goal**: A code introduced in a story's headings, bullets or qualifying table rows is marked wherever it is referenced in that story.

**Independent Test**: Quickstart scenarios 1 to 3.

- [X] T004 [P] [US1] Write unit tests for prefix discovery from a heading, a bullet and a table row, and for a back-reference table that introduces nothing, in `tests/unit/test_discovery.py` (traces: AIS-030, AIS-001, AIS-002, AIS-013)
- [X] T005 [P] [US1] Write integration tests in `tests/integration/test_discovered_references.py`: a discovered code is marked with the hover and click behaviour, the same code in another story is not marked, the fixed list still works, and an undefined or ambiguous discovered code shows the error (traces: AIS-031, AIS-003, AIS-004, AIS-005)
- [X] T006 [US1] Add the first discovery pass to `StoryIndex` in `specview.py`: scan every `.md` file of the story at every depth for a code that starts a heading or a bullet, or is the only content of the first column of a table row whose next column holds a description, and collect the prefixes, rebuilt on each request and never stored (traces: AIS-015, AIS-022, AIS-001, AIS-002, AIS-041, ART-006)
- [X] T007 [US1] Make the definition rules in `find_definitions` use the fixed prefix list plus the story's discovered prefixes, keeping the fixed list and its error behaviour unchanged (traces: AIS-022, AIS-004, AIS-005, ART-005)
- [X] T008 [US1] Make the reference marker mark every code of a discovered form outside inline code and code blocks, with the existing hover, click and error behaviour (traces: AIS-003, AIS-021, ART-005, ART-006)

## Phase 4: User Story 2 - Check build progress (Priority: P2)

**Goal**: A story's `tasks.md` is shown as a read-only kanban board.

**Independent Test**: Quickstart scenarios 4 to 8.

- [X] T009 [P] [US2] Write unit tests for the kanban parser (each mark and tag, blocked winning over in progress, phases, `[USn]` labels, malformed lines ignored) and for grouping by phase and by user story with the Unallocated group, in `tests/unit/test_kanban.py` (traces: AIS-030, AIS-009, AIS-014, AIS-027, AIS-038)
- [X] T010 [P] [US2] Write end to end tests in `tests/integration/test_kanban_route.py`: the board for a story with tasks, `?group=story`, an unknown group value, an empty `tasks.md`, no `tasks.md`, `tasks.md` unchanged afterwards, and a wrong `Host` header or path outside `specs/` refused (traces: AIS-032, AIS-034, AIS-010, AIS-011, AIS-026)
- [X] T011 [US2] Implement the kanban parser in `specview.py` as a dedicated line parser separate from the Markdown renderer: a `## ` heading starts a phase, a `- [mark] T### …` line is a card with task ID, `[USn]` story label, description, phase and column, derived and never written back (traces: AIS-017, AIS-029, AIS-009, AIS-014, AIS-024, ART-005)
- [X] T012 [US2] Implement the board cache in `specview.py`: keep each story's parsed cards in memory with the file's modified time and parse again only when that time changes (traces: AIS-018, AIS-019, ART-005)
- [X] T013 [US2] Implement the kanban page in `specview.py`: four columns of cards grouped by phase or by user story, the Unallocated group, HTML-escaped descriptions and labels, and the no-tasks message for a missing, empty or unreadable `tasks.md` (traces: AIS-016, AIS-007, AIS-011, AIS-027, AIS-036, AIS-037, ART-005, ART-007)
- [X] T014 [US2] Route `GET /specs/<story>/kanban[?group=phase|story]` in the request handler of `specview.py` behind the existing `Host` check and path guard, with phase as the fallback for any other group value and no write to the project (traces: AIS-023, AIS-026, AIS-034, AIS-035, AIS-006, AIS-040, ART-007)

## Phase 5: User Story 3 - Open pages refresh themselves (Priority: P3)

**Goal**: A document page or the kanban page shows the new content within about 10 seconds of its file changing, keeping scroll position and grouping.

**Independent Test**: Quickstart scenarios 9 to 12.

- [X] T015 [P] [US3] Write refresh tests in `tests/integration/test_refresh.py`: the stamp route returns the modified time, returns null for an unreadable file, and refuses a path outside `specs/` or a wrong `Host`; the served pages carry the refresher with a 10-second interval (traces: AIS-033, AIS-025, AIS-034, AIS-039, AIS-043)
- [X] T016 [US3] Route `GET /api/stamp?path=<path under specs/>` in `specview.py` returning `{"stamp": <modified time or null>}` through the same `Host` check and path guard (traces: AIS-025, AIS-023, AIS-034, AIS-039, ART-007)
- [X] T017 [US3] Add the page refresher script to every document page and the kanban page in `specview.py`: every 10 seconds fetch the stamp of the shown file, reload when it differs from the stamp the page loaded with, restore the document's scroll position, keep the kanban grouping, and keep the current content when the stamp is null (traces: AIS-012, AIS-018, AIS-043, AIS-047, ART-008)

## Phase 6: Polish & Cross-Cutting Concerns

- [X] T018 [P] Describe the kanban view, the story menu and the automatic refresh in `README.md` (traces: AIS-044)
- [X] T019 Run `python3 -m unittest discover -s tests` and the quickstart validation scenarios in `specs/003-code-references-and-kanban/quickstart.md` (traces: AIS-042, AIS-033)

## Dependencies & Execution Order

- Setup (T001, T002) first; T003 before the user stories.
- US1 (T004 to T008) and US2 (T009 to T014) are independent of each other. US3 (T015 to T017) needs the kanban page (T013) and the document pages.
- Within a story, tests come first and fail before the implementation, then parser or index, then page, then route.
- Polish last.

## Parallel Examples

- T001 and T002 together; T004 and T005 together; T009 and T010 together.
- US1 and US2 can proceed in parallel.

## Implementation Strategy

- MVP is US1, the discovery of codes. Then US2, the kanban board, then US3, the automatic refresh. All changes go into the single `specview.py`, so tasks that edit it run one after another.

## Not applicable

<!-- Sections removed from this document, each with its reason. -->

## Challenges

<!-- Recorded by `eil challenge`. -->

## Overrides

<!-- Recorded by `eil override`, each naming who, what and why. -->

## Change Log

<!-- eil:begin changelog -->
<!-- eil:end changelog -->

## Record

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
        "at": "2026-10-17T02:57:40Z",
        "list": "RVW-012",
        "reply": "yes"
      }
    },
    "#2cf5717e5d14": {
      "hash": "sha256:2cf5717e5d14288202df5613edf212e42618ba7e9f8bd855a74bb75cd8230860",
      "class": "inferred",
      "reviewed": {
        "by": "Lee Sinclair",
        "at": "2026-10-17T02:57:40Z",
        "list": "RVW-012",
        "reply": "yes"
      }
    },
    "Tasks: Cross-reference codes and tasks kanban view#d422cb72ef55": {
      "hash": "sha256:d422cb72ef55b3510ec1373fa3d82adc305ee67931b12f4f62ab49597a49b0c0",
      "class": "inferred",
      "reviewed": {
        "by": "Lee Sinclair",
        "at": "2026-10-17T02:57:40Z",
        "list": "RVW-012",
        "reply": "yes"
      }
    },
    "Tasks: Cross-reference codes and tasks kanban view#2871d140bc6e": {
      "hash": "sha256:2871d140bc6efb8e4f6e9c43318f7f4be9c267eb3db23a8e0484aad21ea339a6",
      "class": "inferred",
      "reviewed": {
        "by": "Lee Sinclair",
        "at": "2026-10-17T02:57:40Z",
        "list": "RVW-012",
        "reply": "yes"
      }
    },
    "Tasks: Cross-reference codes and tasks kanban view#3f49598a1878": {
      "hash": "sha256:3f49598a18784f6214ea964393e308880881fffebde92fcbd9b1018e09648063",
      "class": "inferred",
      "reviewed": {
        "by": "Lee Sinclair",
        "at": "2026-10-17T02:57:40Z",
        "list": "RVW-012",
        "reply": "yes"
      }
    },
    "Tasks: Cross-reference codes and tasks kanban view#535bf6399d7f": {
      "hash": "sha256:535bf6399d7ff08cd7d968e671d64f5367e22e63855bd7894d6b8bfaeff9a531",
      "class": "inferred",
      "reviewed": {
        "by": "Lee Sinclair",
        "at": "2026-10-17T02:57:40Z",
        "list": "RVW-012",
        "reply": "yes"
      }
    },
    "§Format: `[ID] [P?] [Story] Description `": {
      "hash": "sha256:78ecff41c1b9dbf4c7a3caffaf8d3df65f3a498a6db05a25bb4b8e93ae5f0f99",
      "class": "inferred",
      "reviewed": {
        "by": "Lee Sinclair",
        "at": "2026-10-17T02:57:40Z",
        "list": "RVW-012",
        "reply": "yes"
      }
    },
    "T001": {
      "hash": "sha256:8a3b3c76d783239adc015d85a398e95cfc34f6ccb70fa6e708bb6f41dd8bb729",
      "class": "restated",
      "cites": {
        "AIS-030": "sha256:885fdd8c923445091f587b09f7d8d7116e67fb916bfce8cb59811d4bc6e5e2f0",
        "AIS-031": "sha256:85752c68b1544f6898725927e601b2ed8496f9739b46c7dbac0c2d2d21acf62d",
        "AIS-005": "sha256:7a396a20f425e8c960f3a5029e88f8a3666ab5a0606c3e66a44d91b6ee96a275"
      },
      "completed_against": {
        "AIS-005": "sha256:7a396a20f425e8c960f3a5029e88f8a3666ab5a0606c3e66a44d91b6ee96a275",
        "AIS-030": "sha256:885fdd8c923445091f587b09f7d8d7116e67fb916bfce8cb59811d4bc6e5e2f0",
        "AIS-031": "sha256:85752c68b1544f6898725927e601b2ed8496f9739b46c7dbac0c2d2d21acf62d",
        "FR-001": "sha256:383f9296ff6a52d4e4c18607d174c816a95c9866b401c32d2b1194eb13a9b02c",
        "FR-002": "sha256:ed7dcf7ed5c6ad99f53a01c0ec96df80de21351bd839845b0ed6f1eef2a95ac7",
        "FR-003": "sha256:6f18dad4de22e5bf0feddcabd830ff23d873cb8dbf764edb96567d43b43cd668",
        "FR-004": "sha256:2ae3eb4329aaec539cf2ad43395016234b0a1d74b69470992d5519897e9b382f",
        "FR-005": "sha256:4fd4014add1830d59d7445913099f5dd61577b4ec75fcd6902f24418f440d04d",
        "FR-007": "sha256:a1b8235dbe5caad9d3c19f5344e9e629dfe07c2ba8ee6f358a2296174454ae28",
        "FR-008": "sha256:b5f49e91e9db1d61276c75c1959d4e30f9d2a96b7a5354e4bf23c554d7e6fcab",
        "REQ-001": "sha256:61e559eef48ae3d2bcafefa82d6db74a8356d04d3b827a3821dddbb4bf197af2",
        "REQ-002": "sha256:9be8cbf31c66cda1de24eb6018e9793bc3124a9883583b70cee59847b13ca3a5",
        "REQ-004": "sha256:11ced25bc5b5a0f3bef0f22de7471d625296fc8ce169ef0d70a30c9f5ffdf44b",
        "REQ-005": "sha256:b7dfc78315bdbaf546f86f722dce88987080968d3808e250013a20df55372105",
        "REQ-006": "sha256:859e9801daa175a7b2b81fda318548d186d0568e0b2a1241b2ae4cdfae93648f",
        "REQ-008": "sha256:db8e8f7793ed484c0fa0960c264ff2a063be41609db925ee0e2e9e49d6cd4f45",
        "REQ-009": "sha256:2acb805067e30d87ac45c5f1d0d4a41128a107a4cef12c892e0cf612bda9d42c",
        "REQ-011": "sha256:7c69a45314c4e67bc3c8e0c9b0325ba25d0d554672948654cf5d1f0effef4ea1",
        "UC-001": "sha256:3e691638c6e12461844d68e2f386ebdc36afc48a479fee7bbc5ada6fafc54fb8"
      },
      "blocked_at_completion": false
    },
    "T002": {
      "hash": "sha256:1902adcf08ba0988c4e4336782f6064492a1cf4384f80eaffda31ded8861ba83",
      "class": "restated",
      "cites": {
        "AIS-032": "sha256:2852fd2521d685cd4d070c48f9ae2bf002eb0fe24ebb93edf45cd6ed71208b72",
        "AIS-009": "sha256:7b8dfc99da4e3d117d27a8744f5781f25be87c9abd49efa0999312363e73330f",
        "AIS-014": "sha256:0b9acb87fcb44ef42a60311b7cb1baffd2c46c7cfcab9ee4b0ae9622b68a1042",
        "AIS-027": "sha256:ea1fe8e036f535a3ed85f1391bf58e178d52867f4213716914eeb0162d861a54",
        "AIS-037": "sha256:a46faccd82a3a075675c2200a988e90ab8cde988b2f6cfbd9c173751e22c8ef3",
        "AIS-038": "sha256:322e03ab76e9bd715ddd15c001c0943825ccb079680669c1562aae38e982a429"
      },
      "completed_against": {
        "AIS-009": "sha256:7b8dfc99da4e3d117d27a8744f5781f25be87c9abd49efa0999312363e73330f",
        "AIS-014": "sha256:0b9acb87fcb44ef42a60311b7cb1baffd2c46c7cfcab9ee4b0ae9622b68a1042",
        "AIS-027": "sha256:ea1fe8e036f535a3ed85f1391bf58e178d52867f4213716914eeb0162d861a54",
        "AIS-032": "sha256:2852fd2521d685cd4d070c48f9ae2bf002eb0fe24ebb93edf45cd6ed71208b72",
        "AIS-037": "sha256:a46faccd82a3a075675c2200a988e90ab8cde988b2f6cfbd9c173751e22c8ef3",
        "AIS-038": "sha256:322e03ab76e9bd715ddd15c001c0943825ccb079680669c1562aae38e982a429",
        "DEC-002": "sha256:450de9b1737c8d785caca57c0b3cc522aed8898e9dcea2c8c953f697e1d03aa3",
        "DEC-003": "sha256:a9f99d3c520b3fe486f6f8103e542d28fb3a7c31a82c82665be1893726556d9d",
        "FR-006": "sha256:81abe569717adc55e2ea4a635ebadcc9268825b269a820b6259f8c2d3580709a",
        "FR-007": "sha256:a1b8235dbe5caad9d3c19f5344e9e629dfe07c2ba8ee6f358a2296174454ae28",
        "FR-008": "sha256:b5f49e91e9db1d61276c75c1959d4e30f9d2a96b7a5354e4bf23c554d7e6fcab",
        "FR-009": "sha256:2f4e357e7c45afc0535ca51280ef4a6cb662efea2c188887a76a8e0bbf79f79c",
        "FR-010": "sha256:f297709714ffd46f93f7abf23c9ebea1294efd150bd16b280ccbcedbc0bffd3c",
        "FR-011": "sha256:faf836f7ec7f293517c93343e6f61f8d0ff39875f6a9c4fcf4e570f136a028ec",
        "NFR-001": "sha256:3131ccae52047de8b10a4105b89cdfc6b05b5b23f14b57040ff773ac24431f08",
        "REQ-003": "sha256:3755f308fed60ce65095a51a1ac6c761e9b9fe1a247dd166b82dfb773272081e",
        "REQ-004": "sha256:11ced25bc5b5a0f3bef0f22de7471d625296fc8ce169ef0d70a30c9f5ffdf44b",
        "REQ-007": "sha256:f510a28f216be7dedb6d892aeaf8f92e1f99cbacc3300e721fbbfd7d5690abe6",
        "REQ-008": "sha256:db8e8f7793ed484c0fa0960c264ff2a063be41609db925ee0e2e9e49d6cd4f45",
        "REQ-010": "sha256:6c90a9a0ceeebd560ba40c37f900ba9247153a25e17cbab86fc3a1b45e0029c9",
        "REQ-011": "sha256:7c69a45314c4e67bc3c8e0c9b0325ba25d0d554672948654cf5d1f0effef4ea1",
        "REQ-012": "sha256:fcb33e719611733ed088a72bb7e1fccbcfd5843c6ed9a4246d3895a161a7e414",
        "UC-002": "sha256:d058ae80de91413ede200a910ed88df18487cbe335ac361823fff73bd99322be"
      },
      "blocked_at_completion": false
    },
    "T003": {
      "hash": "sha256:67a23354a0090a8b4abdb29b91ef739de7459eb4a09343b7908f2b034305b87b",
      "class": "restated",
      "cites": {
        "AIS-028": "sha256:042d43d67bcce8ee2226c2d661a302a05e3a8af1610fd8fd57511e004960ec75",
        "AIS-008": "sha256:e977b028f05ce0aa62d9341bce97d9ccaaf1b3552c1e4b013b25a558a52cdccc",
        "AIS-021": "sha256:9f239571158cf52fe9584c85b73953cfad90dd8e8b5b465d113984417fc1c77d"
      },
      "completed_against": {
        "AIS-008": "sha256:e977b028f05ce0aa62d9341bce97d9ccaaf1b3552c1e4b013b25a558a52cdccc",
        "AIS-021": "sha256:9f239571158cf52fe9584c85b73953cfad90dd8e8b5b465d113984417fc1c77d",
        "AIS-028": "sha256:042d43d67bcce8ee2226c2d661a302a05e3a8af1610fd8fd57511e004960ec75",
        "ART-005": "sha256:ddc99a0e777eeefe57010caa1355dd2acd061ede1711db2f440d2a061dbb0e06",
        "ART-008": "sha256:952782963b9d2dcd8083c0acbf50df86010fad0435552f9058625f9c8d4feb51",
        "DEC-001": "sha256:13a2732b598fcb0a7a620f1cc017318a750024235d9ca1453803f7f35b0ddedd",
        "DEC-003": "sha256:a9f99d3c520b3fe486f6f8103e542d28fb3a7c31a82c82665be1893726556d9d",
        "DEC-004": "sha256:942ab4072dd367c7cc88758bbd6df350e7ce92e76ea93688853324c207fbf0a3",
        "FR-001": "sha256:383f9296ff6a52d4e4c18607d174c816a95c9866b401c32d2b1194eb13a9b02c",
        "FR-002": "sha256:ed7dcf7ed5c6ad99f53a01c0ec96df80de21351bd839845b0ed6f1eef2a95ac7",
        "FR-003": "sha256:6f18dad4de22e5bf0feddcabd830ff23d873cb8dbf764edb96567d43b43cd668",
        "FR-004": "sha256:2ae3eb4329aaec539cf2ad43395016234b0a1d74b69470992d5519897e9b382f",
        "FR-005": "sha256:4fd4014add1830d59d7445913099f5dd61577b4ec75fcd6902f24418f440d04d",
        "FR-006": "sha256:81abe569717adc55e2ea4a635ebadcc9268825b269a820b6259f8c2d3580709a",
        "FR-007": "sha256:a1b8235dbe5caad9d3c19f5344e9e629dfe07c2ba8ee6f358a2296174454ae28",
        "FR-008": "sha256:b5f49e91e9db1d61276c75c1959d4e30f9d2a96b7a5354e4bf23c554d7e6fcab",
        "FR-010": "sha256:f297709714ffd46f93f7abf23c9ebea1294efd150bd16b280ccbcedbc0bffd3c",
        "FR-011": "sha256:faf836f7ec7f293517c93343e6f61f8d0ff39875f6a9c4fcf4e570f136a028ec",
        "FR-012": "sha256:c45b0cea6084477d35f71746737ceb52e6c4bb25a3d53d5867516cbcb168058b",
        "NFR-001": "sha256:3131ccae52047de8b10a4105b89cdfc6b05b5b23f14b57040ff773ac24431f08",
        "REQ-001": "sha256:61e559eef48ae3d2bcafefa82d6db74a8356d04d3b827a3821dddbb4bf197af2",
        "REQ-002": "sha256:9be8cbf31c66cda1de24eb6018e9793bc3124a9883583b70cee59847b13ca3a5",
        "REQ-003": "sha256:3755f308fed60ce65095a51a1ac6c761e9b9fe1a247dd166b82dfb773272081e",
        "REQ-004": "sha256:11ced25bc5b5a0f3bef0f22de7471d625296fc8ce169ef0d70a30c9f5ffdf44b",
        "REQ-005": "sha256:b7dfc78315bdbaf546f86f722dce88987080968d3808e250013a20df55372105",
        "REQ-006": "sha256:859e9801daa175a7b2b81fda318548d186d0568e0b2a1241b2ae4cdfae93648f",
        "REQ-008": "sha256:db8e8f7793ed484c0fa0960c264ff2a063be41609db925ee0e2e9e49d6cd4f45",
        "REQ-009": "sha256:2acb805067e30d87ac45c5f1d0d4a41128a107a4cef12c892e0cf612bda9d42c",
        "REQ-010": "sha256:6c90a9a0ceeebd560ba40c37f900ba9247153a25e17cbab86fc3a1b45e0029c9",
        "REQ-011": "sha256:7c69a45314c4e67bc3c8e0c9b0325ba25d0d554672948654cf5d1f0effef4ea1",
        "REQ-012": "sha256:fcb33e719611733ed088a72bb7e1fccbcfd5843c6ed9a4246d3895a161a7e414",
        "UC-001": "sha256:3e691638c6e12461844d68e2f386ebdc36afc48a479fee7bbc5ada6fafc54fb8",
        "UC-002": "sha256:d058ae80de91413ede200a910ed88df18487cbe335ac361823fff73bd99322be"
      },
      "blocked_at_completion": false
    },
    "Phase 3: User Story 1 - Follow a newly introduced code (Priority: P1) 🎯 MVP#edcbc2bbee99": {
      "hash": "sha256:edcbc2bbee9979786d6358d2d2b513c3a716139bbe62c02c2ce271786d920134",
      "class": "inferred",
      "reviewed": {
        "by": "Lee Sinclair",
        "at": "2026-10-17T02:57:40Z",
        "list": "RVW-012",
        "reply": "yes"
      }
    },
    "Phase 3: User Story 1 - Follow a newly introduced code (Priority: P1) 🎯 MVP#2937c20b2640": {
      "hash": "sha256:2937c20b26407c16dd9c662056950bb33464a6b149aa52f65c787625a13b733c",
      "class": "inferred",
      "reviewed": {
        "by": "Lee Sinclair",
        "at": "2026-10-17T02:57:40Z",
        "list": "RVW-012",
        "reply": "yes"
      }
    },
    "T004": {
      "hash": "sha256:0ce69e72d52f84e1c14be4d32f93e7826d8eb1bc0c9ca33688ce0e4b22c0f82c",
      "class": "restated",
      "cites": {
        "AIS-030": "sha256:885fdd8c923445091f587b09f7d8d7116e67fb916bfce8cb59811d4bc6e5e2f0",
        "AIS-001": "sha256:e945959400e16b4ff3de439ea4a5f4f3616474cf08d507206d0142e277dd09b5",
        "AIS-002": "sha256:5019706629fce1459cbfc5c6ca17e3fb6a1a567e30c87173bc3fc90a8502e294",
        "AIS-013": "sha256:4594c9e74124ed7d1a2533729f830a57064a729f58de54f665358730af534fae"
      },
      "completed_against": {
        "AIS-001": "sha256:e945959400e16b4ff3de439ea4a5f4f3616474cf08d507206d0142e277dd09b5",
        "AIS-002": "sha256:5019706629fce1459cbfc5c6ca17e3fb6a1a567e30c87173bc3fc90a8502e294",
        "AIS-013": "sha256:4594c9e74124ed7d1a2533729f830a57064a729f58de54f665358730af534fae",
        "AIS-030": "sha256:885fdd8c923445091f587b09f7d8d7116e67fb916bfce8cb59811d4bc6e5e2f0",
        "FR-001": "sha256:383f9296ff6a52d4e4c18607d174c816a95c9866b401c32d2b1194eb13a9b02c",
        "FR-002": "sha256:ed7dcf7ed5c6ad99f53a01c0ec96df80de21351bd839845b0ed6f1eef2a95ac7",
        "FR-007": "sha256:a1b8235dbe5caad9d3c19f5344e9e629dfe07c2ba8ee6f358a2296174454ae28",
        "FR-008": "sha256:b5f49e91e9db1d61276c75c1959d4e30f9d2a96b7a5354e4bf23c554d7e6fcab",
        "REQ-001": "sha256:61e559eef48ae3d2bcafefa82d6db74a8356d04d3b827a3821dddbb4bf197af2",
        "REQ-002": "sha256:9be8cbf31c66cda1de24eb6018e9793bc3124a9883583b70cee59847b13ca3a5",
        "REQ-004": "sha256:11ced25bc5b5a0f3bef0f22de7471d625296fc8ce169ef0d70a30c9f5ffdf44b",
        "REQ-006": "sha256:859e9801daa175a7b2b81fda318548d186d0568e0b2a1241b2ae4cdfae93648f",
        "REQ-008": "sha256:db8e8f7793ed484c0fa0960c264ff2a063be41609db925ee0e2e9e49d6cd4f45",
        "REQ-009": "sha256:2acb805067e30d87ac45c5f1d0d4a41128a107a4cef12c892e0cf612bda9d42c",
        "REQ-011": "sha256:7c69a45314c4e67bc3c8e0c9b0325ba25d0d554672948654cf5d1f0effef4ea1"
      },
      "blocked_at_completion": false
    },
    "T005": {
      "hash": "sha256:67523a997f731bfb011c26ad94b41bbc68c7282c90d2508011c716c7c0c6e8e3",
      "class": "restated",
      "cites": {
        "AIS-031": "sha256:85752c68b1544f6898725927e601b2ed8496f9739b46c7dbac0c2d2d21acf62d",
        "AIS-003": "sha256:9fa5829481906405ae54b0536f5600a0688ca69055883f40c7eaebfeb9c65983",
        "AIS-004": "sha256:f799df77d1abb5ac97abbf3b39ece3f9342216a1185f4505b49fa77179278cd3",
        "AIS-005": "sha256:7a396a20f425e8c960f3a5029e88f8a3666ab5a0606c3e66a44d91b6ee96a275"
      },
      "completed_against": {
        "AIS-003": "sha256:9fa5829481906405ae54b0536f5600a0688ca69055883f40c7eaebfeb9c65983",
        "AIS-004": "sha256:f799df77d1abb5ac97abbf3b39ece3f9342216a1185f4505b49fa77179278cd3",
        "AIS-005": "sha256:7a396a20f425e8c960f3a5029e88f8a3666ab5a0606c3e66a44d91b6ee96a275",
        "AIS-031": "sha256:85752c68b1544f6898725927e601b2ed8496f9739b46c7dbac0c2d2d21acf62d",
        "FR-003": "sha256:6f18dad4de22e5bf0feddcabd830ff23d873cb8dbf764edb96567d43b43cd668",
        "FR-004": "sha256:2ae3eb4329aaec539cf2ad43395016234b0a1d74b69470992d5519897e9b382f",
        "FR-005": "sha256:4fd4014add1830d59d7445913099f5dd61577b4ec75fcd6902f24418f440d04d",
        "REQ-001": "sha256:61e559eef48ae3d2bcafefa82d6db74a8356d04d3b827a3821dddbb4bf197af2",
        "REQ-005": "sha256:b7dfc78315bdbaf546f86f722dce88987080968d3808e250013a20df55372105",
        "REQ-009": "sha256:2acb805067e30d87ac45c5f1d0d4a41128a107a4cef12c892e0cf612bda9d42c",
        "UC-001": "sha256:3e691638c6e12461844d68e2f386ebdc36afc48a479fee7bbc5ada6fafc54fb8"
      },
      "blocked_at_completion": false
    },
    "T006": {
      "hash": "sha256:c5e8ddcde77e8820c86a330b97237a87a2babb3e1aa332d9a9769c046e0a5289",
      "class": "restated",
      "cites": {
        "AIS-015": "sha256:3cd8a63029947a310a5e2360eafe83a9a604cca723a2751a4e43b6766cf43b84",
        "AIS-022": "sha256:ab5ce28ac559e901fe5c95fe6fd6ae950c73e001151eb72863745800f745e7f6",
        "AIS-001": "sha256:e945959400e16b4ff3de439ea4a5f4f3616474cf08d507206d0142e277dd09b5",
        "AIS-002": "sha256:5019706629fce1459cbfc5c6ca17e3fb6a1a567e30c87173bc3fc90a8502e294",
        "AIS-041": "sha256:d4c8c76d709d245432beb2646da2f417e393dc69f46f5fc5298886f8021f6935",
        "ART-006": "sha256:295316b3f91e78fc07ccec63c7dc4ff5d3e4e70575de34d2bb3fc5bb198878b5"
      },
      "completed_against": {
        "AIS-001": "sha256:e945959400e16b4ff3de439ea4a5f4f3616474cf08d507206d0142e277dd09b5",
        "AIS-002": "sha256:5019706629fce1459cbfc5c6ca17e3fb6a1a567e30c87173bc3fc90a8502e294",
        "AIS-015": "sha256:3cd8a63029947a310a5e2360eafe83a9a604cca723a2751a4e43b6766cf43b84",
        "AIS-022": "sha256:ab5ce28ac559e901fe5c95fe6fd6ae950c73e001151eb72863745800f745e7f6",
        "AIS-041": "sha256:d4c8c76d709d245432beb2646da2f417e393dc69f46f5fc5298886f8021f6935",
        "ART-006": "sha256:295316b3f91e78fc07ccec63c7dc4ff5d3e4e70575de34d2bb3fc5bb198878b5",
        "DEC-001": "sha256:13a2732b598fcb0a7a620f1cc017318a750024235d9ca1453803f7f35b0ddedd",
        "FR-001": "sha256:383f9296ff6a52d4e4c18607d174c816a95c9866b401c32d2b1194eb13a9b02c",
        "FR-002": "sha256:ed7dcf7ed5c6ad99f53a01c0ec96df80de21351bd839845b0ed6f1eef2a95ac7",
        "FR-003": "sha256:6f18dad4de22e5bf0feddcabd830ff23d873cb8dbf764edb96567d43b43cd668",
        "FR-004": "sha256:2ae3eb4329aaec539cf2ad43395016234b0a1d74b69470992d5519897e9b382f",
        "FR-005": "sha256:4fd4014add1830d59d7445913099f5dd61577b4ec75fcd6902f24418f440d04d",
        "NFR-001": "sha256:3131ccae52047de8b10a4105b89cdfc6b05b5b23f14b57040ff773ac24431f08",
        "REQ-001": "sha256:61e559eef48ae3d2bcafefa82d6db74a8356d04d3b827a3821dddbb4bf197af2",
        "REQ-002": "sha256:9be8cbf31c66cda1de24eb6018e9793bc3124a9883583b70cee59847b13ca3a5",
        "REQ-003": "sha256:3755f308fed60ce65095a51a1ac6c761e9b9fe1a247dd166b82dfb773272081e",
        "REQ-005": "sha256:b7dfc78315bdbaf546f86f722dce88987080968d3808e250013a20df55372105",
        "REQ-006": "sha256:859e9801daa175a7b2b81fda318548d186d0568e0b2a1241b2ae4cdfae93648f",
        "REQ-009": "sha256:2acb805067e30d87ac45c5f1d0d4a41128a107a4cef12c892e0cf612bda9d42c",
        "REQ-012": "sha256:fcb33e719611733ed088a72bb7e1fccbcfd5843c6ed9a4246d3895a161a7e414",
        "UC-001": "sha256:3e691638c6e12461844d68e2f386ebdc36afc48a479fee7bbc5ada6fafc54fb8"
      },
      "blocked_at_completion": false
    },
    "T007": {
      "hash": "sha256:6347d600404f1a73881b055a111d77909b0a82c3f84ff2fc81eb5339666d4c5c",
      "class": "restated",
      "cites": {
        "AIS-022": "sha256:ab5ce28ac559e901fe5c95fe6fd6ae950c73e001151eb72863745800f745e7f6",
        "AIS-004": "sha256:f799df77d1abb5ac97abbf3b39ece3f9342216a1185f4505b49fa77179278cd3",
        "AIS-005": "sha256:7a396a20f425e8c960f3a5029e88f8a3666ab5a0606c3e66a44d91b6ee96a275",
        "ART-005": "sha256:ddc99a0e777eeefe57010caa1355dd2acd061ede1711db2f440d2a061dbb0e06"
      },
      "completed_against": {
        "AIS-004": "sha256:f799df77d1abb5ac97abbf3b39ece3f9342216a1185f4505b49fa77179278cd3",
        "AIS-005": "sha256:7a396a20f425e8c960f3a5029e88f8a3666ab5a0606c3e66a44d91b6ee96a275",
        "AIS-022": "sha256:ab5ce28ac559e901fe5c95fe6fd6ae950c73e001151eb72863745800f745e7f6",
        "ART-005": "sha256:ddc99a0e777eeefe57010caa1355dd2acd061ede1711db2f440d2a061dbb0e06",
        "DEC-001": "sha256:13a2732b598fcb0a7a620f1cc017318a750024235d9ca1453803f7f35b0ddedd",
        "DEC-003": "sha256:a9f99d3c520b3fe486f6f8103e542d28fb3a7c31a82c82665be1893726556d9d",
        "FR-001": "sha256:383f9296ff6a52d4e4c18607d174c816a95c9866b401c32d2b1194eb13a9b02c",
        "FR-002": "sha256:ed7dcf7ed5c6ad99f53a01c0ec96df80de21351bd839845b0ed6f1eef2a95ac7",
        "FR-003": "sha256:6f18dad4de22e5bf0feddcabd830ff23d873cb8dbf764edb96567d43b43cd668",
        "FR-004": "sha256:2ae3eb4329aaec539cf2ad43395016234b0a1d74b69470992d5519897e9b382f",
        "FR-005": "sha256:4fd4014add1830d59d7445913099f5dd61577b4ec75fcd6902f24418f440d04d",
        "FR-006": "sha256:81abe569717adc55e2ea4a635ebadcc9268825b269a820b6259f8c2d3580709a",
        "FR-007": "sha256:a1b8235dbe5caad9d3c19f5344e9e629dfe07c2ba8ee6f358a2296174454ae28",
        "FR-008": "sha256:b5f49e91e9db1d61276c75c1959d4e30f9d2a96b7a5354e4bf23c554d7e6fcab",
        "FR-010": "sha256:f297709714ffd46f93f7abf23c9ebea1294efd150bd16b280ccbcedbc0bffd3c",
        "NFR-001": "sha256:3131ccae52047de8b10a4105b89cdfc6b05b5b23f14b57040ff773ac24431f08",
        "REQ-001": "sha256:61e559eef48ae3d2bcafefa82d6db74a8356d04d3b827a3821dddbb4bf197af2",
        "REQ-002": "sha256:9be8cbf31c66cda1de24eb6018e9793bc3124a9883583b70cee59847b13ca3a5",
        "REQ-003": "sha256:3755f308fed60ce65095a51a1ac6c761e9b9fe1a247dd166b82dfb773272081e",
        "REQ-004": "sha256:11ced25bc5b5a0f3bef0f22de7471d625296fc8ce169ef0d70a30c9f5ffdf44b",
        "REQ-005": "sha256:b7dfc78315bdbaf546f86f722dce88987080968d3808e250013a20df55372105",
        "REQ-006": "sha256:859e9801daa175a7b2b81fda318548d186d0568e0b2a1241b2ae4cdfae93648f",
        "REQ-008": "sha256:db8e8f7793ed484c0fa0960c264ff2a063be41609db925ee0e2e9e49d6cd4f45",
        "REQ-009": "sha256:2acb805067e30d87ac45c5f1d0d4a41128a107a4cef12c892e0cf612bda9d42c",
        "REQ-010": "sha256:6c90a9a0ceeebd560ba40c37f900ba9247153a25e17cbab86fc3a1b45e0029c9",
        "REQ-011": "sha256:7c69a45314c4e67bc3c8e0c9b0325ba25d0d554672948654cf5d1f0effef4ea1",
        "REQ-012": "sha256:fcb33e719611733ed088a72bb7e1fccbcfd5843c6ed9a4246d3895a161a7e414",
        "UC-001": "sha256:3e691638c6e12461844d68e2f386ebdc36afc48a479fee7bbc5ada6fafc54fb8",
        "UC-002": "sha256:d058ae80de91413ede200a910ed88df18487cbe335ac361823fff73bd99322be"
      },
      "blocked_at_completion": false
    },
    "T008": {
      "hash": "sha256:767ba3115e65e26cd14286b9881b5c20f9d254df974d7600d76c3896797ec11f",
      "class": "restated",
      "cites": {
        "AIS-003": "sha256:9fa5829481906405ae54b0536f5600a0688ca69055883f40c7eaebfeb9c65983",
        "AIS-021": "sha256:9f239571158cf52fe9584c85b73953cfad90dd8e8b5b465d113984417fc1c77d",
        "ART-005": "sha256:ddc99a0e777eeefe57010caa1355dd2acd061ede1711db2f440d2a061dbb0e06",
        "ART-006": "sha256:295316b3f91e78fc07ccec63c7dc4ff5d3e4e70575de34d2bb3fc5bb198878b5"
      },
      "completed_against": {
        "AIS-003": "sha256:9fa5829481906405ae54b0536f5600a0688ca69055883f40c7eaebfeb9c65983",
        "AIS-021": "sha256:9f239571158cf52fe9584c85b73953cfad90dd8e8b5b465d113984417fc1c77d",
        "ART-005": "sha256:ddc99a0e777eeefe57010caa1355dd2acd061ede1711db2f440d2a061dbb0e06",
        "ART-006": "sha256:295316b3f91e78fc07ccec63c7dc4ff5d3e4e70575de34d2bb3fc5bb198878b5",
        "ART-008": "sha256:952782963b9d2dcd8083c0acbf50df86010fad0435552f9058625f9c8d4feb51",
        "DEC-001": "sha256:13a2732b598fcb0a7a620f1cc017318a750024235d9ca1453803f7f35b0ddedd",
        "DEC-003": "sha256:a9f99d3c520b3fe486f6f8103e542d28fb3a7c31a82c82665be1893726556d9d",
        "DEC-004": "sha256:942ab4072dd367c7cc88758bbd6df350e7ce92e76ea93688853324c207fbf0a3",
        "FR-001": "sha256:383f9296ff6a52d4e4c18607d174c816a95c9866b401c32d2b1194eb13a9b02c",
        "FR-002": "sha256:ed7dcf7ed5c6ad99f53a01c0ec96df80de21351bd839845b0ed6f1eef2a95ac7",
        "FR-003": "sha256:6f18dad4de22e5bf0feddcabd830ff23d873cb8dbf764edb96567d43b43cd668",
        "FR-004": "sha256:2ae3eb4329aaec539cf2ad43395016234b0a1d74b69470992d5519897e9b382f",
        "FR-005": "sha256:4fd4014add1830d59d7445913099f5dd61577b4ec75fcd6902f24418f440d04d",
        "FR-006": "sha256:81abe569717adc55e2ea4a635ebadcc9268825b269a820b6259f8c2d3580709a",
        "FR-007": "sha256:a1b8235dbe5caad9d3c19f5344e9e629dfe07c2ba8ee6f358a2296174454ae28",
        "FR-008": "sha256:b5f49e91e9db1d61276c75c1959d4e30f9d2a96b7a5354e4bf23c554d7e6fcab",
        "FR-010": "sha256:f297709714ffd46f93f7abf23c9ebea1294efd150bd16b280ccbcedbc0bffd3c",
        "FR-012": "sha256:c45b0cea6084477d35f71746737ceb52e6c4bb25a3d53d5867516cbcb168058b",
        "NFR-001": "sha256:3131ccae52047de8b10a4105b89cdfc6b05b5b23f14b57040ff773ac24431f08",
        "REQ-001": "sha256:61e559eef48ae3d2bcafefa82d6db74a8356d04d3b827a3821dddbb4bf197af2",
        "REQ-002": "sha256:9be8cbf31c66cda1de24eb6018e9793bc3124a9883583b70cee59847b13ca3a5",
        "REQ-003": "sha256:3755f308fed60ce65095a51a1ac6c761e9b9fe1a247dd166b82dfb773272081e",
        "REQ-004": "sha256:11ced25bc5b5a0f3bef0f22de7471d625296fc8ce169ef0d70a30c9f5ffdf44b",
        "REQ-005": "sha256:b7dfc78315bdbaf546f86f722dce88987080968d3808e250013a20df55372105",
        "REQ-006": "sha256:859e9801daa175a7b2b81fda318548d186d0568e0b2a1241b2ae4cdfae93648f",
        "REQ-008": "sha256:db8e8f7793ed484c0fa0960c264ff2a063be41609db925ee0e2e9e49d6cd4f45",
        "REQ-009": "sha256:2acb805067e30d87ac45c5f1d0d4a41128a107a4cef12c892e0cf612bda9d42c",
        "REQ-010": "sha256:6c90a9a0ceeebd560ba40c37f900ba9247153a25e17cbab86fc3a1b45e0029c9",
        "REQ-011": "sha256:7c69a45314c4e67bc3c8e0c9b0325ba25d0d554672948654cf5d1f0effef4ea1",
        "REQ-012": "sha256:fcb33e719611733ed088a72bb7e1fccbcfd5843c6ed9a4246d3895a161a7e414",
        "UC-001": "sha256:3e691638c6e12461844d68e2f386ebdc36afc48a479fee7bbc5ada6fafc54fb8",
        "UC-002": "sha256:d058ae80de91413ede200a910ed88df18487cbe335ac361823fff73bd99322be"
      },
      "blocked_at_completion": false
    },
    "Phase 4: User Story 2 - Check build progress (Priority: P2)#dcd20f110223": {
      "hash": "sha256:dcd20f110223dbcbd09549fe92f9fd3bfa211aa1ddd375083aa42eec31505295",
      "class": "inferred",
      "reviewed": {
        "by": "Lee Sinclair",
        "at": "2026-10-17T02:57:40Z",
        "list": "RVW-012",
        "reply": "yes"
      }
    },
    "Phase 4: User Story 2 - Check build progress (Priority: P2)#964816a5de51": {
      "hash": "sha256:964816a5de51853a401c6b812bd4ef2abe67ff411fcd939818054f765ca0b234",
      "class": "inferred",
      "reviewed": {
        "by": "Lee Sinclair",
        "at": "2026-10-17T02:57:40Z",
        "list": "RVW-012",
        "reply": "yes"
      }
    },
    "T009": {
      "hash": "sha256:0600d3ddf0c87823d3d0abdf5894418b43b1cf14c3f83e46ca303105f11efb16",
      "class": "restated",
      "cites": {
        "AIS-030": "sha256:885fdd8c923445091f587b09f7d8d7116e67fb916bfce8cb59811d4bc6e5e2f0",
        "AIS-009": "sha256:7b8dfc99da4e3d117d27a8744f5781f25be87c9abd49efa0999312363e73330f",
        "AIS-014": "sha256:0b9acb87fcb44ef42a60311b7cb1baffd2c46c7cfcab9ee4b0ae9622b68a1042",
        "AIS-027": "sha256:ea1fe8e036f535a3ed85f1391bf58e178d52867f4213716914eeb0162d861a54",
        "AIS-038": "sha256:322e03ab76e9bd715ddd15c001c0943825ccb079680669c1562aae38e982a429"
      },
      "completed_against": {
        "AIS-009": "sha256:7b8dfc99da4e3d117d27a8744f5781f25be87c9abd49efa0999312363e73330f",
        "AIS-014": "sha256:0b9acb87fcb44ef42a60311b7cb1baffd2c46c7cfcab9ee4b0ae9622b68a1042",
        "AIS-027": "sha256:ea1fe8e036f535a3ed85f1391bf58e178d52867f4213716914eeb0162d861a54",
        "AIS-030": "sha256:885fdd8c923445091f587b09f7d8d7116e67fb916bfce8cb59811d4bc6e5e2f0",
        "AIS-038": "sha256:322e03ab76e9bd715ddd15c001c0943825ccb079680669c1562aae38e982a429",
        "DEC-002": "sha256:450de9b1737c8d785caca57c0b3cc522aed8898e9dcea2c8c953f697e1d03aa3",
        "DEC-003": "sha256:a9f99d3c520b3fe486f6f8103e542d28fb3a7c31a82c82665be1893726556d9d",
        "FR-001": "sha256:383f9296ff6a52d4e4c18607d174c816a95c9866b401c32d2b1194eb13a9b02c",
        "FR-002": "sha256:ed7dcf7ed5c6ad99f53a01c0ec96df80de21351bd839845b0ed6f1eef2a95ac7",
        "FR-006": "sha256:81abe569717adc55e2ea4a635ebadcc9268825b269a820b6259f8c2d3580709a",
        "FR-007": "sha256:a1b8235dbe5caad9d3c19f5344e9e629dfe07c2ba8ee6f358a2296174454ae28",
        "FR-008": "sha256:b5f49e91e9db1d61276c75c1959d4e30f9d2a96b7a5354e4bf23c554d7e6fcab",
        "FR-009": "sha256:2f4e357e7c45afc0535ca51280ef4a6cb662efea2c188887a76a8e0bbf79f79c",
        "FR-010": "sha256:f297709714ffd46f93f7abf23c9ebea1294efd150bd16b280ccbcedbc0bffd3c",
        "FR-011": "sha256:faf836f7ec7f293517c93343e6f61f8d0ff39875f6a9c4fcf4e570f136a028ec",
        "NFR-001": "sha256:3131ccae52047de8b10a4105b89cdfc6b05b5b23f14b57040ff773ac24431f08",
        "REQ-001": "sha256:61e559eef48ae3d2bcafefa82d6db74a8356d04d3b827a3821dddbb4bf197af2",
        "REQ-002": "sha256:9be8cbf31c66cda1de24eb6018e9793bc3124a9883583b70cee59847b13ca3a5",
        "REQ-003": "sha256:3755f308fed60ce65095a51a1ac6c761e9b9fe1a247dd166b82dfb773272081e",
        "REQ-004": "sha256:11ced25bc5b5a0f3bef0f22de7471d625296fc8ce169ef0d70a30c9f5ffdf44b",
        "REQ-006": "sha256:859e9801daa175a7b2b81fda318548d186d0568e0b2a1241b2ae4cdfae93648f",
        "REQ-007": "sha256:f510a28f216be7dedb6d892aeaf8f92e1f99cbacc3300e721fbbfd7d5690abe6",
        "REQ-008": "sha256:db8e8f7793ed484c0fa0960c264ff2a063be41609db925ee0e2e9e49d6cd4f45",
        "REQ-010": "sha256:6c90a9a0ceeebd560ba40c37f900ba9247153a25e17cbab86fc3a1b45e0029c9",
        "REQ-011": "sha256:7c69a45314c4e67bc3c8e0c9b0325ba25d0d554672948654cf5d1f0effef4ea1",
        "REQ-012": "sha256:fcb33e719611733ed088a72bb7e1fccbcfd5843c6ed9a4246d3895a161a7e414",
        "UC-002": "sha256:d058ae80de91413ede200a910ed88df18487cbe335ac361823fff73bd99322be"
      },
      "blocked_at_completion": false
    },
    "T010": {
      "hash": "sha256:716a1cabd708717e6c5ac25eca77be73aa0773c27e024d9e742b61cb86f2e5a0",
      "class": "restated",
      "cites": {
        "AIS-032": "sha256:2852fd2521d685cd4d070c48f9ae2bf002eb0fe24ebb93edf45cd6ed71208b72",
        "AIS-034": "sha256:0b93a6c4055241f189d66b4b0114039979917c050411cc2afe951ce3ee4d2b3a",
        "AIS-010": "sha256:c76ef3161e1efe0818473324abf3fb03546cccce4772d6006a6f5acd3acd8ed9",
        "AIS-011": "sha256:ace5f9fb8935db7f276be0ab1cc02f4d73f8a147a44bd1031daace92c2605a91",
        "AIS-026": "sha256:8bf6eff2311fa1e0e4d626c709d3b76eae0fe296de11edf30743278b630c8313"
      },
      "completed_against": {
        "AIS-010": "sha256:c76ef3161e1efe0818473324abf3fb03546cccce4772d6006a6f5acd3acd8ed9",
        "AIS-011": "sha256:ace5f9fb8935db7f276be0ab1cc02f4d73f8a147a44bd1031daace92c2605a91",
        "AIS-026": "sha256:8bf6eff2311fa1e0e4d626c709d3b76eae0fe296de11edf30743278b630c8313",
        "AIS-032": "sha256:2852fd2521d685cd4d070c48f9ae2bf002eb0fe24ebb93edf45cd6ed71208b72",
        "AIS-034": "sha256:0b93a6c4055241f189d66b4b0114039979917c050411cc2afe951ce3ee4d2b3a",
        "DEC-002": "sha256:450de9b1737c8d785caca57c0b3cc522aed8898e9dcea2c8c953f697e1d03aa3",
        "DEC-004": "sha256:942ab4072dd367c7cc88758bbd6df350e7ce92e76ea93688853324c207fbf0a3",
        "FR-006": "sha256:81abe569717adc55e2ea4a635ebadcc9268825b269a820b6259f8c2d3580709a",
        "FR-007": "sha256:a1b8235dbe5caad9d3c19f5344e9e629dfe07c2ba8ee6f358a2296174454ae28",
        "FR-009": "sha256:2f4e357e7c45afc0535ca51280ef4a6cb662efea2c188887a76a8e0bbf79f79c",
        "FR-010": "sha256:f297709714ffd46f93f7abf23c9ebea1294efd150bd16b280ccbcedbc0bffd3c",
        "FR-011": "sha256:faf836f7ec7f293517c93343e6f61f8d0ff39875f6a9c4fcf4e570f136a028ec",
        "FR-012": "sha256:c45b0cea6084477d35f71746737ceb52e6c4bb25a3d53d5867516cbcb168058b",
        "NFR-001": "sha256:3131ccae52047de8b10a4105b89cdfc6b05b5b23f14b57040ff773ac24431f08",
        "REQ-003": "sha256:3755f308fed60ce65095a51a1ac6c761e9b9fe1a247dd166b82dfb773272081e",
        "REQ-004": "sha256:11ced25bc5b5a0f3bef0f22de7471d625296fc8ce169ef0d70a30c9f5ffdf44b",
        "REQ-007": "sha256:f510a28f216be7dedb6d892aeaf8f92e1f99cbacc3300e721fbbfd7d5690abe6",
        "REQ-010": "sha256:6c90a9a0ceeebd560ba40c37f900ba9247153a25e17cbab86fc3a1b45e0029c9",
        "REQ-012": "sha256:fcb33e719611733ed088a72bb7e1fccbcfd5843c6ed9a4246d3895a161a7e414",
        "UC-002": "sha256:d058ae80de91413ede200a910ed88df18487cbe335ac361823fff73bd99322be"
      },
      "blocked_at_completion": false
    },
    "T011": {
      "hash": "sha256:c80927e027bee65a086fb17a56101d5f983841f84cb658f4b9b8a016e2c66536",
      "class": "restated",
      "cites": {
        "AIS-017": "sha256:9dd0669614eaa47d12926b51126a209c16509140ef159f4a5e25fc0af8dd0448",
        "AIS-029": "sha256:becd651ddfc64bf81b82fe6708e067880c4955048fcb9d5e5a4e1a74367d5cb2",
        "AIS-009": "sha256:7b8dfc99da4e3d117d27a8744f5781f25be87c9abd49efa0999312363e73330f",
        "AIS-014": "sha256:0b9acb87fcb44ef42a60311b7cb1baffd2c46c7cfcab9ee4b0ae9622b68a1042",
        "AIS-024": "sha256:eceb65f1b56cb5f9df5cfd8b0674ab23b5308036e29a2ea9a6d0a2bcc5c9914e",
        "ART-005": "sha256:ddc99a0e777eeefe57010caa1355dd2acd061ede1711db2f440d2a061dbb0e06"
      },
      "completed_against": {
        "AIS-009": "sha256:7b8dfc99da4e3d117d27a8744f5781f25be87c9abd49efa0999312363e73330f",
        "AIS-014": "sha256:0b9acb87fcb44ef42a60311b7cb1baffd2c46c7cfcab9ee4b0ae9622b68a1042",
        "AIS-017": "sha256:9dd0669614eaa47d12926b51126a209c16509140ef159f4a5e25fc0af8dd0448",
        "AIS-024": "sha256:eceb65f1b56cb5f9df5cfd8b0674ab23b5308036e29a2ea9a6d0a2bcc5c9914e",
        "AIS-029": "sha256:becd651ddfc64bf81b82fe6708e067880c4955048fcb9d5e5a4e1a74367d5cb2",
        "ART-005": "sha256:ddc99a0e777eeefe57010caa1355dd2acd061ede1711db2f440d2a061dbb0e06",
        "DEC-001": "sha256:13a2732b598fcb0a7a620f1cc017318a750024235d9ca1453803f7f35b0ddedd",
        "DEC-003": "sha256:a9f99d3c520b3fe486f6f8103e542d28fb3a7c31a82c82665be1893726556d9d",
        "FR-001": "sha256:383f9296ff6a52d4e4c18607d174c816a95c9866b401c32d2b1194eb13a9b02c",
        "FR-002": "sha256:ed7dcf7ed5c6ad99f53a01c0ec96df80de21351bd839845b0ed6f1eef2a95ac7",
        "FR-003": "sha256:6f18dad4de22e5bf0feddcabd830ff23d873cb8dbf764edb96567d43b43cd668",
        "FR-004": "sha256:2ae3eb4329aaec539cf2ad43395016234b0a1d74b69470992d5519897e9b382f",
        "FR-005": "sha256:4fd4014add1830d59d7445913099f5dd61577b4ec75fcd6902f24418f440d04d",
        "FR-006": "sha256:81abe569717adc55e2ea4a635ebadcc9268825b269a820b6259f8c2d3580709a",
        "FR-007": "sha256:a1b8235dbe5caad9d3c19f5344e9e629dfe07c2ba8ee6f358a2296174454ae28",
        "FR-008": "sha256:b5f49e91e9db1d61276c75c1959d4e30f9d2a96b7a5354e4bf23c554d7e6fcab",
        "FR-010": "sha256:f297709714ffd46f93f7abf23c9ebea1294efd150bd16b280ccbcedbc0bffd3c",
        "NFR-001": "sha256:3131ccae52047de8b10a4105b89cdfc6b05b5b23f14b57040ff773ac24431f08",
        "REQ-001": "sha256:61e559eef48ae3d2bcafefa82d6db74a8356d04d3b827a3821dddbb4bf197af2",
        "REQ-002": "sha256:9be8cbf31c66cda1de24eb6018e9793bc3124a9883583b70cee59847b13ca3a5",
        "REQ-003": "sha256:3755f308fed60ce65095a51a1ac6c761e9b9fe1a247dd166b82dfb773272081e",
        "REQ-004": "sha256:11ced25bc5b5a0f3bef0f22de7471d625296fc8ce169ef0d70a30c9f5ffdf44b",
        "REQ-005": "sha256:b7dfc78315bdbaf546f86f722dce88987080968d3808e250013a20df55372105",
        "REQ-006": "sha256:859e9801daa175a7b2b81fda318548d186d0568e0b2a1241b2ae4cdfae93648f",
        "REQ-008": "sha256:db8e8f7793ed484c0fa0960c264ff2a063be41609db925ee0e2e9e49d6cd4f45",
        "REQ-009": "sha256:2acb805067e30d87ac45c5f1d0d4a41128a107a4cef12c892e0cf612bda9d42c",
        "REQ-010": "sha256:6c90a9a0ceeebd560ba40c37f900ba9247153a25e17cbab86fc3a1b45e0029c9",
        "REQ-011": "sha256:7c69a45314c4e67bc3c8e0c9b0325ba25d0d554672948654cf5d1f0effef4ea1",
        "REQ-012": "sha256:fcb33e719611733ed088a72bb7e1fccbcfd5843c6ed9a4246d3895a161a7e414",
        "UC-001": "sha256:3e691638c6e12461844d68e2f386ebdc36afc48a479fee7bbc5ada6fafc54fb8",
        "UC-002": "sha256:d058ae80de91413ede200a910ed88df18487cbe335ac361823fff73bd99322be"
      },
      "blocked_at_completion": false
    },
    "T012": {
      "hash": "sha256:882ffc64208ee5a597243d3c2ae8dec6d2d2221e608a63f3bd3c54d9dfb55fa7",
      "class": "restated",
      "cites": {
        "AIS-018": "sha256:3798cc9f0d4a1cdbed1b2269788519e78710776d78a91dbc570f3e35755b6cd0",
        "AIS-019": "sha256:dfb9a447f2d02858af8946ec06cf6a158d658fe2c2219237be8f02f2d2e263f0",
        "ART-005": "sha256:ddc99a0e777eeefe57010caa1355dd2acd061ede1711db2f440d2a061dbb0e06"
      },
      "completed_against": {
        "AIS-018": "sha256:3798cc9f0d4a1cdbed1b2269788519e78710776d78a91dbc570f3e35755b6cd0",
        "AIS-019": "sha256:dfb9a447f2d02858af8946ec06cf6a158d658fe2c2219237be8f02f2d2e263f0",
        "ART-004": "sha256:4b39c4b13aeb75a9f406bf14f4086f90145e8c067318a8d9c7117bc59ad99bed",
        "ART-005": "sha256:ddc99a0e777eeefe57010caa1355dd2acd061ede1711db2f440d2a061dbb0e06",
        "DEC-001": "sha256:13a2732b598fcb0a7a620f1cc017318a750024235d9ca1453803f7f35b0ddedd",
        "DEC-002": "sha256:450de9b1737c8d785caca57c0b3cc522aed8898e9dcea2c8c953f697e1d03aa3",
        "DEC-003": "sha256:a9f99d3c520b3fe486f6f8103e542d28fb3a7c31a82c82665be1893726556d9d",
        "DEC-004": "sha256:942ab4072dd367c7cc88758bbd6df350e7ce92e76ea93688853324c207fbf0a3",
        "FR-001": "sha256:383f9296ff6a52d4e4c18607d174c816a95c9866b401c32d2b1194eb13a9b02c",
        "FR-002": "sha256:ed7dcf7ed5c6ad99f53a01c0ec96df80de21351bd839845b0ed6f1eef2a95ac7",
        "FR-003": "sha256:6f18dad4de22e5bf0feddcabd830ff23d873cb8dbf764edb96567d43b43cd668",
        "FR-004": "sha256:2ae3eb4329aaec539cf2ad43395016234b0a1d74b69470992d5519897e9b382f",
        "FR-005": "sha256:4fd4014add1830d59d7445913099f5dd61577b4ec75fcd6902f24418f440d04d",
        "FR-006": "sha256:81abe569717adc55e2ea4a635ebadcc9268825b269a820b6259f8c2d3580709a",
        "FR-007": "sha256:a1b8235dbe5caad9d3c19f5344e9e629dfe07c2ba8ee6f358a2296174454ae28",
        "FR-008": "sha256:b5f49e91e9db1d61276c75c1959d4e30f9d2a96b7a5354e4bf23c554d7e6fcab",
        "FR-009": "sha256:2f4e357e7c45afc0535ca51280ef4a6cb662efea2c188887a76a8e0bbf79f79c",
        "FR-010": "sha256:f297709714ffd46f93f7abf23c9ebea1294efd150bd16b280ccbcedbc0bffd3c",
        "FR-011": "sha256:faf836f7ec7f293517c93343e6f61f8d0ff39875f6a9c4fcf4e570f136a028ec",
        "FR-012": "sha256:c45b0cea6084477d35f71746737ceb52e6c4bb25a3d53d5867516cbcb168058b",
        "NFR-001": "sha256:3131ccae52047de8b10a4105b89cdfc6b05b5b23f14b57040ff773ac24431f08",
        "REQ-001": "sha256:61e559eef48ae3d2bcafefa82d6db74a8356d04d3b827a3821dddbb4bf197af2",
        "REQ-002": "sha256:9be8cbf31c66cda1de24eb6018e9793bc3124a9883583b70cee59847b13ca3a5",
        "REQ-003": "sha256:3755f308fed60ce65095a51a1ac6c761e9b9fe1a247dd166b82dfb773272081e",
        "REQ-004": "sha256:11ced25bc5b5a0f3bef0f22de7471d625296fc8ce169ef0d70a30c9f5ffdf44b",
        "REQ-005": "sha256:b7dfc78315bdbaf546f86f722dce88987080968d3808e250013a20df55372105",
        "REQ-006": "sha256:859e9801daa175a7b2b81fda318548d186d0568e0b2a1241b2ae4cdfae93648f",
        "REQ-007": "sha256:f510a28f216be7dedb6d892aeaf8f92e1f99cbacc3300e721fbbfd7d5690abe6",
        "REQ-008": "sha256:db8e8f7793ed484c0fa0960c264ff2a063be41609db925ee0e2e9e49d6cd4f45",
        "REQ-009": "sha256:2acb805067e30d87ac45c5f1d0d4a41128a107a4cef12c892e0cf612bda9d42c",
        "REQ-010": "sha256:6c90a9a0ceeebd560ba40c37f900ba9247153a25e17cbab86fc3a1b45e0029c9",
        "REQ-011": "sha256:7c69a45314c4e67bc3c8e0c9b0325ba25d0d554672948654cf5d1f0effef4ea1",
        "REQ-012": "sha256:fcb33e719611733ed088a72bb7e1fccbcfd5843c6ed9a4246d3895a161a7e414",
        "UC-001": "sha256:3e691638c6e12461844d68e2f386ebdc36afc48a479fee7bbc5ada6fafc54fb8",
        "UC-002": "sha256:d058ae80de91413ede200a910ed88df18487cbe335ac361823fff73bd99322be"
      },
      "blocked_at_completion": false
    },
    "T013": {
      "hash": "sha256:a9864c8a15c2358112df33b143f421f570f9fb90aa1a258aef7fa3d2a6f47197",
      "class": "restated",
      "cites": {
        "AIS-016": "sha256:8ec6c8ae19f260077bd25aa927135e54748ce590567e8645231d75ec3391e82e",
        "AIS-007": "sha256:5187e8b721a6f85619c7f8ef2751c4b83c2c9665b7f731258e56cba32bbdca1c",
        "AIS-011": "sha256:ace5f9fb8935db7f276be0ab1cc02f4d73f8a147a44bd1031daace92c2605a91",
        "AIS-027": "sha256:ea1fe8e036f535a3ed85f1391bf58e178d52867f4213716914eeb0162d861a54",
        "AIS-036": "sha256:24faaad353cca6eee26bba8fa653c030694acb46b71e7c4dcc7f0aa8b3eff8f5",
        "AIS-037": "sha256:a46faccd82a3a075675c2200a988e90ab8cde988b2f6cfbd9c173751e22c8ef3",
        "ART-005": "sha256:ddc99a0e777eeefe57010caa1355dd2acd061ede1711db2f440d2a061dbb0e06",
        "ART-007": "sha256:e235f1fce07d44c485bfb4c27d046a24339b14a74bb0da9185ddd1d23a0826f6"
      },
      "completed_against": {
        "AIS-007": "sha256:5187e8b721a6f85619c7f8ef2751c4b83c2c9665b7f731258e56cba32bbdca1c",
        "AIS-011": "sha256:ace5f9fb8935db7f276be0ab1cc02f4d73f8a147a44bd1031daace92c2605a91",
        "AIS-016": "sha256:8ec6c8ae19f260077bd25aa927135e54748ce590567e8645231d75ec3391e82e",
        "AIS-027": "sha256:ea1fe8e036f535a3ed85f1391bf58e178d52867f4213716914eeb0162d861a54",
        "AIS-036": "sha256:24faaad353cca6eee26bba8fa653c030694acb46b71e7c4dcc7f0aa8b3eff8f5",
        "AIS-037": "sha256:a46faccd82a3a075675c2200a988e90ab8cde988b2f6cfbd9c173751e22c8ef3",
        "ART-005": "sha256:ddc99a0e777eeefe57010caa1355dd2acd061ede1711db2f440d2a061dbb0e06",
        "ART-007": "sha256:e235f1fce07d44c485bfb4c27d046a24339b14a74bb0da9185ddd1d23a0826f6",
        "DEC-001": "sha256:13a2732b598fcb0a7a620f1cc017318a750024235d9ca1453803f7f35b0ddedd",
        "DEC-002": "sha256:450de9b1737c8d785caca57c0b3cc522aed8898e9dcea2c8c953f697e1d03aa3",
        "DEC-003": "sha256:a9f99d3c520b3fe486f6f8103e542d28fb3a7c31a82c82665be1893726556d9d",
        "DEC-004": "sha256:942ab4072dd367c7cc88758bbd6df350e7ce92e76ea93688853324c207fbf0a3",
        "FR-001": "sha256:383f9296ff6a52d4e4c18607d174c816a95c9866b401c32d2b1194eb13a9b02c",
        "FR-002": "sha256:ed7dcf7ed5c6ad99f53a01c0ec96df80de21351bd839845b0ed6f1eef2a95ac7",
        "FR-003": "sha256:6f18dad4de22e5bf0feddcabd830ff23d873cb8dbf764edb96567d43b43cd668",
        "FR-004": "sha256:2ae3eb4329aaec539cf2ad43395016234b0a1d74b69470992d5519897e9b382f",
        "FR-005": "sha256:4fd4014add1830d59d7445913099f5dd61577b4ec75fcd6902f24418f440d04d",
        "FR-006": "sha256:81abe569717adc55e2ea4a635ebadcc9268825b269a820b6259f8c2d3580709a",
        "FR-007": "sha256:a1b8235dbe5caad9d3c19f5344e9e629dfe07c2ba8ee6f358a2296174454ae28",
        "FR-008": "sha256:b5f49e91e9db1d61276c75c1959d4e30f9d2a96b7a5354e4bf23c554d7e6fcab",
        "FR-009": "sha256:2f4e357e7c45afc0535ca51280ef4a6cb662efea2c188887a76a8e0bbf79f79c",
        "FR-010": "sha256:f297709714ffd46f93f7abf23c9ebea1294efd150bd16b280ccbcedbc0bffd3c",
        "FR-011": "sha256:faf836f7ec7f293517c93343e6f61f8d0ff39875f6a9c4fcf4e570f136a028ec",
        "FR-012": "sha256:c45b0cea6084477d35f71746737ceb52e6c4bb25a3d53d5867516cbcb168058b",
        "NFR-001": "sha256:3131ccae52047de8b10a4105b89cdfc6b05b5b23f14b57040ff773ac24431f08",
        "REQ-001": "sha256:61e559eef48ae3d2bcafefa82d6db74a8356d04d3b827a3821dddbb4bf197af2",
        "REQ-002": "sha256:9be8cbf31c66cda1de24eb6018e9793bc3124a9883583b70cee59847b13ca3a5",
        "REQ-003": "sha256:3755f308fed60ce65095a51a1ac6c761e9b9fe1a247dd166b82dfb773272081e",
        "REQ-004": "sha256:11ced25bc5b5a0f3bef0f22de7471d625296fc8ce169ef0d70a30c9f5ffdf44b",
        "REQ-005": "sha256:b7dfc78315bdbaf546f86f722dce88987080968d3808e250013a20df55372105",
        "REQ-006": "sha256:859e9801daa175a7b2b81fda318548d186d0568e0b2a1241b2ae4cdfae93648f",
        "REQ-007": "sha256:f510a28f216be7dedb6d892aeaf8f92e1f99cbacc3300e721fbbfd7d5690abe6",
        "REQ-008": "sha256:db8e8f7793ed484c0fa0960c264ff2a063be41609db925ee0e2e9e49d6cd4f45",
        "REQ-009": "sha256:2acb805067e30d87ac45c5f1d0d4a41128a107a4cef12c892e0cf612bda9d42c",
        "REQ-010": "sha256:6c90a9a0ceeebd560ba40c37f900ba9247153a25e17cbab86fc3a1b45e0029c9",
        "REQ-011": "sha256:7c69a45314c4e67bc3c8e0c9b0325ba25d0d554672948654cf5d1f0effef4ea1",
        "REQ-012": "sha256:fcb33e719611733ed088a72bb7e1fccbcfd5843c6ed9a4246d3895a161a7e414",
        "UC-001": "sha256:3e691638c6e12461844d68e2f386ebdc36afc48a479fee7bbc5ada6fafc54fb8",
        "UC-002": "sha256:d058ae80de91413ede200a910ed88df18487cbe335ac361823fff73bd99322be"
      },
      "blocked_at_completion": false
    },
    "T014": {
      "hash": "sha256:1918a9bf0d89b8bd016d2ed594704af4eb24bda73828d3a496bcb3e862e09d03",
      "class": "restated",
      "cites": {
        "AIS-023": "sha256:0141e7767e1a4a670dd0aa1cc28dd78787d47eec46f8f3f37ecff3712c9f090c",
        "AIS-026": "sha256:8bf6eff2311fa1e0e4d626c709d3b76eae0fe296de11edf30743278b630c8313",
        "AIS-034": "sha256:0b93a6c4055241f189d66b4b0114039979917c050411cc2afe951ce3ee4d2b3a",
        "AIS-035": "sha256:0ab4f5f1259c5bcc6e20731abca38b90e4ee5c4fca507f03ecd2f1974e022f8b",
        "AIS-006": "sha256:6e7e7098491cf25f1f5df4ccaabf0aa43bdfe093326f80c534f7b9e61d75c2da",
        "AIS-040": "sha256:bb79051dcb607067c04bd5d6e7afda9d9ce9589bd542c163a93eec91c169ea1b",
        "ART-007": "sha256:e235f1fce07d44c485bfb4c27d046a24339b14a74bb0da9185ddd1d23a0826f6"
      },
      "completed_against": {
        "AIS-006": "sha256:6e7e7098491cf25f1f5df4ccaabf0aa43bdfe093326f80c534f7b9e61d75c2da",
        "AIS-023": "sha256:0141e7767e1a4a670dd0aa1cc28dd78787d47eec46f8f3f37ecff3712c9f090c",
        "AIS-026": "sha256:8bf6eff2311fa1e0e4d626c709d3b76eae0fe296de11edf30743278b630c8313",
        "AIS-034": "sha256:0b93a6c4055241f189d66b4b0114039979917c050411cc2afe951ce3ee4d2b3a",
        "AIS-035": "sha256:0ab4f5f1259c5bcc6e20731abca38b90e4ee5c4fca507f03ecd2f1974e022f8b",
        "AIS-040": "sha256:bb79051dcb607067c04bd5d6e7afda9d9ce9589bd542c163a93eec91c169ea1b",
        "ART-007": "sha256:e235f1fce07d44c485bfb4c27d046a24339b14a74bb0da9185ddd1d23a0826f6",
        "DEC-002": "sha256:450de9b1737c8d785caca57c0b3cc522aed8898e9dcea2c8c953f697e1d03aa3",
        "DEC-003": "sha256:a9f99d3c520b3fe486f6f8103e542d28fb3a7c31a82c82665be1893726556d9d",
        "DEC-004": "sha256:942ab4072dd367c7cc88758bbd6df350e7ce92e76ea93688853324c207fbf0a3",
        "FR-006": "sha256:81abe569717adc55e2ea4a635ebadcc9268825b269a820b6259f8c2d3580709a",
        "FR-007": "sha256:a1b8235dbe5caad9d3c19f5344e9e629dfe07c2ba8ee6f358a2296174454ae28",
        "FR-008": "sha256:b5f49e91e9db1d61276c75c1959d4e30f9d2a96b7a5354e4bf23c554d7e6fcab",
        "FR-009": "sha256:2f4e357e7c45afc0535ca51280ef4a6cb662efea2c188887a76a8e0bbf79f79c",
        "FR-010": "sha256:f297709714ffd46f93f7abf23c9ebea1294efd150bd16b280ccbcedbc0bffd3c",
        "FR-011": "sha256:faf836f7ec7f293517c93343e6f61f8d0ff39875f6a9c4fcf4e570f136a028ec",
        "FR-012": "sha256:c45b0cea6084477d35f71746737ceb52e6c4bb25a3d53d5867516cbcb168058b",
        "NFR-001": "sha256:3131ccae52047de8b10a4105b89cdfc6b05b5b23f14b57040ff773ac24431f08",
        "REQ-003": "sha256:3755f308fed60ce65095a51a1ac6c761e9b9fe1a247dd166b82dfb773272081e",
        "REQ-004": "sha256:11ced25bc5b5a0f3bef0f22de7471d625296fc8ce169ef0d70a30c9f5ffdf44b",
        "REQ-007": "sha256:f510a28f216be7dedb6d892aeaf8f92e1f99cbacc3300e721fbbfd7d5690abe6",
        "REQ-008": "sha256:db8e8f7793ed484c0fa0960c264ff2a063be41609db925ee0e2e9e49d6cd4f45",
        "REQ-010": "sha256:6c90a9a0ceeebd560ba40c37f900ba9247153a25e17cbab86fc3a1b45e0029c9",
        "REQ-011": "sha256:7c69a45314c4e67bc3c8e0c9b0325ba25d0d554672948654cf5d1f0effef4ea1",
        "REQ-012": "sha256:fcb33e719611733ed088a72bb7e1fccbcfd5843c6ed9a4246d3895a161a7e414",
        "UC-002": "sha256:d058ae80de91413ede200a910ed88df18487cbe335ac361823fff73bd99322be"
      },
      "blocked_at_completion": false
    },
    "Phase 5: User Story 3 - Open pages refresh themselves (Priority: P3)#f978ecd59229": {
      "hash": "sha256:f978ecd592298628d1e46803467102684e6eca429f91550a12687f48daee0d33",
      "class": "inferred",
      "reviewed": {
        "by": "Lee Sinclair",
        "at": "2026-10-17T02:57:40Z",
        "list": "RVW-012",
        "reply": "yes"
      }
    },
    "Phase 5: User Story 3 - Open pages refresh themselves (Priority: P3)#aafb2ec0e266": {
      "hash": "sha256:aafb2ec0e2666e5ca610a08bf0a26ae552ab2c83c4212f0deb9d7b8f03eb98cf",
      "class": "inferred",
      "reviewed": {
        "by": "Lee Sinclair",
        "at": "2026-10-17T02:57:40Z",
        "list": "RVW-012",
        "reply": "yes"
      }
    },
    "T015": {
      "hash": "sha256:5b672423de640378977425cbd04425338dfccfe20092e3e773e359615f0e4b41",
      "class": "restated",
      "cites": {
        "AIS-033": "sha256:1384d3251da72858bb2a104fd7ef3dae18ee70787bf5fc4b6b74b4beae5b1f1c",
        "AIS-025": "sha256:a1dd7661e9b9404a6bd63366611eb673cf941680d96e04ef0846d8fcf81622b4",
        "AIS-034": "sha256:0b93a6c4055241f189d66b4b0114039979917c050411cc2afe951ce3ee4d2b3a",
        "AIS-039": "sha256:92f92676fc4b6d891601ba7f91b65ccaf2726cbfc2a71cc421154597fefce0dc",
        "AIS-043": "sha256:ccfbc623efb904d0d27f4bd25095a49ae3d2cf6d444ec1cf3ce9d6cecfc4672d"
      },
      "completed_against": {
        "AIS-025": "sha256:a1dd7661e9b9404a6bd63366611eb673cf941680d96e04ef0846d8fcf81622b4",
        "AIS-033": "sha256:1384d3251da72858bb2a104fd7ef3dae18ee70787bf5fc4b6b74b4beae5b1f1c",
        "AIS-034": "sha256:0b93a6c4055241f189d66b4b0114039979917c050411cc2afe951ce3ee4d2b3a",
        "AIS-039": "sha256:92f92676fc4b6d891601ba7f91b65ccaf2726cbfc2a71cc421154597fefce0dc",
        "AIS-043": "sha256:ccfbc623efb904d0d27f4bd25095a49ae3d2cf6d444ec1cf3ce9d6cecfc4672d",
        "DEC-002": "sha256:450de9b1737c8d785caca57c0b3cc522aed8898e9dcea2c8c953f697e1d03aa3",
        "DEC-004": "sha256:942ab4072dd367c7cc88758bbd6df350e7ce92e76ea93688853324c207fbf0a3",
        "FR-006": "sha256:81abe569717adc55e2ea4a635ebadcc9268825b269a820b6259f8c2d3580709a",
        "FR-007": "sha256:a1b8235dbe5caad9d3c19f5344e9e629dfe07c2ba8ee6f358a2296174454ae28",
        "FR-009": "sha256:2f4e357e7c45afc0535ca51280ef4a6cb662efea2c188887a76a8e0bbf79f79c",
        "FR-011": "sha256:faf836f7ec7f293517c93343e6f61f8d0ff39875f6a9c4fcf4e570f136a028ec",
        "FR-012": "sha256:c45b0cea6084477d35f71746737ceb52e6c4bb25a3d53d5867516cbcb168058b",
        "NFR-001": "sha256:3131ccae52047de8b10a4105b89cdfc6b05b5b23f14b57040ff773ac24431f08",
        "REQ-003": "sha256:3755f308fed60ce65095a51a1ac6c761e9b9fe1a247dd166b82dfb773272081e",
        "REQ-004": "sha256:11ced25bc5b5a0f3bef0f22de7471d625296fc8ce169ef0d70a30c9f5ffdf44b",
        "REQ-007": "sha256:f510a28f216be7dedb6d892aeaf8f92e1f99cbacc3300e721fbbfd7d5690abe6",
        "REQ-012": "sha256:fcb33e719611733ed088a72bb7e1fccbcfd5843c6ed9a4246d3895a161a7e414",
        "UC-002": "sha256:d058ae80de91413ede200a910ed88df18487cbe335ac361823fff73bd99322be"
      },
      "blocked_at_completion": false
    },
    "T016": {
      "hash": "sha256:954f56d4f3eaaefb7ec02a595e5bbbf3df752cdebc0f42ff5de9cb5ccce315e7",
      "class": "restated",
      "cites": {
        "AIS-025": "sha256:a1dd7661e9b9404a6bd63366611eb673cf941680d96e04ef0846d8fcf81622b4",
        "AIS-023": "sha256:0141e7767e1a4a670dd0aa1cc28dd78787d47eec46f8f3f37ecff3712c9f090c",
        "AIS-034": "sha256:0b93a6c4055241f189d66b4b0114039979917c050411cc2afe951ce3ee4d2b3a",
        "AIS-039": "sha256:92f92676fc4b6d891601ba7f91b65ccaf2726cbfc2a71cc421154597fefce0dc",
        "ART-007": "sha256:e235f1fce07d44c485bfb4c27d046a24339b14a74bb0da9185ddd1d23a0826f6"
      },
      "completed_against": {
        "AIS-023": "sha256:0141e7767e1a4a670dd0aa1cc28dd78787d47eec46f8f3f37ecff3712c9f090c",
        "AIS-025": "sha256:a1dd7661e9b9404a6bd63366611eb673cf941680d96e04ef0846d8fcf81622b4",
        "AIS-034": "sha256:0b93a6c4055241f189d66b4b0114039979917c050411cc2afe951ce3ee4d2b3a",
        "AIS-039": "sha256:92f92676fc4b6d891601ba7f91b65ccaf2726cbfc2a71cc421154597fefce0dc",
        "ART-007": "sha256:e235f1fce07d44c485bfb4c27d046a24339b14a74bb0da9185ddd1d23a0826f6",
        "DEC-002": "sha256:450de9b1737c8d785caca57c0b3cc522aed8898e9dcea2c8c953f697e1d03aa3",
        "DEC-003": "sha256:a9f99d3c520b3fe486f6f8103e542d28fb3a7c31a82c82665be1893726556d9d",
        "DEC-004": "sha256:942ab4072dd367c7cc88758bbd6df350e7ce92e76ea93688853324c207fbf0a3",
        "FR-006": "sha256:81abe569717adc55e2ea4a635ebadcc9268825b269a820b6259f8c2d3580709a",
        "FR-007": "sha256:a1b8235dbe5caad9d3c19f5344e9e629dfe07c2ba8ee6f358a2296174454ae28",
        "FR-008": "sha256:b5f49e91e9db1d61276c75c1959d4e30f9d2a96b7a5354e4bf23c554d7e6fcab",
        "FR-009": "sha256:2f4e357e7c45afc0535ca51280ef4a6cb662efea2c188887a76a8e0bbf79f79c",
        "FR-010": "sha256:f297709714ffd46f93f7abf23c9ebea1294efd150bd16b280ccbcedbc0bffd3c",
        "FR-011": "sha256:faf836f7ec7f293517c93343e6f61f8d0ff39875f6a9c4fcf4e570f136a028ec",
        "FR-012": "sha256:c45b0cea6084477d35f71746737ceb52e6c4bb25a3d53d5867516cbcb168058b",
        "NFR-001": "sha256:3131ccae52047de8b10a4105b89cdfc6b05b5b23f14b57040ff773ac24431f08",
        "REQ-003": "sha256:3755f308fed60ce65095a51a1ac6c761e9b9fe1a247dd166b82dfb773272081e",
        "REQ-004": "sha256:11ced25bc5b5a0f3bef0f22de7471d625296fc8ce169ef0d70a30c9f5ffdf44b",
        "REQ-007": "sha256:f510a28f216be7dedb6d892aeaf8f92e1f99cbacc3300e721fbbfd7d5690abe6",
        "REQ-008": "sha256:db8e8f7793ed484c0fa0960c264ff2a063be41609db925ee0e2e9e49d6cd4f45",
        "REQ-010": "sha256:6c90a9a0ceeebd560ba40c37f900ba9247153a25e17cbab86fc3a1b45e0029c9",
        "REQ-011": "sha256:7c69a45314c4e67bc3c8e0c9b0325ba25d0d554672948654cf5d1f0effef4ea1",
        "REQ-012": "sha256:fcb33e719611733ed088a72bb7e1fccbcfd5843c6ed9a4246d3895a161a7e414",
        "UC-002": "sha256:d058ae80de91413ede200a910ed88df18487cbe335ac361823fff73bd99322be"
      },
      "blocked_at_completion": false
    },
    "T017": {
      "hash": "sha256:4044f4cb01694224db0217441377bd7924651e3fa66c74adec07af7b59d6fb05",
      "class": "restated",
      "cites": {
        "AIS-012": "sha256:d7c2c4c3bf48318481866ac34969ce229af12e8da9c157092edaeb7b16c115a0",
        "AIS-018": "sha256:3798cc9f0d4a1cdbed1b2269788519e78710776d78a91dbc570f3e35755b6cd0",
        "AIS-043": "sha256:ccfbc623efb904d0d27f4bd25095a49ae3d2cf6d444ec1cf3ce9d6cecfc4672d",
        "AIS-047": "sha256:1adc7d40779a72fbc721e00b57796b1cfe5df704eff1b95b7a716506da55f4f2",
        "ART-008": "sha256:952782963b9d2dcd8083c0acbf50df86010fad0435552f9058625f9c8d4feb51"
      },
      "completed_against": {
        "AIS-012": "sha256:d7c2c4c3bf48318481866ac34969ce229af12e8da9c157092edaeb7b16c115a0",
        "AIS-018": "sha256:3798cc9f0d4a1cdbed1b2269788519e78710776d78a91dbc570f3e35755b6cd0",
        "AIS-043": "sha256:ccfbc623efb904d0d27f4bd25095a49ae3d2cf6d444ec1cf3ce9d6cecfc4672d",
        "AIS-047": "sha256:1adc7d40779a72fbc721e00b57796b1cfe5df704eff1b95b7a716506da55f4f2",
        "ART-008": "sha256:952782963b9d2dcd8083c0acbf50df86010fad0435552f9058625f9c8d4feb51",
        "DEC-004": "sha256:942ab4072dd367c7cc88758bbd6df350e7ce92e76ea93688853324c207fbf0a3",
        "FR-006": "sha256:81abe569717adc55e2ea4a635ebadcc9268825b269a820b6259f8c2d3580709a",
        "FR-012": "sha256:c45b0cea6084477d35f71746737ceb52e6c4bb25a3d53d5867516cbcb168058b",
        "NFR-001": "sha256:3131ccae52047de8b10a4105b89cdfc6b05b5b23f14b57040ff773ac24431f08",
        "REQ-003": "sha256:3755f308fed60ce65095a51a1ac6c761e9b9fe1a247dd166b82dfb773272081e",
        "REQ-012": "sha256:fcb33e719611733ed088a72bb7e1fccbcfd5843c6ed9a4246d3895a161a7e414",
        "UC-002": "sha256:d058ae80de91413ede200a910ed88df18487cbe335ac361823fff73bd99322be"
      },
      "blocked_at_completion": false
    },
    "T018": {
      "hash": "sha256:50852ddcfe003ac1db1c6f221263144fcd37eb58241ed00679311dc9b7b3cfbe",
      "class": "restated",
      "cites": {
        "AIS-044": "sha256:87e460dfc8f47e25f60139d2b9e5d5deab11df551a6e6c48eef3617c3c92605b"
      },
      "completed_against": {
        "AIS-044": "sha256:87e460dfc8f47e25f60139d2b9e5d5deab11df551a6e6c48eef3617c3c92605b",
        "FR-006": "sha256:81abe569717adc55e2ea4a635ebadcc9268825b269a820b6259f8c2d3580709a",
        "FR-012": "sha256:c45b0cea6084477d35f71746737ceb52e6c4bb25a3d53d5867516cbcb168058b",
        "REQ-003": "sha256:3755f308fed60ce65095a51a1ac6c761e9b9fe1a247dd166b82dfb773272081e",
        "REQ-012": "sha256:fcb33e719611733ed088a72bb7e1fccbcfd5843c6ed9a4246d3895a161a7e414",
        "UC-002": "sha256:d058ae80de91413ede200a910ed88df18487cbe335ac361823fff73bd99322be"
      },
      "blocked_at_completion": false
    },
    "T019": {
      "hash": "sha256:6f8e17cd4a4f0dd722cd7d91f3e9f2e0865ffc3e1655668832e444d9db069ef0",
      "class": "restated",
      "cites": {
        "AIS-042": "sha256:9fd23817168dd25e5375c3b318972507b91ed0d5d998412ee068842c67982de2",
        "AIS-033": "sha256:1384d3251da72858bb2a104fd7ef3dae18ee70787bf5fc4b6b74b4beae5b1f1c"
      },
      "completed_against": {
        "AIS-033": "sha256:1384d3251da72858bb2a104fd7ef3dae18ee70787bf5fc4b6b74b4beae5b1f1c",
        "AIS-042": "sha256:9fd23817168dd25e5375c3b318972507b91ed0d5d998412ee068842c67982de2",
        "DEC-001": "sha256:13a2732b598fcb0a7a620f1cc017318a750024235d9ca1453803f7f35b0ddedd",
        "DEC-002": "sha256:450de9b1737c8d785caca57c0b3cc522aed8898e9dcea2c8c953f697e1d03aa3",
        "DEC-004": "sha256:942ab4072dd367c7cc88758bbd6df350e7ce92e76ea93688853324c207fbf0a3",
        "FR-001": "sha256:383f9296ff6a52d4e4c18607d174c816a95c9866b401c32d2b1194eb13a9b02c",
        "FR-002": "sha256:ed7dcf7ed5c6ad99f53a01c0ec96df80de21351bd839845b0ed6f1eef2a95ac7",
        "FR-003": "sha256:6f18dad4de22e5bf0feddcabd830ff23d873cb8dbf764edb96567d43b43cd668",
        "FR-004": "sha256:2ae3eb4329aaec539cf2ad43395016234b0a1d74b69470992d5519897e9b382f",
        "FR-005": "sha256:4fd4014add1830d59d7445913099f5dd61577b4ec75fcd6902f24418f440d04d",
        "FR-006": "sha256:81abe569717adc55e2ea4a635ebadcc9268825b269a820b6259f8c2d3580709a",
        "FR-007": "sha256:a1b8235dbe5caad9d3c19f5344e9e629dfe07c2ba8ee6f358a2296174454ae28",
        "FR-009": "sha256:2f4e357e7c45afc0535ca51280ef4a6cb662efea2c188887a76a8e0bbf79f79c",
        "FR-011": "sha256:faf836f7ec7f293517c93343e6f61f8d0ff39875f6a9c4fcf4e570f136a028ec",
        "FR-012": "sha256:c45b0cea6084477d35f71746737ceb52e6c4bb25a3d53d5867516cbcb168058b",
        "NFR-001": "sha256:3131ccae52047de8b10a4105b89cdfc6b05b5b23f14b57040ff773ac24431f08",
        "REQ-001": "sha256:61e559eef48ae3d2bcafefa82d6db74a8356d04d3b827a3821dddbb4bf197af2",
        "REQ-002": "sha256:9be8cbf31c66cda1de24eb6018e9793bc3124a9883583b70cee59847b13ca3a5",
        "REQ-003": "sha256:3755f308fed60ce65095a51a1ac6c761e9b9fe1a247dd166b82dfb773272081e",
        "REQ-004": "sha256:11ced25bc5b5a0f3bef0f22de7471d625296fc8ce169ef0d70a30c9f5ffdf44b",
        "REQ-005": "sha256:b7dfc78315bdbaf546f86f722dce88987080968d3808e250013a20df55372105",
        "REQ-006": "sha256:859e9801daa175a7b2b81fda318548d186d0568e0b2a1241b2ae4cdfae93648f",
        "REQ-007": "sha256:f510a28f216be7dedb6d892aeaf8f92e1f99cbacc3300e721fbbfd7d5690abe6",
        "REQ-009": "sha256:2acb805067e30d87ac45c5f1d0d4a41128a107a4cef12c892e0cf612bda9d42c",
        "REQ-012": "sha256:fcb33e719611733ed088a72bb7e1fccbcfd5843c6ed9a4246d3895a161a7e414",
        "UC-001": "sha256:3e691638c6e12461844d68e2f386ebdc36afc48a479fee7bbc5ada6fafc54fb8",
        "UC-002": "sha256:d058ae80de91413ede200a910ed88df18487cbe335ac361823fff73bd99322be"
      },
      "blocked_at_completion": false
    },
    "Dependencies & Execution Order#96f85424b78b": {
      "hash": "sha256:96f85424b78b910e51985f1769b21beeec781d52e2b1b8cbb751ef61218e6381",
      "class": "inferred",
      "reviewed": {
        "by": "Lee Sinclair",
        "at": "2026-10-17T02:57:40Z",
        "list": "RVW-012",
        "reply": "yes"
      }
    },
    "Parallel Examples#b380d87581fd": {
      "hash": "sha256:b380d87581fd010e7505290f9435252f83192ecab89a65e58114c08e954e516b",
      "class": "inferred",
      "reviewed": {
        "by": "Lee Sinclair",
        "at": "2026-10-17T02:57:40Z",
        "list": "RVW-012",
        "reply": "yes"
      }
    },
    "Implementation Strategy#73b8925531da": {
      "hash": "sha256:73b8925531daacb220d923c8aa9125baa3b2b3f76360b8e2640a0c467fe999e5",
      "class": "inferred",
      "reviewed": {
        "by": "Lee Sinclair",
        "at": "2026-10-17T02:57:40Z",
        "list": "RVW-012",
        "reply": "yes"
      }
    }
  },
  "acceptances": [
    {
      "id": "RVW-012",
      "stage": "tasks",
      "kind": "inferred",
      "digest": "sha256:2b8e0e270d893ea093dbcb5e9872c5088bb23dcbb9bc810b307005d046dac865",
      "by": "Lee Sinclair",
      "at": "2026-10-17T02:57:40Z",
      "reply": "yes",
      "accepted": [
        "#f52d711103d5",
        "#2cf5717e5d14",
        "Tasks: Cross-reference codes and tasks kanban view#d422cb72ef55",
        "Tasks: Cross-reference codes and tasks kanban view#2871d140bc6e",
        "Tasks: Cross-reference codes and tasks kanban view#3f49598a1878",
        "Tasks: Cross-reference codes and tasks kanban view#535bf6399d7f",
        "§Format: `[ID] [P?] [Story] Description `",
        "Phase 3: User Story 1 - Follow a newly introduced code (Priority: P1) 🎯 MVP#edcbc2bbee99",
        "Phase 3: User Story 1 - Follow a newly introduced code (Priority: P1) 🎯 MVP#2937c20b2640",
        "Phase 4: User Story 2 - Check build progress (Priority: P2)#dcd20f110223",
        "Phase 4: User Story 2 - Check build progress (Priority: P2)#964816a5de51",
        "Phase 5: User Story 3 - Open pages refresh themselves (Priority: P3)#f978ecd59229",
        "Phase 5: User Story 3 - Open pages refresh themselves (Priority: P3)#aafb2ec0e266",
        "Dependencies & Execution Order#96f85424b78b",
        "Parallel Examples#b380d87581fd",
        "Implementation Strategy#73b8925531da"
      ],
      "except": [],
      "questioned": [],
      "reopened": [],
      "reason": null,
      "hashes": {
        "#f52d711103d5": "sha256:f52d711103d50a437830c6fbcd04fb4bab49a0f82f6d26d1c791c6e8488dd090",
        "#2cf5717e5d14": "sha256:2cf5717e5d14288202df5613edf212e42618ba7e9f8bd855a74bb75cd8230860",
        "Tasks: Cross-reference codes and tasks kanban view#d422cb72ef55": "sha256:d422cb72ef55b3510ec1373fa3d82adc305ee67931b12f4f62ab49597a49b0c0",
        "Tasks: Cross-reference codes and tasks kanban view#2871d140bc6e": "sha256:2871d140bc6efb8e4f6e9c43318f7f4be9c267eb3db23a8e0484aad21ea339a6",
        "Tasks: Cross-reference codes and tasks kanban view#3f49598a1878": "sha256:3f49598a18784f6214ea964393e308880881fffebde92fcbd9b1018e09648063",
        "Tasks: Cross-reference codes and tasks kanban view#535bf6399d7f": "sha256:535bf6399d7ff08cd7d968e671d64f5367e22e63855bd7894d6b8bfaeff9a531",
        "§Format: `[ID] [P?] [Story] Description `": "sha256:78ecff41c1b9dbf4c7a3caffaf8d3df65f3a498a6db05a25bb4b8e93ae5f0f99",
        "Phase 3: User Story 1 - Follow a newly introduced code (Priority: P1) 🎯 MVP#edcbc2bbee99": "sha256:edcbc2bbee9979786d6358d2d2b513c3a716139bbe62c02c2ce271786d920134",
        "Phase 3: User Story 1 - Follow a newly introduced code (Priority: P1) 🎯 MVP#2937c20b2640": "sha256:2937c20b26407c16dd9c662056950bb33464a6b149aa52f65c787625a13b733c",
        "Phase 4: User Story 2 - Check build progress (Priority: P2)#dcd20f110223": "sha256:dcd20f110223dbcbd09549fe92f9fd3bfa211aa1ddd375083aa42eec31505295",
        "Phase 4: User Story 2 - Check build progress (Priority: P2)#964816a5de51": "sha256:964816a5de51853a401c6b812bd4ef2abe67ff411fcd939818054f765ca0b234",
        "Phase 5: User Story 3 - Open pages refresh themselves (Priority: P3)#f978ecd59229": "sha256:f978ecd592298628d1e46803467102684e6eca429f91550a12687f48daee0d33",
        "Phase 5: User Story 3 - Open pages refresh themselves (Priority: P3)#aafb2ec0e266": "sha256:aafb2ec0e2666e5ca610a08bf0a26ae552ab2c83c4212f0deb9d7b8f03eb98cf",
        "Dependencies & Execution Order#96f85424b78b": "sha256:96f85424b78b910e51985f1769b21beeec781d52e2b1b8cbb751ef61218e6381",
        "Parallel Examples#b380d87581fd": "sha256:b380d87581fd010e7505290f9435252f83192ecab89a65e58114c08e954e516b",
        "Implementation Strategy#73b8925531da": "sha256:73b8925531daacb220d923c8aa9125baa3b2b3f76360b8e2640a0c467fe999e5"
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
  "evaluated_at": "2026-10-17T03:10:08Z",
  "fingerprint": "sha256:856d957a0212ae3d49de3659310437517b6e98ded67be43392b9c6ae5cbed61f",
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
      "reason": "AI assessment: Every task carries out an AI Specification item and adds no component, route or data store beyond the approved design; the fixtures, menu and README tasks serve AIS-030 to AIS-032, AIS-028 and AIS-044.",
      "basis": "sha256:856d957a0212ae3d49de3659310437517b6e98ded67be43392b9c6ae5cbed61f"
    }
  ],
  "assessment": {
    "ambiguity": [],
    "missing": [],
    "contradictions": [],
    "unsupported_assumptions": [
      "Grouping the work into three stories (codes, kanban, refresh) is the plan's choice; the approved stages name two use cases and a requirement (REQ-012)."
    ],
    "untestable": []
  },
  "findings": []
}
```
<!-- eil:end assessment -->
