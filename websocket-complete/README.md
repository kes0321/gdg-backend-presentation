# Complete WebSocket Reference Demo

This directory will become the complete reference version of the GDGoC WebSocket workshop. M02 adds player joining and connection cleanup; movement and live broadcasts are added in a later milestone.

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

## M02 WebSocket flow

The frontend opens `ws://localhost:8000/ws` (or `wss` under HTTPS) and sends:

```json
{ "type": "join", "name": "Alice" }
```

The server accepts the connection, generates the player ID, stores the player in memory, and returns a state snapshot containing `id`, `name`, `x`, and `y` for each player. Closing the connection removes that player from server memory.

Movement messages and the all-client broadcast loop are intentionally deferred to M03.
