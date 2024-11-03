import json
import logging
from pathlib import Path
from typing import Any, Dict, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LocalStorageManager:
    """
    Manages local storage for the 2048 game, handling best scores and game states.
    
    This class simulates browser-like localStorage using a JSON file.
    If the storage file is not supported or accessible, it falls back to an in-memory storage.
    """
    # Storage keys
    KEY_BEST_SCORE = "best_score"
    KEY_GAME_STATE = "game_state"

    def __init__(self, storage_file: str = 'local_storage.json') -> None:
        """
        Initializes the LocalStorageManager.

        Args:
            storage_file (str): The path to the JSON file used for persistent storage.
                                Defaults to 'local_storage.json'.
        """
        self.best_score_key: str = self.KEY_BEST_SCORE
        self.game_state_key: str = self.KEY_GAME_STATE

        self.storage_path: Path = Path(storage_file)
        self._data: Dict[str, Any] = {}

        if self.local_storage_supported():
            self._load_storage()
        else:
            self._data = {}
            logger.warning("Local storage not supported. Using in-memory storage.")

    def local_storage_supported(self) -> bool:
        """
        Checks if the local storage is supported by attempting to read/write to the storage file.

        Returns:
            bool: True if storage is supported, False otherwise.
        """
        try:
            # Attempt to create or open the storage file
            if not self.storage_path.exists():
                self.storage_path.touch()
                self.storage_path.write_text("{}")

            # Attempt to read and write to the storage file
            temp_data = {"test": "1"}
            self.storage_path.write_text(json.dumps(temp_data))
            data = json.loads(self.storage_path.read_text())
            if data.get("test") == "1":
                del data["test"]
                self.storage_path.write_text(json.dumps(data))
                return True
        except (IOError, json.JSONDecodeError) as e:
            logger.error(f"Local storage check failed: {e}")
            return False
        return False

    def _load_storage(self) -> None:
        """
        Loads data from the storage file into the internal dictionary.
        """
        try:
            self._data = json.loads(self.storage_path.read_text())
            logger.info("Local storage loaded successfully.")
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.error(f"Error loading storage: {e}")
            self._data = {}

    def _save_storage(self) -> None:
        """
        Saves the internal dictionary data to the storage file.
        """
        try:
            self.storage_path.write_text(json.dumps(self._data, indent=4))
            logger.info("Local storage saved successfully.")
        except IOError as e:
            logger.error(f"Error saving storage: {e}")

    # Best score getters/setters
    def get_best_score(self) -> int:
        """
        Retrieves the best score from storage.

        Returns:
            int: The best score, or 0 if not set.
        """
        try:
            return int(self._data.get(self.best_score_key, 0))
        except (ValueError, TypeError) as e:
            logger.error(f"Invalid best score value: {e}")
            return 0

    def set_best_score(self, score: int) -> None:
        """
        Sets the best score in storage.

        Args:
            score (int): The score to set as the best score.
        """
        self._data[self.best_score_key] = score
        self._save_storage()

    # Game state getters/setters and clearing
    def get_game_state(self) -> Optional[Dict[str, Any]]:
        """
        Retrieves the current game state from storage.

        Returns:
            Optional[Dict[str, Any]]: The game state if exists, otherwise None.
        """
        state_json = self._data.get(self.game_state_key)
        if state_json:
            try:
                return json.loads(state_json)
            except json.JSONDecodeError as e:
                logger.error(f"Error decoding game state: {e}")
        return None

    def set_game_state(self, game_state: Dict[str, Any]) -> None:
        """
        Sets the current game state in storage.

        Args:
            game_state (Dict[str, Any]): The game state to store.
        """
        try:
            self._data[self.game_state_key] = json.dumps(game_state)
            self._save_storage()
        except (TypeError, ValueError) as e:
            logger.error(f"Error encoding game state: {e}")

    def clear_game_state(self) -> None:
        """
        Clears the current game state from storage.
        """
        if self.game_state_key in self._data:
            del self._data[self.game_state_key]
            self._save_storage()