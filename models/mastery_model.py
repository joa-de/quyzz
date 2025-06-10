import json
import os
import random
from pathlib import Path

import json
import os
from glob import glob


class MasteryModel:
    def __init__(self):
        pass

    @staticmethod
    def load_mastery_data(user_name, vocab_dir="vocabularies"):
        """
        Load or initialize the mastery data for the given user, ensuring it includes
        all words from the vocabulary files in the specified directory.

        Args:
            user_name (str): Name of the user.
            vocab_dir (str): Path to the directory containing vocabulary files.

        Returns:
            dict: Mastery data for all words in the vocabulary files.
        """
        file_name = f"{user_name}_vocabulary_mastery.json"
        mastery_file = Path("./user_data") / file_name

        # Load existing mastery data if available
        if os.path.exists(mastery_file):
            with open(mastery_file, "r", encoding="utf-8") as file:
                mastery_data = json.load(file)
        else:
            mastery_data = {}

        # Load all vocabulary files
        vocab_files = glob(os.path.join(vocab_dir, "*.txt"))
        all_words = {}

        for vocab_file in vocab_files:
            with open(vocab_file, "r", encoding="utf-8") as file:
                for line in file:
                    if line.strip():
                        parts = line.split("|")
                        word_id = parts[0].strip()
                        if word_id not in all_words:
                            all_words[word_id] = {
                                "correct_attempts": 0,
                                "total_attempts": 0,
                            }

        # Merge new words into mastery data
        for word_id, default_values in all_words.items():
            if word_id not in mastery_data:
                mastery_data[word_id] = default_values

        # Sort mastery data by word_id
        mastery_data = {k: mastery_data[k] for k in sorted(mastery_data, key=int)}

        # Save the updated mastery file
        with open(mastery_file, "w", encoding="utf-8") as file:
            json.dump(mastery_data, file, indent=4)

        return mastery_data

    @staticmethod
    def save_mastery_data(user_name, mastery_data):
        """Save the mastery data for the given user."""
        file_name = f"{user_name}_vocabulary_mastery.json"
        mastery_file = Path("./user_data") / file_name

        with open(mastery_file, "w", encoding="utf-8") as file:
            json.dump(mastery_data, file, indent=4)

    def weighted_choice(available_words, mastery_data):
        """
        Select a word ID based on mastery data with weighting:
        - Higher weight for unplayed words.
        - Medium weight for less mastered words.
        - Lower weight for well-mastered words.

        Args:
            available_words (set): Set of available word IDs.
            mastery_data (dict): User performance data.

        Returns:
            str: Selected word ID.
        """
        weights = []
        for word_id in available_words:
            data = mastery_data.get(
                str(word_id), {"correct_attempts": 0, "total_attempts": 0}
            )
            total_attempts = data["total_attempts"]
            correct_attempts = data["correct_attempts"]

            if total_attempts == 0:
                # Unplayed words get the highest weight
                weight = 10
            else:
                # Weight inversely proportional to performance (1 - success rate)
                success_rate = correct_attempts / total_attempts
                weight = max(1, int((1 - success_rate) * 10))

            weights.append(weight)

        # Use the weights to make a random choice
        word_ids = list(available_words)
        return random.choices(word_ids, weights=weights, k=1)[0]
