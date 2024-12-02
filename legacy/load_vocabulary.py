import os
from pathlib import Path
from models.language_manager import LanguageManager

# Description: Load vocabulary from a file and return it as a dictionary.
# Denis Joassin 2024


class Vocabulary:
    def __init__(
        self, directory="./vocabularies", lang_manager: LanguageManager = None
    ):
        self.directory = Path(directory)
        self._set_langage_manager(lang_manager)
        self.data = {}

    def _set_langage_manager(self, lang_manager: LanguageManager):
        self.lang_manager = lang_manager

    def get_word_id_range(self, filenames):
        """
        Determine the minimum and maximum word IDs across all files.

        Args:
            directory (Path): The directory containing the vocabulary files.
            filenames (list): The list of vocabulary file names.

        Returns:
            tuple: A tuple containing the minimum and maximum word IDs.
        """

        directory = self.directory

        min_id, max_id = float("inf"), float("-inf")

        for filename in filenames:
            with open(directory / filename, "r", encoding="utf-8") as file:
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

    def load_vocabulary(self):

        lang = self.lang_manager
        directory = self.directory
        filenames, custom_range = self.choose_file_or_custom(directory)
        vocabulary = {}

        try:
            for filename in filenames:
                with open(directory / filename, "r", encoding="utf-8") as file:
                    for line in file:
                        parts = line.strip().split("|")
                        if len(parts) >= 5:
                            try:
                                word_id = int(
                                    parts[0]
                                )  # Ensure word_id is treated as an integer
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
        except FileNotFoundError:
            print(
                lang.get("vocabulary_management.file_not_found").format(
                    filename=filename
                )
            )
            exit(1)
        except Exception as e:
            print(lang.get("vocabulary_management.loading_error").format(error=str(e)))
            exit(1)

        # Ensure vocabulary is sorted by word_id
        vocabulary = dict(sorted(vocabulary.items()))

        return vocabulary, filenames

    def choose_file_or_custom(self, directory):
        """
        Prompt the player to select a specific file, all files, or a custom range.
        """
        lang = self.lang_manager
        directory = self.directory
        files = [f for f in os.listdir(directory) if f.endswith(".txt")]

        if not files:
            print(lang.get("vocabulary_management.no_files_found"))
            exit(1)

        # Get the global word_id range across all files
        min_id, max_id = self.get_word_id_range(files)

        print(f"\n{lang.get('vocabulary_management.available_lists')}")
        print(f"0: {lang.get('vocabulary_management.all_chapters')}")
        print(
            f"-1: {lang.get('vocabulary_management.custom_range').format(min_id=min_id, max_id=max_id)}"
        )
        for i, file in enumerate(files):
            print(f"{i + 1}: {file[:-4]}")

        while True:
            try:
                choice = int(input(lang.get("vocabulary_management.file_selection")))
                if 0 < choice <= len(files):
                    return [files[choice - 1]], None
                elif choice == 0:
                    return files, None  # Return all files
                elif choice == -1:
                    # Handle custom range
                    range_input = input(
                        lang.get("vocabulary_management.enter_range").format(
                            min_id=min_id, max_id=max_id
                        )
                    )
                    try:
                        start, end = map(int, range_input.split("-"))
                        if start < min_id or end > max_id:
                            print(
                                lang.get("vocabulary_management.invalid_range").format(
                                    min_id=min_id, max_id=max_id
                                )
                            )
                        elif start <= end:
                            return files, (start, end)
                        else:
                            print(lang.get("vocabulary_management.invalid_range_order"))
                    except ValueError:
                        print(lang.get("vocabulary_management.invalid_range_format"))
                print(lang.get("vocabulary_management.invalid_choice"))
            except ValueError:
                print(lang.get("vocabulary_management.enter_valid_number"))
