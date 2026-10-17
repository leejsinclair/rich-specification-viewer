# Research: Reading-order navigation for story documents

No item in the Technical Context was left as NEEDS CLARIFICATION, so there was nothing to research. The decisions below are those already made and approved in `s03-technical-spec.md`; this file only points at them.

| Topic | Decision | Alternative rejected |
|-------|----------|----------------------|
| Where the section is built | Server side, in `Viewer._render_document` (DEC-001) | A new `/api/...` endpoint filled in by the page script |
| How documents are found | `Viewer._markdown_files` and `PathGuard.resolve` (DEC-002) | Filtering the cached `StoryIndex.documents` |
| What counts as an alias | A `spec.md`, `plan.md` or `tasks.md` symbolic link whose resolved target is a listed, staged document of the same story (DEC-003) | Name and symbolic link alone |
| Ordering | One sort key over the whole list (DEC-004) | A recursive walk sorting each folder separately |
| Current entry and links | Current entry by path viewed; cross-story links go to the target's real path (DEC-005) | Always linking to the entry's own path |
| Markup and style | `nav` with an `h2` and an `ol`, current entry a `span aria-current="page"`, inline CSS (DEC-006) | An unordered list marking the current entry by background colour |
| Tests | Unit tests for the pure rules, integration tests through the real server (DEC-007) | Integration tests only |
