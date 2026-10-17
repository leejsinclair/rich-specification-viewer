<!--
  STAGE 4 OF THE DEFINITION PIPELINE: how should the AI execute the approved design?

  This document is `spec.md` as Spec Kit sees it (an alias of this file). It translates the approved
  Requirements, Functional and Technical Specifications into an implementation context for an AI
  coding agent. It does not redesign anything.

  Gate: AIS-G01 to AIS-G05 (`eil check --stage ai-spec`). This stage is not approved by a person: a
  passing check is the gate, and a human review is optional. Plan and Tasks refuse to start until it passes.

  - Every item is one line `**AIS-001**: text (traces: FR-001, DEC-004)` naming the approved
    requirement, functional requirement, decision or artefact it comes from. Text without a source is
    not written: it is raised as a challenge or a question.
  - Do not add a functional or architectural decision that is not in an approved stage.
  - Do not draw a diagram here. List the approved artefacts the agent must read, under Artefacts in
    Scope, as items tracing to their `ART` ids.
  - An answer collected by /speckit-clarify is written as an item tagged [pending-clarification]
    until it has been carried to the earliest stage it affects (/speckit-eil-resolve).
  - A section that does not apply is removed and listed under "Not applicable" with a reason.
-->

# AI Specification: Cross-reference codes and tasks kanban view

## Functional Requirements

<!-- The functional requirements to build, restated for the agent: `**AIS-001**: Flag duplicate customers on import. (traces: FR-001)`. -->

**AIS-001**: Treat the prefix of a code (two or more capital letters, a hyphen and one or more digits) as a form of code when a code with that prefix starts a heading or a bullet point in a document of the story. (traces: FR-001)

**AIS-002**: Also treat a code as introducing a form when it is the only content of the first column of a table row whose next column holds a description, judged by structure alone, and take that row as its defining section; a table whose rows only point back to a code defined elsewhere introduces no form. (traces: FR-002)

**AIS-003**: Mark every code of a discovered form wherever it is referenced in a document of the story, with the same hover, click and error behaviour as the codes already recognised. (traces: FR-003)

**AIS-004**: Keep recognising the existing fixed list of prefixes, including the errors for undefined and ambiguous codes. (traces: FR-004)

**AIS-005**: Discover forms of code only from the documents of the story being viewed and never carry a form from one story into another. (traces: FR-005)

**AIS-006**: Show, for a story, a kanban view of the tasks in its `tasks.md`. (traces: FR-006)

**AIS-007**: Show each task as a card with its task ID, story label and description, and let the developer group cards by phase or by user story. (traces: FR-007)

**AIS-008**: Offer the kanban view as a page reached from a link on the story's pages, grouped by phase unless the developer chooses to group by user story. (traces: FR-011)

**AIS-009**: Place each task in one of four columns: in progress for a `[~]` marker or an `(in progress)` tag, blocked for a `[!]` marker or a `(blocked)` tag, done when marked done, and backlog otherwise. (traces: FR-008)

**AIS-010**: Never change `tasks.md` or any other document from the kanban view. (traces: FR-009)

**AIS-011**: When a story has no `tasks.md` or an empty one, show a message that no tasks were found in place of the board. (traces: FR-010)

**AIS-012**: Check the file shown by an open document page or kanban view about every 10 seconds, refresh the page with the new content when the file's modified time has changed, keep the reader's position in a document and the kanban grouping, and when the file can no longer be read keep showing the last content and do not refresh. (traces: FR-012)

## Business Rules

<!-- The rules that govern behaviour, each traced to its functional requirement. -->

**AIS-013**: A code starting a heading or a bullet point introduces its form; a code in a table row introduces a form only under the table rule; discovered forms are per story. (traces: REQ-002, REQ-006, REQ-009)

**AIS-014**: A task carrying both an in progress and a blocked marker or tag goes in the blocked column. (traces: FR-008)

## Technical Decisions

<!-- The approved decisions, each with the constraint it imposes: `**AIS-003**: Analysis runs asynchronously in a worker. (traces: DEC-001)`. -->

**AIS-015**: Find a story's code prefixes in a first pass over its documents at every request, use the fixed list plus those prefixes for definitions and reference marking, and store nothing. (traces: DEC-001)

**AIS-016**: Serve the kanban as a server-rendered page at `GET /specs/<story>/kanban`, grouped by phase by default or by user story with `?group=story`, reading `tasks.md` on each build and writing nothing. (traces: DEC-002)

**AIS-017**: Parse `tasks.md` with a dedicated line parser separate from the Markdown renderer: a `## ` heading starts a phase, a `- [mark] T### …` line is a card, blocked wins over in progress, and the `[USn]` tag gives the story label. (traces: DEC-003)

**AIS-018**: Keep the parsed cards of each story's `tasks.md` in memory with the file's modified time and parse again only when that time changes; every open document and kanban page checks its file's modified time every 10 seconds and reloads when it changed, a document keeping the scroll position and the board keeping its grouping. (traces: DEC-004)

## Architectural Constraints

<!-- Boundaries the agent must respect: what may depend on what, and where things live. -->

**AIS-019**: Keep one Python process, the viewer server, serving pages to the viewer page, with no new data store, process or network dependency. (traces: ART-004, DEC-004)

**AIS-020**: Run on Python 3.11 or later with only the standard library, started the same way as before. (traces: DEC-001, DEC-002)

**AIS-021**: Put the discovery pass in the story index and the marking in the reference marker; put the kanban parser, board cache and kanban page in the viewer server; put the page refresher in the viewer page. (traces: ART-005, ART-008)

## Existing Code

<!-- Existing files, modules and patterns to reuse or follow, and those not to follow. If the story is wholly new, list this section under Not applicable. -->

**AIS-022**: Extend `StoryIndex` and `find_definitions` in `specview.py` so the definition rules use the fixed prefix list plus the discovered prefixes; keep the fixed list and the existing error behaviour unchanged. (traces: DEC-001, FR-004)

**AIS-023**: Add the kanban route and the stamp route to the request handling in `specview.py` behind the existing `Host` header check and `PathGuard`, and leave the existing routes and their responses unchanged. (traces: DEC-002, DEC-004, FR-009)

**AIS-024**: The task format is read in two places, the kanban parser and the existing task-definition rule, so update both together if the format changes. (traces: DEC-003)

## Interfaces

<!-- Endpoints, operations, messages and their contracts, from the approved design. -->

**AIS-025**: `GET /api/stamp?path=<path under specs/>` returns JSON `{"stamp": <modified time of that file, or null when it cannot be read>}` through the same `Host` check and path guard, and refuses a path outside `specs/` with `403`. (traces: DEC-004, FR-012)

**AIS-026**: `GET /specs/<story>/kanban` returns the HTML board grouped by phase; `?group=story` groups by user story and any other value falls back to phase; it is refused with `403` and `404` in the same cases as every other path. (traces: DEC-002, FR-007, FR-011)

**AIS-027**: Tasks with no phase heading, or with no `[USn]` tag when grouped by user story, go in a group called Unallocated. (traces: DEC-002, FR-007)

**AIS-028**: Every page of a story carries a menu listing its documents and the kanban board. (traces: FR-011)

## Data Structures

<!-- Entities, fields, keys and relationships, from the approved design. -->

**AIS-029**: A card holds a task ID, a story label, a description, its phase and its column (backlog, in progress, blocked or done), derived from the task line and never written back. (traces: FR-007, FR-008, DEC-003)

## Testing Requirements

<!-- What must be tested, at which level, and how each is verified. -->

**AIS-030**: Unit tests: prefix discovery from a heading, a bullet and a table row, and a back-reference table that introduces nothing; the kanban parser for each mark, tag and the blocked-over-in-progress tie; grouping by phase and by user story. (traces: FR-001, FR-002, FR-007, FR-008)

**AIS-031**: Integration tests: a code introduced in one document and referenced in another is marked with the hover and click behaviour; the same code in a different story is not marked; an undefined or ambiguous code of a discovered form shows the error. (traces: FR-003, FR-004, FR-005)

**AIS-032**: End to end tests: request the kanban route for a story with tasks, with an empty `tasks.md` and with none, and confirm `tasks.md` is unchanged afterwards. (traces: FR-006, FR-009, FR-010)

**AIS-033**: Refresh tests: change a document or `tasks.md` while its page is open and confirm the new content shows within about 10 seconds with the scroll position and grouping kept; leave it unchanged and confirm no reload and, for the board, no re-parse; remove the file and confirm the page keeps its last content. (traces: FR-012, NFR-001, DEC-004)

## Security Requirements

<!-- Authentication, authorisation, secrets and sensitive-data rules the implementation must meet. -->

**AIS-034**: Send the new routes through the same `Host` header check and path guard as every other request so they read only inside `specs/`; refuse a wrong `Host` header and a path outside `specs/`. (traces: DEC-002, DEC-004)

**AIS-035**: Only read files; write nothing. (traces: FR-009)

**AIS-036**: HTML-escape task descriptions and story labels before putting them on the page. (traces: DEC-002, DEC-003)

## Edge Cases

<!-- Known edge cases and the behaviour required for each. -->

**AIS-037**: A missing, empty or unreadable `tasks.md` shows the no-tasks message and does not fail the request. (traces: FR-010, DEC-003)

**AIS-038**: Ignore a line in `tasks.md` that does not match the task pattern so one malformed line does not hide the other cards. (traces: DEC-003)

**AIS-039**: When the shown file can no longer be read, the stamp is null and the page keeps its last content. (traces: FR-012, DEC-004)

## Explicit Exclusions

<!-- What must not be built or changed, from the approved scope. -->

**AIS-040**: Do not make the kanban view change `tasks.md` or any other document, and do not write anything to the project. (traces: FR-009, REQ-007)

**AIS-041**: Do not cache discovered prefixes or carry them between stories, and do not set a limit on the discovery pass. (traces: DEC-001, FR-005)

## Implementation Constraints

<!-- Performance limits, compatibility, migration and rollout constraints. -->

**AIS-042**: Ship as a change to `specview.py` with no data migration or configuration; rollback is reverting the script. (traces: DEC-001, DEC-002)

**AIS-043**: Each open page adds one request every 10 seconds that only checks a file's modified time. (traces: FR-012, DEC-004)

**AIS-044**: Update the README to describe the kanban view and the automatic refresh. (traces: FR-006, FR-012)

## Artefacts in Scope

<!--
  The approved diagrams and wireframes the agent must read, each as an item tracing to its ART id.
  A wireframe, ER diagram or technical sequence diagram listed here must be covered by a task.

  **AIS-013**: Read the container view before changing the API. (traces: ART-004)
-->

**AIS-045**: Read the container view before changing the server or the page. (traces: ART-004)

**AIS-046**: Read the viewer server component view before changing the story index, the reference marker, the kanban parser, the board cache, the kanban page or the request handler. (traces: ART-005)

**AIS-047**: Read the viewer page component view before adding the page refresher. (traces: ART-008)

**AIS-048**: Read the sequence diagram for following a newly introduced code before changing discovery or marking. (traces: ART-006)

**AIS-049**: Read the sequence diagram for checking build progress before changing the kanban route, parser or refresh. (traces: ART-007)

**AIS-050**: Read the system context diagram for the people and systems around the viewer. (traces: ART-001)

**AIS-051**: Read the functional sequence diagrams for the two use cases. (traces: ART-002, ART-003)

## Agent Guidance

<!-- Optional. Relevant files and directories, existing patterns to follow, commands and tests to run, constraints on modification. Delete this section if unused. -->

## Not applicable

<!-- Sections removed from this document, each with its reason: `- Existing Code: a new component`. -->

- Agent Guidance: nothing beyond the sections above.

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
    "AIS-001": {
      "hash": "sha256:e945959400e16b4ff3de439ea4a5f4f3616474cf08d507206d0142e277dd09b5",
      "class": "restated",
      "cites": {
        "FR-001": "sha256:383f9296ff6a52d4e4c18607d174c816a95c9866b401c32d2b1194eb13a9b02c"
      }
    },
    "AIS-002": {
      "hash": "sha256:5019706629fce1459cbfc5c6ca17e3fb6a1a567e30c87173bc3fc90a8502e294",
      "class": "restated",
      "cites": {
        "FR-002": "sha256:ed7dcf7ed5c6ad99f53a01c0ec96df80de21351bd839845b0ed6f1eef2a95ac7"
      }
    },
    "AIS-003": {
      "hash": "sha256:9fa5829481906405ae54b0536f5600a0688ca69055883f40c7eaebfeb9c65983",
      "class": "restated",
      "cites": {
        "FR-003": "sha256:6f18dad4de22e5bf0feddcabd830ff23d873cb8dbf764edb96567d43b43cd668"
      }
    },
    "AIS-004": {
      "hash": "sha256:f799df77d1abb5ac97abbf3b39ece3f9342216a1185f4505b49fa77179278cd3",
      "class": "restated",
      "cites": {
        "FR-004": "sha256:2ae3eb4329aaec539cf2ad43395016234b0a1d74b69470992d5519897e9b382f"
      }
    },
    "AIS-005": {
      "hash": "sha256:7a396a20f425e8c960f3a5029e88f8a3666ab5a0606c3e66a44d91b6ee96a275",
      "class": "restated",
      "cites": {
        "FR-005": "sha256:4fd4014add1830d59d7445913099f5dd61577b4ec75fcd6902f24418f440d04d"
      }
    },
    "AIS-006": {
      "hash": "sha256:6e7e7098491cf25f1f5df4ccaabf0aa43bdfe093326f80c534f7b9e61d75c2da",
      "class": "restated",
      "cites": {
        "FR-006": "sha256:81abe569717adc55e2ea4a635ebadcc9268825b269a820b6259f8c2d3580709a"
      }
    },
    "AIS-007": {
      "hash": "sha256:5187e8b721a6f85619c7f8ef2751c4b83c2c9665b7f731258e56cba32bbdca1c",
      "class": "restated",
      "cites": {
        "FR-007": "sha256:a1b8235dbe5caad9d3c19f5344e9e629dfe07c2ba8ee6f358a2296174454ae28"
      }
    },
    "AIS-008": {
      "hash": "sha256:e977b028f05ce0aa62d9341bce97d9ccaaf1b3552c1e4b013b25a558a52cdccc",
      "class": "restated",
      "cites": {
        "FR-011": "sha256:faf836f7ec7f293517c93343e6f61f8d0ff39875f6a9c4fcf4e570f136a028ec"
      }
    },
    "AIS-009": {
      "hash": "sha256:7b8dfc99da4e3d117d27a8744f5781f25be87c9abd49efa0999312363e73330f",
      "class": "restated",
      "cites": {
        "FR-008": "sha256:b5f49e91e9db1d61276c75c1959d4e30f9d2a96b7a5354e4bf23c554d7e6fcab"
      }
    },
    "AIS-010": {
      "hash": "sha256:c76ef3161e1efe0818473324abf3fb03546cccce4772d6006a6f5acd3acd8ed9",
      "class": "restated",
      "cites": {
        "FR-009": "sha256:2f4e357e7c45afc0535ca51280ef4a6cb662efea2c188887a76a8e0bbf79f79c"
      }
    },
    "AIS-011": {
      "hash": "sha256:ace5f9fb8935db7f276be0ab1cc02f4d73f8a147a44bd1031daace92c2605a91",
      "class": "restated",
      "cites": {
        "FR-010": "sha256:f297709714ffd46f93f7abf23c9ebea1294efd150bd16b280ccbcedbc0bffd3c"
      }
    },
    "AIS-012": {
      "hash": "sha256:d7c2c4c3bf48318481866ac34969ce229af12e8da9c157092edaeb7b16c115a0",
      "class": "restated",
      "cites": {
        "FR-012": "sha256:c45b0cea6084477d35f71746737ceb52e6c4bb25a3d53d5867516cbcb168058b"
      }
    },
    "AIS-013": {
      "hash": "sha256:4594c9e74124ed7d1a2533729f830a57064a729f58de54f665358730af534fae",
      "class": "restated",
      "cites": {
        "REQ-002": "sha256:9be8cbf31c66cda1de24eb6018e9793bc3124a9883583b70cee59847b13ca3a5",
        "REQ-006": "sha256:859e9801daa175a7b2b81fda318548d186d0568e0b2a1241b2ae4cdfae93648f",
        "REQ-009": "sha256:2acb805067e30d87ac45c5f1d0d4a41128a107a4cef12c892e0cf612bda9d42c"
      }
    },
    "AIS-014": {
      "hash": "sha256:0b9acb87fcb44ef42a60311b7cb1baffd2c46c7cfcab9ee4b0ae9622b68a1042",
      "class": "restated",
      "cites": {
        "FR-008": "sha256:b5f49e91e9db1d61276c75c1959d4e30f9d2a96b7a5354e4bf23c554d7e6fcab"
      }
    },
    "AIS-015": {
      "hash": "sha256:3cd8a63029947a310a5e2360eafe83a9a604cca723a2751a4e43b6766cf43b84",
      "class": "restated",
      "cites": {
        "DEC-001": "sha256:13a2732b598fcb0a7a620f1cc017318a750024235d9ca1453803f7f35b0ddedd"
      }
    },
    "AIS-016": {
      "hash": "sha256:8ec6c8ae19f260077bd25aa927135e54748ce590567e8645231d75ec3391e82e",
      "class": "restated",
      "cites": {
        "DEC-002": "sha256:450de9b1737c8d785caca57c0b3cc522aed8898e9dcea2c8c953f697e1d03aa3"
      }
    },
    "AIS-017": {
      "hash": "sha256:9dd0669614eaa47d12926b51126a209c16509140ef159f4a5e25fc0af8dd0448",
      "class": "restated",
      "cites": {
        "DEC-003": "sha256:a9f99d3c520b3fe486f6f8103e542d28fb3a7c31a82c82665be1893726556d9d"
      }
    },
    "AIS-018": {
      "hash": "sha256:3798cc9f0d4a1cdbed1b2269788519e78710776d78a91dbc570f3e35755b6cd0",
      "class": "restated",
      "cites": {
        "DEC-004": "sha256:942ab4072dd367c7cc88758bbd6df350e7ce92e76ea93688853324c207fbf0a3"
      }
    },
    "AIS-019": {
      "hash": "sha256:dfb9a447f2d02858af8946ec06cf6a158d658fe2c2219237be8f02f2d2e263f0",
      "class": "restated",
      "cites": {
        "ART-004": "sha256:4b39c4b13aeb75a9f406bf14f4086f90145e8c067318a8d9c7117bc59ad99bed",
        "DEC-004": "sha256:942ab4072dd367c7cc88758bbd6df350e7ce92e76ea93688853324c207fbf0a3"
      }
    },
    "AIS-020": {
      "hash": "sha256:e792b4a4a920a6bdf2cb366532d191fc7d77923ec5117256f533221efcbf9fba",
      "class": "restated",
      "cites": {
        "DEC-001": "sha256:13a2732b598fcb0a7a620f1cc017318a750024235d9ca1453803f7f35b0ddedd",
        "DEC-002": "sha256:450de9b1737c8d785caca57c0b3cc522aed8898e9dcea2c8c953f697e1d03aa3"
      }
    },
    "AIS-021": {
      "hash": "sha256:9f239571158cf52fe9584c85b73953cfad90dd8e8b5b465d113984417fc1c77d",
      "class": "restated",
      "cites": {
        "ART-005": "sha256:ddc99a0e777eeefe57010caa1355dd2acd061ede1711db2f440d2a061dbb0e06",
        "ART-008": "sha256:952782963b9d2dcd8083c0acbf50df86010fad0435552f9058625f9c8d4feb51"
      }
    },
    "AIS-022": {
      "hash": "sha256:ab5ce28ac559e901fe5c95fe6fd6ae950c73e001151eb72863745800f745e7f6",
      "class": "inferred",
      "adds": "Names the existing StoryIndex and find_definitions in specview.py as the code to extend.",
      "reviewed": {
        "by": "Lee Sinclair",
        "at": "2026-10-17T02:54:24Z",
        "list": "RVW-010",
        "reply": "yes"
      },
      "sources": {
        "DEC-001": "sha256:13a2732b598fcb0a7a620f1cc017318a750024235d9ca1453803f7f35b0ddedd",
        "FR-004": "sha256:2ae3eb4329aaec539cf2ad43395016234b0a1d74b69470992d5519897e9b382f"
      }
    },
    "AIS-023": {
      "hash": "sha256:0141e7767e1a4a670dd0aa1cc28dd78787d47eec46f8f3f37ecff3712c9f090c",
      "class": "inferred",
      "adds": "Names the request handling in specview.py and the existing PathGuard as where the routes go.",
      "reviewed": {
        "by": "Lee Sinclair",
        "at": "2026-10-17T02:54:24Z",
        "list": "RVW-010",
        "reply": "yes"
      },
      "sources": {
        "DEC-002": "sha256:450de9b1737c8d785caca57c0b3cc522aed8898e9dcea2c8c953f697e1d03aa3",
        "DEC-004": "sha256:942ab4072dd367c7cc88758bbd6df350e7ce92e76ea93688853324c207fbf0a3",
        "FR-009": "sha256:2f4e357e7c45afc0535ca51280ef4a6cb662efea2c188887a76a8e0bbf79f79c"
      }
    },
    "AIS-024": {
      "hash": "sha256:eceb65f1b56cb5f9df5cfd8b0674ab23b5308036e29a2ea9a6d0a2bcc5c9914e",
      "class": "restated",
      "cites": {
        "DEC-003": "sha256:a9f99d3c520b3fe486f6f8103e542d28fb3a7c31a82c82665be1893726556d9d"
      }
    },
    "AIS-025": {
      "hash": "sha256:a1dd7661e9b9404a6bd63366611eb673cf941680d96e04ef0846d8fcf81622b4",
      "class": "restated",
      "cites": {
        "DEC-004": "sha256:942ab4072dd367c7cc88758bbd6df350e7ce92e76ea93688853324c207fbf0a3",
        "FR-012": "sha256:c45b0cea6084477d35f71746737ceb52e6c4bb25a3d53d5867516cbcb168058b"
      }
    },
    "AIS-026": {
      "hash": "sha256:8bf6eff2311fa1e0e4d626c709d3b76eae0fe296de11edf30743278b630c8313",
      "class": "restated",
      "cites": {
        "DEC-002": "sha256:450de9b1737c8d785caca57c0b3cc522aed8898e9dcea2c8c953f697e1d03aa3",
        "FR-007": "sha256:a1b8235dbe5caad9d3c19f5344e9e629dfe07c2ba8ee6f358a2296174454ae28",
        "FR-011": "sha256:faf836f7ec7f293517c93343e6f61f8d0ff39875f6a9c4fcf4e570f136a028ec"
      }
    },
    "AIS-027": {
      "hash": "sha256:ea1fe8e036f535a3ed85f1391bf58e178d52867f4213716914eeb0162d861a54",
      "class": "restated",
      "cites": {
        "DEC-002": "sha256:450de9b1737c8d785caca57c0b3cc522aed8898e9dcea2c8c953f697e1d03aa3",
        "FR-007": "sha256:a1b8235dbe5caad9d3c19f5344e9e629dfe07c2ba8ee6f358a2296174454ae28"
      }
    },
    "AIS-028": {
      "hash": "sha256:042d43d67bcce8ee2226c2d661a302a05e3a8af1610fd8fd57511e004960ec75",
      "class": "restated",
      "cites": {
        "FR-011": "sha256:faf836f7ec7f293517c93343e6f61f8d0ff39875f6a9c4fcf4e570f136a028ec"
      }
    },
    "AIS-029": {
      "hash": "sha256:becd651ddfc64bf81b82fe6708e067880c4955048fcb9d5e5a4e1a74367d5cb2",
      "class": "inferred",
      "adds": "Names the existing StoryIndex and find_definitions in specview.py as the code to extend.",
      "reviewed": {
        "by": "Lee Sinclair",
        "at": "2026-10-17T02:54:24Z",
        "list": "RVW-010",
        "reply": "yes"
      },
      "sources": {
        "FR-007": "sha256:a1b8235dbe5caad9d3c19f5344e9e629dfe07c2ba8ee6f358a2296174454ae28",
        "FR-008": "sha256:b5f49e91e9db1d61276c75c1959d4e30f9d2a96b7a5354e4bf23c554d7e6fcab",
        "DEC-003": "sha256:a9f99d3c520b3fe486f6f8103e542d28fb3a7c31a82c82665be1893726556d9d"
      }
    },
    "AIS-030": {
      "hash": "sha256:885fdd8c923445091f587b09f7d8d7116e67fb916bfce8cb59811d4bc6e5e2f0",
      "class": "inferred",
      "adds": "Names specview.py request handling and PathGuard as where the routes go.",
      "reviewed": {
        "by": "Lee Sinclair",
        "at": "2026-10-17T02:54:24Z",
        "list": "RVW-010",
        "reply": "yes"
      },
      "sources": {
        "FR-001": "sha256:383f9296ff6a52d4e4c18607d174c816a95c9866b401c32d2b1194eb13a9b02c",
        "FR-002": "sha256:ed7dcf7ed5c6ad99f53a01c0ec96df80de21351bd839845b0ed6f1eef2a95ac7",
        "FR-007": "sha256:a1b8235dbe5caad9d3c19f5344e9e629dfe07c2ba8ee6f358a2296174454ae28",
        "FR-008": "sha256:b5f49e91e9db1d61276c75c1959d4e30f9d2a96b7a5354e4bf23c554d7e6fcab"
      }
    },
    "AIS-031": {
      "hash": "sha256:85752c68b1544f6898725927e601b2ed8496f9739b46c7dbac0c2d2d21acf62d",
      "class": "restated",
      "cites": {
        "FR-003": "sha256:6f18dad4de22e5bf0feddcabd830ff23d873cb8dbf764edb96567d43b43cd668",
        "FR-004": "sha256:2ae3eb4329aaec539cf2ad43395016234b0a1d74b69470992d5519897e9b382f",
        "FR-005": "sha256:4fd4014add1830d59d7445913099f5dd61577b4ec75fcd6902f24418f440d04d"
      }
    },
    "AIS-032": {
      "hash": "sha256:2852fd2521d685cd4d070c48f9ae2bf002eb0fe24ebb93edf45cd6ed71208b72",
      "class": "restated",
      "cites": {
        "FR-006": "sha256:81abe569717adc55e2ea4a635ebadcc9268825b269a820b6259f8c2d3580709a",
        "FR-009": "sha256:2f4e357e7c45afc0535ca51280ef4a6cb662efea2c188887a76a8e0bbf79f79c",
        "FR-010": "sha256:f297709714ffd46f93f7abf23c9ebea1294efd150bd16b280ccbcedbc0bffd3c"
      }
    },
    "AIS-033": {
      "hash": "sha256:1384d3251da72858bb2a104fd7ef3dae18ee70787bf5fc4b6b74b4beae5b1f1c",
      "class": "restated",
      "cites": {
        "FR-012": "sha256:c45b0cea6084477d35f71746737ceb52e6c4bb25a3d53d5867516cbcb168058b",
        "NFR-001": "sha256:3131ccae52047de8b10a4105b89cdfc6b05b5b23f14b57040ff773ac24431f08",
        "DEC-004": "sha256:942ab4072dd367c7cc88758bbd6df350e7ce92e76ea93688853324c207fbf0a3"
      }
    },
    "AIS-034": {
      "hash": "sha256:0b93a6c4055241f189d66b4b0114039979917c050411cc2afe951ce3ee4d2b3a",
      "class": "restated",
      "cites": {
        "DEC-002": "sha256:450de9b1737c8d785caca57c0b3cc522aed8898e9dcea2c8c953f697e1d03aa3",
        "DEC-004": "sha256:942ab4072dd367c7cc88758bbd6df350e7ce92e76ea93688853324c207fbf0a3"
      }
    },
    "AIS-035": {
      "hash": "sha256:0ab4f5f1259c5bcc6e20731abca38b90e4ee5c4fca507f03ecd2f1974e022f8b",
      "class": "restated",
      "cites": {
        "FR-009": "sha256:2f4e357e7c45afc0535ca51280ef4a6cb662efea2c188887a76a8e0bbf79f79c"
      }
    },
    "AIS-036": {
      "hash": "sha256:24faaad353cca6eee26bba8fa653c030694acb46b71e7c4dcc7f0aa8b3eff8f5",
      "class": "restated",
      "cites": {
        "DEC-002": "sha256:450de9b1737c8d785caca57c0b3cc522aed8898e9dcea2c8c953f697e1d03aa3",
        "DEC-003": "sha256:a9f99d3c520b3fe486f6f8103e542d28fb3a7c31a82c82665be1893726556d9d"
      }
    },
    "AIS-037": {
      "hash": "sha256:a46faccd82a3a075675c2200a988e90ab8cde988b2f6cfbd9c173751e22c8ef3",
      "class": "restated",
      "cites": {
        "FR-010": "sha256:f297709714ffd46f93f7abf23c9ebea1294efd150bd16b280ccbcedbc0bffd3c",
        "DEC-003": "sha256:a9f99d3c520b3fe486f6f8103e542d28fb3a7c31a82c82665be1893726556d9d"
      }
    },
    "AIS-038": {
      "hash": "sha256:322e03ab76e9bd715ddd15c001c0943825ccb079680669c1562aae38e982a429",
      "class": "restated",
      "cites": {
        "DEC-003": "sha256:a9f99d3c520b3fe486f6f8103e542d28fb3a7c31a82c82665be1893726556d9d"
      }
    },
    "AIS-039": {
      "hash": "sha256:92f92676fc4b6d891601ba7f91b65ccaf2726cbfc2a71cc421154597fefce0dc",
      "class": "restated",
      "cites": {
        "FR-012": "sha256:c45b0cea6084477d35f71746737ceb52e6c4bb25a3d53d5867516cbcb168058b",
        "DEC-004": "sha256:942ab4072dd367c7cc88758bbd6df350e7ce92e76ea93688853324c207fbf0a3"
      }
    },
    "AIS-040": {
      "hash": "sha256:bb79051dcb607067c04bd5d6e7afda9d9ce9589bd542c163a93eec91c169ea1b",
      "class": "restated",
      "cites": {
        "FR-009": "sha256:2f4e357e7c45afc0535ca51280ef4a6cb662efea2c188887a76a8e0bbf79f79c",
        "REQ-007": "sha256:f510a28f216be7dedb6d892aeaf8f92e1f99cbacc3300e721fbbfd7d5690abe6"
      }
    },
    "AIS-041": {
      "hash": "sha256:d4c8c76d709d245432beb2646da2f417e393dc69f46f5fc5298886f8021f6935",
      "class": "restated",
      "cites": {
        "DEC-001": "sha256:13a2732b598fcb0a7a620f1cc017318a750024235d9ca1453803f7f35b0ddedd",
        "FR-005": "sha256:4fd4014add1830d59d7445913099f5dd61577b4ec75fcd6902f24418f440d04d"
      }
    },
    "AIS-042": {
      "hash": "sha256:9fd23817168dd25e5375c3b318972507b91ed0d5d998412ee068842c67982de2",
      "class": "restated",
      "cites": {
        "DEC-001": "sha256:13a2732b598fcb0a7a620f1cc017318a750024235d9ca1453803f7f35b0ddedd",
        "DEC-002": "sha256:450de9b1737c8d785caca57c0b3cc522aed8898e9dcea2c8c953f697e1d03aa3"
      }
    },
    "AIS-043": {
      "hash": "sha256:ccfbc623efb904d0d27f4bd25095a49ae3d2cf6d444ec1cf3ce9d6cecfc4672d",
      "class": "restated",
      "cites": {
        "FR-012": "sha256:c45b0cea6084477d35f71746737ceb52e6c4bb25a3d53d5867516cbcb168058b",
        "DEC-004": "sha256:942ab4072dd367c7cc88758bbd6df350e7ce92e76ea93688853324c207fbf0a3"
      }
    },
    "AIS-044": {
      "hash": "sha256:87e460dfc8f47e25f60139d2b9e5d5deab11df551a6e6c48eef3617c3c92605b",
      "class": "restated",
      "cites": {
        "FR-006": "sha256:81abe569717adc55e2ea4a635ebadcc9268825b269a820b6259f8c2d3580709a",
        "FR-012": "sha256:c45b0cea6084477d35f71746737ceb52e6c4bb25a3d53d5867516cbcb168058b"
      }
    },
    "AIS-045": {
      "hash": "sha256:90fc41ca86fcc46029f9fc3a25dea01e05ab96a4eceb9e84dea7bb4763bc2f17",
      "class": "restated",
      "cites": {
        "ART-004": "sha256:4b39c4b13aeb75a9f406bf14f4086f90145e8c067318a8d9c7117bc59ad99bed"
      }
    },
    "AIS-046": {
      "hash": "sha256:6401c8c2dd27acb00de629b59dea228e4898bdffb499e19cc56b2ba6bf28b826",
      "class": "restated",
      "cites": {
        "ART-005": "sha256:ddc99a0e777eeefe57010caa1355dd2acd061ede1711db2f440d2a061dbb0e06"
      }
    },
    "AIS-047": {
      "hash": "sha256:1adc7d40779a72fbc721e00b57796b1cfe5df704eff1b95b7a716506da55f4f2",
      "class": "restated",
      "cites": {
        "ART-008": "sha256:952782963b9d2dcd8083c0acbf50df86010fad0435552f9058625f9c8d4feb51"
      }
    },
    "AIS-048": {
      "hash": "sha256:1cf5b967568ab5ec960721f3fc4f1f914175674f1ddbae11f65f676838a843a2",
      "class": "restated",
      "cites": {
        "ART-006": "sha256:295316b3f91e78fc07ccec63c7dc4ff5d3e4e70575de34d2bb3fc5bb198878b5"
      }
    },
    "AIS-049": {
      "hash": "sha256:ed325d882cb09b86163a1e46f6d5139f20b3cf1857fac4e384e1d4d5ced9b4b5",
      "class": "restated",
      "cites": {
        "ART-007": "sha256:e235f1fce07d44c485bfb4c27d046a24339b14a74bb0da9185ddd1d23a0826f6"
      }
    },
    "AIS-050": {
      "hash": "sha256:60711b8b7423e12ab4d5f8233964b3198f3390092f385645c32164919a2212a2",
      "class": "restated",
      "cites": {
        "ART-001": "sha256:86c8f49df2bedd958e24bdebfd6c865e8b7acb3fa4623c080e1f4cf2df07186f"
      }
    },
    "AIS-051": {
      "hash": "sha256:42debc00d8ab2f81a9539e76e4b89602e85a7d814b562aceb30c19003eb91a60",
      "class": "restated",
      "cites": {
        "ART-002": "sha256:c302fdf2c8655eae84364c8c97a62113be43940a14189c5eda58d113efaa79e4",
        "ART-003": "sha256:e18e9bad6486683ffa1630f1c82cef39eb92d8e28225334b6a9f8312f5a8bbe2"
      }
    },
    "Not applicable#fcc96d1c4cf4": {
      "hash": "sha256:fcc96d1c4cf4217bc9561944a6504e081dcd82cff1d06b44723bb6b28655f49a",
      "reviewed": {
        "by": "Lee Sinclair",
        "at": "2026-10-17T02:54:24Z",
        "list": "RVW-010",
        "reply": "yes"
      },
      "class": "inferred"
    }
  },
  "acceptances": [
    {
      "id": "RVW-010",
      "stage": "ai-spec",
      "kind": "inferred",
      "digest": "sha256:97fabad5d8e58c691c847707cf54d9fbb05f4767ae7397e2bc7784acc9f41b63",
      "by": "Lee Sinclair",
      "at": "2026-10-17T02:54:24Z",
      "reply": "yes",
      "accepted": [
        "AIS-022",
        "AIS-023",
        "AIS-029",
        "AIS-030",
        "Not applicable#fcc96d1c4cf4"
      ],
      "except": [],
      "questioned": [],
      "reopened": [],
      "reason": null,
      "hashes": {
        "AIS-022": "sha256:ab5ce28ac559e901fe5c95fe6fd6ae950c73e001151eb72863745800f745e7f6",
        "AIS-023": "sha256:0141e7767e1a4a670dd0aa1cc28dd78787d47eec46f8f3f37ecff3712c9f090c",
        "AIS-029": "sha256:becd651ddfc64bf81b82fe6708e067880c4955048fcb9d5e5a4e1a74367d5cb2",
        "AIS-030": "sha256:885fdd8c923445091f587b09f7d8d7116e67fb916bfce8cb59811d4bc6e5e2f0",
        "Not applicable#fcc96d1c4cf4": "sha256:fcc96d1c4cf4217bc9561944a6504e081dcd82cff1d06b44723bb6b28655f49a"
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
  "stage": "ai-spec",
  "evaluated_at": "2026-10-17T02:53:15Z",
  "fingerprint": "sha256:5327ee068cfb913247dc784c05aa8989b2f2036cf34bb138d2ed8aeb88cf193b",
  "criteria": [
    {
      "id": "AIS-G01",
      "kind": "structural",
      "status": "met",
      "reason": ""
    },
    {
      "id": "AIS-G02",
      "kind": "traceability",
      "status": "met",
      "reason": ""
    },
    {
      "id": "AIS-G03",
      "kind": "traceability",
      "status": "met",
      "reason": ""
    },
    {
      "id": "AIS-G04",
      "kind": "traceability",
      "status": "met",
      "reason": ""
    },
    {
      "id": "AIS-G05",
      "kind": "structural",
      "status": "met",
      "reason": ""
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
