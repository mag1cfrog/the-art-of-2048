from typing import Dict, Any
import curses

class Renderer:
    """
    Handles rendering of the game state to the terminal using curses.
    """
    def __init__(self, stdscr: curses.window) -> None:
        """
        Initializes the Renderer with a curses window.

        Args:
            stdscr (curses.window): The curses window object.
        """
        self.stdscr = stdscr
        curses.curs_set(0)  # Hide cursor
        self.stdscr.nodelay(False)
        self.stdscr.keypad(True)

    def render_grid(self, grid_state: Dict[str, Any]) -> None:
        """
        Renders the current game grid and score.

        Args:
            grid_state (Dict[str, Any]): The current state of the game grid and score.
        """
        self.stdscr.clear()
        self.stdscr.addstr(0, 0, f"Score: {grid_state['score']}", curses.A_BOLD)
        self.stdscr.addstr(1, 0, "-" * (grid_state['grid']['size'] * 6))

        for y in range(grid_state['grid']['size']):
            row = ""
            for x in range(grid_state['grid']['size']):
                cell = grid_state['grid']['cells'][x][y]
                if cell:
                    row += f"{cell['value']:4} "
                else:
                    row += "   . "
            self.stdscr.addstr(y + 2, 0, row)

        self.stdscr.addstr(grid_state['grid']['size'] + 3, 0, "Use WASD or Arrow keys to move. Press 'q' to exit.")
        self.stdscr.refresh()

    def show_game_over(self, message: str) -> None:
        """
        Displays the game over message.

        Args:
            message (str): The game over message to display.
        """
        self.stdscr.addstr(0, 0, message, curses.A_BLINK | curses.A_BOLD)
        self.stdscr.addstr(1, 0, "Press any key to exit.")
        self.stdscr.refresh()