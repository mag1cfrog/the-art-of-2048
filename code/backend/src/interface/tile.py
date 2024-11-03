from abc import ABC, abstractmethod

class Tile(ABC):
    """
    Abstract class to define the interface of a Tile.
    """

    @abstractmethod
    def __init__(self, position, value) -> None:
        pass

    @abstractmethod
    def save_position(self) -> None:
        pass

    @abstractmethod
    def update_position(self, new_position) -> None:
        pass

    @abstractmethod
    def serialize(self) -> None:
        pass