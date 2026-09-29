<!--
  STAGE 5 OF THE DEFINITION PIPELINE: In what sequence, and on what structure?

  This document is `plan.md` as Spec Kit sees it (an alias of this file). It is derived from the
  approved Technical Specification and adds no architecture of its own.

  - Every `##` section names, in its heading, the approved decision it derives from:
    `## Summary (traces: DEC-001)`. Replace `DEC-###` with real ids of the Technical Specification.
  - Content that cannot be derived from an approved decision is not written; it is raised as a
    challenge or a question instead.
  - Gate: PLN-G01 and PLN-G02 (`eil check --stage plan`). The plan is not approved by a person.
-->

# Implementation Plan: Rich specification viewer

**Branch**: `001-rich-spec-viewer` | **Date**: 2026-09-29 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/001-rich-spec-viewer/spec.md` (the AI Specification, `s04-ai-spec.md`)

## Summary (traces: DEC-001, DEC-004)

Build a local viewer that shows the Markdown documents of Spec Kit stories as readable HTML pages. One Python script, `specview.py`, serves every page over HTTP and renders the requested document on each request, caching by the modification time and size of every document in the story (DEC-001). Reference codes are resolved when a page is rendered and the defining sections of the codes a page uses are embedded in it as JSON, so tooltips need no further request (DEC-004). Search is a glob match on the server (DEC-005), and Mermaid diagrams are drawn in the browser by `mermaid@11` from jsDelivr (DEC-003). [ai-draft]

## Technical Context (traces: DEC-001, DEC-002, DEC-003, DEC-006, DEC-007, DEC-008)

**Language/Version**: Python 3.11 or later (DEC-006); HTML, CSS and JavaScript (ES modules) in the page, inlined by the server (DEC-001). [ai-draft]

**Primary Dependencies**: Python standard library only: `http.server.ThreadingHTTPServer`, `pathlib`, `fnmatch`, `html`, `json`, `threading`, `urllib.parse`, `webbrowser`, `argparse` (DEC-001, DEC-005, DEC-006, DEC-007). In the page: `mermaid@11` from jsDelivr, the only outside script (DEC-003). [ai-draft]

**Storage**: None. In-memory render cache and story index only, lost when the viewer stops (DEC-001). [ai-draft]

**Testing**: `unittest` from the standard library for unit and integration tests; manual browser checks for tooltips, diagrams and readability (Technical Specification, Testing Strategy; DEC-006). [ai-draft]

**Target Platform**: The developer's machine (Linux, macOS or Windows with Python 3.11+) or a devcontainer, viewed in a current browser (DEC-006, DEC-008). [ai-draft]

**Project Type**: Single-script local web viewer (DEC-007). [ai-draft]

**Performance Goals**: No target is set by the approved stages; the Technical Specification expects a page to render well under a second for a few stories of up to about twenty documents each, and no parsing on a refresh of an unchanged story (DEC-001). [ai-draft]

**Constraints**: Nothing to install and no configuration (FR-017, DEC-007); bind to `127.0.0.1`, or `0.0.0.0` inside a container (DEC-008); answer only `localhost` and `127.0.0.1` Host headers; read only, never outside `<start>/specs` (DEC-001, DEC-008). [ai-draft]

**Scale/Scope**: One developer; a few stories of up to about twenty documents, each under a few hundred kilobytes (Technical Specification, Performance). [ai-draft]

## Constitution Check (traces: DEC-006)

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

`.specify/memory/constitution.md` is still the unfilled Spec Kit template: it states no principles, so there are no constitution gates to evaluate. The plan's constraints come from the approved Technical Specification (standard library only, DEC-006). **Result: pass (no gates).** Re-checked after Phase 1: pass. [ai-draft]

## Project Structure (traces: DEC-007, DEC-002, DEC-006)

### Documentation (this feature)

```text
specs/001-rich-spec-viewer/
├── s00-README.md … s04-ai-spec.md   # approved stages and the AI Specification
├── spec.md -> s04-ai-spec.md        # alias
├── plan.md -> s05-plan.md           # this file
├── research.md                      # Phase 0 output
├── data-model.md                    # Phase 1 output (in-memory structures)
├── quickstart.md                    # Phase 1 output (run and validation guide)
├── contracts/
│   ├── http.md                      # routes, status codes, search JSON, Host check
│   └── cli.md                       # command, flags, start-up output
└── tasks.md                         # Phase 2 output (/speckit-tasks, not created here)
```

### Source Code (repository root)

```text
specview.py                  # the whole viewer: server, renderer, index, search, inline CSS and JS (DEC-007)
tests/
├── unit/                    # unittest: parser, business rules, glob, path guard, Host check, detection
├── integration/             # unittest: start the server on a free port against a fixture project over HTTP
└── fixtures/
    └── project/specs/…      # fixture stories: links, copies, nested checklists/, specs/README.md, broken codes
```

**Structure Decision**: One script at the repository root, as DEC-007 decides, so the developer can copy it anywhere and run it with `python3 specview.py`. Tests use the standard library runner (`python3 -m unittest discover -s tests`), split into unit and integration as the Technical Specification's Testing Strategy describes; the fixture project gives the integration tests a known `specs/` tree. [ai-draft]

## Not applicable

- Complexity Tracking: the Constitution Check has no gates, so there is no violation to justify. [ai-draft]

## Challenges

<!-- Recorded by `eil challenge`. -->

## Overrides

<!-- Recorded by `eil override`, each naming who, what and why. -->

## Quality Assessment

<!-- eil:begin assessment -->
```json
{
  "stage": "plan",
  "evaluated_at": "2026-09-29T11:01:40Z",
  "fingerprint": "sha256:d72087dd30ffdac3f58e51852df02cea99b446988c3cd9e192a2345902634be3",
  "criteria": [
    {
      "id": "PLN-G01",
      "kind": "traceability",
      "status": "met",
      "reason": ""
    },
    {
      "id": "PLN-G02",
      "kind": "judgment",
      "status": "met",
      "reason": "AI assessment: The plan keeps the approved single-script server and in-page script (DEC-001, DEC-007) with no new container, component, store or integration; the tests/ layout follows the approved Testing Strategy."
    }
  ],
  "assessment": {
    "ambiguity": [],
    "missing": [],
    "contradictions": [],
    "unsupported_assumptions": [
      "research.md R-10 proposes concrete readability values (72ch column, about 1.6 line height, tooltip capped near 60% of viewport height) that no approved stage states",
      "contracts/cli.md adds behaviour not in the approved stages: an explicit --port fails when busy rather than falling back, and a Python older than 3.11 exits with a message",
      "contracts/http.md fixes presentation details not in the approved stages: anchor ids like fr-012 and a warning-sign icon for error codes"
    ],
    "untestable": []
  },
  "findings": []
}
```
<!-- eil:end assessment -->
