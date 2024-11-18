import os
from pathlib import Path

# Description: Load vocabulary from a file and return it as a dictionary.
# Denis Joassin 2024


def load_vocabulary():
    def choose_file(directory):
        files = [f for f in os.listdir(directory) if f.endswith(".txt")]
        if not files:
            print("No .txt files found in the current directory.")
            exit(1)
        print("\nAvailable vocabulary lists:")
        print(f"{0}: All chapters combined")
        for i, file in enumerate(files):
            print(f"{i + 1}: {file[:-4]}")

        while True:
            try:
                choice = int(input("Enter the number of the file: "))
                if 0 < choice <= len(files):
                    return [files[choice - 1]]
                elif choice == 0:
                    return files, "all_chapters"
                print("Invalid choice.")
            except ValueError:
                print("Please enter a valid number.")

    directory = Path("./vocabularies")
    filenames = choose_file(directory)
    vocabulary = {}

    try:
        for filename in filenames:
            with open(directory / filename, "r", encoding="utf-8") as file:
                for line in file:
                    parts = line.strip().split("|")
                    if len(parts) >= 5:
                        word_id = parts[0]
                        vocabulary[word_id] = {
                            "word": parts[1],
                            "form": parts[2],
                            "translation": parts[3],
                            "hint": parts[4] if len(parts) > 4 else "",
                            "word_type": parts[5] if len(parts) > 5 else "",
                        }
    except FileNotFoundError:
        print(f"Error: Could not find vocabulary file '{filename}'")
        exit(1)
    except Exception as e:
        print(f"Error loading vocabulary: {e}")
        exit(1)

    return vocabulary, filenames
