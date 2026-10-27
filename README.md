# Shiprr Learning Panel

A small, original FastAPI dashboard for learning Git-based deployment on Shiprr. It is inspired by common admin-panel layouts, but it is **not a clone** of SpiderPanel and does not implement proxy relays, network scanners, subscription-link generation, or Telegram sales automation.

## Features
- Responsive dashboard UI
- Demo account list with add/pause/resume actions
- Summary cards and a basic activity feed
- `/health` endpoint for a simple health check
- `/api/...` endpoints for learning how a web UI talks to a Python API
- No Dockerfile required; designed for a source-based build

## Deploy on Shiprr
1. Upload these files to a new GitHub repository.
2. In Shiprr, choose **Create app** and connect GitHub.
3. Select your repository and branch.
4. Runtime: Python.
5. Build command: `pip install -r requirements.txt`
6. Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
7. Health-check path (if requested): `/health`
8. Deploy, then open the generated URL.

Shiprr's source-build runtime provides the `PORT` environment variable. Do not hard-code a public port for deployment.

## Run locally (optional)
```bash
python -m venv .venv
# Windows:
.venv\\Scripts\\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```
Open `http://127.0.0.1:8000`.

## Important limitations
- The demo data is stored in memory and resets when the process restarts or redeploys.
- There is no login/authentication. Do not expose real personal data or use this as a production admin panel.
- It does not connect to external servers or create real network configurations.
- Shiprr usage can incur charges for CPU/RAM and other usage beyond any included allowance. Check current pricing before deploying.
