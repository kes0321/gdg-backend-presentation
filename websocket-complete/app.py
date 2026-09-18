import random
import uuid
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles


app = FastAPI(title="WebSocket Game Demo")

STATIC_DIR = Path(__file__).parent / "static"
GAME_WIDTH = 640
GAME_HEIGHT = 360
PLAYER_SIZE = 28

# M02 keeps the shared game state and WebSocket connections in memory.
players: dict[str, dict[str, int | str]] = {}
active_connections: list[WebSocket] = []
connection_player_ids: dict[WebSocket, str] = {}

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
async def index() -> FileResponse:
    """Serve the single-page frontend."""
    return FileResponse(STATIC_DIR / "index.html")


async def broadcast_state() -> None:
    """Send the current player state to every connected WebSocket client."""
    payload = {"type": "state", "players": list(players.values())}

    # M03 workshop focus: broadcast the updated state to every active client.
    for connection in active_connections:
        await connection.send_json(payload)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    await websocket.accept()
    active_connections.append(websocket)

    try:
        while True:
            data = await websocket.receive_json()

            if data.get("type") == "join" and websocket not in connection_player_ids:
                name = str(data.get("name", "")).strip()[:30]
                if not name:
                    continue

                player_id = uuid.uuid4().hex
                players[player_id] = {
                    "id": player_id,
                    "name": name,
                    "x": random.randint(0, GAME_WIDTH - PLAYER_SIZE),
                    "y": random.randint(0, GAME_HEIGHT - PLAYER_SIZE),
                }
                connection_player_ids[websocket] = player_id
                await broadcast_state()

            elif data.get("type") == "move":
                player_id = connection_player_ids.get(websocket)
                if not player_id:
                    continue

                player = players[player_id]
                player["x"] = max(0, min(int(data.get("x", player["x"])), GAME_WIDTH - PLAYER_SIZE))
                player["y"] = max(0, min(int(data.get("y", player["y"])), GAME_HEIGHT - PLAYER_SIZE))
                await broadcast_state()

    except WebSocketDisconnect:
        active_connections.remove(websocket)
        player_id = connection_player_ids.pop(websocket, None)
        if player_id:
            players.pop(player_id, None)
            await broadcast_state()
