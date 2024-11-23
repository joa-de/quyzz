import os
from pathlib import Path

# Description: Load vocabulary from a file and return it as a dictionary.
# Denis Joassin 2024


def get_word_id_range(directory, filenames):
    """
    Determine the minimum and maximum word IDs across all files.

    Args:
        directory (Path): The directory containing the vocabulary files.
        filenames (list): The list of vocabulary file names.

    Returns:
        tuple: A tuple containing the minimum and maximum word IDs.
    """
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


def load_vocabulary():
    def choose_file_or_custom(directory):
        """
        Prompt the player to select a specific file, all files, or a custom range.
        """
        files = [f for f in os.listdir(directory) if f.endswith(".txt")]
        if not files:
            print("No .txt files found in the current directory.")
            exit(1)

        # Get the global word_id range across all files
        min_id, max_id = get_word_id_range(directory, files)

        print("\nAvailable vocabulary lists:")
        print(f"{0}: All chapters combined")
        print(
            f"{-1}: Custom range of word IDs (from all files, range {min_id}-{max_id})"
        )
        for i, file in enumerate(files):
            print(f"{i + 1}: {file[:-4]}")

        while True:
            try:
                choice = int(input("Enter the number of the file: "))
                if 0 < choice <= len(files):
                    return [files[choice - 1]], None
                elif choice == 0:
                    return files, None  # Return all files
                elif choice == -1:
                    # Handle custom range
                    range_input = input(
                        f"Enter a range of word IDs (e.g., '{min_id}-{max_id}'): "
                    )
                    try:
                        start, end = map(int, range_input.split("-"))
                        if start < min_id or end > max_id:
                            print(
                                f"Invalid range. Please enter a range within {min_id}-{max_id}."
                            )
                        elif start <= end:
                            return files, (start, end)
                        else:
                            print(
                                "Invalid range. Start must be less than or equal to end."
                            )
                    except ValueError:
                        print("Invalid format. Please enter a range like '123-152'.")
                print("Invalid choice.")
            except ValueError:
                print("Please enter a valid number.")

    directory = Path("./vocabularies")
    filenames, custom_range = choose_file_or_custom(directory)
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
        print(f"Error: Could not find vocabulary file '{filename}'")
        exit(1)
    except Exception as e:
        print(f"Error loading vocabulary: {e}")
        exit(1)

    # Ensure vocabulary is sorted by word_id
    vocabulary = dict(sorted(vocabulary.items()))

    if custom_range:
        filenames = ["custom"]

    return vocabulary, filenames
