import curses
from game_backend.core.array_backend import ArrayGrid, ArrayTile
from game_backend.core.comm import InProcessCommunication
from game_backend.services import GameManager, LocalStorageManager
from cli_frontend.renderer import Renderer
from cli_frontend.input_handler import InputHandler
from .game_loop import GameLoop

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


def initialize_backend() -> InProcessCommunication:
    """
    Initializes the backend components.

    Returns:
        InProcessCommunication: Communication interface with the backend.
    """
    storage_manager = LocalStorageManager()
    grid = ArrayGrid(size=4)
    tile_class = ArrayTile
    game_manager = GameManager(
        grid=grid,
        tile_class=tile_class,
        storage_manager=storage_manager
    )
    communication = InProcessCommunication(game_manager=game_manager)
    return communication

def main(stdscr: curses.window) -> None:
    """
    Application entry point. Initializes backend and frontend components.

    Args:
        stdscr (curses.window): The curses window object.
    """
    # Initialize backend
    communication = initialize_backend()
    
    # Initialize frontend with backend communication
    game_loop = initialize_cli_frontend(stdscr, communication)
    
    # Run the game loop
    game_loop.run()

if __name__ == "__main__":
    curses.wrapper(main)