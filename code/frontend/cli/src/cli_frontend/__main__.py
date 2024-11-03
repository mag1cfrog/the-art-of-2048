import curses
from cli_frontend.game_loop import GameLoop
from cli_frontend.renderer import Renderer
from cli_frontend.input_handler import InputHandler
from game_backend.core.array_backend import ArrayGrid, ArrayTile
from game_backend.core.comm import InProcessCommunication
from game_backend.services import GameManager, LocalStorageManager

def initialize_cli_frontend(stdscr, communication):
    """
    Initializes the CLI frontend with the provided communication interface.

    Args:
        stdscr (curses.window): The curses window object.
        communication (InProcessCommunication): Communication interface with the backend.
    
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

