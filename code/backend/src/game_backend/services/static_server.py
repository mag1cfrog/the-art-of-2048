import json

from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from .api_server import manager

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket endpoint
@app.websocket("/ws/game")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()  # Accept connection first
    session_id = str(id(websocket))
    
    try:
        # Then handle game management
        session_id = await manager.connect(websocket)
        game_manager = manager.get_game_manager(session_id)
        
        # Send initial state
        await websocket.send_text(json.dumps(game_manager.get_grid_state()))
        
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            direction = message.get("direction")
            if direction in [0, 1, 2, 3]:
                game_manager.play_turn(direction)
                state = game_manager.get_grid_state()
                await websocket.send_text(json.dumps(state))
            else:
                await websocket.send_text(json.dumps({"error": "Invalid move"}))
    except Exception as e:
        print(f"Error: {e}")
        if session_id:
            manager.disconnect(session_id)
    finally:
        if session_id:
            manager.disconnect(session_id)

# Serve static files
app.mount("/", StaticFiles(directory="/app/frontend/build", html=True), name="static")