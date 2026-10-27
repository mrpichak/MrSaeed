import os
from datetime import datetime, timezone
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

app = FastAPI(title="Shiprr Learning Panel", version="1.0.0")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Demonstration-only in-memory data. It resets whenever the app restarts.
users = [
    {"id": 1, "name": "Demo User", "email": "demo@example.com", "plan": "Starter", "status": "Active"},
    {"id": 2, "name": "Sample Account", "email": "sample@example.com", "plan": "Trial", "status": "Paused"},
]
next_id = 3

class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=60)
    email: str = Field(min_length=5, max_length=120)
    plan: str = Field(default="Starter", max_length=30)

@app.get("/")
def home():
    return FileResponse("static/index.html")

@app.get("/health")
def health():
    return {"status": "ok", "app": "shiprr-learning-panel"}

@app.get("/api/summary")
def summary():
    return {
        "users": len(users),
        "active": sum(1 for user in users if user["status"] == "Active"),
        "paused": sum(1 for user in users if user["status"] == "Paused"),
        "environment": "Shiprr source deployment",
        "checked_at": datetime.now(timezone.utc).isoformat(),
    }

@app.get("/api/users")
def list_users():
    return users

@app.post("/api/users")
def create_user(payload: UserCreate):
    global next_id
    if any(user["email"].lower() == payload.email.lower() for user in users):
        raise HTTPException(status_code=409, detail="This demo email already exists.")
    user = {
        "id": next_id,
        "name": payload.name.strip(),
        "email": payload.email.strip(),
        "plan": payload.plan.strip() or "Starter",
        "status": "Active",
    }
    users.append(user)
    next_id += 1
    return user

@app.patch("/api/users/{user_id}/toggle")
def toggle_user(user_id: int):
    for user in users:
        if user["id"] == user_id:
            user["status"] = "Paused" if user["status"] == "Active" else "Active"
            return user
    raise HTTPException(status_code=404, detail="User not found")

@app.get("/api/activity")
def activity():
    return [
        {"time": "Just now", "event": "Health endpoint available", "kind": "success"},
        {"time": "Demo", "event": "Sample records loaded in memory", "kind": "info"},
        {"time": "Deployment", "event": "Listening on the platform-provided PORT", "kind": "success"},
    ]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.environ.get("PORT", "8000")))
