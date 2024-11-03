from abc import ABC, abstractmethod

class Grid(ABC):
    """
    Abstract class to define the interface of a Grid.
    """

    @abstractmethod
    def __init__(self, size: int, previous_state=None) -> None:
        pass

    @abstractmethod
    def from_state(self, state):
        pass
    
    @abstractmethod
    def random_available_cell(self):
        pass

    @abstractmethod
    def cells_available(self):
        pass
    
    @abstractmethod
    def cell_content(self, cell):
        pass

    @abstractmethod
    def within_bounds(self, position):
        pass

    @abstractmethod
    def cell_available(self, cell):
        pass

    @abstractmethod
    def insert_tile(self, tile):
        pass

    @abstractmethod
    def remove_tile(self, tile):
        pass

    @abstractmethod
    def serialize(self):
        pass