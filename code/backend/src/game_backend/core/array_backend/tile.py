from game_backend.interface.tile import Tile

class ArrayTile(Tile):
    """
    Tile implementation complying with 2D array grid.
    """
    def __init__(self, position: tuple, value: int = 2) -> None:
        self.position = position
        self.value = value
        self.previous_position = None
        self.merged_from = None # Tracks tiles that merged together

    def save_position(self):
        self.previous_position = self.position

    def update_position(self, position: tuple):
        self.position = position

    def serialize(self):
        return {
            "position": self.position,
            "value": self.value,
        }
