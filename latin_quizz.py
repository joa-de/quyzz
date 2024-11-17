# Description: A Latin vocabulary quiz game with multiple levels and feedback.
# Copyright (c) 2024 Denis Joassin
# All rights reserved.

import random
from colorama import init, Fore, Style
import platform
import os
from time import sleep

from display_feedback import display_feedback
from load_vocabulary import load_vocabulary
from get_random_options import get_random_options
from display_roman_intro import display_roman_intro
from player_management import select_player, load_players, save_players
from language_manager import LanguageManager

from score_manager import ScoreManager
from score_manager import ScoreManager
from colorama import init, Fore, Style

# Initialize colorama
init()


def select_level():
    """
    Prompts the user to select a difficulty level for the quiz.

    Levels:
    1. Level 1 (hint displayed before answering)
    2. Level 2 (hint displayed after answering)
    3. Level 3 (options of the same word type, hint after answering)

    Returns:
        int: The selected level (1, 2, or 3).
    """

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


def play_quiz(player_name, level, vocabulary, lang_manager):
    """
    Conducts a Latin vocabulary quiz for the player.
    Args:
        player_name (str): The name of the player.
        level (int): The difficulty level of the quiz (1, 2, or 3).
        vocabulary (dict): A dictionary containing Latin words and their details.
        lang_manager (LanguageManager): The language manager for retrieving strings.
    Returns:
        tuple: A tuple containing the final score and the total number of questions.
    """
    score = 0
    total_questions = 10

    print(
        f"\n{Fore.CYAN}{lang_manager.get('welcome_message', 'Welcome')} {player_name}!"
    )
    print(lang_manager.get("quiz_intro", "Choose the correct translation."))
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
                word_data["translation"], vocabulary, word_data.get("word_type")
            )
        else:
            options = get_random_options(word_data["translation"], vocabulary)

        # Display question
        print(
            f"\n{Fore.YELLOW}{lang_manager.get('question_label', 'Question')} {question_num + 1}/{total_questions}"
        )
        print(
            f"{lang_manager.get('latin_word', 'Latin word')}: {word_data['word']} ({word_data['form']})"
        )
        if level == 3:
            print(
                f"{lang_manager.get('word_type', 'Word type')}: {word_data.get('word_type', '')}{Style.RESET_ALL}"
            )
        else:
            print(Style.RESET_ALL, end="")

        # Display hint based on level
        if level == 1:
            print(f"{lang_manager.get('hint', 'Hint')}: {word_data['hint']}")

        # Display options
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")

        # Get user answer
        while True:
            try:
                answer = int(
                    input(
                        f"\n{lang_manager.get('enter_answer', 'Enter your answer')} (1-4): "
                    )
                )
                if 1 <= answer <= 4:
                    break
                print(
                    lang_manager.get(
                        "enter_valid_number",
                        "Please enter a valid number between 1 and 4.",
                    )
                )
            except ValueError:
                print(
                    lang_manager.get(
                        "enter_valid_number",
                        "Please enter a valid number between 1 and 4.",
                    )
                )

        # Display hint after answering for levels 2 and 3
        if level in [2, 3]:
            print(f"{lang_manager.get('hint', 'Hint')}: {word_data['hint']}")

        # Check answer and display feedback
        is_correct = options[answer - 1] == word_data["translation"]
        if is_correct:
            score += 1
        display_feedback(
            is_correct, word_data["translation"], word_data["hint"], score, question_num
        )

    # Final score with color
    percentage = (score / total_questions) * 100
    print(
        f"\n{Fore.CYAN}{lang_manager.get('quiz_completed', 'Quiz completed')} {player_name}!"
    )
    print(
        f"{lang_manager.get('final_score', 'Final score')}: {score}/{total_questions}"
    )
    print(
        f"{lang_manager.get('percentage', 'Percentage')}: {percentage:.1f}%{Style.RESET_ALL}"
    )

    if percentage == 100:
        print(
            f"{Fore.GREEN}{lang_manager.get('perfect_score', 'Perfect score! Excellent work!')}{Style.RESET_ALL}"
        )
    elif percentage >= 80:
        print(
            f"{Fore.GREEN}{lang_manager.get('great_job', 'Great job!')}{Style.RESET_ALL}"
        )
    elif percentage >= 60:
        print(
            f"{Fore.YELLOW}{lang_manager.get('good_effort', 'Good effort! Keep practicing!')}{Style.RESET_ALL}"
        )
    else:
        print(
            f"{Fore.RED}{lang_manager.get('keep_studying', 'Keep studying!')}{Style.RESET_ALL}"
        )

    return score, total_questions


def main():
    """
    Main function to run the Latin quiz game.
    This function displays the Roman introduction, initializes the score manager,
    and enters a loop where the player can select their name, load vocabulary,
    select a level, and play the quiz. After each quiz, the player's score is
    updated and displayed. The player is then asked if they want to play again.
    The loop continues until the player chooses not to play again.
    """

    lang_manager = LanguageManager()

    # Displays the introduction to the game.
    display_roman_intro()
    score_manager = ScoreManager()

    while True:

        # Prompts the player to enter their name.
        player_name = select_player()
        score_manager.display_player_stats(player_name, lang_manager)

        # Loads the vocabulary for the quiz
        vocabulary, vocab_files = load_vocabulary()

        # Prompts the player to select a difficulty level.
        level = select_level()

        # play_quizz
        score, total_questions = play_quiz(player_name, level, vocabulary, lang_manager)
        percentage = (score / total_questions) * 100

        # Update score with vocabulary information
        score_manager.update_score(player_name, vocab_files, level, percentage)

        # Displays the player's statistics.
        print(f"\n{Fore.CYAN}Updated Statistics:{Style.RESET_ALL}")
        score_manager.display_player_stats(player_name, lang_manager)

        # Ask the player if they want to play again
        play_again = input(
            f"\n{Fore.CYAN}{lang_manager.get('play_again_prompt')} {Style.RESET_ALL}"
        ).lower()
        if play_again not in ["yes", "y", "Y"]:
            print(
                f"{Fore.GREEN}{lang_manager.get('thanks_for_playing')}{Style.RESET_ALL}"
            )
            break


if __name__ == "__main__":

    main()
