# Description: Load vocabulary from a file.
# Copyright (c) 2024 Denis Joassin
# All rights reserved.


def load_vocabulary(filename):
    """Load vocabulary from a file."""
    vocabulary = {}
    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                if line.strip():  # Skip empty lines
                    # Split line by | and remove any whitespace
                    parts = [part.strip() for part in line.split("|")]
                    if len(parts) >= 5:  # Ensure all parts are present
                        word_id = int(parts[0])
                        vocabulary[word_id] = {
                            "word": parts[1],
                            "form": parts[2],
                            "translation": parts[3],
                            "hint": parts[4],
                        }
    except FileNotFoundError:
        print(f"Error: Could not find {filename}")
        exit(1)
    except Exception as e:
        print(f"Error loading vocabulary: {e}")
        exit(1)
    return vocabulary
