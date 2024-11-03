# cli_frontend/main.py
import curses
from cli_frontend.game_loop import GameLoop
from cli_frontend.renderer import Renderer
from cli_frontend.input_handler import InputHandler
from game_backend.core.array_backend import ArrayGrid, ArrayTile
from game_backend.core.comm import InProcessCommunication
from game_backend.services import GameManager, LocalStorageManager

def main(stdscr: curses.window) -> None:
    """
    Entry point for the CLI frontend.

    Initializes the game components and starts the game loop.

    Args:
        stdscr (curses.window): The curses window object.
    """
    # Initialize backend components
    storage_manager = LocalStorageManager()
    grid = ArrayGrid(size=4)
    tile_class = ArrayTile
    game_manager = GameManager(grid=grid, tile_class=tile_class, storage_manager=storage_manager)
    communication = InProcessCommunication(game_manager=game_manager)

    # Initialize frontend components
    renderer = Renderer(stdscr)
    input_handler = InputHandler()

    # Start the game loop
    game_loop = GameLoop(
        communication=communication,
        renderer=renderer,
        input_handler=input_handler
    )
    game_loop.run()

if __name__ == "__main__":
    curses.wrapper(main)