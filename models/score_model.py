import json
import os
from datetime import datetime
from pathlib import Path

PLAYER_DIR = Path("./user_data")


class ScoreModel:
    def __init__(self, filename="player_scores.json", default_period=10):
        """
        Initialize the score manager.

        Args:
            filename: JSON file to store scores.
            default_period: Default period for EMA calculation.
        """
        self.filename = PLAYER_DIR / filename
        self.default_period = default_period
        self.scores = self._load_scores()
        self._load_players_with_scores()
        self._read_player_availaible_levels()

    def _load_scores(self):
        """Load scores from JSON file, create if it doesn't exist."""
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def _load_players_with_scores(self):
        self.players_with_scores = list(self.scores.keys())

    def _read_player_availaible_levels(self):
        player_levels = {}
        for player in self.scores:
            player_levels[player] = []
            for vocab in self.scores[player]["vocabularies"]:
                for level in self.scores[player]["vocabularies"][vocab]["levels"]:
                    if level not in player_levels[player]:
                        player_levels[player].append(level)
            player_levels[player] = sorted(player_levels[player], key=int)

        self.player_levels = player_levels

    def _save_scores(self):
        """Save scores to JSON file."""
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.scores, f, indent=4)

    def get_player_scores(self, player_name):
        """Get all scores for a player."""
        if player_name not in self.scores:
            self.scores[player_name] = {"vocabularies": {}, "last_played": None}
            self._load_players_with_scores()
            self._save_scores()
        return self.scores[player_name]

    def get_vocabulary_identifier(self, filenames):
        """Create a unique identifier for a vocabulary combination."""
        if isinstance(filenames, str):
            filenames = [filenames]
        if len(filenames) == 1:
            return filenames[0].strip(".txt")
        else:
            return "all_files"

    def ensure_vocabulary_scores(self, player_name, vocab_id):
        """Ensure vocabulary scores exist for the player."""
        player_data = self.get_player_scores(player_name)
        if vocab_id not in player_data["vocabularies"]:
            player_data["vocabularies"][vocab_id] = {"levels": {}}
        return player_data["vocabularies"][vocab_id]

    def ensure_level_scores(self, vocab_data, level):
        """
        Ensure that a specific level exists in the vocabulary data.

        Args:
            vocab_data: Dictionary containing vocabulary scores.
            level: The level to check and create if needed.
        """
        level_str = str(level)
        if level_str not in vocab_data["levels"]:
            vocab_data["levels"][level_str] = {"ema": 0.0, "games_played": 0}

    def update_score(self, player_name, vocab_files, level, new_score, period=None):
        """
        Update player's score using EMA.

        Args:
            player_name: Name of the player.
            vocab_files: List of vocabulary files used.
            level: Game level (1, 2, 3, or 4).
            new_score: New score to incorporate (0-100).
            period: Period for EMA calculation (optional).
        """
        if period is None:
            period = self.default_period

        vocab_id = self.get_vocabulary_identifier(vocab_files)
        player_data = self.get_player_scores(player_name)
        vocab_data = self.ensure_vocabulary_scores(player_name, vocab_id)

        # Ensure the level exists in the data
        self.ensure_level_scores(vocab_data, level)
        level_str = str(level)
        level_data = vocab_data["levels"][level_str]

        # Calculate EMA
        alpha = 0.25

        if level_data["games_played"] == 0:
            level_data["ema"] = new_score
        else:
            level_data["ema"] = (alpha * new_score) + ((1 - alpha) * level_data["ema"])

        # Update statistics
        level_data["games_played"] += 1
        player_data["last_played"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self._save_scores()
        return level_data["ema"]
