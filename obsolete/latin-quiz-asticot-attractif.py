# Copyright (c) 2024 Denis Joassin
# All rights reserved.

import random
from colorama import init, Fore, Style
import platform
import os
from time import sleep

from display_feedback import display_feedback
from get_random_options import get_random_options
from load_vocabulary import load_vocabulary
from display_roman_intro import display_roman_intro

# Initialize colorama
init()

# Define the list of players (for now we have only two players, but more can be added)
players = ["Zélie", "Denis"]


# Function to select a player
def select_player():
    print("Select a player:")
    for i, player in enumerate(players, 1):
        print(f"{i}. {player}")
    while True:
        try:
            choice = int(input("Enter the player number: "))
            if 1 <= choice <= len(players):
                selected_player = players[choice - 1]
                print(f"Selected player: {selected_player}\n")
                return selected_player
            print("Please select a valid player number.")
        except ValueError:
            print("Please enter a valid number.")


# Function to select a level
def select_level():
    print("Select a level:")
    print("1. Level 1 (hint displayed before answering)")
    print("2. Level 2 (hint displayed after answering)")
    while True:
        try:
            level = int(input("Enter the level number (1 or 2): "))
            if level in [1, 2]:
                print(f"Selected level: {level}\n")
                return level
            print("Please enter 1 or 2.")
        except ValueError:
            print("Please enter a valid number.")


# Existing code for play_sound, load_vocabulary, get_random_options, display_feedback...


def play_quiz(player_name, level):
    score = 0
    total_questions = 10  # You can adjust the number of questions

    print(f"\n{Fore.CYAN}Welcome, {player_name}, to the Latin Vocabulary Quiz!")
    print("Choose the correct Dutch translation for the given Latin word.")
    print("-" * 50 + Style.RESET_ALL)

    # Convert dictionary items to list for random sampling
    vocab_items = list(vocabulary.items())

    # Keep track of used words to avoid repetition
    used_words = set()
    available_words = set(vocabulary.keys())

    for question_num in range(total_questions):
        # If we've used all words, reset the used_words set
        if len(available_words) == 0:
            available_words = set(vocabulary.keys())
            used_words.clear()

        # Select a random word that hasn't been used yet
        word_id = random.choice(list(available_words))
        available_words.remove(word_id)
        used_words.add(word_id)
        word_data = vocabulary[word_id]

        # Get options for multiple choice
        options = get_random_options(word_data["translation"], vocabulary)

        # Display question
        print(f"\n{Fore.YELLOW}Question {question_num + 1}/{total_questions}")
        print(f"Latin word: {word_data['word']} ({word_data['form']}){Style.RESET_ALL}")

        # Display hint based on level
        if level == 1:
            print(f"Hint: {word_data['hint']}")

        # Display options
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")

        # Get user answer
        while True:
            try:
                answer = int(input("\nEnter your answer (1-4): "))
                if 1 <= answer <= 4:
                    break
                print("Please enter a number between 1 and 4.")
            except ValueError:
                print("Please enter a valid number.")

        # Display hint after answering if level is 2
        if level == 2:
            print(f"Hint: {word_data['hint']}")

        # Check answer and display feedback
        is_correct = options[answer - 1] == word_data["translation"]
        if is_correct:
            score += 1
        display_feedback(
            is_correct, word_data["translation"], word_data["hint"], score, question_num
        )

    # Final score with color
    percentage = (score / total_questions) * 100
    print(f"\n{Fore.CYAN}Quiz completed, {player_name}!")
    print(f"Final score: {score}/{total_questions}")
    print(f"Percentage: {percentage:.1f}%{Style.RESET_ALL}")

    if percentage == 100:
        print(f"{Fore.GREEN}Perfect score! Excellent work!{Style.RESET_ALL}")
    elif percentage >= 80:
        print(f"{Fore.GREEN}Great job!{Style.RESET_ALL}")
    elif percentage >= 60:
        print(f"{Fore.YELLOW}Good effort! Keep practicing!{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Keep studying! You'll improve!{Style.RESET_ALL}")


if __name__ == "__main__":
    # Load vocabulary when the program starts
    vocabulary = load_vocabulary("vocabulary.txt")

    display_roman_intro()

    while True:
        # Select a player and level at the start of each game
        player_name = select_player()
        level = select_level()
        play_quiz(player_name, level)

        play_again = input(
            f"\n{Fore.CYAN}Would you like to play again? (yes/no): {Style.RESET_ALL}"
        ).lower()
        if play_again not in ["yes", "y", "Y"]:
            print(f"{Fore.GREEN}Thanks for playing! Vale!{Style.RESET_ALL}")
            break
