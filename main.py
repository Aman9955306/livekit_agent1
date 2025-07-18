from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv

import os
import jwt
import time
from datetime import datetime
import secrets

# Load env variables
load_dotenv()

# ✅ Initialize FastAPI first
app = FastAPI(title="LiveKit Agent API", version="1.0.0")

# ✅ Then apply middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to frontend origin for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load LiveKit config
LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET")
LIVEKIT_URL = os.getenv("LIVEKIT_URL", "ws://localhost:7880")

if not LIVEKIT_API_KEY or not LIVEKIT_API_SECRET:
    raise ValueError("LIVEKIT_API_KEY and LIVEKIT_API_SECRET must be set in environment variables")

# Pydantic models
class RoomRequest(BaseModel):
    participant_name: str = "User"

class RoomResponse(BaseModel):
    room_name: str
    token: str
    url: str
    participant_name: str

# JWT token generator
def generate_access_token(room_name: str, participant_name: str) -> str:
    now = int(time.time())
    exp = now + 3600  # 1 hour
    payload = {
        "iss": LIVEKIT_API_KEY,
        "sub": participant_name,
        "aud": "livekit",
        "exp": exp,
        "nbf": now,
        "video": {
            "room": room_name,
            "roomJoin": True,
            "roomList": True,
            "roomRecord": True,
            "roomAdmin": True,
            "roomCreate": True,
            "canPublish": True,
            "canSubscribe": True,
            "canPublishData": True,
            "canUpdateOwnMetadata": True,
            "ingressAdmin": True,
            "hidden": False,
            "recorder": False
        }
    }
    return jwt.encode(payload, LIVEKIT_API_SECRET, algorithm="HS256")

@app.get("/")
async def read_root():
    return "helloworld"

@app.post("/create-room", response_model=RoomResponse)
async def create_room(request: RoomRequest):
    try:
        room_name = f"room-{secrets.token_urlsafe(8)}"
        token = generate_access_token(room_name, request.participant_name)
        return RoomResponse(
            room_name=room_name,
            token=token,
            url=LIVEKIT_URL,
            participant_name=request.participant_name
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create room: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
