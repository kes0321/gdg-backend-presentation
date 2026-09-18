# HTTP Polling Game Demo

This standalone version of the GDGoC demo synchronizes the same multiplayer game through repeated HTTP requests instead of WebSockets.

## Requirements and setup

Python 3.11 or newer is required.

```bash
python -m venv .venv
```

Activate the virtual environment:

```bash
# macOS / Linux
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1
```

Install dependencies and run the server:

```bash
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000
```

Open <http://localhost:8000> in two browser windows or tabs to simulate two players.

## HTTP API

- `POST /api/join` with `{ "name": "Alice" }` returns a server-generated `playerId`.
- `POST /api/move` with `playerId`, `x`, and `y` updates that player's position.
- `GET /api/state` returns the current list of players.
- `POST /api/leave` with `playerId` removes the player.

## Polling interval

`static/game.js` defines `const POLL_INTERVAL_MS = 100;` near the top. Change it to `1000`, `500`, or `100` before reloading the page to demonstrate different polling frequencies.

Metrics endpoints are intentionally introduced in M05, not in this milestone.
