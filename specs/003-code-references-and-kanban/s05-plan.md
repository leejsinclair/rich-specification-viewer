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

# Implementation Plan: Cross-reference codes and tasks kanban view

**Branch**: `001-rich-spec-viewer` | **Date**: 2026-10-17 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/003-code-references-and-kanban/spec.md`

## Summary (traces: DEC-001, DEC-002, DEC-003, DEC-004)

Codes introduced in a story's headings, bullets or qualifying table rows are found in a first pass on each request and marked wherever referenced in that story (DEC-001). A new server-rendered kanban page at `/specs/<story>/kanban` is built from `tasks.md` by a dedicated line parser (DEC-002, DEC-003), with the parsed cards cached by modified time. Every document and kanban page polls a stamp route every 10 seconds and refreshes when its file changes (DEC-004).

## Technical Context (traces: DEC-001, DEC-002, DEC-004)

**Language/Version**: Python 3.11 or later

**Primary Dependencies**: standard library only; Mermaid is still loaded from jsDelivr

**Storage**: N/A; the board cache is in memory only (DEC-004)

**Testing**: `python3 -m unittest discover -s tests`

**Target Platform**: the existing local server, started as before

**Project Type**: single-file web viewer (`specview.py`)

**Performance Goals**: an edit shows within about 10 seconds; each open page adds one cheap request every 10 seconds (DEC-004)

**Constraints**: read-only, same `Host` check and path guard, nothing written to the project (DEC-002)

**Scale/Scope**: story-sized folders; no limit set on the discovery pass (DEC-001)

## Constitution Check (traces: DEC-001)

`.specify/memory/constitution.md` is still the unfilled template, so there are no gates to apply and none are violated.

## Project Structure (traces: DEC-001, DEC-002, DEC-003, DEC-004)

### Documentation (this feature)

```text
specs/003-code-references-and-kanban/
├── plan.md              # alias of s05-plan.md
├── quickstart.md
├── contracts/
│   └── http.md
└── tasks.md             # created by /speckit-tasks
```

### Source Code (repository root)

```text
specview.py              # story index, reference marker, kanban parser, board cache,
                         # kanban page, request handler, page refresher script
tests/
├── unit/                # discovery, kanban parser, grouping
└── integration/         # cross-document marking, kanban route, stamp route, refresh
```

**Structure Decision**: keep the single `specview.py` and the existing `tests/unit` and `tests/integration` folders; no new modules or processes (DEC-001, DEC-002).

## Not applicable

<!-- Sections removed from this document, each with its reason. -->

- Complexity Tracking: the Constitution Check has no violations.
- research.md: the Technical Context has nothing to resolve.
- data-model.md: the approved design adds no persistent data and no data model (Data Design is not applicable in the Technical Specification).

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
    "Implementation Plan: Cross-reference codes and tasks kanban view#9e745d056aaf": {
      "hash": "sha256:9e745d056aafefd07671f9b08eccf57d217cb4342bb6de1e7b9295445702f6e7",
      "class": "inferred",
      "reviewed": {
        "by": "Lee Sinclair",
        "at": "2026-10-17T02:55:51Z",
        "list": "RVW-011",
        "reply": "yes"
      }
    },
    "Implementation Plan: Cross-reference codes and tasks kanban view#9d00e8d46e6f": {
      "hash": "sha256:9d00e8d46e6f6471134d54779fd2928f3d09318c2ef6058f4b47230ca0f0ea27",
      "class": "inferred",
      "reviewed": {
        "by": "Lee Sinclair",
        "at": "2026-10-17T02:55:51Z",
        "list": "RVW-011",
        "reply": "yes"
      }
    },
    "§Summary": {
      "hash": "sha256:6aeb9b7567a9b65fc17d5a1b0c5d7688dc76d7031b4032a2d9dd3b3fbfe2409f",
      "class": "restated",
      "cites": {
        "DEC-001": "sha256:13a2732b598fcb0a7a620f1cc017318a750024235d9ca1453803f7f35b0ddedd",
        "DEC-002": "sha256:450de9b1737c8d785caca57c0b3cc522aed8898e9dcea2c8c953f697e1d03aa3",
        "DEC-003": "sha256:a9f99d3c520b3fe486f6f8103e542d28fb3a7c31a82c82665be1893726556d9d",
        "DEC-004": "sha256:942ab4072dd367c7cc88758bbd6df350e7ce92e76ea93688853324c207fbf0a3"
      }
    },
    "§Technical Context": {
      "hash": "sha256:10442a191a1719e020de5edbeba885a436cdf5ee9057998ae893b33b55b3cd6a",
      "class": "restated",
      "cites": {
        "DEC-001": "sha256:13a2732b598fcb0a7a620f1cc017318a750024235d9ca1453803f7f35b0ddedd",
        "DEC-002": "sha256:450de9b1737c8d785caca57c0b3cc522aed8898e9dcea2c8c953f697e1d03aa3",
        "DEC-004": "sha256:942ab4072dd367c7cc88758bbd6df350e7ce92e76ea93688853324c207fbf0a3"
      }
    },
    "§Constitution Check": {
      "hash": "sha256:f5445f5c8d00d0239acc468e4789b90cbb1e9388183a6bf921202e40e784b5ab",
      "class": "inferred",
      "adds": "Notes that the constitution is an unfilled template so there are no gates.",
      "reviewed": {
        "by": "Lee Sinclair",
        "at": "2026-10-17T02:55:51Z",
        "list": "RVW-011",
        "reply": "yes"
      },
      "sources": {
        "DEC-001": "sha256:13a2732b598fcb0a7a620f1cc017318a750024235d9ca1453803f7f35b0ddedd"
      }
    },
    "§Project Structure": {
      "hash": "sha256:839f9deeea39ffe1c4a0c7a817e119646266246c18b5a084bf884fba7c19ac95",
      "class": "restated",
      "cites": {
        "DEC-001": "sha256:13a2732b598fcb0a7a620f1cc017318a750024235d9ca1453803f7f35b0ddedd",
        "DEC-002": "sha256:450de9b1737c8d785caca57c0b3cc522aed8898e9dcea2c8c953f697e1d03aa3",
        "DEC-003": "sha256:a9f99d3c520b3fe486f6f8103e542d28fb3a7c31a82c82665be1893726556d9d",
        "DEC-004": "sha256:942ab4072dd367c7cc88758bbd6df350e7ce92e76ea93688853324c207fbf0a3"
      }
    },
    "Project Structure#01778b413ef8": {
      "hash": "sha256:01778b413ef86ba8210296d5a0731a9735f867520f6356ecf4481befd68d5856",
      "class": "inferred",
      "reviewed": {
        "by": "Lee Sinclair",
        "at": "2026-10-17T02:55:51Z",
        "list": "RVW-011",
        "reply": "yes"
      }
    },
    "Project Structure#7cf7e58b877c": {
      "hash": "sha256:7cf7e58b877c5c203887cc20b155fb3528a24ec0c3ffaa102a4f9de84907fb28",
      "class": "inferred",
      "reviewed": {
        "by": "Lee Sinclair",
        "at": "2026-10-17T02:55:51Z",
        "list": "RVW-011",
        "reply": "yes"
      }
    },
    "Project Structure#98978644b048": {
      "hash": "sha256:98978644b0487ee803d480478c62bdaf8b74ae7a0f06aa25bfb3299bf1f569f7",
      "class": "inferred",
      "reviewed": {
        "by": "Lee Sinclair",
        "at": "2026-10-17T02:55:51Z",
        "list": "RVW-011",
        "reply": "yes"
      }
    },
    "Not applicable#25a1a0f0cf28": {
      "hash": "sha256:25a1a0f0cf283bde00d367255283150e60aa5bd5ab4d450f81a85ae5a757f6f6",
      "class": "inferred",
      "reviewed": {
        "by": "Lee Sinclair",
        "at": "2026-10-17T02:55:51Z",
        "list": "RVW-011",
        "reply": "yes"
      }
    },
    "§Change Log": {
      "hash": "sha256:c8125cc9f94594e60a2e0d68b05f7bf53fc6deba1c17335ae3424c261ec5500a",
      "class": "inferred",
      "reviewed": {
        "by": "Lee Sinclair",
        "at": "2026-10-17T02:55:51Z",
        "list": "RVW-011",
        "reply": "yes"
      },
      "sources": {
        "DEC-001": "sha256:13a2732b598fcb0a7a620f1cc017318a750024235d9ca1453803f7f35b0ddedd"
      }
    },
    "§Record": {
      "hash": "sha256:23b35fe72a02d11c538eeb2fbd5432f29891c68fd3042803822d4ae37373734d",
      "class": "inferred",
      "reviewed": {
        "by": "Lee Sinclair",
        "at": "2026-10-17T02:55:51Z",
        "list": "RVW-011",
        "reply": "yes"
      },
      "sources": {
        "DEC-001": "sha256:13a2732b598fcb0a7a620f1cc017318a750024235d9ca1453803f7f35b0ddedd"
      }
    }
  },
  "acceptances": [
    {
      "id": "RVW-011",
      "stage": "plan",
      "kind": "inferred",
      "digest": "sha256:2c64351615f053ad8717abbd54ef2da58c1dd51baef80ec94c8439c79e98eeed",
      "by": "Lee Sinclair",
      "at": "2026-10-17T02:55:51Z",
      "reply": "yes",
      "accepted": [
        "Implementation Plan: Cross-reference codes and tasks kanban view#9e745d056aaf",
        "Implementation Plan: Cross-reference codes and tasks kanban view#9d00e8d46e6f",
        "§Constitution Check",
        "Project Structure#01778b413ef8",
        "Project Structure#7cf7e58b877c",
        "Project Structure#98978644b048",
        "Not applicable#25a1a0f0cf28",
        "§Change Log",
        "§Record"
      ],
      "except": [],
      "questioned": [],
      "reopened": [],
      "reason": null,
      "hashes": {
        "Implementation Plan: Cross-reference codes and tasks kanban view#9e745d056aaf": "sha256:9e745d056aafefd07671f9b08eccf57d217cb4342bb6de1e7b9295445702f6e7",
        "Implementation Plan: Cross-reference codes and tasks kanban view#9d00e8d46e6f": "sha256:9d00e8d46e6f6471134d54779fd2928f3d09318c2ef6058f4b47230ca0f0ea27",
        "§Constitution Check": "sha256:f5445f5c8d00d0239acc468e4789b90cbb1e9388183a6bf921202e40e784b5ab",
        "Project Structure#01778b413ef8": "sha256:01778b413ef86ba8210296d5a0731a9735f867520f6356ecf4481befd68d5856",
        "Project Structure#7cf7e58b877c": "sha256:7cf7e58b877c5c203887cc20b155fb3528a24ec0c3ffaa102a4f9de84907fb28",
        "Project Structure#98978644b048": "sha256:98978644b0487ee803d480478c62bdaf8b74ae7a0f06aa25bfb3299bf1f569f7",
        "Not applicable#25a1a0f0cf28": "sha256:25a1a0f0cf283bde00d367255283150e60aa5bd5ab4d450f81a85ae5a757f6f6",
        "§Change Log": "sha256:c8125cc9f94594e60a2e0d68b05f7bf53fc6deba1c17335ae3424c261ec5500a",
        "§Record": "sha256:23b35fe72a02d11c538eeb2fbd5432f29891c68fd3042803822d4ae37373734d"
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
  "evaluated_at": "2026-10-17T02:55:14Z",
  "fingerprint": "sha256:6ecebc337f48249c0d6e5d534e8eb241e5ba9bc283a549fd7bbf1fdf383568b7",
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
      "reason": "AI assessment: Every section restates the approved decisions DEC-001 to DEC-004; the plan adds no component, route or data store beyond the Technical Specification.",
      "basis": "sha256:6ecebc337f48249c0d6e5d534e8eb241e5ba9bc283a549fd7bbf1fdf383568b7"
    }
  ],
  "assessment": {
    "ambiguity": [],
    "missing": [
      "The constitution is an unfilled template, so the Constitution Check has no gates to test."
    ],
    "contradictions": [],
    "unsupported_assumptions": [],
    "untestable": []
  },
  "findings": []
}
```
<!-- eil:end assessment -->
