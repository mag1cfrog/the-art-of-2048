from typing import Optional
from game_backend.core.comm import InProcessCommunication
from cli_frontend.renderer import Renderer
from cli_frontend.input_handler import InputHandler
from game_backend.services.game_manager import GameManager

class GameLoop:
    """
    Manages the main game loop for the CLI frontend.
    """
    def __init__(
        self,
        communication: InProcessCommunication,
        renderer: Renderer,
        input_handler: InputHandler
    ) -> None:
        """
        Initializes the GameLoop with necessary components.

        Args:
            communication (InProcessCommunication): Communication interface with the backend.
            renderer (Renderer): Renderer for displaying the game.
            input_handler (InputHandler): Handler for user input.
        """
        self.communication = communication
        self.renderer = renderer
        self.input_handler = input_handler
        self.game_manager: GameManager = communication.game_manager

    def run(self) -> None:
        """
        Executes the main game loop, handling rendering and user input.
        """
        while True:
            grid_state = self.communication.receive_grid_state()
            self.renderer.render_grid(grid_state)

            key = self.renderer.stdscr.getch()

            direction: Optional[int] = self.input_handler.get_direction(key)

            if direction is None and key in InputHandler.EXIT_KEYS:
                break
            elif direction is not None:
                self.communication.send_move(direction)
                if self.game_manager.is_game_terminated():
                    final_state = self.communication.receive_grid_state()
                    self.renderer.render_grid(final_state)
                    self.renderer.show_game_over("Game Over!")
                    self.renderer.stdscr.getch()
                    break