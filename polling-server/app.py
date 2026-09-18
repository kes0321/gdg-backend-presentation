import random
import uuid
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles


app = FastAPI(title="Polling Game Demo")

STATIC_DIR = Path(__file__).parent / "static"
GAME_WIDTH = 640
GAME_HEIGHT = 360
PLAYER_SIZE = 28

# The polling version keeps the same shared game state in server memory.
players: dict[str, dict[str, int | str]] = {}

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
async def index() -> FileResponse:
    """Serve the single-page frontend."""
    return FileResponse(STATIC_DIR / "index.html")


@app.post("/api/join")
async def join_game(data: dict[str, object]) -> dict[str, str]:
    name = str(data.get("name", "")).strip()[:30]
    if not name:
        raise HTTPException(status_code=400, detail="A player name is required.")

    player_id = uuid.uuid4().hex
    players[player_id] = {
        "id": player_id,
        "name": name,
        "x": random.randint(0, GAME_WIDTH - PLAYER_SIZE),
        "y": random.randint(0, GAME_HEIGHT - PLAYER_SIZE),
    }
    return {"playerId": player_id}


@app.post("/api/move")
async def move_player(data: dict[str, object]) -> dict[str, bool]:
    player_id = str(data.get("playerId", ""))
    player = players.get(player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found.")

    player["x"] = max(0, min(int(data.get("x", player["x"])), GAME_WIDTH - PLAYER_SIZE))
    player["y"] = max(0, min(int(data.get("y", player["y"])), GAME_HEIGHT - PLAYER_SIZE))
    return {"ok": True}


@app.get("/api/state")
async def game_state() -> dict[str, list[dict[str, int | str]]]:
    return {"players": list(players.values())}


@app.post("/api/leave")
async def leave_game(data: dict[str, object]) -> dict[str, bool]:
    player_id = str(data.get("playerId", ""))
    players.pop(player_id, None)
    return {"ok": True}
