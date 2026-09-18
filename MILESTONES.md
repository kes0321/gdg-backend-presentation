# Implementation Milestones

The complete project requirements are defined in `SPEC.md`.

Only implement one milestone at a time.

---

## M01 — Workspace and WebSocket Skeleton

Status: COMPLETE

Create:

```text
websocket-server/
websocket-complete/
```

Both must contain:

```text
app.py
requirements.txt
README.md
static/
  index.html
  style.css
  game.js
```

Implement only:

* FastAPI application
* static frontend serving
* simple name entry screen
* empty game area
* Uvicorn-compatible setup
* dependency files

Do not implement multiplayer behavior yet.

Verification:

* both projects install successfully
* `uvicorn app:app --host 0.0.0.0 --port 8000` works
* `http://localhost:8000` loads

---

## M02 — WebSocket Join and Connection

Status: COMPLETE

Implement in both WebSocket projects:

* `/ws`
* WebSocket accept
* active connection tracking
* server-generated player ID
* player name join message
* in-memory player state
* random initial position
* player count
* rendering connected players
* disconnect cleanup

Do not implement movement yet.

Keep `websocket-server` and `websocket-complete` functionally identical.

Verification:

* two browsers can join with different names
* both players appear
* closing one browser removes that player

---

## M03 — WebSocket Movement and Broadcast

Status: COMPLETE

Implement:

* WASD / arrow movement
* client `move` messages
* server state updates
* broadcast updated state to every active WebSocket connection

The broadcast block must remain very easy to identify and later replace with a student TODO.

Do not add unnecessary abstractions.

Verification:

* two browsers connect
* moving player A updates player A on player B's screen
* movement works in both directions
* positions stay within the game area

This milestone contains the core workshop code.

---

## M04 — Polling Version

Status: COMPLETE

Create:

```text
polling-server/
```

Match the WebSocket project's UI and game behavior as closely as possible.

Implement:

* `POST /api/join`
* `POST /api/move`
* `GET /api/state`
* `POST /api/leave`
* server-generated player IDs
* in-memory state
* repeated HTTP polling

Define one obvious frontend constant:

```javascript
const POLL_INTERVAL_MS = 100;
```

Do not use WebSocket, SSE, or another push mechanism.

Verification:

* two browsers can join
* movement is synchronized via HTTP polling
* no WebSocket connection exists
* 1000 ms / 500 ms / 100 ms polling intervals work

---

## M05 — Metrics and Demo Instrumentation

Status: COMPLETE

Add to all relevant projects:

```text
GET /api/metrics
POST /api/metrics/reset
```

WebSocket metrics:

* uptime
* connected players
* current WebSocket connections
* total connections opened
* incoming messages
* join messages
* move messages
* outgoing messages

Polling metrics:

* uptime
* connected players
* total API requests
* join requests
* move requests
* state polling requests
* leave requests

Requirements:

* metrics reset must not remove players
* polling logs must not flood the terminal

Verification:

* metrics increase correctly during gameplay
* reset works without affecting game state

---

## M06 — Final Verification and Documentation

Status: COMPLETE

Perform final consistency pass.

Verify:

* `websocket-server` and `websocket-complete` remain equivalent
* Polling and WebSocket UI/game rules match
* all three projects run independently
* READMEs contain correct setup commands
* WebSocket message flow is documented
* Polling API is documented
* metrics are documented
* broadcast code location is documented
* polling interval location is documented

Run practical multi-browser tests.

Do not deploy to Google Cloud yet.

Do not create the student TODO repository yet.

Finish with a concise final project report.

## M07 — Presentation Structure and Speaker Script

Status: COMPLETE

Read:

* `PRESENTATION_SPEC.md`
* relevant code and README files from all three completed projects

Create:

```text
presentation/script.txt
```

Do NOT create the final PDF yet.

The script must define the complete presentation slide-by-slide.

For every slide include:

* slide number
* slide title
* intended slide content
* what the presenter should say
* demo or hands-on action if applicable
* approximate time allocation when useful

The script must cover the complete 90-minute session defined in `PRESENTATION_SPEC.md`.

Important:

* Ground implementation-specific statements in the actual source code.
* Identify the exact source locations suitable for WebSocket and Polling code snippets.
* Clearly explain why `await websocket.receive_json()` is not HTTP polling.
* Include the async I/O / event loop / OS socket / epoll connection at an appropriate level.
* Do not fabricate benchmark results that have not been measured.
* For the final Polling vs WebSocket live comparison, describe which metrics will be observed during the live experiment.

Verification:

* total session fits approximately 90 minutes
* hands-on exercise timing is realistic
* presentation follows one coherent narrative
* all major technical claims are accurate
* slide count is reasonable for the allotted speaking time
* live demo and hands-on transitions are explicitly scripted

After verification:

* mark M07 complete
* create a local Git commit
* do not begin M08

## M08 — Generate Presentation PDF

Status: COMPLETE

Read the completed:

```text
presentation/script.txt
```

Generate:

```text
presentation/presentation.pdf
```

The PDF must follow `PRESENTATION_SPEC.md`.

Requirements:

* 16:9 landscape
* white background
* simple technical presentation style
* large readable typography
* concise slide text
* simple diagrams where useful
* actual source snippets where specified
* slide numbers
* Korean text rendered correctly
* no unnecessary decoration

The slides and `script.txt` must remain aligned.

The PDF should support the speaker rather than duplicate the entire script.

Do not fill slides with paragraphs from the speaker notes.

Verification:

* PDF opens successfully
* page count matches the script
* slide numbering matches
* no clipping or overflow
* code is readable
* diagrams are readable
* Korean glyphs render correctly

After verification:

* mark M08 complete
* create a local Git commit
* do not begin M09

### Runtime fallback

M08 must not fail solely because a presentation-specific artifact runtime is unavailable.

The deliverable is the PDF itself.

Use an available local PDF-generation approach that satisfies `PRESENTATION_SPEC.md`. Prefer simple and deterministic generation over attempting to reproduce a PowerPoint authoring environment.


## M09 — Final Presentation Verification

Status: TODO

Perform a final presentation review.

Inspect every page of:

```text
presentation/presentation.pdf
```

and cross-check it with:

```text
presentation/script.txt
```

Verify the complete narrative:

1. public WebSocket game demo
2. multiplayer communication problem
3. HTTP request-response limitation
4. polling
5. polling latency/request-frequency tradeoff
6. Long Polling and SSE
7. WebSocket
8. HTTP Upgrade handshake
9. persistent TCP connection and WebSocket frames
10. how the server waits for socket data
11. async/await, event loop, socket readiness, and epoll context
12. actual FastAPI WebSocket implementation
13. hands-on broadcast exercise
14. Polling implementation
15. public Polling demo
16. live metrics comparison
17. appropriate use cases for HTTP vs WebSocket
18. next game-server problems such as concurrency, tick/state synchronization, latency, and server authority

Check technical accuracy especially around:

* TCP vs HTTP vs WebSocket
* WebSocket frames
* `await`
* event loops
* epoll
* server push
* polling request behavior

Do not claim benchmark numbers unless they are actual measured values.

Ensure the final `presentation/` directory contains exactly:

```text
presentation.pdf
script.txt
```

If any issue is found, fix it before completing M09.

Finally:

* mark M09 complete
* create a local Git commit
* report the final page count and approximate presentation duration
