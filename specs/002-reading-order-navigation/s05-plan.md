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

# Implementation Plan: Reading-order navigation for story documents

**Branch**: `002-reading-order-navigation` (no branch created; the working tree is detached) | **Date**: 2026-10-01 | **Spec**: [spec.md](spec.md) (alias of `s04-ai-spec.md`)

**Input**: Approved Requirements, Functional, Technical and AI Specifications of this story.

## Summary (traces: DEC-001, DEC-002, DEC-004, DEC-006)

Every document under a story folder in `specs/<story>/` gets a "Documents in reading order" section at its bottom. `Viewer._render_document` builds it on the server from the files `Viewer._markdown_files` finds in the story (DEC-001, DEC-002), orders them with one sort key (DEC-004) and marks it up as a labelled `nav` with an ordered list (DEC-006). Documents directly under `specs/`, the folder navigation page and the search results get nothing. The change lives in `specview.py` and two new test files; nothing is added to the repository's dependencies.

## Technical Context (traces: DEC-001, DEC-002, DEC-007)

**Language/Version**: Python 3.11 or later, as `specview.py` already requires.

**Primary Dependencies**: None added. Standard library only (DEC-007).

**Storage**: N/A. The section is computed on each render; no data is stored (DEC-001).

**Testing**: `unittest`, run with `python3 -m unittest discover -s tests`. The 74 existing tests must keep passing (DEC-007).

**Target Platform**: The viewer's existing platform: a local HTTP server on `localhost` or `127.0.0.1`. Symbolic-link tests need an operating system that supports them (DEC-007).

**Project Type**: Single-file command-line web viewer.

**Performance Goals**: None stated beyond the existing page cache. One extra walk of the story folder per page render is accepted (DEC-002).

**Constraints**: Server-side only, no JavaScript needed and no new route (DEC-001); discovery and path checks go through `Viewer._markdown_files` and `PathGuard.resolve` (DEC-002); inline CSS only (DEC-006).

**Scale/Scope**: One story folder per page render; the number of documents in a story.

## Constitution Check (traces: DEC-001, DEC-002)

`.specify/memory/constitution.md` is the unfilled template: it has no ratified principles, so there are no constitution gates to evaluate. The approved decisions are the constraints this plan follows, and none is contradicted: no dependency, no new route, existing `Viewer` flow and `PathGuard` reused.

## Project Structure (traces: DEC-001, DEC-007)

### Documentation (this feature)

```text
specs/002-reading-order-navigation/
├── s00-README.md ... s05-plan.md   # the governed stages (plan.md is a link to s05-plan.md)
├── research.md                     # Phase 0 output
├── quickstart.md                   # Phase 1 output
└── s06-tasks.md                    # produced later by /speckit-tasks, not by this command
```

### Source Code (repository root)

```text
specview.py                         # changed: Viewer._render_document, new helpers for the
                                    #   sort key, alias recognition and section markup, CSS rules
tests/
├── unit/test_reading_order.py      # new (DEC-007)
└── integration/test_reading_order.py   # new (DEC-007)
```

**Structure Decision**: Keep the single-file layout and the existing `tests/unit` and `tests/integration` split. The pure rules (stage detection and labels, the sort key, alias recognition) are tested in `tests/unit`; the page, symbolic links and story isolation are tested through the real server, started as `tests/integration/support.py` does (DEC-007).

## Complexity Tracking (traces: DEC-001)

No constitution gate applies, so there is no violation to justify.

## Not applicable

<!-- Sections removed from this document, each with its reason. -->

- Data model (`data-model.md`): the design adds or changes no persistent data and no entity (DEC-001), so there is none to describe.
- Contracts (`contracts/`): the design adds no route, endpoint or other interface; the section is part of the existing page (DEC-001).

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
    "Implementation Plan: Reading-order navigation for story documents#50f94285e2f5": {
      "hash": "sha256:50f94285e2f55841309129cf71d2abb2b5864700e3f4583e54b4b6d9ffea0358",
      "class": "inferred",
      "adds": "Adds the date, the branch note (no branch created) and the link to the AI Specification alias.",
      "reviewed": {
        "by": "Lee Sinclair",
        "at": "2026-10-01T13:32:08Z",
        "list": "RVW-008",
        "reply": "Ok"
      }
    },
    "Implementation Plan: Reading-order navigation for story documents#243c03c94e26": {
      "hash": "sha256:243c03c94e26ed22f44ccaa4d35a254d9c6bdd0764b5fbebdb27491d11cdfef5",
      "class": "inferred",
      "adds": "Adds a statement of which approved stages the plan takes as input.",
      "reviewed": {
        "by": "Lee Sinclair",
        "at": "2026-10-01T13:32:08Z",
        "list": "RVW-008",
        "reply": "Ok"
      }
    },
    "§Summary": {
      "hash": "sha256:0d86cba3ead51560f9fb6b570c2ab4800e8de272a455eba116299bc827f744b1",
      "class": "restated",
      "cites": {
        "DEC-001": "sha256:bb921b2401109f1ece0e7a13243eaba9121b572231d2c6402f21a46830d083aa",
        "DEC-002": "sha256:e5e293b732dc3070124d2538a452ac15b148fb9937d58da144d4ee8d004b2032",
        "DEC-004": "sha256:7b10b4a428165cd28fee8fa2619828a86dc5bbf81c06f10415da597c69d300d7",
        "DEC-006": "sha256:39b03e67818d400e49ee296e2e3c28ac91daeaa69b23d14ab9a0ae88a080b5de"
      }
    },
    "§Technical Context": {
      "hash": "sha256:c65a4a737ce6cabda8c862ee5c863077a75d22df1c23f5b53007d45b3951fd5f",
      "class": "inferred",
      "adds": "Adds the Python 3.11 requirement, the 74-test baseline and the test command from the existing repository, and the platform, project type and scale descriptions.",
      "reviewed": {
        "by": "Lee Sinclair",
        "at": "2026-10-01T13:32:08Z",
        "list": "RVW-008",
        "reply": "Ok"
      },
      "sources": {
        "DEC-001": "sha256:bb921b2401109f1ece0e7a13243eaba9121b572231d2c6402f21a46830d083aa",
        "DEC-002": "sha256:e5e293b732dc3070124d2538a452ac15b148fb9937d58da144d4ee8d004b2032",
        "DEC-007": "sha256:c092606ae0d1acdb955329fb0999903f6b0219c952e9d0bbaa51fa3ef1b8ce76"
      }
    },
    "§Constitution Check": {
      "hash": "sha256:0b6f4b50647d555698f9f3e7079aaa314d7f54d0293206daf60141b49778cabc",
      "class": "inferred",
      "adds": "Adds the observation that the constitution file is an unfilled template with no gates.",
      "reviewed": {
        "by": "Lee Sinclair",
        "at": "2026-10-01T13:32:08Z",
        "list": "RVW-008",
        "reply": "Ok"
      },
      "sources": {
        "DEC-001": "sha256:bb921b2401109f1ece0e7a13243eaba9121b572231d2c6402f21a46830d083aa",
        "DEC-002": "sha256:e5e293b732dc3070124d2538a452ac15b148fb9937d58da144d4ee8d004b2032"
      }
    },
    "§Project Structure": {
      "hash": "sha256:244d7b0d80a4dac91a7c5ee2affe262ffc86ea2bf4c54fa135638b0957bfbda7",
      "class": "restated",
      "cites": {
        "DEC-001": "sha256:bb921b2401109f1ece0e7a13243eaba9121b572231d2c6402f21a46830d083aa",
        "DEC-007": "sha256:c092606ae0d1acdb955329fb0999903f6b0219c952e9d0bbaa51fa3ef1b8ce76"
      }
    },
    "Project Structure#9dcd8fb46501": {
      "hash": "sha256:9dcd8fb46501ffe652f7d61044cd969029ab4a1527cc52b57e2a6039c781f2ad",
      "class": "inferred",
      "adds": "Adds the listing of the story folder's documents and supporting files.",
      "reviewed": {
        "by": "Lee Sinclair",
        "at": "2026-10-01T13:32:08Z",
        "list": "RVW-008",
        "reply": "Ok"
      }
    },
    "Project Structure#603dcd581a03": {
      "hash": "sha256:603dcd581a033bf81718bd30f5e890c4ab7147e1630036928e40eb58a8f9684d",
      "class": "inferred",
      "adds": "Adds the source layout, including that new helper functions go in specview.py beside the changed method.",
      "reviewed": {
        "by": "Lee Sinclair",
        "at": "2026-10-01T13:32:08Z",
        "list": "RVW-008",
        "reply": "Ok"
      }
    },
    "Project Structure#0ee8393ecee8": {
      "hash": "sha256:0ee8393ecee80c5d45842b9f968ac2bc8f7dc3da54b8316f297dbda0fd4bccb5",
      "class": "inferred",
      "reviewed": {
        "by": "Lee Sinclair",
        "at": "2026-10-01T13:32:08Z",
        "list": "RVW-008",
        "reply": "Ok"
      }
    },
    "§Complexity Tracking": {
      "hash": "sha256:94a88a2cff6c245b4e33ebc068c97ee620510e790ac005d833335ee33beb40df",
      "class": "inferred",
      "adds": "Adds the statement that no constitution gate applies so nothing needs justifying.",
      "reviewed": {
        "by": "Lee Sinclair",
        "at": "2026-10-01T13:32:08Z",
        "list": "RVW-008",
        "reply": "Ok"
      },
      "sources": {
        "DEC-001": "sha256:bb921b2401109f1ece0e7a13243eaba9121b572231d2c6402f21a46830d083aa"
      }
    },
    "Not applicable#9f2bc07bb981": {
      "hash": "sha256:9f2bc07bb98146c0efffa9f55b504be92981e65f60e567074dc6f61690a8cf7b",
      "class": "inferred",
      "adds": "Adds the reasons the data model and contracts files are omitted.",
      "reviewed": {
        "by": "Lee Sinclair",
        "at": "2026-10-01T13:32:08Z",
        "list": "RVW-008",
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
      "id": "RVW-008",
      "stage": "plan",
      "kind": "inferred",
      "digest": "sha256:dbce53ec8cf46cce24315458651bfe04c144db6497b21d4a33a4eaad5e7aa8fe",
      "by": "Lee Sinclair",
      "at": "2026-10-01T13:32:08Z",
      "reply": "Ok",
      "accepted": [
        "Implementation Plan: Reading-order navigation for story documents#50f94285e2f5",
        "Implementation Plan: Reading-order navigation for story documents#243c03c94e26",
        "§Technical Context",
        "§Constitution Check",
        "Project Structure#9dcd8fb46501",
        "Project Structure#603dcd581a03",
        "Project Structure#0ee8393ecee8",
        "§Complexity Tracking",
        "Not applicable#9f2bc07bb981"
      ],
      "except": [],
      "questioned": [],
      "reopened": [],
      "reason": null,
      "hashes": {
        "Implementation Plan: Reading-order navigation for story documents#50f94285e2f5": "sha256:50f94285e2f55841309129cf71d2abb2b5864700e3f4583e54b4b6d9ffea0358",
        "Implementation Plan: Reading-order navigation for story documents#243c03c94e26": "sha256:243c03c94e26ed22f44ccaa4d35a254d9c6bdd0764b5fbebdb27491d11cdfef5",
        "§Technical Context": "sha256:c65a4a737ce6cabda8c862ee5c863077a75d22df1c23f5b53007d45b3951fd5f",
        "§Constitution Check": "sha256:0b6f4b50647d555698f9f3e7079aaa314d7f54d0293206daf60141b49778cabc",
        "Project Structure#9dcd8fb46501": "sha256:9dcd8fb46501ffe652f7d61044cd969029ab4a1527cc52b57e2a6039c781f2ad",
        "Project Structure#603dcd581a03": "sha256:603dcd581a033bf81718bd30f5e890c4ab7147e1630036928e40eb58a8f9684d",
        "Project Structure#0ee8393ecee8": "sha256:0ee8393ecee80c5d45842b9f968ac2bc8f7dc3da54b8316f297dbda0fd4bccb5",
        "§Complexity Tracking": "sha256:94a88a2cff6c245b4e33ebc068c97ee620510e790ac005d833335ee33beb40df",
        "Not applicable#9f2bc07bb981": "sha256:9f2bc07bb98146c0efffa9f55b504be92981e65f60e567074dc6f61690a8cf7b"
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
  "stage": "plan",
  "evaluated_at": "2026-10-01T13:30:31Z",
  "fingerprint": "sha256:b3f5641192800b130dcee71a3e3bba400e2d587fb92ac7ac6e6d7bfca1071ffd",
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
      "reason": "AI assessment: Every section restates DEC-001 to DEC-007 (server-side build in Viewer._render_document, existing walk and path guard, one sort key, labelled nav markup, unit and integration tests); the only structure named is the single file and two test files DEC-007 sets out.",
      "basis": "sha256:b3f5641192800b130dcee71a3e3bba400e2d587fb92ac7ac6e6d7bfca1071ffd"
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
