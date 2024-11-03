import random
from typing import List, Optional

from game_backend.interface.grid import Grid
from game_backend.implementations.array_tile import ArrayTile

class ArrayGrid(Grid):
    """
    Grid implementation using a 2D array.
    """
    def __init__(self, size: int = 4, previous_state=None) -> None:
        """
        Initialize the grid.

        Args:
            size: Size of the grid. Default is 4.
            previous_state: State of the grid to initialize with.
        """
        self.size = size
        self.cells = self.from_state(previous_state) if previous_state else self._empty()

    def from_state(self, state):
        """
        Build a grid from a given state.
        """
        cells = []
        for x in range(self.size):
            row = []
            for y in range(self.size):
                tile = state[x][y]
                row.append(ArrayTile(tile.position, tile.value) if tile else None)
            cells.append(row)
        return cells
    
    def random_available_cell(self):
        """
        Get a random available cell.
        """
        available_cell_list: list = self._available_cells()
        if available_cell_list:
            return random.choice(available_cell_list)

    def cells_available(self) -> bool:
        """
        Check if there are any cells available.
        """
        return bool(self._available_cells())
    
    def cell_content(self, cell: Optional[tuple]) -> Optional[ArrayTile]:
        if self.within_bounds(cell):
            return self.cells[cell[0]][cell[1]]
        else:
            return None

    def within_bounds(self, position: Optional[tuple]) -> bool:
        """
        Check if the specified position is within the grid bounds.
        """
        if not position:
            return False
        return 0 <= position[0] < self.size and 0 <= position[1] < self.size

    def cell_available(self, cell: tuple) -> bool:
        """
        Check if the specified cell is taken
        """
        return not self._cell_occupied(cell)

    def insert_tile(self, tile: ArrayTile) -> None:
        """
        Insert a tile into the grid.
        """
        self.cells[tile.position[0]][tile.position[1]] = tile

    def remove_tile(self, tile: ArrayTile) -> None:
        """
        Remove a tile from the grid.
        """
        self.cells[tile.position[0]][tile.position[1]] = None

    def serialize(self) -> dict:
        """
        Serialize the grid.
        """
        cell_state = []
        for x in range(self.size):
            row = []
            for y in range(self.size):
                tile = self.cells[x][y]
                row.append(tile.serialize() if tile else None)
            cell_state.append(row)
        return {
            'size': self.size,
            'cells': cell_state
        }    

    def _empty(self) -> List[List[ArrayTile]]:
        """
        Build an empty grid with specified size.
        """
        return [[None for _ in range(self.size)] for _ in range(self.size)]

    def _available_cells(self) -> List[tuple]:
        """
        Get a list of available cells.
        """
        return [(x, y) for x in range(self.size) for y in range(self.size) if not self.cells[x][y]]

    def _cell_occupied(self, cell: tuple) -> bool:
        return bool(self.cell_content(cell))

    
    
    
