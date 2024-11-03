import random
from typing import Type, Optional, Dict, Any
import logging


from game_backend.interface.grid import Grid
from game_backend.interface.tile import Tile
from game_backend.local_storage_manager import LocalStorageManager

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class GameManager:
    """
    Manages the game logic for the 2048 game.

    This class handles game state, moves, and interactions with the Grid and Tile implementations.
    """
    def __init__(
            self, 
            grid: Grid,
            tile_class: Type[Tile],
            storage_manager: LocalStorageManager,
            start_tiles: int = 2
        ) -> None:
        """
        Initializes the GameManager.

        Args:
            grid (Grid): An instance of a Grid implementation.
            tile_class (Type[Tile]): The Tile class to instantiate tiles.
            storage_manager (LocalStorageManager): Manages game state persistence.
            start_tiles (int): Number of tiles to start the game with. Defaults to 2.
        """
        self.grid: Grid = grid
        self.tile_class: Type[Tile] = tile_class
        self.storage_manager: LocalStorageManager = storage_manager
        self.size: int = grid.size

        self.start_tiles: int = start_tiles
        self.score: int = 0
        self.over: bool = False
        self.won: bool = False
        self.keep_playing: bool = False

        # # Event bindings
        # self.input_manager.on("move", self.move)
        # self.input_manager.on("restart", self.restart)
        # self.input_manager.on("keepPlaying", self.keep_playing_action)

        self.setup()

    def restart(self) -> None:
        """
        Restarts the game by clearing the game state and reinitializing the game.
        """
        self.storage_manager.clear_game_state()
        # self.actuator.continue_game()  # Clear the game won/lost message
        self.setup()

    def keep_playing_action(self) -> None:
        """
        Allows the player to continue playing after winning.
        """
        self.keep_playing = True
        # self.actuator.continue_game()  # Clear the game won/lost message

    def is_game_terminated(self) -> bool:
        """
        Determines if the game has terminated.

        Returns:
            bool: True if the game is over or won without continuation, False otherwise.
        """
        return self.over or (self.won and not self.keep_playing)

    def setup(self) -> None:
        """
        Sets up the game by loading the previous state or initializing a new game.
        """
        previous_state = self.storage_manager.get_game_state()

        if previous_state:
            self.grid = self._initialize_grid_from_state(previous_state['grid'])
            self.score = previous_state['score']
            self.over = previous_state['over']
            self.won = previous_state['won']
            self.keep_playing = previous_state['keepPlaying']
        else:
            self.grid = self.grid.__class__(self.size)
            self.score = 0
            self.over = False
            self.won = False
            self.keep_playing = False

            self.add_start_tiles()

        self.actuate()

    def add_start_tiles(self) -> None:
        """
        Adds the initial number of tiles to the grid.
        """
        for _ in range(self.start_tiles):
            self.add_random_tile()

    def add_random_tile(self) -> None:
        if self.grid.cells_available():
            value = 4 if random.random() < 0.1 else 2
            position = self.grid.random_available_cell()
            tile = self.tile_class(position, value)
            self.grid.insert_tile(tile)

    def play_turn(self, direction: int) -> None:
        """
        Executes a move in the specified direction.

        Args:
            direction (int): Direction of the move (0: up, 1: right, 2: down, 3: left).
        """
        if self.is_game_terminated():
            return  # Game is over; do nothing

        moved = self._move(direction)

        if moved:
            self.add_random_tile()
            if not self.moves_available():
                self.over = True

        self.actuate()

    @staticmethod
    def get_vector(direction: int) -> tuple:
        """
        Converts a direction into a vector.

        Args:
            direction (int): Direction index (0: up, 1: right, 2: down, 3: left).

        Returns:
            tuple: A tuple representing the movement vector.
        """
        # 0: up, 1: right, 2: down, 3: left
        vectors = {
            0: (0, -1),  # Up
            1: (1, 0),   # Right
            2: (0, 1),   # Down
            3: (-1, 0)   # Left
        }
        return vectors.get(direction, (0, 0))

    def build_traversals(self, vector: tuple) -> Dict[str, list]:
        """
        Builds the traversal order based on the movement vector.

        Args:
            vector (tuple): Movement vector.

        Returns:
            Dict[str, list]: Traversal order for 'x' and 'y' axes.
        """
        traversals = {'x': list(range(self.size)), 'y': list(range(self.size))}

        if vector[0] == 1:
            traversals['x'].reverse()
        if vector[1] == 1:
            traversals['y'].reverse()

        return traversals

    def find_farthest_position(self, cell: tuple, vector: tuple) -> Dict[str, Optional[tuple]]:
        """
        Finds the farthest position a tile can move to in the given direction.

        Args:
            cell (tuple): Current cell position.
            vector (tuple): Movement vector.

        Returns:
            Dict[str, Optional[tuple]]: Dictionary with 'farthest' and 'next' cell positions.
        """
        previous = cell
        x, y = cell
        dx, dy = vector

        while True:
            next_cell = (x + dx, y + dy)
            if not self.grid.within_bounds(next_cell) or not self.grid.cell_available(next_cell):
                break
            previous = next_cell
            x, y = next_cell

        next_cell = (x + dx, y + dy) if self.grid.within_bounds((x + dx, y + dy)) else None

        return {
            'farthest': previous,
            'next': next_cell
        }

    def moves_available(self) -> bool:
        """
        Checks if there are any moves available.

        Returns:
            bool: True if moves are available, False otherwise.
        """
        return self.grid.cells_available() or self.tile_matches_available()
    
    def tile_matches_available(self) -> bool:
        """
        Checks if there are any tiles that can be merged.

        Returns:
            bool: True if mergeable tiles exist, False otherwise.
        """
        for x in range(self.size):
            for y in range(self.size):
                tile = self.grid.cell_content((x, y))
                if tile:
                    for direction in range(4):
                        vector = self.get_vector(direction)
                        cell = (x + vector[0], y + vector[1])
                        other = self.grid.cell_content(cell)
                        if other and other.value == tile.value:
                            return True
        return False

    def positions_equal(self, first: tuple, second: tuple) -> bool:
        """
        Checks if two positions are equal.

        Args:
            first (tuple): First position.
            second (tuple): Second position.

        Returns:
            bool: True if positions are equal, False otherwise.
        """
        return first[0] == second[0] and first[1] == second[1]
    
    def move_tile(self, tile: Tile, cell: tuple) -> None:
        """
        Moves a tile to a new cell.

        Args:
            tile (Tile): The tile to move.
            cell (tuple): The target cell position.
        """
        self.grid.remove_tile(tile)
        self.grid.insert_tile(self.tile_class(position=cell, value=tile.value))
        tile.update_position(cell)

    def prepare_tiles(self) -> None:
        """
        Prepares tiles for a new move by resetting their merged status and saving their positions.
        """
        for x in range(self.size):
            for y in range(self.size):
                tile = self.grid.cell_content((x, y))
                if tile:
                    tile.merged_from = None
                    tile.save_position()

    def actuate(self) -> None:
        """
        Updates the storage with the current game state and score.
        """
        if self.storage_manager.get_best_score() < self.score:
            self.storage_manager.set_best_score(self.score)

        if self.over:
            self.storage_manager.clear_game_state()
        else:
            self.storage_manager.set_game_state(self.serialize())


    def serialize(self) -> Dict[str, Any]:
        """
        Serializes the current game state.

        Returns:
            Dict[str, Any]: Serialized game state.
        """
        return {
            'grid': self.grid.serialize(),
            'score': self.score,
            'over': self.over,
            'won': self.won,
            'keepPlaying': self.keep_playing
        }
    
    def get_grid_state(self) -> Dict[str, Any]:
        """
        Retrieves the current game state.

        Returns:
            Dict[str, Any]: Current game state.
        """
        return self.serialize()
    
    def _initialize_grid_from_state(self, grid_state: Dict[str, Any]) -> Grid:
        """
        Initializes the grid from a saved state.

        Args:
            grid_state (Dict[str, Any]): The saved grid state.

        Returns:
            Grid: An initialized Grid instance.
        """
        return self.grid.__class__(size=grid_state['size'], previous_state=grid_state['cells'])
    
    def _move(self, direction: int) -> bool:
        """
        Handles the logic for moving tiles in a specified direction.

        Args:
            direction (int): Direction of the move.

        Returns:
            bool: True if any tiles were moved or merged, False otherwise.
        """

        vector = self.get_vector(direction)
        traversals = self.build_traversals(vector)
        moved = False

        self.prepare_tiles()

        for x in traversals['x']:
            for y in traversals['y']:
                cell = (x, y)
                tile = self.grid.cell_content(cell)

                if tile:
                    positions = self.find_farthest_position(cell, vector)
                    next_cell = positions['next']
                    farthest = positions['farthest']

                    if next_cell:
                        next_tile = self.grid.cell_content(next_cell)
                        logger.debug(f"Next tile at {next_cell}: {next_tile}")
                    else:
                        next_tile = None
                        logger.debug("Next cell is None")

                    if next_tile and next_tile.value == tile.value and not getattr(next_tile, 'merged_from', None):
                        logger.debug(f"Merging tile at {cell} with tile at {next_cell}")
                        merged = self.tile_class(next_cell, tile.value * 2)
                        merged.merged_from = [tile, next_tile]

                        self.grid.insert_tile(merged)
                        self.grid.remove_tile(tile)

                        tile.update_position(next_cell)

                        self.score += merged.value

                        if merged.value == 2048:
                            self.won = True
                    else:
                        logger.debug(f"Moving tile from {cell} to {farthest}")
                        self.move_tile(tile, farthest)

                    if cell != tile.position:
                        moved = True

        # if moved:
        #     self.add_random_tile()

        #     if not self.moves_available():
        #         self.over = True  # Game over!

        #     self.actuate()

        return moved