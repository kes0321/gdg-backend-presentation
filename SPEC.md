# Goal

Build three small standalone multiplayer game demo projects for a backend study presentation about HTTP Polling vs WebSocket.

Create all three projects as subdirectories of the current workspace root:

```text id="aqa7px"
websocket-server/
polling-server/
websocket-complete/
```

Do not create files outside these directories unless absolutely necessary.

The application is intentionally very small.

The only game features are:

1. A player enters a name and joins.
2. Players are displayed as simple shapes with their names.
3. A player moves using WASD or arrow keys.
4. Other connected clients can see that player's movement.
5. When a player disconnects or leaves, that player disappears.

Do NOT add chat, authentication, database persistence, rooms, combat, scores, matchmaking, accounts, animations, game engines, or other game features.

The purpose of this project is to demonstrate the difference between:

* persistent bidirectional WebSocket communication
* repeated HTTP Polling

---

# Technology

Use:

* Python 3.11+
* FastAPI
* Uvicorn
* FastAPI native WebSocket support
* Vanilla HTML / CSS / JavaScript
* in-memory server state

Do NOT use:

* Spring
* Node.js
* Socket.IO
* React / Vue / Next.js
* Redis
* databases
* Docker as a requirement
* external realtime frameworks
* STOMP
* SSE

Keep dependencies minimal.

Each project must be independently runnable.

Use a simple setup such as:

```bash id="t3vbew"
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000
```

On Windows, document the corresponding virtual environment activation command in the README.

Use port 8000 by default.

The applications should be deployable later to a Google Cloud VM without major code changes.

---

# Important Teaching Principle

This is teaching/demo code.

The networking concepts must be visible directly in the source code.

Do NOT over-abstract the WebSocket logic.

In particular, avoid hiding the important logic behind large helper classes such as a complex `ConnectionManager`.

It is acceptable to use a very small helper function where it improves readability, but the following concepts should remain immediately visible to students:

```python id="5l0vf2"
await websocket.accept()

await websocket.receive_json()

active_connections

for connection in active_connections:
    await connection.send_json(...)

WebSocketDisconnect
```

The exercise should make it obvious that broadcasting means:

> keeping track of connected WebSocket clients and sending data to each relevant connection.

Optimize for educational clarity rather than production architecture.

---

# Shared UI / Game Behavior

The WebSocket and Polling versions must look and behave as similarly as possible.

Use the same frontend design and game rules in both implementations.

Initial screen:

```text id="ocmdg1"
Enter your name
[            ]
[ Join Game ]
```

After joining:

```text id="o7qv3a"
┌─────────────────────────────────────┐
│ Players: 4                          │
│                                     │
│       Alice                         │
│         ■                           │
│                         Bob         │
│                          ■          │
│                                     │
│ Controls: WASD / Arrow Keys         │
└─────────────────────────────────────┘
```

Requirements:

* Give each player a server-generated unique ID.
* The client submits only the player's display name.
* Store player state in memory.
* Each player state should contain at least:

  * id
  * name
  * x
  * y
* Constrain player positions to the visible game area.
* Initial positions may be random.
* Movement should feel responsive.
* No collision detection is required.
* No physics is required.
* Display the current number of connected players.
* Keep rendering simple with DOM elements and CSS.

Use the same:

* game dimensions
* movement step/speed
* player representation
* name rendering
* overall UI
* game rules

for WebSocket and Polling versions.

---

# Project 1 — websocket-server

Directory:

```text id="yc79go"
websocket-server/
```

This is the complete WebSocket version that will later be deployed to Google Cloud as the public multiplayer demo.

Use FastAPI native WebSocket support.

Serve the frontend from the same FastAPI application.

A simple structure is preferred:

```text id="cdtg7g"
websocket-server/
├── app.py
├── requirements.txt
├── README.md
└── static/
    ├── index.html
    ├── style.css
    └── game.js
```

Equivalent minimal structure is acceptable.

---

# WebSocket Endpoint

Use:

```text id="4ftdhi"
/ws
```

The connection lifecycle should be easy to understand.

Conceptually:

```python id="23bb1q"
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    # track connection

    try:
        while True:
            data = await websocket.receive_json()

            # process join / move
            # update server state
            # broadcast updated state

    except WebSocketDisconnect:
        # remove connection
        # remove player
        # broadcast updated state
```

The exact code may differ, but preserve this educational structure.

---

# WebSocket Message Flow

Client → Server:

Join:

```json id="ghhtxd"
{
  "type": "join",
  "name": "Alice"
}
```

Move:

```json id="i5gspq"
{
  "type": "move",
  "x": 120,
  "y": 200
}
```

The server should NOT trust a client-provided player ID.

Associate each WebSocket connection with the player ID generated by the server.

Server → Client:

Use a simple shared-state message such as:

```json id="5rm8db"
{
  "type": "state",
  "players": [
    {
      "id": "abc123",
      "name": "Alice",
      "x": 120,
      "y": 200
    }
  ]
}
```

The exact schema may be slightly adjusted if needed, but keep it minimal and document it.

---

# WebSocket Server Behavior

Requirements:

* Server is authoritative for shared player state.
* Generate player IDs on the server.
* Store players in an in-memory dictionary.
* Track active WebSocket connections explicitly.
* Associate a connection with its player after `join`.
* Update the player's position when a `move` message arrives.
* Broadcast the current state when relevant state changes.
* Remove the player when the WebSocket connection closes.
* Broadcast the updated state after a player disconnects.

Keep the broadcast implementation clearly visible.

For example, the source should contain an easily identifiable block conceptually similar to:

```python id="hu0lkv"
for connection in active_connections:
    await connection.send_json(payload)
```

Do not hide this behind excessive abstraction.

---

# Project 2 — polling-server

Directory:

```text id="h6rz6g"
polling-server/
```

Implement the SAME visible multiplayer game using HTTP Polling instead of WebSocket.

There must be NO WebSocket usage in this project.

Do not use SSE or another push mechanism.

Use normal FastAPI HTTP endpoints.

Suggested API:

```text id="py1dsn"
POST /api/join
POST /api/move
GET  /api/state
POST /api/leave
```

A clean equivalent API is acceptable.

---

# Polling Behavior

The frontend should repeatedly request:

```text id="wyus8m"
GET /api/state
```

Default polling interval:

```text id="djo01g"
100 ms
```

Define it as one obvious constant near the top of `static/game.js`, for example:

```javascript id="qir61b"
const POLL_INTERVAL_MS = 100;
```

It must be easy to change during the presentation to:

```text id="g0lwmw"
1000
500
100
```

Moving a player should send an HTTP request such as:

```text id="mjxl7d"
POST /api/move
```

Other players' positions must only become visible through repeated polling of `/api/state`.

Do NOT implement client-side WebSocket fallback or hidden push behavior.

---

# Polling Identity

Because HTTP requests are independent, `POST /api/join` should return a server-generated player ID or session token.

For example:

```json id="1jw7rk"
{
  "playerId": "abc123"
}
```

Subsequent move/leave requests may use this value.

Keep this intentionally simple.

Do not implement authentication or cookies unless there is a strong reason.

This is a teaching demo, not a security exercise.

---

# Metrics / Presentation Instrumentation

The public WebSocket and Polling servers will later be compared during the presentation.

Implement lightweight, in-memory metrics in both projects.

Do NOT install Prometheus, Grafana, OpenTelemetry, or another monitoring stack.

Expose:

```text id="0wz7pj"
GET /api/metrics
```

and:

```text id="5jav26"
POST /api/metrics/reset
```

Resetting metrics must NOT disconnect players or reset game state.

---

# websocket-server Metrics

Track at least:

* uptime seconds
* current connected players
* current WebSocket connections
* total WebSocket connections opened
* total incoming WebSocket messages
* total join messages
* total move messages
* total outgoing WebSocket messages

Important:

If one state update is sent to 10 WebSocket connections, count that as 10 outgoing WebSocket messages.

Example response:

```json id="q2zz18"
{
  "uptimeSeconds": 60,
  "connectedPlayers": 15,
  "currentWebSocketConnections": 15,
  "totalConnectionsOpened": 15,
  "incomingMessages": 420,
  "joinMessages": 15,
  "moveMessages": 405,
  "outgoingMessages": 6080
}
```

Example values are illustrative only.

---

# polling-server Metrics

Track at least:

* uptime seconds
* current connected players
* total HTTP API requests
* join request count
* move request count
* state polling request count
* leave request count

Example:

```json id="t0apkr"
{
  "uptimeSeconds": 60,
  "connectedPlayers": 15,
  "totalApiRequests": 9510,
  "joinRequests": 15,
  "moveRequests": 480,
  "stateRequests": 9000,
  "leaveRequests": 15
}
```

Example values are illustrative only.

---

# Server Logging

Keep logs concise and useful for a live presentation.

Log events such as:

```text id="qp0nv1"
[player joined] Alice
[player left] Alice
```

Do NOT print every `GET /api/state` polling request manually.

Polling can generate many requests, so use the metrics endpoint to observe request volume.

Unexpected errors should be logged clearly.

Uvicorn's normal request logging behavior may be configured if necessary to prevent the polling demo from flooding the terminal.

Document any such configuration.

---

# Project 3 — websocket-complete

Directory:

```text id="p3jasx"
websocket-complete/
```

This is the complete reference implementation for the hands-on exercise.

Its behavior and core source code should match `websocket-server` as closely as possible.

It must be completely standalone and include its own:

```text id="qj5ymh"
app.py
requirements.txt
README.md
static/
```

Do NOT use:

* symlinks
* imports from `websocket-server`
* shared packages between the two directories

Duplicating this small project is preferred because this directory will later be turned into a separate GitHub repository.

---

# Workshop-Oriented WebSocket Code

The important teaching section must be extremely easy to find.

Students will later receive a TODO version where only the broadcast block is removed.

Structure the code so that a section similar to this can later be replaced:

```python id="206rrd"
# TODO: send the updated state to every active WebSocket connection

for connection in active_connections:
    await connection.send_json(payload)
```

The student exercise should eventually require only a few lines.

Do not make students implement:

* game state parsing
* player IDs
* HTML
* movement logic
* disconnect handling
* JSON schema
* metrics

unless absolutely necessary.

The conceptual learning objective is:

```text id="984hl5"
Client A
   │ move
   ▼
FastAPI WebSocket server
   │
   ├── send state → Client A
   ├── send state → Client B
   └── send state → Client C
```

---

# Shared Frontend

Use Vanilla HTML/CSS/JavaScript.

Do not use a bundler unless absolutely necessary.

Prefer static files that the FastAPI server can serve directly.

The frontend should:

1. show the name-entry screen
2. establish the appropriate connection
3. render all known players
4. listen for WASD / arrow keys
5. update the local player's position
6. send movement to the server
7. render state received from the server

The WebSocket and Polling frontends should remain as similar as reasonably possible.

The primary difference should be the networking code.

---

# Static File Serving

Use FastAPI to serve the frontend.

For example, use FastAPI's static file support or a minimal root route.

Opening:

```text id="gsleij"
http://localhost:8000
```

must load the game.

Do not require a separate frontend development server.

---

# requirements.txt

Keep dependencies minimal.

Expected dependencies should be approximately:

```text id="mqtek7"
fastapi
uvicorn[standard]
```

Add only dependencies that are actually necessary.

Do not introduce a large dependency stack.

---

# README Requirements

Each directory must contain its own concise README.

## WebSocket projects

Document:

1. purpose
2. requirements
3. virtual environment setup
4. dependency installation
5. how to start Uvicorn
6. open `http://localhost:8000`
7. open two browser windows/tabs to simulate multiple clients
8. WebSocket endpoint
9. WebSocket message flow
10. `/api/metrics`
11. `/api/metrics/reset`
12. important source code locations for the workshop

Explain briefly that multiple browser windows represent independent WebSocket clients connected to one local server.

## Polling project

Document:

1. purpose
2. setup
3. how to start Uvicorn
4. HTTP API overview
5. where `POLL_INTERVAL_MS` is defined
6. how to change it
7. `/api/metrics`
8. `/api/metrics/reset`

---

# Verification

After implementation, verify all three projects independently.

For each project:

1. create/install dependencies
2. start Uvicorn
3. confirm `http://localhost:8000` loads
4. test with multiple browser clients

Do not leave multiple servers fighting over port 8000 at the same time.

Stop one before starting the next.

---

# WebSocket Verification

For both:

```text id="b7gdtb"
websocket-server
websocket-complete
```

verify:

* two browser clients can join using different names
* each gets a different server-generated ID
* moving one player appears on the other browser
* movement works in both directions
* the server receives move messages
* broadcast updates all connected clients
* disconnecting a browser removes the player
* `/api/metrics` returns valid values
* `/api/metrics/reset` resets counters without removing players

---

# Polling Verification

Verify:

* two browser clients can join
* each receives a server-generated ID
* movement request updates server state
* another browser sees the movement through polling
* there is no WebSocket connection
* changing `POLL_INTERVAL_MS` changes polling frequency
* `/api/metrics` reflects repeated state requests
* `/api/metrics/reset` works
* the game remains usable at 1000 ms, 500 ms, and 100 ms intervals

---

# Optional Automated Tests

Add small automated tests if they provide meaningful value.

Prioritize simple tests around:

* join
* move
* state
* leave
* metrics

Do not build a large testing framework.

Do not let testing complexity obscure the demo code.

---

# Code Quality Constraints

Optimize in this order:

1. educational readability
2. reliability during a live demo
3. minimal dependencies
4. consistency between WebSocket and Polling implementations
5. ease of later deployment

Avoid production-oriented abstractions that make the core networking flow harder to see.

Simple code duplication is acceptable in this teaching project.

---

# Scope Guard

Do NOT add:

* chat
* rooms
* lobby system
* authentication
* database
* persistent users
* player customization
* combat
* collision detection
* NPCs
* scores
* leaderboard
* matchmaking
* Redis
* background workers
* Docker requirement
* Kubernetes
* React
* TypeScript
* Socket.IO
* SSE
* STOMP

If a feature is not necessary to demonstrate player join, movement synchronization, WebSocket broadcast, or Polling comparison, do not implement it.

---

# Final Report

When finished, report:

1. directory/file structure created
2. how each application works
3. exact WebSocket lifecycle
4. exact WebSocket message schemas
5. where the broadcast code is located
6. exact Polling API flow
7. where `POLL_INTERVAL_MS` is located
8. metrics supported by each server
9. commands used to run each project
10. verification/test results
11. any limitations
12. anything that should be checked before deploying to Google Cloud

Do NOT deploy anything to Google Cloud yet.

Do NOT configure nginx yet.

Do NOT create a GitHub remote.

Do NOT push, pull, or fetch from any remote repository.

Do NOT create the student TODO version yet.

Only create the three complete projects requested above.
