import json
from pathlib import Path
from typing import List, Optional

class PlayerModel:
    """Model for managing player data and interactions."""

    def __init__(self, data_path: Path = Path("./user_data"), 
                 filename: str = "players.json"):
        """
        Initialize PlayerModel with data storage configuration.
        
        Args:
            data_path (Path): Directory for storing player data
            filename (str): Filename for player data storage
        """
        self._data_path = data_path
        self._file_path = data_path / filename
        
        # Ensure data directory exists
        self._data_path.mkdir(parents=True, exist_ok=True)
        
        # Load players on initialization
        self._players = self._load_players()

    def _load_players(self) -> List[str]:
        """
        Load players from JSON file, create default if not exists.
        
        Returns:
            List of player names
        """
        if not self._file_path.exists():
            # Create file with default player
            return self._save_players(["Zélie"])
        
        with open(self._file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def _save_players(self, players: List[str]) -> List[str]:
        """
        Save players to JSON file.
        
        Args:
            players (List[str]): List of player names to save
        
        Returns:
            The saved player list
        """
        with open(self._file_path, "w", encoding="utf-8") as file:
            json.dump(players, file, indent=4, ensure_ascii=False)
        return players

    def get_players(self) -> List[str]:
        """
        Get current list of players.
        
        Returns:
            List of player names
        """
        return self._players.copy()

    def add_player(self, player_name: str) -> Optional[str]:
        """
        Add a new player.
        
        Args:
            player_name (str): Name of player to add
        
        Returns:
            Added player name or None if invalid
        """
        player_name = player_name.strip()
        if not player_name:
            return None
        
        if player_name not in self._players:
            self._players.append(player_name)
            self._save_players(self._players)
        
        return player_name

    def select_player(self, index: int) -> Optional[str]:
        """
        Select a player by list index.
        
        Args:
            index (int): 1-based index of player
        
        Returns:
            Selected player name or None
        """
        if 1 <= index <= len(self._players):
            return self._players[index - 1]
        return None
