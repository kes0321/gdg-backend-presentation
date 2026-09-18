# Complete WebSocket Reference Demo

This directory will become the complete reference version of the GDGoC WebSocket workshop. M01 provides the runnable FastAPI and frontend skeleton only; multiplayer behavior is added in later milestones.

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

Open <http://localhost:8000>. The name-entry screen and empty game area should load.

Future milestones will add the `/ws` endpoint, WebSocket message flow, multiplayer rendering, and metrics.
