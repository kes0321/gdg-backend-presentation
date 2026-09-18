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


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    await websocket.accept()
    active_connections.append(websocket)

    try:
        while True:
            data = await websocket.receive_json()

            if data.get("type") != "join" or websocket in connection_player_ids:
                continue

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

            # M02 sends the joining client a snapshot. M03 adds the broadcast loop.
            await websocket.send_json({"type": "state", "players": list(players.values())})

    except WebSocketDisconnect:
        active_connections.remove(websocket)
        player_id = connection_player_ids.pop(websocket, None)
        if player_id:
            players.pop(player_id, None)
