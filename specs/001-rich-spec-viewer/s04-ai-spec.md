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

# AI Specification: Rich specification viewer

## Functional Requirements

**AIS-001**: Show the folders and Markdown documents under `specs/` in the start folder, navigable down one level at a time. (traces: FR-001, UC-002)

**AIS-002**: Search by a glob pattern matched against each document's folder and file path below `specs/`, listing every matching document. (traces: FR-002, UC-002)

**AIS-003**: Open a document chosen from navigation or search results as an HTML page. (traces: FR-003)

**AIS-004**: Render headings, paragraphs, emphasis, links, block quotes, ordered, unordered and nested lists, task-list items, tables, inline code and fenced code blocks as formatted content. (traces: FR-004)

**AIS-005**: Style pages with just enough CSS for a fixed reading width, clear fonts, visible spacing between elements and scannable headings and lists. (traces: FR-005, NFR-001)

**AIS-006**: Regenerate a page whenever its Markdown changes so a refresh shows the saved content; an open page need not update itself. (traces: FR-006, NFR-002)

**AIS-007**: Show navigation and search results as they are at request time, including documents added, renamed or removed since start. (traces: FR-007)

**AIS-008**: Recognise and visibly mark every reference code in a viewed document. (traces: FR-008)

**AIS-009**: Resolve codes only against documents of the same story, the folder directly under `specs/` holding the viewed document. (traces: FR-009, REQ-002)

**AIS-010**: On hover over a resolved code, show a tooltip with the whole defining section, formatted, naming its source document, capped at a maximum size and scrolling inside. (traces: FR-010, UC-001)

**AIS-011**: Show tooltips for codes defined in the viewed document itself as well as in other documents of the story. (traces: FR-011)

**AIS-012**: On click of a resolved code, open the defining document at the defining section, or scroll to it when it is in the same document. (traces: FR-012, UC-004)

**AIS-013**: Highlight a code with no definition, or with definitions in more than one document of the story, as an error with an error icon and red text. (traces: FR-013, REQ-007)

**AIS-014**: Draw every valid Mermaid diagram of any type, including C4 and entity relationship diagrams, in place of its source. (traces: FR-014, REQ-004)

**AIS-015**: When a diagram cannot be drawn, including when the diagram library cannot load, show an error message in place of that diagram and still show the rest of the page. (traces: FR-015)

**AIS-016**: Treat a Mermaid block that is not valid syntax as an undrawable diagram. (traces: FR-016)

**AIS-017**: Start with a single command from the project folder with no configuration and nothing to install. (traces: FR-017, REQ-005)

**AIS-018**: Never read, list or show anything outside the start folder, and refuse such a request with a message saying the location is outside the viewer's folder. (traces: FR-018)

**AIS-019**: Do not show HTML comments, `eil:` blocks or the assessment, comprehension and approval regions. (traces: FR-019)

**AIS-020**: Show breadcrumbs on every navigation view and document page from the top of `specs/` to the current location, each part opening that folder, with the search box always available. (traces: FR-020)

**AIS-021**: Open no tooltip for a code shown inside a tooltip. (traces: FR-021)

**AIS-022**: For a challenge code, show its text, target, status and, once answered, the response, who answered and the reason; a click opens the Challenges section of the recording document. (traces: FR-022)

**AIS-023**: Do not draw diagrams inside a tooltip; show a note that a diagram is shown in the document instead. (traces: FR-023)

## Business Rules

**AIS-024**: Reference codes are the Spec Kit forms `REQ`, `UC`, `OQ`, `ART`, `CH`, `FR`, `NFR`, `SC`, `DEC`, `AIS`, `EVD` as `PREFIX-001`, decisions as `D-01`, and tasks as `T001`. (traces: FR-008)

**AIS-025**: A code is defined by a line starting with the bolded code and a colon (optionally a list item), a heading starting with the code, a task line `- [ ] T001`, or an `eil:challenge` block whose `id` is the code. (traces: FR-008, FR-022)

**AIS-026**: A defining section runs from the defining line up to, not including, the next definition or the next heading of the same or higher level. (traces: FR-010)

**AIS-027**: A code with no definition in the story is unresolved; with definitions in two or more documents of the story it is ambiguous; both are errors. (traces: FR-013)

**AIS-028**: A code inside inline code or a fenced code block, and the code on its own defining line, is not a reference. (traces: FR-008)

**AIS-088**: Treat an alias and its target as one document when resolving codes: resolve symbolic links, and skip a file whose content is identical to another document of the story; the alias still appears in navigation and opens normally. (traces: FR-024)

**AIS-089**: Every `.md` file at any depth under a story folder belongs to that story when resolving codes. (traces: FR-025)

**AIS-090**: A heading for a code already defined as an item elsewhere in the story expands that definition rather than defining it a second time: the item is the code's definition (its tooltip and link target), and the heading still gets its own anchor. (traces: FR-026) [pending-clarification]

## Technical Decisions

**AIS-029**: Serve every page from one Python process that renders the requested document on each request, caching by the modification time and size of every document in the story. (traces: DEC-001)

**AIS-030**: Parse Markdown with an own line-based block parser plus an inline pass covering the Spec Kit subset; show unparseable constructs as escaped plain text. (traces: DEC-002)

**AIS-031**: Import `mermaid@11` as an ES module from jsDelivr in the page and render each block with `mermaid.render()` in `try`/`catch`. (traces: DEC-003)

**AIS-032**: Resolve references when the page is rendered and embed the pre-rendered defining sections of the codes used on the page as JSON. (traces: DEC-004)

**AIS-033**: Search on the server with `fnmatch` over paths relative to `specs/`, lower-cased; wrap a pattern with no wildcard as `*pattern*`; sort results by path. (traces: DEC-005)

**AIS-034**: Support Python 3.11 and later, using the standard library only. (traces: DEC-006, NFR-003)

**AIS-035**: Start as `python3 specview.py`, using the first free port from 8000 to 8019, print the URL and open it in the browser; `--port` and `--host` are optional, never required. (traces: DEC-007)

**AIS-036**: Bind to `0.0.0.0` when `/.dockerenv` exists or `REMOTE_CONTAINERS` or `CODESPACES` is set, otherwise `127.0.0.1`; print the chosen address and why; `--host` overrides. (traces: DEC-008)

## Architectural Constraints

**AIS-037**: Build two containers only: the Viewer server (Python standard library, `http.server`) and the Viewer page (HTML, CSS and JavaScript in the browser). (traces: ART-012, DEC-001)

**AIS-038**: Keep the server as one script, `specview.py`, with the CSS and page JavaScript embedded in it and inlined into every page. (traces: DEC-007, DEC-001)

**AIS-039**: Structure the server as Request handler, Path guard, Markdown renderer, Story index, Reference marker, Search and Page template. (traces: ART-013)

**AIS-040**: Structure the page script as Tooltip controller, Diagram loader and Search box. (traces: ART-014)

**AIS-041**: Open every file, including the Story index's reads of other story documents, through the Path guard only. (traces: ART-013, FR-018)

**AIS-042**: Load Mermaid in the browser only; the server makes no outside request. (traces: DEC-003, NFR-003)

## Interfaces

**AIS-043**: `GET /` and `GET /specs/<folder>/` return the HTML navigation view of that folder. (traces: FR-001, FR-020, DEC-001)

**AIS-044**: `GET /specs/<story>/<file>.md` returns the HTML document page. (traces: FR-003, DEC-001)

**AIS-045**: `GET /api/search?q=<pattern>` returns JSON with `specs` (true or false) and `results`, each with `story`, `file` and `href`. (traces: FR-002, DEC-005)

**AIS-046**: A path outside `specs/` returns `403` with an HTML message; a missing path returns `404`; an unexpected rendering error returns `500` with the message while the server keeps running. (traces: FR-018, DEC-001)

**AIS-047**: The page imports `https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs`. (traces: DEC-003)

## Data Structures

**AIS-048**: The story index maps each code to its definitions: source document, anchor and the rendered HTML of its defining section; challenge definitions carry text, target, status, response, answerer and reason. (traces: DEC-004, FR-022)

**AIS-049**: The page embeds the tooltip data of the codes it uses as JSON in a `<script type="application/json">` element. (traces: DEC-004)

**AIS-050**: The render cache key for a story is the list of its documents with their modification times in nanoseconds and sizes; the cache is in memory, guarded by a lock, and nothing is persisted. (traces: DEC-001)

## Testing Requirements

**AIS-051**: Unit-test with `unittest`: each Markdown construct of FR-004, dropping of comments and `eil:` blocks, definitions and section boundaries, code marking and non-references, story scope, unresolved and ambiguous codes, challenge definitions, glob matching, the Path guard with `..`, absolute paths and symbolic links, the Host check, and container detection. (traces: FR-004, FR-008, FR-013, FR-018, FR-019, DEC-005, DEC-008)

**AIS-052**: Integration-test by starting the server on a free port against a fixture project in a temporary folder and requesting pages, search and forbidden paths over HTTP, covering the functional acceptance criteria AC-1 to AC-5, AC-9 to AC-11, AC-13, AC-14 and AC-17. (traces: FR-001, FR-002, FR-003, FR-006, FR-009, FR-012, FR-018, FR-020)

**AIS-053**: Integration-test that changing one document of a story updates another document's tooltip after a refresh, and that a request with a foreign `Host` header is refused. (traces: DEC-001, FR-006, FR-010)

**AIS-054**: Check manually in a browser: tooltips, scrolling and no nested tooltips, every diagram type including C4 and ER, offline and invalid diagrams, and readability. (traces: FR-010, FR-014, FR-015, FR-021, FR-023, NFR-001)

## Security Requirements

**AIS-055**: Refuse with `403` any request whose `Host` header names anything other than `localhost` or `127.0.0.1`, at any port. (traces: DEC-008, FR-018)

**AIS-056**: Resolve every path, following symbolic links and `..`, and refuse it unless it lies inside `<start>/specs`. (traces: FR-018)

**AIS-057**: Open files read-only and never create, change or delete a file in the project. (traces: FR-018, DEC-001)

**AIS-058**: HTML-escape all document text before inline formatting; show raw HTML from Markdown escaped. (traces: DEC-002)

**AIS-059**: Escape `<`, `>` and `&` as Unicode escapes in the embedded tooltip JSON so section content cannot close the script element. (traces: DEC-004)

## Edge Cases

**AIS-060**: No `specs/` folder in the start folder: show "No specs folder found" underneath the search box on every page. (traces: FR-001, FR-002)

**AIS-061**: A search pattern that matches nothing: say that nothing matches; an empty pattern leaves the navigation view as it is. (traces: FR-002)

**AIS-062**: The diagram library cannot be imported: show the error message in place of every diagram; tooltips and the rest of the page still work. (traces: FR-015, DEC-003)

**AIS-063**: A document removed or renamed after it was served: the open page stays unchanged; a refresh returns `404` with a message. (traces: FR-007, DEC-001)

**AIS-064**: An unresolved or ambiguous code is rendered as a `<span>`, not a link, so clicking it does not navigate; its tooltip explains the error. (traces: FR-013, ART-018)

**AIS-065**: All ports from 8000 to 8019 are busy: stop with a message. (traces: DEC-007)

**AIS-066**: A symbolic link in a story folder that resolves outside `specs/`: skip it. (traces: FR-018, ART-013)

## Explicit Exclusions

**AIS-067**: Do not edit Markdown documents or change the content or format of Spec Kit documents. (traces: REQ-001, FR-018)

**AIS-068**: Do not show Markdown documents outside `specs/`. (traces: REQ-001)

**AIS-069**: Do not resolve references across stories. (traces: FR-009)

**AIS-070**: Do not make tooltips reachable without a mouse. (traces: REQ-002)

**AIS-071**: Do not search the text inside documents. (traces: REQ-003)

**AIS-072**: Do not add authentication, persistence or any third-party Python package, and do not load any outside script other than Mermaid. (traces: NFR-003, DEC-006)

## Implementation Constraints

**AIS-073**: Use only the Python 3.11 standard library; nothing to install and no configuration file. (traces: DEC-006, FR-017, NFR-003)

**AIS-074**: Use `http.server.ThreadingHTTPServer`. (traces: ART-013, DEC-001)

**AIS-075**: Print one line per request, tracebacks of rendering errors, and on start the start folder, the URL and how to stop. (traces: DEC-007, DEC-001)

## Artefacts in Scope

**AIS-076**: Read the system context before starting: the external systems and their names. (traces: ART-001)

**AIS-077**: Read the functional sequence diagram for reading a document with its references explained. (traces: ART-002)

**AIS-078**: Read the functional sequence diagram for finding a document. (traces: ART-003)

**AIS-079**: Read the functional sequence diagram for reading a diagram. (traces: ART-004)

**AIS-080**: Read the functional sequence diagram for following a reference. (traces: ART-005)

**AIS-081**: Read the container view before creating the server and page. (traces: ART-012)

**AIS-082**: Read the viewer server component view before structuring `specview.py`. (traces: ART-013)

**AIS-083**: Read the viewer page component view before writing the page script. (traces: ART-014)

**AIS-084**: Implement page rendering and tooltips as the technical sequence diagram for reading a document shows. (traces: ART-015)

**AIS-085**: Implement search as the technical sequence diagram for finding a document shows. (traces: ART-016)

**AIS-086**: Implement diagram drawing as the technical sequence diagram for drawing diagrams shows. (traces: ART-017)

**AIS-087**: Implement reference following as the technical sequence diagram for following a reference shows. (traces: ART-018)

## Not applicable

- Existing Code: the repository contains only the `specs/` documents; the viewer is wholly new.
- Agent Guidance: nothing beyond the sections above.

## Challenges

<!-- Recorded by `eil challenge`. -->

## Overrides

<!-- Recorded by `eil override`, each naming who, what and why. -->

## Quality Assessment

<!-- eil:begin assessment -->
```json
{
  "stage": "ai-spec",
  "evaluated_at": "2026-09-29T10:58:37Z",
  "fingerprint": "sha256:250e0c806d43ab4b5022e8ead9fb69a112a8cd53539690b4b9e6e4685fd9cf53",
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
