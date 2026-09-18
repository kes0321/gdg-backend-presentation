# Project Instructions

This repository contains a teaching/demo project for a GDGoC backend presentation about HTTP Polling vs WebSocket.

## Source of Truth

Before implementing any milestone, read:

* `SPEC.md` — complete project requirements and constraints
* `MILESTONES.md` — implementation order and current progress

Do not reinterpret or expand the scope beyond these documents.

## Working Rules

* Implement exactly one milestone at a time.
* Do not start the next milestone unless explicitly asked.
* Keep every completed milestone runnable.
* Prefer simple, educational code over production abstractions.
* Do not add unrequested features.
* Do not over-engineer.
* Minimize dependencies.
* Keep WebSocket concepts directly visible in the source code.
* Do not hide broadcast behavior behind large abstractions such as a complex `ConnectionManager`.
* Keep the WebSocket and Polling game behavior/UI as similar as possible.

## Tech Stack

* Python 3.11+
* FastAPI
* Uvicorn
* FastAPI native WebSocket support
* Vanilla HTML/CSS/JavaScript
* In-memory state

Do not introduce React, Node.js, Spring, Socket.IO, Redis, databases, Docker requirements, SSE, STOMP, or other unnecessary infrastructure.

## Workspace Structure

The final workspace must contain:

```text
websocket-server/
polling-server/
websocket-complete/
```

Each project must be standalone.

Do not use symlinks or cross-project imports.

## Verification

At the end of each milestone:

1. Run the relevant application/tests.
2. Fix errors before stopping.
3. Confirm that previously completed milestones still work.
4. Update the milestone status in `MILESTONES.md`.
5. Give a concise report containing:

   * files changed
   * behavior implemented
   * verification performed
   * remaining milestone

Avoid repeating the entire project specification in the final report.

## Git

Use local Git only.

* Do not create remotes.
* Do not push, pull, or fetch.
* Create one clear commit after each successfully verified milestone.
* Do not amend previous milestone commits unless explicitly requested.

## Token / Context Efficiency

* Read only the parts of `SPEC.md` relevant to the current milestone unless broader context is required.
* Do not repeatedly summarize the full specification.
* Do not inspect unrelated files without a reason.
* Prefer targeted edits over large rewrites.
* Do not regenerate files that already satisfy the requirements.
