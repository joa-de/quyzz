# Description: A Latin vocabulary quiz game with multiple levels and feedback.
# Copyright (c) 2024 Denis Joassin
# All rights reserved.

import random
from colorama import init, Fore, Style
import platform
import os
from time import sleep

from display_feedback import display_feedback
from load_vocabulary_enhanced import load_vocabulary, load_vocabulary2
from display_roman_intro import display_roman_intro
from score_manager import ScoreManager
from enhanced_score_manager import EnhancedScoreManager
from colorama import init, Fore, Style

init()


# Initialize colorama
init()

# Define the list of players
players = ["Zélie", "Denis"]


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


def select_level():
    print("Select a level:")
    print("1. Level 1 (hint displayed before answering)")
    print("2. Level 2 (hint displayed after answering)")
    print("3. Level 3 (options of the same word type, hint after answering)")
    while True:
        try:
            level = int(input("Enter the level number (1, 2, or 3): "))
            if level in [1, 2, 3]:
                print(f"Selected level: {level}\n")
                return level
            print("Please enter 1, 2, or 3.")
        except ValueError:
            print("Please enter a valid number.")


def get_random_options(correct_answer, vocabulary, word_type=None):
    """
    Get random options for multiple choice, with support for word type matching.

    Args:
        correct_answer: The correct translation
        vocabulary: The complete vocabulary dictionary
        word_type: The type of word to match (for level 3)
    """
    options = [correct_answer]
    vocab_items = list(vocabulary.items())

    if word_type:
        # Filter vocabulary items to only include words of the same type
        same_type_items = [
            item
            for item in vocab_items
            if item[1]["word_type"] == word_type
            and item[1]["translation"] != correct_answer
        ]

        # If we don't have enough words of the same type, fall back to random words
        if len(same_type_items) < 3:
            different_items = [
                item for item in vocab_items if item[1]["translation"] != correct_answer
            ]
            while len(options) < 4:
                random_item = random.choice(different_items)
                if random_item[1]["translation"] not in options:
                    options.append(random_item[1]["translation"])
        else:
            # Add three random words of the same type
            while len(options) < 4:
                random_item = random.choice(same_type_items)
                if random_item[1]["translation"] not in options:
                    options.append(random_item[1]["translation"])
    else:
        # Original behavior for levels 1 and 2
        different_items = [
            item for item in vocab_items if item[1]["translation"] != correct_answer
        ]
        while len(options) < 4:
            random_item = random.choice(different_items)
            if random_item[1]["translation"] not in options:
                options.append(random_item[1]["translation"])

    # Shuffle the options
    random.shuffle(options)
    return options


def play_quiz(player_name, level, vocabulary):
    score = 0
    total_questions = 10

    print(f"\n{Fore.CYAN}Welcome, {player_name}, to the Latin Vocabulary Quiz!")
    print("Choose the correct Dutch translation for the given Latin word.")
    print("-" * 50 + Style.RESET_ALL)

    vocab_items = list(vocabulary.items())
    used_words = set()
    available_words = set(vocabulary.keys())

    for question_num in range(total_questions):
        if len(available_words) == 0:
            available_words = set(vocabulary.keys())
            used_words.clear()

        word_id = random.choice(list(available_words))
        available_words.remove(word_id)
        used_words.add(word_id)
        word_data = vocabulary[word_id]

        # Get options for multiple choice, using word type for level 3
        if level == 3:
            options = get_random_options(
                word_data["translation"], vocabulary, word_data["word_type"]
            )
        else:
            options = get_random_options(word_data["translation"], vocabulary)

        # Display question
        print(f"\n{Fore.YELLOW}Question {question_num + 1}/{total_questions}")
        print(f"Latin word: {word_data['word']} ({word_data['form']})")
        if level == 3:
            print(f"Word type: {word_data['word_type']}{Style.RESET_ALL}")
        else:
            print(Style.RESET_ALL, end="")

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

        # Display hint after answering for levels 2 and 3
        if level in [2, 3]:
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

    return score, total_questions


def main():
    display_roman_intro()

    while True:
        player_name = select_player()
        vocabulary = load_vocabulary()
        level = select_level()
        play_quiz(player_name, level, vocabulary)

        play_again = input(
            f"\n{Fore.CYAN}Would you like to play again? (yes/no): {Style.RESET_ALL}"
        ).lower()
        if play_again not in ["yes", "y", "Y"]:
            print(f"{Fore.GREEN}Thanks for playing! Vale!{Style.RESET_ALL}")
            break


def main2():
    display_roman_intro()
    score_manager = ScoreManager()  # Initialize score manager

    while True:
        player_name = select_player()
        # Display player stats before the game
        score_manager.display_player_stats(player_name)

        vocabulary = load_vocabulary()
        level = select_level()
        score, total_questions = play_quiz(player_name, level, vocabulary)

        # After play_quiz function, update and display new score
        percentage = (score / total_questions) * 100
        new_ema = score_manager.update_score(player_name, level, percentage)

        print(f"\n{Fore.CYAN}Updated Statistics:{Style.RESET_ALL}")
        score_manager.display_player_stats(player_name)

        play_again = input(
            f"\n{Fore.CYAN}Would you like to play again? (yes/no): {Style.RESET_ALL}"
        ).lower()
        if play_again not in ["yes", "y", "Y"]:
            print(f"{Fore.GREEN}Thanks for playing! Vale!{Style.RESET_ALL}")
            break


def main3():
    display_roman_intro()
    score_manager = EnhancedScoreManager()

    while True:
        player_name = select_player()
        score_manager.display_player_stats(player_name)

        vocabulary, vocab_files = load_vocabulary2()
        level = select_level()

        score, total_questions = play_quiz(player_name, level, vocabulary)
        percentage = (score / total_questions) * 100

        # Update score with vocabulary information
        new_ema = score_manager.update_score(
            player_name, vocab_files, level, percentage
        )

        print(f"\n{Fore.CYAN}Updated Statistics:{Style.RESET_ALL}")
        score_manager.display_player_stats(player_name)

        play_again = input(
            f"\n{Fore.CYAN}Would you like to play again? (yes/no): {Style.RESET_ALL}"
        ).lower()
        if play_again not in ["yes", "y", "Y"]:
            print(f"{Fore.GREEN}Thanks for playing! Vale!{Style.RESET_ALL}")
            break


if __name__ == "__main__":

    main3()
