from typing import Any, Dict

from backend.interface.communication import CommunicationInterface
from game_backend.game_manager import GameManager

class InProcessCommunication(CommunicationInterface):
    def __init__(self, game_manager: GameManager):
        self.game_manager = game_manager

    def send_move(self, direction: int) -> None:
        self.game_manager.play_turn(direction)

    def receive_grid_state(self) -> Dict[str, Any]:
        return self.game_manager.get_grid_state()