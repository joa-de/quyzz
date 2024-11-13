import os
from pathlib import Path

# Description: Load vocabulary from a file and return it as a dictionary.
# Copyright (c) 2024 Denis Joassin
# All rights reserved.


def load_vocabulary():

    def choose_file(directory):

        files = [f for f in os.listdir(directory) if f.endswith(".txt")]
        if not files:
            print("No .txt files found in the current directory.")
            exit(1)

        print("Please choose a file to load:")
        for i, file in enumerate(files):
            print(f"{i + 1}: {file[:-5]} {file[-5]}")
            max_idx = i
        print(f"{max_idx + 2}: Alle hoofdstukken")

        choice = int(input("Enter the number of the file: ")) - 1
        if choice < 0 or choice >= (len(files) + 1):
            print("Invalid choice.")
            exit(1)

        if choice == (max_idx + 1):  # Load all files
            return files
        else:
            return [files[choice]]

    directory = Path("./vocabularies")
    filenames = choose_file(directory)

    vocabulary = {}
    try:
        for filename in filenames:
            with open(directory / filename, "r", encoding="utf-8") as file:
                for line in file:
                    # Split the line by the pipe character
                    parts = line.strip().split("|")
                    if len(parts) >= 5:  # Make sure we have all needed parts
                        word_id = parts[0]
                        vocabulary[word_id] = {
                            "word": parts[1],
                            "form": parts[2],
                            "translation": parts[3],
                            "hint": parts[4] if len(parts) > 4 else "",
                            "word_type": (
                                parts[5] if len(parts) > 5 else ""
                            ),  # Add word type
                        }

    except FileNotFoundError:
        print(f"Error: Could not find vocabulary file '{filename}'")
        exit(1)
    except Exception as e:
        print(f"Error loading vocabulary: {e}")
        exit(1)

    return vocabulary


def load_vocabulary2():
    def choose_file(directory):
        files = [f for f in os.listdir(directory) if f.endswith(".txt")]
        if not files:
            print("No .txt files found in the current directory.")
            exit(1)
        print("\nAvailable vocabulary lists:")
        for i, file in enumerate(files):
            print(f"{i + 1}: {file[:-4]}")
        print(f"{len(files) + 1}: All chapters combined")

        while True:
            try:
                choice = int(input("Enter the number of the file: ")) - 1
                if 0 <= choice < len(files):
                    return [files[choice]], files[choice]
                elif choice == len(files):
                    return files, "all_chapters"
                print("Invalid choice.")
            except ValueError:
                print("Please enter a valid number.")

    directory = Path("./vocabularies")
    filenames, selected_vocab = choose_file(directory)
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
