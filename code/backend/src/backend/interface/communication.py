from abc import ABC, abstractmethod
from typing import Dict, Any

class CommunicationInterface(ABC):
    @abstractmethod
    def send_move(self, direction: int) -> None:
        pass

    @abstractmethod
    def receive_grid_state(self) -> Dict[str, Any]:
        pass