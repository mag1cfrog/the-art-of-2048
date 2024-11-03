from typing import Optional

class InputHandler:
    """
    Handles user input from the keyboard.
    """
    DIRECTION_KEYS = {
        259: 0,  # KEY_UP
        261: 1,  # KEY_RIGHT
        258: 2,  # KEY_DOWN
        260: 3,  # KEY_LEFT
        ord('w'): 0,
        ord('d'): 1,
        ord('s'): 2,
        ord('a'): 3
    }

    EXIT_KEYS = {ord('q'), ord('Q')}

    def get_direction(self, key: int) -> Optional[int]:
        """
        Maps a key press to a game direction.

        Args:
            key (int): The key code pressed by the user.

        Returns:
            Optional[int]: The corresponding direction (0: up, 1: right, 2: down, 3: left), or None if it's an exit key.
        """
        if key in self.DIRECTION_KEYS:
            return self.DIRECTION_KEYS[key]
        elif key in self.EXIT_KEYS:
            return None
        return None