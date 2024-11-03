import curses
from backend.services import GameManager, LocalStorageManager
from backend.core.array_backend import ArrayGrid, ArrayTile
from backend.core.comm import InProcessCommunication
from frontend.cli_frontend.main import initialize_cli_frontend

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