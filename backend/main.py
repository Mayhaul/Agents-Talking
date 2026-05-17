from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from orchestrator import run_agents

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Backend is running"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    await websocket.accept()

    while True:

        data = await websocket.receive_json()

        user_message = data["message"]

        await run_agents(user_message, websocket)