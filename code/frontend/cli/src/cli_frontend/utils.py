from typing import Any, Dict

def format_grid_state(grid_state: Dict[str, Any]) -> str:
    """
    Formats the grid state into a string for display.

    Args:
        grid_state (Dict[str, Any]): The current state of the game grid.

    Returns:
        str: Formatted grid state.
    """
    size = grid_state['grid']['size']
    lines = [f"Score: {grid_state['score']}"]
    lines.append("-" * (size * 6))
    for y in range(size):
        row = ""
        for x in range(size):
            cell = grid_state['grid']['cells'][x][y]
            if cell:
                row += f"{cell['value']:4} "
            else:
                row += "   . "
        lines.append(row)
    lines.append("Use WASD or Arrow keys to move. Press 'q' to exit.")
    return "\n".join(lines)