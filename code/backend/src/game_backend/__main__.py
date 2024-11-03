from game_backend.implementations.array_tile import ArrayTile
from game_backend.implementations.array_grid import ArrayGrid
from game_backend.game_manager import GameManager
from game_backend.local_storage_manager import LocalStorageManager
from backend.implementations.in_process_comm import InProcessCommunication

def main():
    # Initialize storage manager
    storage_manager = LocalStorageManager()

    # Initialize grid and tile implementations
    grid = ArrayGrid(size=4)
    tile_class = ArrayTile

    # Initialize game manager with dependency injection
    game_manager = GameManager(grid=grid, tile_class=tile_class, storage_manager=storage_manager)

    # Initialize communication interface
    communication = InProcessCommunication(game_manager=game_manager)

    # Example CLI Loop
    while not game_manager.is_game_terminated():
        print(f"Score: {game_manager.score}")
        # Display grid state (implementation depends on your actuator/frontend)
        grid_state = communication.receive_grid_state()
        print(grid_state)

        # Get user input for direction
        direction = int(input("Enter move direction (0: up, 1: right, 2: down, 3: left): "))
        communication.send_move(direction)

    print("Game Over!")

if __name__ == "__main__":
    main()