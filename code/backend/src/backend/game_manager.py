import random
from typing import Type, Optional, Dict, Any

from backend.interface.grid import Grid
from backend.interface.tile import Tile
from backend.local_storage_manager import LocalStorageManager

class GameManager:
    def __init__(self, size, input_manager, actuator, storage_manager):
        self.size = size  # Size of the grid
        self.input_manager = input_manager
        self.storage_manager = storage_manager
        self.actuator = actuator

        self.start_tiles = 2
        self.score = 0
        self.over = False
        self.won = False
        self.keep_playing = False

        # Event bindings
        self.input_manager.on("move", self.move)
        self.input_manager.on("restart", self.restart)
        self.input_manager.on("keepPlaying", self.keep_playing_action)

        self.setup()

    def restart(self, event=None):
        self.storage_manager.clear_game_state()
        self.actuator.continue_game()  # Clear the game won/lost message
        self.setup()

    def keep_playing_action(self, event=None):
        self.keep_playing = True
        self.actuator.continue_game()  # Clear the game won/lost message

    def is_game_terminated(self):
        return self.over or (self.won and not self.keep_playing)

    def setup(self):
        previous_state = self.storage_manager.get_game_state()

        if previous_state:
            self.grid = Grid(previous_state['grid']['size'], previous_state['grid']['cells'])
            self.score = previous_state['score']
            self.over = previous_state['over']
            self.won = previous_state['won']
            self.keep_playing = previous_state['keepPlaying']
        else:
            self.grid = Grid(self.size)
            self.score = 0
            self.over = False
            self.won = False
            self.keep_playing = False

            self.add_start_tiles()

        self.actuate()

    def add_start_tiles(self):
        for _ in range(self.start_tiles):
            self.add_random_tile()

    def add_random_tile(self):
        if self.grid.cells_available():
            value = 4 if random.random() < 0.1 else 2
            position = self.grid.random_available_cell()
            tile = Tile(position, value)
            self.grid.insert_tile(tile)

    def actuate(self):
        if self.storage_manager.get_best_score() < self.score:
            self.storage_manager.set_best_score(self.score)

        if self.over:
            self.storage_manager.clear_game_state()
        else:
            self.storage_manager.set_game_state(self.serialize())

        self.actuator.actuate(self.grid, {
            'score': self.score,
            'over': self.over,
            'won': self.won,
            'bestScore': self.storage_manager.get_best_score(),
            'terminated': self.is_game_terminated()
        })

    def serialize(self):
        return {
            'grid': self.grid.serialize(),
            'score': self.score,
            'over': self.over,
            'won': self.won,
            'keepPlaying': self.keep_playing
        }

    def prepare_tiles(self):
        for x in range(self.size):
            for y in range(self.size):
                tile = self.grid.cell_content((x, y))
                if tile:
                    tile.merged_from = None
                    tile.save_position()

    def move_tile(self, tile, cell):
        self.grid.cells[tile.x][tile.y] = None
        self.grid.cells[cell[0]][cell[1]] = tile
        tile.update_position(cell)

    def move(self, direction):
        if self.is_game_terminated():
            return  # Don't do anything if the game's over

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
                    next_tile = self.grid.cell_content(next_cell)

                    if next_tile and next_tile.value == tile.value and not next_tile.merged_from:
                        merged = Tile(next_cell, tile.value * 2)
                        merged.merged_from = [tile, next_tile]

                        self.grid.insert_tile(merged)
                        self.grid.remove_tile(tile)

                        tile.update_position(next_cell)

                        self.score += merged.value

                        if merged.value == 2048:
                            self.won = True
                    else:
                        self.move_tile(tile, positions['farthest'])

                    if cell != tile.position():
                        moved = True

        if moved:
            self.add_random_tile()

            if not self.moves_available():
                self.over = True  # Game over!

            self.actuate()

    def get_vector(self, direction):
        # 0: up, 1: right, 2: down, 3: left
        vectors = {
            0: (0, -1),  # Up
            1: (1, 0),   # Right
            2: (0, 1),   # Down
            3: (-1, 0)   # Left
        }
        return vectors.get(direction, (0, 0))

    def build_traversals(self, vector):
        traversals = {'x': list(range(self.size)), 'y': list(range(self.size))}

        if vector[0] == 1:
            traversals['x'].reverse()
        if vector[1] == 1:
            traversals['y'].reverse()

        return traversals

    def find_farthest_position(self, cell, vector):
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

    def moves_available(self):
        return self.grid.cells_available() or self.tile_matches_available()

    def tile_matches_available(self):
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

    def positions_equal(self, first, second):
        return first[0] == second[0] and first[1] == second[1]