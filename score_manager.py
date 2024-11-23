import json
import os
from datetime import datetime
from pathlib import Path
from tabulate import tabulate
from colorama import Fore, Style


PLAYER_DIR = Path("./user_data")


class ScoreManager:
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

    def _load_scores(self):
        """Load scores from JSON file, create if it doesn't exist."""
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def _save_scores(self):
        """Save scores to JSON file."""
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.scores, f, indent=4)

    def get_player_scores(self, player_name):
        """Get all scores for a player."""
        if player_name not in self.scores:
            self.scores[player_name] = {"vocabularies": {}, "last_played": None}
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

    def display_player_stats(self, player_name, lang_manager):
        """Display player's statistics in a formatted table with levels as rows, vocabularies as columns, and averages."""

        player_data = self.get_player_scores(player_name)

        print(
            f"\n{Fore.CYAN}{lang_manager.get('statistics_for')} {player_name}:{Style.RESET_ALL}"
        )
        if player_data["last_played"]:
            print(f"{lang_manager.get('last_played')}: {player_data['last_played']}")
        print()

        # Prepare table headers
        vocabularies = sorted(player_data["vocabularies"].keys())
        headers = (
            [lang_manager.get("level")] + vocabularies + [lang_manager.get("average")]
        )
        table_data = []

        # Collect totals for calculating averages
        vocabulary_totals = {vocab_id: 0 for vocab_id in vocabularies}
        vocabulary_counts = {vocab_id: 0 for vocab_id in vocabularies}

        for level in ["1", "2", "3", "4"]:
            row = [f"{lang_manager.get('level')} {level}"]
            level_total = 0
            level_count = 0

            for vocab_id in vocabularies:
                vocab_data = player_data["vocabularies"][vocab_id]
                self.ensure_level_scores(vocab_data, level)
                level_data = vocab_data["levels"][level]
                ema = level_data["ema"]
                played = level_data["games_played"]

                level_total += ema
                level_count += 1
                vocabulary_totals[vocab_id] += ema
                vocabulary_counts[vocab_id] += 1

                if ema >= 80:
                    score_str = f"{Fore.GREEN}{ema:.1f}%{Style.RESET_ALL} ({played})"
                elif ema >= 60:
                    score_str = f"{Fore.YELLOW}{ema:.1f}%{Style.RESET_ALL} ({played})"
                else:
                    score_str = f"{Fore.RED}{ema:.1f}%{Style.RESET_ALL} ({played})"

                row.append(score_str)

            table_data.append(row)

        avg_row = [lang_manager.get("average")]
        for vocab_id in vocabularies:
            vocab_avg = vocabulary_totals[vocab_id] / vocabulary_counts[vocab_id]
            avg_color = (
                f"{Fore.GREEN}{vocab_avg:.1f}%{Style.RESET_ALL}"
                if vocab_avg >= 80
                else (
                    f"{Fore.YELLOW}{vocab_avg:.1f}%{Style.RESET_ALL}"
                    if vocab_avg >= 60
                    else f"{Fore.RED}{vocab_avg:.1f}%{Style.RESET_ALL}"
                )
            )
            avg_row.append(avg_color)

        table_data.append(avg_row)

        print(tabulate(table_data, headers=headers, tablefmt="grid", stralign="center"))
