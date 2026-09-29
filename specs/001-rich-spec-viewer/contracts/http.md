# Contract: HTTP interface of the viewer server

From the Technical Specification's API and Integration Design, DEC-001, DEC-004, DEC-005 and DEC-008.

## Every request

1. **Host check** (CH-016): the `Host` header, with any `:port` removed, must be `localhost` or `127.0.0.1`. Otherwise `403`, with a short HTML message, before anything else is done.
2. **Path guard** (FR-018): every path is resolved, following symbolic links and `..`, and must lie inside `<start>/specs`. Otherwise `403` with the message "This location is outside the viewer's folder."

## Routes

| Method and path | Response | Source |
|---|---|---|
| `GET /` | `200` HTML navigation view of `specs/`; if there is no `specs/` folder, the page shows "No specs folder found" under the search box | FR-001, FR-020, AC-17 |
| `GET /specs/<folder>/` | `200` HTML navigation view of that folder | FR-001, FR-020 |
| `GET /specs/<path>.md` | `200` HTML document page | FR-003 |
| `GET /api/search?q=<pattern>` | `200` JSON, below | FR-002, DEC-005 |
| anything missing | `404` HTML message | Error Handling |
| rendering exception | `500` HTML with the exception message; traceback printed to the terminal; the server keeps running | Error Handling |

All HTML responses are `text/html; charset=utf-8`; JSON is `application/json; charset=utf-8`.

## `GET /api/search`

```json
{
  "specs": true,
  "results": [
    {"story": "001-rich-spec-viewer", "file": "s01-requirements.md", "href": "/specs/001-rich-spec-viewer/s01-requirements.md"}
  ]
}
```

- `specs` is `false` when the start folder has no `specs/`; `results` is then empty and the page shows "No specs folder found".
- Matching (DEC-005): each path relative to `specs/`, lower-cased, against the lower-cased pattern with `fnmatch`; a pattern with no `*`, `?` or `[` is treated as `*pattern*`. Results are sorted by path. An empty `q` returns no results, and the page leaves the navigation view as it is.

## Document page

- Breadcrumbs from `specs/` to the current location, each part a link to that folder (FR-020); the search box is always present.
- HTML comments, `eil:` blocks and the assessment, comprehension and approval regions are not rendered (FR-019).
- A resolved code is `<a class="ref" data-code="FR-012" href="/specs/…#fr-012">FR-012</a>` (FR-008, FR-012).
- An unresolved or ambiguous code is `<span class="ref ref-error" data-code="…">⚠ FR-099</span>`, red, not a link (FR-013).
- On a document directly in `specs/`, codes are plain text (FR-009).
- Tooltip data is embedded once per page (DEC-004):

```html
<script type="application/json" id="refs">
{"FR-012": {"state": "resolved", "doc": "s02-functional-spec.md", "href": "/specs/001-x/s02-functional-spec.md#fr-012", "html": "…"},
 "FR-099": {"state": "unresolved"},
 "UC-009": {"state": "ambiguous", "documents": ["s01-requirements.md", "notes/extra.md"]}}
</script>
```

  `<`, `>` and `&` inside the JSON are written as `<`, `>` and `&`.
- Each Mermaid block is `<pre class="mermaid-src">…escaped source…</pre>`; the page script replaces it with the drawn diagram, or with an error message (FR-014, FR-015).
