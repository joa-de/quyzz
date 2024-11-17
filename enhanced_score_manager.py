import json
import os
from datetime import datetime
from pathlib import Path
from tabulate import tabulate
from colorama import Fore, Style


class EnhancedScoreManager:
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
            self.scores[player_name] = {"vocabularies": {}, "last_played": None}
        return self.scores[player_name]

    def get_vocabulary_identifier(self, filenames):
        """Create a unique identifier for a vocabulary combination"""
        if isinstance(filenames, str):
            filenames = [filenames]
        # Sort and join filenames without .txt extension
        return "+".join(sorted([f[:-4] for f in filenames]))

    def ensure_vocabulary_scores(self, player_name, vocab_id):
        """Ensure vocabulary scores exist for the player"""
        player_data = self.get_player_scores(player_name)
        if vocab_id not in player_data["vocabularies"]:
            player_data["vocabularies"][vocab_id] = {
                "levels": {
                    "1": {"ema": 0.0, "games_played": 0},
                    "2": {"ema": 0.0, "games_played": 0},
                    "3": {"ema": 0.0, "games_played": 0},
                }
            }
        return player_data["vocabularies"][vocab_id]

    def update_score(self, player_name, vocab_files, level, new_score, period=None):
        """
        Update player's score using EMA

        Args:
            player_name: Name of the player
            vocab_files: List of vocabulary files used
            level: Game level (1, 2, or 3)
            new_score: New score to incorporate (0-100)
            period: Period for EMA calculation (optional)
        """
        if period is None:
            period = self.default_period

        vocab_id = self.get_vocabulary_identifier(vocab_files)
        player_data = self.get_player_scores(player_name)
        vocab_data = self.ensure_vocabulary_scores(player_name, vocab_id)
        level_str = str(level)
        level_data = vocab_data["levels"][level_str]

        # Calculate EMA
        alpha = 0.1

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
        """Display player's statistics in a formatted table"""
        player_data = self.get_player_scores(player_name)

        print(f"\n{Fore.CYAN}Statistics for {player_name}:{Style.RESET_ALL}")
        if player_data["last_played"]:
            print(f"Last played: {player_data['last_played']}")
        print()

        # Prepare table data
        table_data = []
        headers = ["Vocabulary", "Level", "Score", "Games"]

        for vocab_id in sorted(player_data["vocabularies"].keys()):
            vocab_data = player_data["vocabularies"][vocab_id]
            for level in ["1", "2", "3"]:
                level_data = vocab_data["levels"][level]
                ema = level_data["ema"]
                games = level_data["games_played"]

                # Color coding based on EMA score
                if ema >= 80:
                    score_str = f"{Fore.GREEN}{ema:.1f}%{Style.RESET_ALL}"
                elif ema >= 60:
                    score_str = f"{Fore.YELLOW}{ema:.1f}%{Style.RESET_ALL}"
                else:
                    score_str = f"{Fore.RED}{ema:.1f}%{Style.RESET_ALL}"

                table_data.append([vocab_id, level, score_str, games])

        # Display table using tabulate
        print(tabulate(table_data, headers=headers, tablefmt="grid", stralign="center"))
