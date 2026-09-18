# Complete WebSocket Reference Demo

This directory will become the complete reference version of the GDGoC WebSocket workshop. M03 adds keyboard movement and state broadcasts to connected clients.

## Requirements

Python 3.11 or newer.

## Setup and run

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

Install dependencies and start the server:

```bash
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000
```

Open <http://localhost:8000>, enter a name, and select **Join Game**. Open another browser window or tab to join as another player.

## WebSocket flow

The frontend opens `ws://localhost:8000/ws` (or `wss` under HTTPS) and sends:

```json
{ "type": "join", "name": "Alice" }
```

The server accepts the connection, generates the player ID, stores the player in memory, and broadcasts a state snapshot containing `id`, `name`, `x`, and `y` for each player.

Use WASD or the arrow keys to send a move message:

```json
{ "type": "move", "x": 120, "y": 200 }
```

The server associates the message with the WebSocket connection, clamps the position to the game area, then broadcasts the updated state to every active connection. Closing a connection removes that player and broadcasts the reduced state. The visible workshop broadcast loop is in `app.py` inside `broadcast_state`.
