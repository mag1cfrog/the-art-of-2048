import asyncio
import curses
import threading
import time

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn

from game_backend.core.array_backend import ArrayGrid, ArrayTile
from game_backend.services import GameManager, LocalStorageManager
from game_backend.services.api_server import app as fastapi_app
from cli_frontend.ws_comm import WebSocketCommunication
from cli_frontend.renderer import Renderer
from cli_frontend.input_handler import InputHandler
from .game_loop import GameLoop

def run_server():
    """Run the FastAPI server."""
    uvicorn.run(fastapi_app, host="127.0.0.1", port=8000)


def initialize_cli_frontend(stdscr, communication: WebSocketCommunication) -> GameLoop:
    """
    Initializes the CLI frontend with the provided communication interface.

    Args:
        stdscr (curses.window): The curses window object.
        communication (WebSocketCommunication): Communication interface with the backend.
    
    Returns:
        GameLoop: An instance of the game loop.
    """
    renderer = Renderer(stdscr)
    input_handler = InputHandler()
    game_loop = GameLoop(
        communication=communication,
        renderer=renderer,
        input_handler=input_handler
    )
    return game_loop


def main(stdscr: curses.window) -> None:
    """
    Application entry point. Initializes backend and frontend components.

    Args:
        stdscr (curses.window): The curses window object.
    """
    # Start FastAPI server in a background thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

    # Wait briefly to ensure the server is up
    time.sleep(1)

    # Initialize WebSocket communication
    ws_uri = "ws://127.0.0.1:8000/ws/game"
    communication = WebSocketCommunication(uri=ws_uri)
    
    # Initialize frontend with communication
    game_loop = initialize_cli_frontend(stdscr, communication)
    
    # Run the game loop
    try:
        asyncio.run(game_loop.run())
    except KeyboardInterrupt:
        pass
    finally:
        # Ensure the server thread stops when the main program exits
        # Since it's a daemon thread, it will exit automatically
        pass

if __name__ == "__main__":
    curses.wrapper(main)