import asyncio
import json
from typing import Any, Dict, Optional
import websockets
import logging

logger = logging.getLogger(__name__)

class WebSocketCommunication:
    def __init__(self, uri: str):
        self.uri = uri
        self.websocket: Optional[websockets.WebSocketClientProtocol] = None
        self.game_state: Optional[Dict[str, Any]] = None

    async def connect(self):
        try:
            self.websocket = await websockets.connect(self.uri)
            # Receive initial game state
            data = await self.websocket.recv()
            self.game_state = json.loads(data)
            logger.info("Connected to WebSocket server.")
        except Exception as e:
            logger.error(f"Failed to connect to WebSocket server: {e}")

    async def send_move(self, direction: int) -> bool:
        if self.websocket:
            try:
                message = json.dumps({"direction": direction})
                await self.websocket.send(message)
                data = await self.websocket.recv()
                self.game_state = json.loads(data)
                return True
            except websockets.exceptions.ConnectionClosed:
                logger.error("WebSocket connection closed by the server.")
                return False
            except Exception as e:
                logger.error(f"Error sending move: {e}")
                return False
        logger.error("WebSocket is not connected.")
        return False

    def get_game_state(self) -> Optional[Dict[str, Any]]:
        return self.game_state

    async def close(self):
        if self.websocket:
            await self.websocket.close()
            logger.info("WebSocket connection closed.")