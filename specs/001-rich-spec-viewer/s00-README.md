<!-- eil:generated — edit the stage documents, not this file -->
# Rich specification viewer

## Story

- Title: Rich specification viewer
- Owner: Lee Sinclair

## Status

- Current stage: functional
- Overall status: needs-re-review

## Documents

| Document | State |
|---|---|
| [s00-README.md](s00-README.md) | generated |
| [s01-requirements.md](s01-requirements.md) | approved |
| [s02-functional-spec.md](s02-functional-spec.md) | needs-re-review |
| [s03-technical-spec.md](s03-technical-spec.md) | needs-re-review |
| [s04-ai-spec.md](s04-ai-spec.md) | draft |
| [s05-plan.md](s05-plan.md) | in-review |
| [s06-tasks.md](s06-tasks.md) | in-review |
| s07-verification.md | not-started |
| s08-completion.md | not-started |

## Artefacts

| Artefact | Kind | Stage | State | Link |
|---|---|---|---|---|
| ART-001 | c4-context | requirements | ok | [System context](s01-requirements.md) |
| ART-002 | sequence | functional | ok | [Developer reads a document with its references explained](s02-functional-spec.md) |
| ART-003 | sequence | functional | ok | [Developer finds a document to view](s02-functional-spec.md) |
| ART-004 | sequence | functional | ok | [Developer reads a diagram](s02-functional-spec.md) |
| ART-005 | sequence | functional | ok | [Developer follows a reference](s02-functional-spec.md) |
| ART-006 | unknown | functional | unregistered | [Navigation view, default state](s02-functional-spec.md) |
| ART-007 | unknown | functional | unregistered | [Navigation view, empty state with no `specs/` folder](s02-functional-spec.md) |
| ART-008 | unknown | functional | unregistered | [Search results, default and no-matches states](s02-functional-spec.md) |
| ART-009 | unknown | functional | unregistered | [Document page, default state with marked references and a drawn diagram](s02-functional-spec.md) |
| ART-010 | unknown | functional | unregistered | [Document page with a reference tooltip open](s02-functional-spec.md) |
| ART-011 | unknown | functional | unregistered | [Document page, error states: an unresolved code and an undrawable diagram](s02-functional-spec.md) |
| ART-012 | c4-container | technical | ok | [Containers of the rich specification viewer](s03-technical-spec.md) |
| ART-013 | c4-component | technical | ok | [Inside the viewer server](s03-technical-spec.md) |
| ART-014 | c4-component | technical | ok | [Inside the viewer page](s03-technical-spec.md) |
| ART-015 | sequence | technical | ok | [Reading a document with its references explained](s03-technical-spec.md) |
| ART-016 | sequence | technical | changed-since-approval | [Finding a document by search](s03-technical-spec.md) |
| ART-017 | sequence | technical | ok | [Drawing diagrams](s03-technical-spec.md) |
| ART-018 | sequence | technical | ok | [Following a reference](s03-technical-spec.md) |

## Approvals

| Stage | Approved by | At | Fingerprint | Comprehension |
|---|---|---|---|---|
| requirements | Lee Sinclair | 2026-09-27T11:32:19Z | fccddf46c6af |  |

## Outstanding

- Open questions: OQ-018
- Open challenges: none
- Pending clarifications: AIS-090
- Overrides: OVR-001 (functional FUN-G15 by Lee Sinclair)
- Issues: none

## Accepted risks

none

## Abbreviated stages

none

## Mirrors

none
