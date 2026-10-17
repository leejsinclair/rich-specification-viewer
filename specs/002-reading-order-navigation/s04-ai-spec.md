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

# AI Specification: Reading-order navigation for story documents

## Functional Requirements

<!-- The functional requirements to build, restated for the agent: `**AIS-001**: Flag duplicate customers on import. (traces: FR-001)`. -->

**AIS-001**: Show, at the bottom of every document viewed from inside a story folder (`specs/<story>/`) at any depth, a section headed "Documents in reading order" with one entry for every Markdown document in that story folder and all its nested subfolders. (traces: FR-001)

**AIS-002**: Present the section as a navigation region whose accessible name is "Documents in reading order", with its entries as a list. (traces: FR-002)

**AIS-003**: Show each entry's document path relative to the story folder without the file extension, with the folder path kept in front for a nested document. (traces: FR-003)

**AIS-004**: Show a document whose file name is `s`, exactly two digits `NN`, a hyphen and a name as `[stage NN: <name>]`, with any folder path kept in front and the file name not repeated. (traces: FR-004)

**AIS-005**: Show a document without a stage prefix as its path relative to the story folder without the extension, followed by `[ref doc: <name>]`. (traces: FR-005)

**AIS-006**: Treat `spec.md`, `plan.md` or `tasks.md` as an alias only when it is a symbolic link to a document with a stage in the same story; do not list an alias as its own entry, show its file name in round brackets after the source entry (one group of brackets per alias, in alphanumeric order), and list any other file with one of those names as an ordinary document. (traces: FR-006)

**AIS-007**: Order the entries deterministically, the same on every page view and every run, comparing numbers inside names by value so `s10` does not come before `s02`. (traces: FR-007)

**AIS-008**: List the documents of a folder before the documents of its nested folders, whether or not they have a stage. (traces: FR-008)

**AIS-009**: List within each folder the documents without a stage after those with a stage and before the nested folders, in alphanumeric order with case ignored, numbers compared by value, and names differing only in case ordered by their exact characters. (traces: FR-009)

**AIS-010**: Include the document being viewed in the section as plain text with `aria-current="page"`, distinguished from the links by more than colour (links underlined, plain text not); when the document is viewed through its alias the source entry is current; no other entry carries `aria-current="page"`, including when the document is the only one in the story. (traces: FR-010)

**AIS-011**: Make every entry other than the current document a link that opens that document and can be reached and followed with the keyboard. (traces: FR-011)

**AIS-012**: Show no reading-order section on a Markdown document that lies directly under `specs/` and not inside a story folder. (traces: FR-012)

**AIS-013**: Never list in a story's section a document of another story, except a document that a symbolic link inside that story points to; label such an entry by the link's path relative to the story folder and make its link open the document at its real path in the other story. (traces: FR-013)

**AIS-014**: List only documents that the viewer's existing document discovery and path resolution treat as reachable under `specs/`, and never list or link a file that resolves outside `specs/`. (traces: FR-014)

**AIS-015**: Add no entry, no error and no empty heading for a folder without Markdown documents, and show no broken section for a story whose folders are all empty. (traces: FR-015)

**AIS-016**: Keep every existing feature working unchanged: reference tooltips and click-through, error marking of references, search, folder navigation and breadcrumbs, and Mermaid diagrams. (traces: FR-016)

**AIS-017**: Show the section only at the bottom of document pages, never on the folder navigation view, the search results or any other page. (traces: FR-017)

## Business Rules

<!-- The rules that govern behaviour, each traced to its functional requirement. -->

**AIS-018**: A document belongs to the story whose folder directly under `specs/` contains it at any depth; a document directly under `specs/` belongs to no story. (traces: FR-001, FR-012)

**AIS-019**: A document has a stage only when its file name is `s`, exactly two digits, a hyphen and a name; `s1-x.md`, `s100-x.md`, `S01-x.md`, `s01_x.md` and `s01.md` have no stage. (traces: FR-004, FR-005)

**AIS-020**: Within a folder list documents with a stage first, then documents without a stage in alphanumeric order, then the contents of its nested folders, each nested folder following the same rule. (traces: FR-007, FR-008, FR-009)

**AIS-021**: An alias is shown only through its source document's entry, and any other file named `spec.md`, `plan.md` or `tasks.md` is an ordinary document. (traces: FR-006)

**AIS-022**: Only documents the viewer already considers reachable under `specs/` can be listed. (traces: FR-014)

## Technical Decisions

<!-- The approved decisions, each with the constraint it imposes: `**AIS-003**: Analysis runs asynchronously in a worker. (traces: DEC-001)`. -->

**AIS-023**: Build the section on the server: `Viewer._render_document` appends its HTML after the rendered body of every document inside a story folder, and adds nothing to a document directly under `specs/`, the folder navigation page or the search results. (traces: DEC-001)

**AIS-024**: Take the story's documents from `Viewer._markdown_files(<story folder>)`, which walks the story at any depth, matches `.md` in any case, does not follow symbolic links to folders and skips files that `PathGuard.resolve` places outside `specs/`; an empty folder contributes no entry; do not use `StoryIndex.aliases`. (traces: DEC-002)

**AIS-025**: A file is an alias when its name is in `ALIAS_NAMES`, it is itself a symbolic link, and its fully resolved target lies in the same story, has a stage-prefixed file name and has an entry in the list; any other file with such a name, including a link to a missing, unreachable, outside-the-story, unstaged or unlisted target, is an ordinary entry. (traces: DEC-003)

**AIS-026**: Give each document one sort key (a folder part for each folder on its path, then a document part) and sort the whole list once: a folder's documents before a nested folder's, staged before unstaged within a folder, names compared with `casefold`, digit runs by numeric value, ties by exact characters, sibling folders by the same name comparison. (traces: DEC-004)

**AIS-027**: The current entry is the entry whose path is the path being viewed; for an alias it is the source entry, and a symbolic link that is not an alias is current under its own path; every other entry links to its own path built with `doc_url`, except an entry whose symbolic link resolves into another story, which links to the target's real path. (traces: DEC-005)

**AIS-028**: Write the section as `<nav class="reading-order" aria-label="Documents in reading order">` holding a visible `<h2>` with the same text and an `<ol>` with one `<li>` per entry; a link entry is an `<a href>` with any alias names in round brackets after it in the same `<li>`, the current entry is a `<span aria-current="page">` and not a link, links keep the existing underlined style and colour, and the current entry is bold, not underlined, in the text colour, styled by a few rules added to the inline `CSS` with a contrast ratio of at least 4.5:1. (traces: DEC-006)

**AIS-029**: Test the pure rules in `tests/unit/test_reading_order.py` and the page through the real server in `tests/integration/test_reading_order.py`, add a test that computes the contrast ratios from the CSS colours, add no package, and keep the existing tests passing. (traces: DEC-007)

## Architectural Constraints

<!-- Boundaries the agent must respect: what may depend on what, and where things live. -->

**AIS-030**: Keep the viewer one process and one source file, `specview.py`; add no container, route, store or external system. (traces: DEC-001, ART-007)

**AIS-031**: Put the reading-order builder inside the Viewer server: the Viewer asks the builder for a story's section, and the builder resolves each path through the path guard and depends only on `Viewer._markdown_files`, `PathGuard.resolve`, `doc_url` and `esc`. (traces: ART-008, DEC-002)

**AIS-032**: Keep the builder free of state, so repeated and concurrent renders of one page give the same HTML. (traces: DEC-001, ART-008)

**AIS-033**: Leave the request handler and the path guard unchanged, and change only `Viewer._render_document` and the inline `CSS`; `navigation_page`, `search` and `page_html` stay as they are. (traces: ART-008, DEC-001, FR-017)

## Existing Code

<!-- Existing files, modules and patterns to reuse or follow, and those not to follow. If the story is wholly new, list this section under Not applicable. -->

**AIS-034**: Reuse `Viewer._markdown_files` and `PathGuard.resolve` for discovery and path safety. (traces: DEC-002, FR-014)

**AIS-035**: Use the names in `ALIAS_NAMES` for alias recognition. (traces: DEC-003)

**AIS-036**: Build every link with `doc_url` and escape every file and folder name with `esc`. (traces: DEC-006, FR-014)

**AIS-037**: Keep the existing page cache and its key, which already changes when a Markdown file of the story is added, renamed, removed or edited. (traces: DEC-001)

**AIS-038**: Do not reuse `StoryIndex.documents` or `StoryIndex.aliases` for the section, because they treat any byte-identical copy as an alias, which FR-006 does not allow. (traces: DEC-002, FR-006)

**AIS-039**: Write the style rules for `.reading-order` in the existing inline `CSS`, with no external file. (traces: DEC-006)

**AIS-040**: The breadcrumbs also use `aria-current="page"` on a `span`, so a test for the section's current entry must look inside the section. (traces: DEC-006, DEC-007)

## Interfaces

<!-- Endpoints, operations, messages and their contracts, from the approved design. -->

**AIS-041**: Add `Viewer.reading_order(story, current_rel)`, which returns the HTML string of the section, with helpers `stage_of(file_name)`, `natural_key(text)` and `reading_order_key(parts, staged)`. (traces: DEC-001, DEC-004)

**AIS-042**: Add no endpoint, request or response structure; the links use the existing `/specs/<path>` document route built with `doc_url`. (traces: DEC-001, FR-011)

## Testing Requirements

<!-- What must be tested, at which level, and how each is verified. -->

**AIS-043**: Add unit tests for `stage_of` and the labels, the sort key (`s00` to `s10`, case, numbers inside names, a folder's documents before a nested folder's, staged before unstaged, sibling folders, the same order for any creation order) and alias recognition on temporary folders with real symbolic links (a regular `plan.md`, a link to an unstaged document, a link into another story, a link to a missing target, two aliases of one document). (traces: DEC-007, FR-004, FR-005, FR-006, FR-007, FR-008, FR-009, NFR-001)

**AIS-044**: Add integration tests that start the real server on temporary story folders and check: nested story order, exactly one `aria-current="page"` with the current entry as plain text, an alias shown in round brackets with its source current, a one-document story, a document directly under `specs/` with no section, no section on the folder navigation page or search result, an empty folder adding nothing, two stories not listing each other, a symbolic link into another story listed and linked to its real path, a link to a file outside `specs/` not listed, and the region's accessible name and list. (traces: DEC-007, FR-001, FR-002, FR-010, FR-012, FR-013, FR-014, FR-015, FR-017)

**AIS-045**: Add a test that computes the contrast ratio of the link colour and the text colour against the background from the CSS values and requires at least 4.5:1. (traces: DEC-007, NFR-002)

**AIS-046**: Keep all existing tests passing, which shows tooltips, error marking, search, navigation and diagrams are unchanged. (traces: FR-016, NFR-003)

**AIS-047**: Cover nested documents, ordering, the current-document state, isolation between stories, documents directly under `specs/`, empty folders, path safety, aliased documents and the entry label formats. (traces: NFR-003)

## Security Requirements

<!-- Authentication, authorisation, secrets and sensitive-data rules the implementation must meet. -->

**AIS-048**: Build the section from names and resolved paths only and never open a document to do it; never list or link a file that `PathGuard.resolve` places outside `specs/`. (traces: DEC-002, FR-014)

**AIS-049**: Treat file and folder names as untrusted text: escape each with `esc` in a label or alias name and build each link with `doc_url`, so a name holding `<`, `&`, a quote or a space cannot change the markup or the link target. (traces: DEC-006, FR-014)

**AIS-050**: List a symbolic link inside a story that points to a document elsewhere under `specs/`; do not list one that resolves outside `specs/`. (traces: FR-013, FR-014)

## Edge Cases

<!-- Known edge cases and the behaviour required for each. -->

**AIS-051**: A folder with no Markdown documents adds no entry, error or empty heading. (traces: FR-015)

**AIS-052**: A story with one document shows that document as the only entry, marked current. (traces: FR-010)

**AIS-053**: A file named exactly `.md` has an empty name once the extension is removed and is labelled `[ref doc: blank]`, after its folder path when it is in a nested folder. (traces: FR-003, FR-005)

**AIS-054**: A document viewed through a symbolic link to a folder is not among the walked files, so add it to the list as the current entry under its own path, labelled and placed by the same rules, and list no other file of that linked folder. (traces: FR-010, DEC-002)

**AIS-055**: A symbolic link whose target is missing is not listed, because its resolved path is not a file, and a file that cannot be statted or resolved is skipped. (traces: DEC-002, DEC-003)

**AIS-056**: A listed document removed after the page was rendered gives the existing not-found page when its link is followed; an open page can be stale until it is reloaded. (traces: FR-016, DEC-001)

**AIS-057**: A symbolic link inside a story to a document in another story is listed under the link's path and links to the real path. (traces: FR-013, DEC-005)

## Explicit Exclusions

<!-- What must not be built or changed, from the approved scope. -->

**AIS-058**: Add no dependency; use only the Python standard library and keep the Python 3.11 minimum. (traces: FR-016, NFR-003)

**AIS-059**: Add no new route, endpoint or script that fetches the section. (traces: DEC-001)

**AIS-060**: Add no section to a document directly under `specs/`, the folder navigation page or the search results. (traces: FR-012, FR-017)

**AIS-061**: Do not change reference tooltips, error marking, search, folder navigation, breadcrumbs or Mermaid diagrams. (traces: FR-016)

**AIS-062**: Add no rule for two aliases with the same file name in different folders linked to one document. (traces: FR-006)

## Implementation Constraints

<!-- Performance limits, compatibility, migration and rollout constraints. -->

**AIS-063**: Order the entries as a pure function of the names, never of the order the file system returns or files were created. (traces: NFR-001, DEC-004)

**AIS-064**: Meet a contrast ratio of at least 4.5:1 between the text colour and the background for the links and the current entry. (traces: NFR-002, DEC-006)

**AIS-065**: Ship as an edited `specview.py` and two new test files, with no data to migrate, no feature flag and no configuration; rollback is reverting the change. (traces: DEC-001, DEC-007)

## Artefacts in Scope

<!--
  The approved diagrams and wireframes the agent must read, each as an item tracing to its ART id.
  A wireframe, ER diagram or technical sequence diagram listed here must be covered by a task.

  **AIS-013**: Read the container view before changing the API. (traces: ART-004)
-->

**AIS-066**: Read the system context diagram before changing the viewer. (traces: ART-001)

**AIS-067**: Read the sequence diagram of a developer reading a story from start to finish. (traces: ART-002)

**AIS-068**: Read the sequence diagram of a developer finding a nested document. (traces: ART-003)

**AIS-069**: Read the sequence diagram of a developer reading a document directly under `specs`. (traces: ART-004)

**AIS-070**: Read the container view before changing the viewer server. (traces: ART-007)

**AIS-071**: Read the component view before adding the reading-order builder or changing the Viewer and the page template. (traces: ART-008)

## Agent Guidance

<!-- Optional. Relevant files and directories, existing patterns to follow, commands and tests to run, constraints on modification. Delete this section if unused. -->

**AIS-072**: Run the whole suite with `python3 -m unittest discover -s tests`; it passes 74 tests before the change and must keep passing. (traces: DEC-007, NFR-003)

**AIS-073**: Start the real server in the integration tests as `tests/integration/support.py` does. (traces: DEC-007)

## Not applicable

<!-- Sections removed from this document, each with its reason: `- Existing Code: a new component`. -->

- Data Structures: the approved design adds or changes no persistent data and no entity (Data Design and Data Model are not applicable in the Technical Specification).

## Challenges

<!-- Recorded by `eil challenge`. -->

## Overrides

<!-- Recorded by `eil override`, each naming who, what and why. -->

## Change Log

<!-- eil:begin changelog -->
<!-- eil:end changelog -->

## Record

<!-- eil:begin provenance -->
```json
{
  "version": 1,
  "blocks": {
    "AIS-001": {
      "hash": "sha256:d157fbcce84c54aa24e00f7ae8e8ae0cdbb649c7b07153e755835040d5e200bf",
      "class": "restated",
      "cites": {
        "FR-001": "sha256:9b8829cba27184e4e9004fc0ba4af995bb30d52c81be952f804b2817d4ed7a36"
      }
    },
    "AIS-002": {
      "hash": "sha256:35ecb780bd8181dbfa7fc004c93f08cf48306642484514ae5cb8c443562d9beb",
      "class": "restated",
      "cites": {
        "FR-002": "sha256:32dc804048b7e426e532d1b98c0fc50d4ebdb1ebea550a3caa6e72002e6f2e6f"
      }
    },
    "AIS-003": {
      "hash": "sha256:61c489ff9eeee1832f21b88e834333b1c3e6ad34b12d9dff3aac3399c0f4b36e",
      "class": "restated",
      "cites": {
        "FR-003": "sha256:197f0e7bf32d3fffc1d86caf9e93b21576f2146c4b96744d98b9195835da670b"
      }
    },
    "AIS-004": {
      "hash": "sha256:e065331d34cf6e63b623a6c46d64e211944d9457578a6f4fe2b3005f65baab08",
      "class": "restated",
      "cites": {
        "FR-004": "sha256:9351afecec6d138f345d4b8a50128f10215e41705620c6441d15ebeb92e564a8"
      }
    },
    "AIS-005": {
      "hash": "sha256:7b3efe32a84407449feb6f0e6e2b14b6872e5a1bcefcaac8963c2aa6217bf1b4",
      "class": "restated",
      "cites": {
        "FR-005": "sha256:65cffe4e76d287540239f49d99854034164b552e04e3a5f968efbc820d0fc590"
      }
    },
    "AIS-006": {
      "hash": "sha256:54e23a48faf12e83c12c8f4538e2532f9ed4cebc29b900f82752975ca73a130b",
      "class": "restated",
      "cites": {
        "FR-006": "sha256:3e514e8dfd04bc478e405c56c902c4d400ee8620a0edc9f5da1d311dea49978d"
      }
    },
    "AIS-007": {
      "hash": "sha256:852b862cde2ffbc3856bf05a919a51e86888254ded48dd7e8b37ddd3058e9f8f",
      "class": "restated",
      "cites": {
        "FR-007": "sha256:7bcffe16420753854d6ef411e7c3099f58fe40bf91b17e707680884c894d989d"
      }
    },
    "AIS-008": {
      "hash": "sha256:ae0244647a8219ec8f3cd692a80d70c59679bc0502fada26aec39a85c98a61a7",
      "class": "restated",
      "cites": {
        "FR-008": "sha256:1efd77e47f9d55a3f735dac2b82d9d1534cd786f60fffcd8463bf2a28f8da6c6"
      }
    },
    "AIS-009": {
      "hash": "sha256:ca8faee8ca35286fad97ea40959e30bb078badade6d67c8dccdd9cff915f73f7",
      "class": "restated",
      "cites": {
        "FR-009": "sha256:ac1727d2ea6122e201b9f35a77530ece91dba013c30ac656bc80c791a5884aa5"
      }
    },
    "AIS-010": {
      "hash": "sha256:9f67f5f2fa3c62011554348671067d4429d372c85c25c1c2fb4a5f75e9f1c69f",
      "class": "restated",
      "cites": {
        "FR-010": "sha256:8aa5f448ddb370a99dcbb5281add4a0106cbb03152c32325dd17c921f07fe781"
      }
    },
    "AIS-011": {
      "hash": "sha256:c61dfa8f0d5ecf2716ab632ff7adf1e72c1a6949ea7f3a929fd37d8471306e6a",
      "class": "restated",
      "cites": {
        "FR-011": "sha256:0ca8c3df85b82bec17637d1f09bab4668b4bd26b3337664b6990b103bab3b0ec"
      }
    },
    "AIS-012": {
      "hash": "sha256:5bc6336c1bd0f8671de8ae8806beb0553d90203d3b451bb782bd67da09492001",
      "class": "restated",
      "cites": {
        "FR-012": "sha256:c398b73a4cbf412ded409ed8f094ae59ed47616c7a4bca37420906c7d2f7291c"
      }
    },
    "AIS-013": {
      "hash": "sha256:3a67ab57e283b333f166a1ffee484866594a8f199e200c2be907ebdc19a8eb7b",
      "class": "restated",
      "cites": {
        "FR-013": "sha256:38d94ad5c0f0b784877847af344fd77e14f9941ad73bbc98a535b7942b21e73a"
      }
    },
    "AIS-014": {
      "hash": "sha256:63501bcbe2699b95976faa6310fc67bcc0a812aa72a0cbbe5827fe33f3e87b66",
      "class": "restated",
      "cites": {
        "FR-014": "sha256:ad118cfdcba914b6dcced02aeaa12e219170b3d9b9b64e1cb3ae800f2cf133cd"
      }
    },
    "AIS-015": {
      "hash": "sha256:04a4bcfcfbe3b003ff1f953449e83f69bb14f8d5255add3bd21134a93d020b09",
      "class": "restated",
      "cites": {
        "FR-015": "sha256:f1d6d8705d95ac71564ee91d3882b78a9adc9ded77660d8d1531a57c74db3bb0"
      }
    },
    "AIS-016": {
      "hash": "sha256:ab023f06526e4601e7e4f6a76b3f05c41396747454b74be9fa4aae10707987e0",
      "class": "restated",
      "cites": {
        "FR-016": "sha256:ea3570068dfeaaa7dda913bd48c48be6dd4a84a8b69fe0e06859657edfaeb67d"
      }
    },
    "AIS-017": {
      "hash": "sha256:c917cf5df2dff0aba7c55da433e076853b08bdb67c203676b492393593e0fa7f",
      "class": "restated",
      "cites": {
        "FR-017": "sha256:1dd105d6d7f7eac38abd4ce9c97be3e06a173c742a3cb34e6d0bcf1e15376376"
      }
    },
    "AIS-018": {
      "hash": "sha256:de11e45b65e87fd463a911bef1475c1eaf39b9973938c7d144cbe5bd8e9917a6",
      "class": "restated",
      "cites": {
        "FR-001": "sha256:9b8829cba27184e4e9004fc0ba4af995bb30d52c81be952f804b2817d4ed7a36",
        "FR-012": "sha256:c398b73a4cbf412ded409ed8f094ae59ed47616c7a4bca37420906c7d2f7291c"
      }
    },
    "AIS-019": {
      "hash": "sha256:a997103070992e4c060534caba5663d24445fe04793930c80f13b655fe2ba3d7",
      "class": "restated",
      "cites": {
        "FR-004": "sha256:9351afecec6d138f345d4b8a50128f10215e41705620c6441d15ebeb92e564a8",
        "FR-005": "sha256:65cffe4e76d287540239f49d99854034164b552e04e3a5f968efbc820d0fc590"
      }
    },
    "AIS-020": {
      "hash": "sha256:a4a3c69d47e31fa59042fbcc5d4992379696223e9ccdf5a8de3800aaaacc30ed",
      "class": "restated",
      "cites": {
        "FR-007": "sha256:7bcffe16420753854d6ef411e7c3099f58fe40bf91b17e707680884c894d989d",
        "FR-008": "sha256:1efd77e47f9d55a3f735dac2b82d9d1534cd786f60fffcd8463bf2a28f8da6c6",
        "FR-009": "sha256:ac1727d2ea6122e201b9f35a77530ece91dba013c30ac656bc80c791a5884aa5"
      }
    },
    "AIS-021": {
      "hash": "sha256:635c20f5f43fc191ccdea31f97c26bfbbb66d4456df7d66c5a4253117b55e035",
      "class": "restated",
      "cites": {
        "FR-006": "sha256:3e514e8dfd04bc478e405c56c902c4d400ee8620a0edc9f5da1d311dea49978d"
      }
    },
    "AIS-022": {
      "hash": "sha256:55edcfd29969634bfdf1c81455cbf667576f9a63480b72acfc324ed8cd6e0769",
      "class": "restated",
      "cites": {
        "FR-014": "sha256:ad118cfdcba914b6dcced02aeaa12e219170b3d9b9b64e1cb3ae800f2cf133cd"
      }
    },
    "AIS-023": {
      "hash": "sha256:6644b93f8f8e69eb7e83d12643e22e6e83e44cefa9cb5a084ea219723345591c",
      "class": "restated",
      "cites": {
        "DEC-001": "sha256:bb921b2401109f1ece0e7a13243eaba9121b572231d2c6402f21a46830d083aa"
      }
    },
    "AIS-024": {
      "hash": "sha256:3f7c205c5d9ce8b91e3549e8711d2e35bcd942ce700b387a39a5225d3b7fd017",
      "class": "restated",
      "cites": {
        "DEC-002": "sha256:e5e293b732dc3070124d2538a452ac15b148fb9937d58da144d4ee8d004b2032"
      }
    },
    "AIS-025": {
      "hash": "sha256:c2bdca8fedfad8142d89052404b3d2ea44ac83970c8de11130fbf87af4d57794",
      "class": "restated",
      "cites": {
        "DEC-003": "sha256:36efe9d2ce0818895e0200cf12258c73ee561dcb82dbf2c4a1723d203a605105"
      }
    },
    "AIS-026": {
      "hash": "sha256:fb41e3346fa2320682eaa6c062601114552d60ebb273a6e385bebbfced0034ec",
      "class": "restated",
      "cites": {
        "DEC-004": "sha256:7b10b4a428165cd28fee8fa2619828a86dc5bbf81c06f10415da597c69d300d7"
      }
    },
    "AIS-027": {
      "hash": "sha256:a9f6fde904cd4b9b50af42f8df0504ff65dee864f66e6603a578d45e5c5f124b",
      "class": "restated",
      "cites": {
        "DEC-005": "sha256:141ce780db6dcb541ca4b1c2e4792550978c143cbd5eea57838c9736579db7be"
      }
    },
    "AIS-028": {
      "hash": "sha256:f23788fe05415553188b54763ee5135117d61b2507b290f16d7efb9f0b7530c6",
      "class": "restated",
      "cites": {
        "DEC-006": "sha256:39b03e67818d400e49ee296e2e3c28ac91daeaa69b23d14ab9a0ae88a080b5de"
      }
    },
    "AIS-029": {
      "hash": "sha256:8fd58257e32932167fab06b2858c2d35a2e89a004cfd293468c5a4e765e5f1b3",
      "class": "restated",
      "cites": {
        "DEC-007": "sha256:c092606ae0d1acdb955329fb0999903f6b0219c952e9d0bbaa51fa3ef1b8ce76"
      }
    },
    "AIS-030": {
      "hash": "sha256:e57d7d30152612780d8e18253036a07ff2c04f1462133d3e4a696d3afdcc4aa0",
      "class": "restated",
      "cites": {
        "DEC-001": "sha256:bb921b2401109f1ece0e7a13243eaba9121b572231d2c6402f21a46830d083aa",
        "ART-007": "sha256:084128aeb0d17c901971f78251314276ef4c4b2cc3d9bb09ed723e078fc5eeb9"
      }
    },
    "AIS-031": {
      "hash": "sha256:6591d4b6a388c08e9447c97cae6a6479374087c10fa73ff0b34c853c9f53bbcc",
      "class": "restated",
      "cites": {
        "ART-008": "sha256:f6fef5898a572d62890e617df6b3c58cd89f75af3a3f1c891255b59bd498b730",
        "DEC-002": "sha256:e5e293b732dc3070124d2538a452ac15b148fb9937d58da144d4ee8d004b2032"
      }
    },
    "AIS-032": {
      "hash": "sha256:42f55118f599932cdb6870ba5de41307bf89222be427097fa315daa98882e0da",
      "class": "inferred",
      "adds": "States from the Technical Specification's component text that the builder keeps no state.",
      "reviewed": {
        "by": "Lee Sinclair",
        "at": "2026-10-01T13:28:35Z",
        "list": "RVW-007",
        "reply": "Ok"
      },
      "sources": {
        "DEC-001": "sha256:bb921b2401109f1ece0e7a13243eaba9121b572231d2c6402f21a46830d083aa",
        "ART-008": "sha256:f6fef5898a572d62890e617df6b3c58cd89f75af3a3f1c891255b59bd498b730"
      }
    },
    "AIS-033": {
      "hash": "sha256:4d0d690106232bcac25a8dc35253845b7d23ae80f1a5bd59f3f1d0de01a8f365",
      "class": "restated",
      "cites": {
        "ART-008": "sha256:f6fef5898a572d62890e617df6b3c58cd89f75af3a3f1c891255b59bd498b730",
        "DEC-001": "sha256:bb921b2401109f1ece0e7a13243eaba9121b572231d2c6402f21a46830d083aa",
        "FR-017": "sha256:1dd105d6d7f7eac38abd4ce9c97be3e06a173c742a3cb34e6d0bcf1e15376376"
      }
    },
    "AIS-034": {
      "hash": "sha256:78bddaf7b4901a446ac1c0da1b283fa70f1452351fb39a34a5545c5e3dc4045c",
      "class": "restated",
      "cites": {
        "DEC-002": "sha256:e5e293b732dc3070124d2538a452ac15b148fb9937d58da144d4ee8d004b2032",
        "FR-014": "sha256:ad118cfdcba914b6dcced02aeaa12e219170b3d9b9b64e1cb3ae800f2cf133cd"
      }
    },
    "AIS-035": {
      "hash": "sha256:36f2adb477c1ed19b889389cd562597743c5e0fec1c126b5b37be07fa564cde8",
      "class": "restated",
      "cites": {
        "DEC-003": "sha256:36efe9d2ce0818895e0200cf12258c73ee561dcb82dbf2c4a1723d203a605105"
      }
    },
    "AIS-036": {
      "hash": "sha256:a550507c3cd8f3326ff97eeb9c0622d5da8ba74ee1dfb197ddd296e56da8e1e5",
      "class": "restated",
      "cites": {
        "DEC-006": "sha256:39b03e67818d400e49ee296e2e3c28ac91daeaa69b23d14ab9a0ae88a080b5de",
        "FR-014": "sha256:ad118cfdcba914b6dcced02aeaa12e219170b3d9b9b64e1cb3ae800f2cf133cd"
      }
    },
    "AIS-037": {
      "hash": "sha256:a31c9ae82c6ba4d575326b3d37805d76fc703a2edd8ea312feddd78e6b20f5c3",
      "class": "inferred",
      "adds": "Restates the Technical Specification's note that the page cache key already follows the story's Markdown files.",
      "reviewed": {
        "by": "Lee Sinclair",
        "at": "2026-10-01T13:28:35Z",
        "list": "RVW-007",
        "reply": "Ok"
      },
      "sources": {
        "DEC-001": "sha256:bb921b2401109f1ece0e7a13243eaba9121b572231d2c6402f21a46830d083aa"
      }
    },
    "AIS-038": {
      "hash": "sha256:ba473fccf4a4206208df9e0d0a9296d04740897cb107d829fbfe14b6d9f3e1f8",
      "class": "restated",
      "cites": {
        "DEC-002": "sha256:e5e293b732dc3070124d2538a452ac15b148fb9937d58da144d4ee8d004b2032",
        "FR-006": "sha256:3e514e8dfd04bc478e405c56c902c4d400ee8620a0edc9f5da1d311dea49978d"
      }
    },
    "AIS-039": {
      "hash": "sha256:ad883fe95ed533f35a62281366d369cc0dc5c866a542dc3ca2d00247901050be",
      "class": "restated",
      "cites": {
        "DEC-006": "sha256:39b03e67818d400e49ee296e2e3c28ac91daeaa69b23d14ab9a0ae88a080b5de"
      }
    },
    "AIS-040": {
      "hash": "sha256:593a84b3698508d760d5c5a181b96836d01b867fc566cb39f88f0edd9922ea95",
      "class": "inferred",
      "adds": "Carries the Existing System Impact note about the breadcrumbs' aria-current into an instruction.",
      "reviewed": {
        "by": "Lee Sinclair",
        "at": "2026-10-01T13:28:35Z",
        "list": "RVW-007",
        "reply": "Ok"
      },
      "sources": {
        "DEC-006": "sha256:39b03e67818d400e49ee296e2e3c28ac91daeaa69b23d14ab9a0ae88a080b5de",
        "DEC-007": "sha256:c092606ae0d1acdb955329fb0999903f6b0219c952e9d0bbaa51fa3ef1b8ce76"
      }
    },
    "AIS-041": {
      "hash": "sha256:950b583b5ce9974d7997eb650727f9c9e6b030de2e4db703f07b7f4bed46a3fc",
      "class": "inferred",
      "adds": "Names the builder's method and helper functions from the Technical Specification's Component Design.",
      "reviewed": {
        "by": "Lee Sinclair",
        "at": "2026-10-01T13:28:35Z",
        "list": "RVW-007",
        "reply": "Ok"
      },
      "sources": {
        "DEC-001": "sha256:bb921b2401109f1ece0e7a13243eaba9121b572231d2c6402f21a46830d083aa",
        "DEC-004": "sha256:7b10b4a428165cd28fee8fa2619828a86dc5bbf81c06f10415da597c69d300d7"
      }
    },
    "AIS-042": {
      "hash": "sha256:e20769aec8cd41ccf0b8dc382eb5b6b1f9fb630c2f2a2aadb819c995dd147ad9",
      "class": "restated",
      "cites": {
        "DEC-001": "sha256:bb921b2401109f1ece0e7a13243eaba9121b572231d2c6402f21a46830d083aa",
        "FR-011": "sha256:0ca8c3df85b82bec17637d1f09bab4668b4bd26b3337664b6990b103bab3b0ec"
      }
    },
    "AIS-043": {
      "hash": "sha256:ecbd7b859a28e78c8fb5102a68f8a73ac13df9e8c1862fda89e5240b590b68f0",
      "class": "restated",
      "cites": {
        "DEC-007": "sha256:c092606ae0d1acdb955329fb0999903f6b0219c952e9d0bbaa51fa3ef1b8ce76",
        "FR-004": "sha256:9351afecec6d138f345d4b8a50128f10215e41705620c6441d15ebeb92e564a8",
        "FR-005": "sha256:65cffe4e76d287540239f49d99854034164b552e04e3a5f968efbc820d0fc590",
        "FR-006": "sha256:3e514e8dfd04bc478e405c56c902c4d400ee8620a0edc9f5da1d311dea49978d",
        "FR-007": "sha256:7bcffe16420753854d6ef411e7c3099f58fe40bf91b17e707680884c894d989d",
        "FR-008": "sha256:1efd77e47f9d55a3f735dac2b82d9d1534cd786f60fffcd8463bf2a28f8da6c6",
        "FR-009": "sha256:ac1727d2ea6122e201b9f35a77530ece91dba013c30ac656bc80c791a5884aa5",
        "NFR-001": "sha256:df17800aee3588d157d4116760d6c0ac8b1aaaf338acd002ab064f7c755650e9"
      }
    },
    "AIS-044": {
      "hash": "sha256:50a4a6ae4576b654b7ac1578481d148899518955f15500b3d709f8c107cbd983",
      "class": "restated",
      "cites": {
        "DEC-007": "sha256:c092606ae0d1acdb955329fb0999903f6b0219c952e9d0bbaa51fa3ef1b8ce76",
        "FR-001": "sha256:9b8829cba27184e4e9004fc0ba4af995bb30d52c81be952f804b2817d4ed7a36",
        "FR-002": "sha256:32dc804048b7e426e532d1b98c0fc50d4ebdb1ebea550a3caa6e72002e6f2e6f",
        "FR-010": "sha256:8aa5f448ddb370a99dcbb5281add4a0106cbb03152c32325dd17c921f07fe781",
        "FR-012": "sha256:c398b73a4cbf412ded409ed8f094ae59ed47616c7a4bca37420906c7d2f7291c",
        "FR-013": "sha256:38d94ad5c0f0b784877847af344fd77e14f9941ad73bbc98a535b7942b21e73a",
        "FR-014": "sha256:ad118cfdcba914b6dcced02aeaa12e219170b3d9b9b64e1cb3ae800f2cf133cd",
        "FR-015": "sha256:f1d6d8705d95ac71564ee91d3882b78a9adc9ded77660d8d1531a57c74db3bb0",
        "FR-017": "sha256:1dd105d6d7f7eac38abd4ce9c97be3e06a173c742a3cb34e6d0bcf1e15376376"
      }
    },
    "AIS-045": {
      "hash": "sha256:e42a3ac6a992fe9a3a24deead6ecc93c3b1da3e78be7c23ede5257aa6c1ae9ea",
      "class": "restated",
      "cites": {
        "DEC-007": "sha256:c092606ae0d1acdb955329fb0999903f6b0219c952e9d0bbaa51fa3ef1b8ce76",
        "NFR-002": "sha256:b6d43217718ec3585d21c7e35c03545369d59141a6cd7f07acb47100eef1826b"
      }
    },
    "AIS-046": {
      "hash": "sha256:4792cd0d137f7703b41afb02fef701d595b090df0d8ca64756f18f64a6c3256a",
      "class": "restated",
      "cites": {
        "FR-016": "sha256:ea3570068dfeaaa7dda913bd48c48be6dd4a84a8b69fe0e06859657edfaeb67d",
        "NFR-003": "sha256:38473b65fca10e09faa1982b8eee81daace9150eebf3baefbaa5e7209036eabf"
      }
    },
    "AIS-047": {
      "hash": "sha256:d00cae3fd57ea3b2f433c6b5fff99fa07d2841409c68b29065dbd30ec0ac64a4",
      "class": "restated",
      "cites": {
        "NFR-003": "sha256:38473b65fca10e09faa1982b8eee81daace9150eebf3baefbaa5e7209036eabf"
      }
    },
    "AIS-048": {
      "hash": "sha256:f7558a2888e61d956d25926606b4453d188b26a00d183fb0d1d92784835552a7",
      "class": "restated",
      "cites": {
        "DEC-002": "sha256:e5e293b732dc3070124d2538a452ac15b148fb9937d58da144d4ee8d004b2032",
        "FR-014": "sha256:ad118cfdcba914b6dcced02aeaa12e219170b3d9b9b64e1cb3ae800f2cf133cd"
      }
    },
    "AIS-049": {
      "hash": "sha256:5f71e91094328301a8d34c12620a403975b866de38b82b0d469c277af597a0d8",
      "class": "restated",
      "cites": {
        "DEC-006": "sha256:39b03e67818d400e49ee296e2e3c28ac91daeaa69b23d14ab9a0ae88a080b5de",
        "FR-014": "sha256:ad118cfdcba914b6dcced02aeaa12e219170b3d9b9b64e1cb3ae800f2cf133cd"
      }
    },
    "AIS-050": {
      "hash": "sha256:61ffe257563f058d194c7a2b53f194c7214e6bf8d8bc6da4fb12868459ee68be",
      "class": "restated",
      "cites": {
        "FR-013": "sha256:38d94ad5c0f0b784877847af344fd77e14f9941ad73bbc98a535b7942b21e73a",
        "FR-014": "sha256:ad118cfdcba914b6dcced02aeaa12e219170b3d9b9b64e1cb3ae800f2cf133cd"
      }
    },
    "AIS-051": {
      "hash": "sha256:e5f372d0f875d229848dba789a21a65c62debd127131a4ac1696bbc41a36bd62",
      "class": "restated",
      "cites": {
        "FR-015": "sha256:f1d6d8705d95ac71564ee91d3882b78a9adc9ded77660d8d1531a57c74db3bb0"
      }
    },
    "AIS-052": {
      "hash": "sha256:76fca578e34b38ea8bc39a80729fcc493c169028c447bbeaaf0d590f3184a0a3",
      "class": "restated",
      "cites": {
        "FR-010": "sha256:8aa5f448ddb370a99dcbb5281add4a0106cbb03152c32325dd17c921f07fe781"
      }
    },
    "AIS-053": {
      "hash": "sha256:43784ea41393117378d068f0daba401fd45776c5a9f855a78b939b5d523777df",
      "class": "inferred",
      "adds": "Carries the label of a file named exactly .md from the Component Design, accepted in CH-010.",
      "reviewed": {
        "by": "Lee Sinclair",
        "at": "2026-10-01T13:28:35Z",
        "list": "RVW-007",
        "reply": "Ok"
      },
      "sources": {
        "FR-003": "sha256:197f0e7bf32d3fffc1d86caf9e93b21576f2146c4b96744d98b9195835da670b",
        "FR-005": "sha256:65cffe4e76d287540239f49d99854034164b552e04e3a5f968efbc820d0fc590"
      }
    },
    "AIS-054": {
      "hash": "sha256:7a39487f01f3a80c3ee002b024dabd3721110513298b128067743627c1b79aa3",
      "class": "inferred",
      "adds": "Carries the handling of a document viewed through a linked folder from the Component Design, accepted in CH-009.",
      "reviewed": {
        "by": "Lee Sinclair",
        "at": "2026-10-01T13:28:35Z",
        "list": "RVW-007",
        "reply": "Ok"
      },
      "sources": {
        "FR-010": "sha256:8aa5f448ddb370a99dcbb5281add4a0106cbb03152c32325dd17c921f07fe781",
        "DEC-002": "sha256:e5e293b732dc3070124d2538a452ac15b148fb9937d58da144d4ee8d004b2032"
      }
    },
    "AIS-055": {
      "hash": "sha256:98bfdbf9348e859ca1304c5b69a29c498cf4ec9f2d44244cfc810b4f26316bfe",
      "class": "inferred",
      "adds": "Carries the skipping of unreadable or missing-target links from the Error Handling section.",
      "reviewed": {
        "by": "Lee Sinclair",
        "at": "2026-10-01T13:28:35Z",
        "list": "RVW-007",
        "reply": "Ok"
      },
      "sources": {
        "DEC-002": "sha256:e5e293b732dc3070124d2538a452ac15b148fb9937d58da144d4ee8d004b2032",
        "DEC-003": "sha256:36efe9d2ce0818895e0200cf12258c73ee561dcb82dbf2c4a1723d203a605105"
      }
    },
    "AIS-056": {
      "hash": "sha256:7318ba523083068f8e195f78ec77a7c0b642b9f52f7a863dafa8c421ceeb7a7f",
      "class": "inferred",
      "adds": "Carries the stale-page and removed-document behaviour from the Error Handling section.",
      "reviewed": {
        "by": "Lee Sinclair",
        "at": "2026-10-01T13:28:35Z",
        "list": "RVW-007",
        "reply": "Ok"
      },
      "sources": {
        "FR-016": "sha256:ea3570068dfeaaa7dda913bd48c48be6dd4a84a8b69fe0e06859657edfaeb67d",
        "DEC-001": "sha256:bb921b2401109f1ece0e7a13243eaba9121b572231d2c6402f21a46830d083aa"
      }
    },
    "AIS-057": {
      "hash": "sha256:8676693afdc4b17e371018536f85159d37c6ed8161a1223016b4c0a9fd45be97",
      "class": "restated",
      "cites": {
        "FR-013": "sha256:38d94ad5c0f0b784877847af344fd77e14f9941ad73bbc98a535b7942b21e73a",
        "DEC-005": "sha256:141ce780db6dcb541ca4b1c2e4792550978c143cbd5eea57838c9736579db7be"
      }
    },
    "AIS-058": {
      "hash": "sha256:31f0a466e2d5a2de65bf3281a01357947b596fe09b91be59b86926900d117152",
      "class": "restated",
      "cites": {
        "FR-016": "sha256:ea3570068dfeaaa7dda913bd48c48be6dd4a84a8b69fe0e06859657edfaeb67d",
        "NFR-003": "sha256:38473b65fca10e09faa1982b8eee81daace9150eebf3baefbaa5e7209036eabf"
      }
    },
    "AIS-059": {
      "hash": "sha256:980c28303da1bead8671df27d5a416e946d3bc28609c246558b51026f89adba6",
      "class": "restated",
      "cites": {
        "DEC-001": "sha256:bb921b2401109f1ece0e7a13243eaba9121b572231d2c6402f21a46830d083aa"
      }
    },
    "AIS-060": {
      "hash": "sha256:e9ac7c0cdaf9029090ee28b5d46e6691d0f80829449612677ebd0656896c53dc",
      "class": "restated",
      "cites": {
        "FR-012": "sha256:c398b73a4cbf412ded409ed8f094ae59ed47616c7a4bca37420906c7d2f7291c",
        "FR-017": "sha256:1dd105d6d7f7eac38abd4ce9c97be3e06a173c742a3cb34e6d0bcf1e15376376"
      }
    },
    "AIS-061": {
      "hash": "sha256:28096f8adbffe497dfb993efa0b188bc016240654b224714b46bf13bbe144abb",
      "class": "restated",
      "cites": {
        "FR-016": "sha256:ea3570068dfeaaa7dda913bd48c48be6dd4a84a8b69fe0e06859657edfaeb67d"
      }
    },
    "AIS-062": {
      "hash": "sha256:80cd3c27482939fb3730e0c8c7334e3fb9fb389cdad56cd2848b63088b2b9334",
      "class": "inferred",
      "adds": "States that the Technical Specification's risk of two same-named aliases is left without a rule.",
      "reviewed": {
        "by": "Lee Sinclair",
        "at": "2026-10-01T13:28:35Z",
        "list": "RVW-007",
        "reply": "Ok"
      },
      "sources": {
        "FR-006": "sha256:3e514e8dfd04bc478e405c56c902c4d400ee8620a0edc9f5da1d311dea49978d"
      }
    },
    "AIS-063": {
      "hash": "sha256:9f81319bfeb664e3fd3502379d744995dd2ed0514c9d81352c8a6aa5aa66297d",
      "class": "restated",
      "cites": {
        "NFR-001": "sha256:df17800aee3588d157d4116760d6c0ac8b1aaaf338acd002ab064f7c755650e9",
        "DEC-004": "sha256:7b10b4a428165cd28fee8fa2619828a86dc5bbf81c06f10415da597c69d300d7"
      }
    },
    "AIS-064": {
      "hash": "sha256:3cdad1b135aa83d533900483967d0038eb5757e96280afad24c7c1ce2dc0953c",
      "class": "restated",
      "cites": {
        "NFR-002": "sha256:b6d43217718ec3585d21c7e35c03545369d59141a6cd7f07acb47100eef1826b",
        "DEC-006": "sha256:39b03e67818d400e49ee296e2e3c28ac91daeaa69b23d14ab9a0ae88a080b5de"
      }
    },
    "AIS-065": {
      "hash": "sha256:128abb124e342a32b0a9722b3ab6ef7d20ec160ddd2951c3d5d7e70e816784ad",
      "class": "restated",
      "cites": {
        "DEC-001": "sha256:bb921b2401109f1ece0e7a13243eaba9121b572231d2c6402f21a46830d083aa",
        "DEC-007": "sha256:c092606ae0d1acdb955329fb0999903f6b0219c952e9d0bbaa51fa3ef1b8ce76"
      }
    },
    "AIS-066": {
      "hash": "sha256:74470d9070ee0a7f576cb17c21693efd3dfbb0e679fafd1aa2b70d0f106d8c9d",
      "class": "restated",
      "cites": {
        "ART-001": "sha256:db09019fe61826127e6ddee74f38ebd6ccf021a75950a1581faf261735a28082"
      }
    },
    "AIS-067": {
      "hash": "sha256:4e5cda7ad36f19239bd52ec97992bbdea29ea5387a8b9403a25f861d17befc5a",
      "class": "restated",
      "cites": {
        "ART-002": "sha256:838fefba764faf33481f62a05116992002aab4302863b86d1bb9d36d421be3b0"
      }
    },
    "AIS-068": {
      "hash": "sha256:e13e4a4b72a912f1a50cc34c3974fda7a1909c654610269bc3d818a2449772d9",
      "class": "restated",
      "cites": {
        "ART-003": "sha256:4de5457a0b5bfa6ddea42f1d85df6e68891e5fcdd4e063054d9a130882c55a6e"
      }
    },
    "AIS-069": {
      "hash": "sha256:943f98682a7109638e79552b646c0f59a99c7d4f90c39c71b9886b65515588e4",
      "class": "restated",
      "cites": {
        "ART-004": "sha256:83f9249852f7a21d3cdb6d99a2f40ae2cdda500c21f45597f0402513bd982847"
      }
    },
    "AIS-070": {
      "hash": "sha256:393dec9b65fd2c1aec9a44685ba02a0b5e01e6c3f9be900bc3472b85cbfca47d",
      "class": "restated",
      "cites": {
        "ART-007": "sha256:084128aeb0d17c901971f78251314276ef4c4b2cc3d9bb09ed723e078fc5eeb9"
      }
    },
    "AIS-071": {
      "hash": "sha256:949f5154a1095c8df264687c4ac55e9526173f0ef925ac5686dfbfda4f868179",
      "class": "restated",
      "cites": {
        "ART-008": "sha256:f6fef5898a572d62890e617df6b3c58cd89f75af3a3f1c891255b59bd498b730"
      }
    },
    "AIS-072": {
      "hash": "sha256:0bf9e4d35bb7db4ce08bc326a291c9f80c1fce8aa4ceca7880769384588e0e7d",
      "class": "inferred",
      "adds": "Names the repository's test command and the baseline of 74 passing tests from the Technical Specification's text.",
      "reviewed": {
        "by": "Lee Sinclair",
        "at": "2026-10-01T13:28:35Z",
        "list": "RVW-007",
        "reply": "Ok"
      },
      "sources": {
        "DEC-007": "sha256:c092606ae0d1acdb955329fb0999903f6b0219c952e9d0bbaa51fa3ef1b8ce76",
        "NFR-003": "sha256:38473b65fca10e09faa1982b8eee81daace9150eebf3baefbaa5e7209036eabf"
      }
    },
    "AIS-073": {
      "hash": "sha256:339a23541e50e8ae1a51f34e0731075e73ce78d34235127ca88ec96786c9ca58",
      "class": "inferred",
      "adds": "Points to the existing integration test support module named in DEC-007.",
      "reviewed": {
        "by": "Lee Sinclair",
        "at": "2026-10-01T13:28:35Z",
        "list": "RVW-007",
        "reply": "Ok"
      },
      "sources": {
        "DEC-007": "sha256:c092606ae0d1acdb955329fb0999903f6b0219c952e9d0bbaa51fa3ef1b8ce76"
      }
    },
    "Not applicable#7964320e1605": {
      "hash": "sha256:7964320e16056d309f15bf4a4bc443c4919d97610afdda9cc2638d6715a55aec",
      "reviewed": {
        "by": "Lee Sinclair",
        "at": "2026-10-01T13:28:35Z",
        "list": "RVW-007",
        "reply": "Ok"
      },
      "class": "inferred"
    }
  },
  "acceptances": [
    {
      "id": "RVW-007",
      "stage": "ai-spec",
      "kind": "inferred",
      "digest": "sha256:d610fc066c1fda30618b9867899e2241b797ac718aae8fbc9c313384b790b0c1",
      "by": "Lee Sinclair",
      "at": "2026-10-01T13:28:35Z",
      "reply": "Ok",
      "accepted": [
        "AIS-032",
        "AIS-037",
        "AIS-040",
        "AIS-041",
        "AIS-053",
        "AIS-054",
        "AIS-055",
        "AIS-056",
        "AIS-062",
        "AIS-072",
        "AIS-073",
        "Not applicable#7964320e1605"
      ],
      "except": [],
      "questioned": [],
      "reopened": [],
      "reason": null,
      "hashes": {
        "AIS-032": "sha256:42f55118f599932cdb6870ba5de41307bf89222be427097fa315daa98882e0da",
        "AIS-037": "sha256:a31c9ae82c6ba4d575326b3d37805d76fc703a2edd8ea312feddd78e6b20f5c3",
        "AIS-040": "sha256:593a84b3698508d760d5c5a181b96836d01b867fc566cb39f88f0edd9922ea95",
        "AIS-041": "sha256:950b583b5ce9974d7997eb650727f9c9e6b030de2e4db703f07b7f4bed46a3fc",
        "AIS-053": "sha256:43784ea41393117378d068f0daba401fd45776c5a9f855a78b939b5d523777df",
        "AIS-054": "sha256:7a39487f01f3a80c3ee002b024dabd3721110513298b128067743627c1b79aa3",
        "AIS-055": "sha256:98bfdbf9348e859ca1304c5b69a29c498cf4ec9f2d44244cfc810b4f26316bfe",
        "AIS-056": "sha256:7318ba523083068f8e195f78ec77a7c0b642b9f52f7a863dafa8c421ceeb7a7f",
        "AIS-062": "sha256:80cd3c27482939fb3730e0c8c7334e3fb9fb389cdad56cd2848b63088b2b9334",
        "AIS-072": "sha256:0bf9e4d35bb7db4ce08bc326a291c9f80c1fce8aa4ceca7880769384588e0e7d",
        "AIS-073": "sha256:339a23541e50e8ae1a51f34e0731075e73ce78d34235127ca88ec96786c9ca58",
        "Not applicable#7964320e1605": "sha256:7964320e16056d309f15bf4a4bc443c4919d97610afdda9cc2638d6715a55aec"
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
  "stage": "ai-spec",
  "evaluated_at": "2026-10-01T13:26:57Z",
  "fingerprint": "sha256:721541aec86ff0b9cb3d78c5edaa8160e9f3417e607d68b8fb033ef2bbd834d9",
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
