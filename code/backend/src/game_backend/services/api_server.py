from typing import Dict, Optional, Any
import json

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from game_backend.services import GameManager, LocalStorageManager
from game_backend.core.array_backend import ArrayGrid, ArrayTile


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.game_managers: Dict[str, GameManager] = {}

    async def connect(self, websocket: WebSocket) -> str:
        # await websocket.accept()
        session_id = str(id(websocket))
        self.active_connections[session_id] = websocket

        # Initialize a new game for each connection
        storage_manager = LocalStorageManager()
        grid = ArrayGrid(size=4)
        tile_class = ArrayTile
        game_manager = GameManager(
            grid=grid,
            tile_class=tile_class,
            storage_manager=storage_manager
        )
        self.game_managers[session_id] = game_manager

        return session_id

    def disconnect(self, session_id: str):
        del self.active_connections[session_id]
        del self.game_managers[session_id]

    def get_game_manager(self, session_id: str) -> GameManager:
        return self.game_managers[session_id]

manager = ConnectionManager()

@app.websocket("/ws/game")
async def game_endpoint(websocket: WebSocket):
    # Allow any origin for WebSocket connections
    await websocket.accept()
    session_id = await manager.connect(websocket)
    game_manager = manager.get_game_manager(session_id)
    try:
        # Send initial game state
        await websocket.send_text(json.dumps(game_manager.get_grid_state()))

        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            direction = message.get("direction")
            if direction in [0, 1, 2, 3]:
                game_manager.play_turn(direction)
                state = game_manager.get_grid_state()
                await websocket.send_text(json.dumps(state))
                if game_manager.is_game_terminated():
                    await websocket.close()
                    break
            else:
                await websocket.send_text(json.dumps({"error": "Invalid move"}))
    except WebSocketDisconnect:
        manager.disconnect(session_id)

