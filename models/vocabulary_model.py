import os
from pathlib import Path


class VocabularyModel:
    def __init__(self, directory="./vocabularies"):
        self.directory = Path(directory)
        self.data = {}

    def get_word_id_range(self, filenames):
        """Determine the min and max word IDs across all files."""
        min_id, max_id = float("inf"), float("-inf")

        for filename in filenames:
            with open(self.directory / filename, "r", encoding="utf-8") as file:
                for line in file:
                    parts = line.strip().split("|")
                    if len(parts) >= 1:
                        try:
                            word_id = int(parts[0])
                            min_id = min(min_id, word_id)
                            max_id = max(max_id, word_id)
                        except ValueError:
                            continue  # Skip lines with invalid word IDs

        if min_id == float("inf") or max_id == float("-inf"):
            raise ValueError("No valid word IDs found in the provided files.")

        return min_id, max_id

    def load(self, filenames, custom_range=None):
        """Load vocabulary from specified files and optional word ID range."""
        vocabulary = {}

        for filename in filenames:
            with open(self.directory / filename, "r", encoding="utf-8") as file:
                for line in file:
                    parts = line.strip().split("|")
                    if len(parts) >= 5:
                        try:
                            word_id = int(parts[0])
                            if custom_range:
                                start, end = custom_range
                                if not (start <= word_id <= end):
                                    continue  # Skip words outside the range
                            vocabulary[word_id] = {
                                "word": parts[1],
                                "form": parts[2],
                                "translation": parts[3],
                                "hint": parts[4] if len(parts) > 4 else "",
                                "word_type": parts[5] if len(parts) > 5 else "",
                            }
                        except ValueError:
                            continue  # Skip lines with invalid word IDs

        # Ensure vocabulary is sorted by word_id
        return dict(sorted(vocabulary.items()))
