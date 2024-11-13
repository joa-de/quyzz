import json
import os
from datetime import datetime
from colorama import Fore, Style


class ScoreManager:
    def __init__(self, filename="player_scores.json", default_period=10):
        """
        Initialize the score manager

        Args:
            filename: JSON file to store scores
            default_period: Default period for EMA calculation
        """
        self.filename = filename
        self.default_period = default_period
        self.scores = self._load_scores()

    def _load_scores(self):
        """Load scores from JSON file, create if doesn't exist"""
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                return json.load(f)
        return {}

    def _save_scores(self):
        """Save scores to JSON file"""
        with open(self.filename, "w") as f:
            json.dump(self.scores, f, indent=4)

    def get_player_scores(self, player_name):
        """Get all scores for a player"""
        if player_name not in self.scores:
            self.scores[player_name] = {
                "levels": {
                    "1": {"ema": 0.0, "games_played": 0},
                    "2": {"ema": 0.0, "games_played": 0},
                    "3": {"ema": 0.0, "games_played": 0},
                },
                "last_played": None,
            }
        return self.scores[player_name]

    def update_score(self, player_name, level, new_score, period=None):
        """
        Update player's score using EMA

        Args:
            player_name: Name of the player
            level: Game level (1, 2, or 3)
            new_score: New score to incorporate (0-100)
            period: Period for EMA calculation (optional)
        """
        if period is None:
            period = self.default_period

        player_data = self.get_player_scores(player_name)
        level_str = str(level)
        level_data = player_data["levels"][level_str]

        # Calculate EMA
        alpha = 2 / (period + 1)
        if level_data["games_played"] == 0:
            level_data["ema"] = new_score
        else:
            level_data["ema"] = (alpha * new_score) + ((1 - alpha) * level_data["ema"])

        # Update statistics
        level_data["games_played"] += 1
        player_data["last_played"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self._save_scores()
        return level_data["ema"]

    def display_player_stats(self, player_name):
        """Display player's statistics in a formatted way"""
        player_data = self.get_player_scores(player_name)

        print(f"\n{Fore.CYAN}Statistics for {player_name}:{Style.RESET_ALL}")
        print("-" * 40)

        for level in ["1", "2", "3"]:
            level_data = player_data["levels"][level]
            ema = level_data["ema"]
            games = level_data["games_played"]

            # Color coding based on EMA score
            if ema >= 80:
                color = Fore.GREEN
            elif ema >= 60:
                color = Fore.YELLOW
            else:
                color = Fore.RED

            print(f"Level {level}:")
            print(f"  Average Score: {color}{ema:.1f}%{Style.RESET_ALL}")
            print(f"  Games Played: {games}")

        if player_data["last_played"]:
            print(f"\nLast played: {player_data['last_played']}")
