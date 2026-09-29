# Data Model: Rich specification viewer

Nothing is persisted (Technical Specification: Data Design and Data Model are not applicable). These are the in-memory structures the viewer builds, from DEC-001, DEC-002, DEC-004 and DEC-005 and the Functional business rules BR-1 to BR-6.

## Document

One Markdown file under `specs/`.

| Field | Type | Notes |
|---|---|---|
| `rel_path` | str | Path relative to `specs/`, `/`-separated; the URL is `/specs/<rel_path>` |
| `story` | str or None | First path segment when the file is inside a story folder; `None` for a file directly in `specs/` (FR-009) |
| `mtime_ns`, `size` | int | From `os.stat`; part of the cache key |
| `alias_of` | str or None | `rel_path` of the document this one is a link to or an identical copy of (FR-024) |

## Definition

Where a code is introduced (BR-2).

| Field | Type | Notes |
|---|---|---|
| `code` | str | e.g. `FR-012`, `D-01`, `T001`, `CH-007` (BR-1) |
| `document` | str | `rel_path` of the defining document |
| `anchor` | str | Element id on the rendered page, derived from the code (e.g. `fr-012`) |
| `kind` | str | `item`, `heading`, `task` or `challenge` |
| `section_html` | str | Rendered defining section (BR-3); diagrams replaced by a note for tooltips (FR-023) |
| `challenge` | dict or None | For `kind == "challenge"`: `text`, `target`, `status`, and once answered `response`, `by`, `reason` (FR-022) |

## StoryIndex

Built per story, cached under its cache key (DEC-001, DEC-004).

| Field | Type | Notes |
|---|---|---|
| `story` | str | Story folder name |
| `key` | tuple | Sorted `(rel_path, mtime_ns, size)` of every `.md` at any depth (FR-025) |
| `documents` | dict[str, Document] | By `rel_path`, aliases included but marked |
| `definitions` | dict[str, list[Definition]] | By code; aliases contribute nothing (FR-024) |

**Resolution state of a code** (BR-5, FR-013): `resolved` when `len(definitions[code]) == 1`; `unresolved` when absent; `ambiguous` when two or more.

## RenderedPage

Cached per document under its story's key.

| Field | Type | Notes |
|---|---|---|
| `html` | str | Complete page: breadcrumbs, search box, body, inline CSS and script |
| `refs` | dict[str, TooltipEntry] | Embedded as JSON (DEC-004) |

## TooltipEntry

The JSON embedded in each page, one per code used on the page (see `contracts/http.md`).

| Field | Type | Notes |
|---|---|---|
| `state` | `"resolved"`, `"unresolved"`, `"ambiguous"` | |
| `doc` | str | Defining document name (resolved) |
| `href` | str | `/specs/<rel_path>#<anchor>` (resolved) |
| `html` | str | Defining section HTML (resolved) |
| `documents` | list[str] | Defining documents (ambiguous) |

## SearchResult

Returned by `/api/search` (DEC-005).

| Field | Type | Notes |
|---|---|---|
| `story` | str or None | Story folder, or `None` for a file directly in `specs/` |
| `file` | str | Path within the story |
| `href` | str | Page URL |

## State

A rendered page is **current** while its story's key is unchanged and **out of date** once any document in the story changes; the next request re-renders it (Functional: State and Workflow; DEC-001).
