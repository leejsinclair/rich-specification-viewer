# HTTP contract: kanban and stamp routes

Both routes pass through the existing `Host` header check and path guard. Existing routes are unchanged.

## `GET /specs/<story>/kanban[?group=phase|story]`

- `200` HTML: four columns (backlog, in progress, blocked, done) of cards, grouped by phase by default; `?group=story` groups by user story; any other value falls back to phase. Tasks with no phase, or with no `[USn]` tag when grouped by story, go in Unallocated.
- `200` HTML with a "no tasks found" message in place of the board when `tasks.md` is missing, empty or unreadable.
- `403` for a wrong `Host` header or a path outside `specs/`; `404` where any other path would give it.
- Reads only; nothing is written.

## `GET /api/stamp?path=<path under specs/>`

- `200` JSON `{"stamp": <modified time of that file>}`, or `{"stamp": null}` when the file cannot be read.
- `403` for a wrong `Host` header or a path outside `specs/`.
- Polled every 10 seconds by each open document and kanban page.
