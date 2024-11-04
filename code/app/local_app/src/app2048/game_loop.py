import asyncio

from typing import Optional
from cli_frontend.ws_comm import WebSocketCommunication
from cli_frontend.renderer import Renderer
from cli_frontend.input_handler import InputHandler
from game_backend.services.game_manager import GameManager

class GameLoop:
    """
    Manages the main game loop for the CLI frontend.
    """
    def __init__(
        self,
        communication: WebSocketCommunication,
        renderer: Renderer,
        input_handler: InputHandler
    ) -> None:
        """
        Initializes the GameLoop with necessary components.

        Args:
            communication (WebSocketCommunication): Communication interface with the backend.
            renderer (Renderer): Renderer for displaying the game.
            input_handler (InputHandler): Handler for user input.
        """
        self.communication = communication
        self.renderer = renderer
        self.input_handler = input_handler
        # self.game_manager: GameManager = communication.game_manager

    async def run(self) -> None:
        """
        Executes the main game loop, handling rendering and user input.
        """
        await self.communication.connect()
        while True:
            grid_state = self.communication.get_game_state()
            self.renderer.render_grid(grid_state)

            key = self.renderer.stdscr.getch()
            direction: Optional[int] = self.input_handler.get_direction(key)

            if direction is None and key in InputHandler.EXIT_KEYS:
                await self.communication.close()
                break
            elif direction is not None:
                move_success = await self.communication.send_move(direction)
                if not move_success:
                    break
                grid_state = self.communication.get_game_state()
                if grid_state.get('over', False):
                    self.renderer.render_grid(grid_state)
                    self.renderer.show_game_over("Game Over!")
                    self.renderer.stdscr.getch()
                    await self.communication.close()
                    break