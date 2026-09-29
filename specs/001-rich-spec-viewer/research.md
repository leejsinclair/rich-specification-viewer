# Research: Rich specification viewer

Phase 0 of the plan. Every architectural choice here was already made and approved in the Technical Specification (`s03-technical-spec.md`, DEC-001 to DEC-008); this file records how each is carried out with the standard library and the Mermaid API. It adds no new decision. There were no `NEEDS CLARIFICATION` items in the Technical Context.

## R-1 Serving and threading (DEC-001, DEC-007)

- **Decision**: `http.server.ThreadingHTTPServer` with a `BaseHTTPRequestHandler` subclass; one daemon thread per request.
- **Rationale**: standard library; concurrent requests do not block each other; shared caches are guarded by one `threading.Lock`.
- **Alternatives considered**: `HTTPServer` (single-threaded; a slow render blocks the browser's parallel requests); `asyncio` streams (no ready-made HTTP parsing in the standard library).

## R-2 Cache key (DEC-001, CH-015)

- **Decision**: per story, a tuple of `(relative_path, st_mtime_ns, st_size)` for every `.md` file at any depth, sorted; computed with one `os.scandir` walk per request.
- **Rationale**: nanosecond modification times avoid missing two saves in the same second; including size catches most same-timestamp edits; a changed, added or removed file changes the tuple.
- **Alternatives considered**: hashing file contents on every request (correct but reads every file each time); `st_mtime` in seconds (misses fast successive saves).

## R-3 Path confinement (FR-018, CH-017)

- **Decision**: `Path.resolve(strict=True)` on the joined path, then `resolved.is_relative_to(specs_root)` where `specs_root = (start / "specs").resolve()`.
- **Rationale**: `resolve()` follows symbolic links and removes `..`; `is_relative_to` (3.9+) is an exact ancestor test, unlike a string prefix check (`/specs-other` would pass a prefix test).
- **Alternatives considered**: `os.path.commonpath` (equivalent but less direct); rejecting `..` textually (misses symbolic links).

## R-4 Alias detection (FR-024)

- **Decision**: while walking a story, keep a map from resolved path to the first document read, and from `(size, sha256 of bytes)` to the first document read; a later file matching either is recorded as an alias of that document and contributes no definitions.
- **Rationale**: resolved paths catch symbolic links (`spec.md -> s04-ai-spec.md`); content hashes catch the helper's read-only mirror copies; size is checked first to avoid hashing most files.
- **Alternatives considered**: a fixed list of alias names (`spec.md`, `plan.md`, `tasks.md`) (brittle, and not what FR-024 says).

## R-5 Glob search (DEC-005)

- **Decision**: `fnmatch.fnmatchcase(path.lower(), pattern.lower())` over paths relative to `specs/` with `/` separators; a pattern with none of `*?[` is wrapped as `*pattern*`; results sorted by that path.
- **Rationale**: `fnmatchcase` after lower-casing gives case-insensitive matching on every platform (plain `fnmatch` is case-insensitive only on Windows); `*` in `fnmatch` also crosses `/`, so `*s01*` finds files in any story.
- **Alternatives considered**: `pathlib.PurePath.match` (right-anchored, awkward for "contains").

## R-6 Host check (CH-016)

- **Decision**: read the `Host` header, strip a trailing `:port` (and brackets for IPv6), and accept only `localhost` and `127.0.0.1`; anything else, or a missing header, gets `403`.
- **Rationale**: defends against DNS rebinding; ignoring the port keeps it working when editor port forwarding maps the port to a different number on the host.

## R-7 Container detection (DEC-008)

- **Decision**: container if `Path("/.dockerenv").exists()` or `os.environ` has `REMOTE_CONTAINERS` or `CODESPACES`; `--host` overrides.

## R-8 Mermaid in the page (DEC-003, FR-015, FR-023)

- **Decision**: `const m = await import("https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs")`, then `m.default.initialize({ startOnLoad: false })`, then for each block `const { svg } = await m.default.render(id, source)` inside `try`/`catch`. The server emits each Mermaid block as `<pre class="mermaid-src">` with the source HTML-escaped; the script reads `textContent`.
- **Rationale**: `startOnLoad: false` gives the script control of each block, so one failure replaces only that block; a failed `import` is caught once and every block gets the error message.
- **Alternatives considered**: `startOnLoad: true` (Mermaid renders all blocks itself and reports errors in its own way, so FR-015's per-block message is harder to guarantee).

## R-9 Embedding tooltip JSON safely (DEC-004)

- **Decision**: `json.dumps(data, ensure_ascii=False)` then replace `<`, `>` and `&` with `<`, `>` and `&`; place it in `<script type="application/json" id="refs">`; the page reads it with `JSON.parse(el.textContent)`.
- **Rationale**: the escapes are valid JSON and cannot close the `<script>` element.

## R-10 Readable CSS (NFR-001)

- **Decision**: a single inline stylesheet: a reading column of about 72 characters (`max-width: 72ch`), the system font stack, a line height around 1.6, vertical spacing between blocks, a monospace stack for code, bordered tables, and a tooltip capped at about 60% of the viewport height with `overflow: auto`.
- **Rationale**: meets the reviewer checklist in NFR-001 with no web fonts or outside CSS.
