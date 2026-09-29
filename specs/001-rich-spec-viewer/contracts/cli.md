# Contract: starting the viewer

From DEC-006, DEC-007 and DEC-008.

## Command

```text
python3 specview.py [--port N] [--host ADDRESS]
```

Run from the project folder; that folder is the start folder, and only `specs/` below it is served. Requires Python 3.11 or later and nothing else (DEC-006).

| Flag | Default | Meaning |
|---|---|---|
| `--port N` | first free port from 8000 to 8019 | Use exactly this port; fail with a message if it is busy |
| `--host ADDRESS` | `0.0.0.0` in a detected container, otherwise `127.0.0.1` | Override the bind address (DEC-008) |

Neither flag is ever required (FR-017).

## Container detection (DEC-008)

A container is detected when `/.dockerenv` exists, or the environment has `REMOTE_CONTAINERS` or `CODESPACES`.

## Start-up output

```text
Serving specs/ from /home/lee/projects/app
Listening on 127.0.0.1:8000 (no container detected)
Open http://localhost:8000/
Press Ctrl+C to stop.
```

Inside a container the second line reads, for example, `Listening on 0.0.0.0:8000 (container detected: /.dockerenv)`. The URL is then opened with `webbrowser`; failure to open a browser is not an error.

## Exit

- All ports 8000 to 8019 busy: a message naming the range, exit status 1.
- A Python older than 3.11: a message naming the required version, exit status 1.
- Ctrl+C: stops cleanly, exit status 0.

## Terminal output while running

One line per request (method, path, status), and the traceback of any rendering error (Technical Specification, Observability).
