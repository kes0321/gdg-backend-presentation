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

Status: TODO

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
