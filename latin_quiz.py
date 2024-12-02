# Description: A Latin vocabulary quiz game with multiple levels and feedback.
# Copyright (c) 2024 Denis Joassin
# All rights reserved.

import random
from colorama import init, Fore, Style
import platform
import os
from time import sleep

from legacy.display_feedback import display_feedback
from get_random_options import get_random_options
from legacy.display_roman_intro import display_roman_intro
from legacy.player_management import select_player
from mastery_management import load_mastery_data, save_mastery_data, weighted_choice
from legacy.level_management import select_level

from models.language_model import LanguageManager
from score_manager import ScoreManager
from legacy.config_manager import config_manager

from legacy.load_vocabulary import Vocabulary

from colorama import init, Fore, Style

# Initialize colorama
init()


def play_quiz(
    player_name, level, vocabulary, lang_manager, mastery_data, total_questions=10
):
    """
    Conducts a Latin vocabulary quiz for the player.
    Args:
        player_name (str): The name of the player.
        level (int): The difficulty level of the quiz (1, 2, or 3).
        vocabulary (dict): A dictionary containing Latin words and their details.
        lang_manager (LanguageManager): The language manager for retrieving strings.
        mastery_data (dict): A dictionary containing user performance on each word.

    Returns:
        tuple: A tuple containing the final score and the total number of questions.
    """
    score = 0

    print(
        f"\n{Fore.CYAN}{lang_manager.get('core.welcome_message', 'Welcome')} {player_name}!"
    )
    print(lang_manager.get("core.quiz_intro", "Choose the correct translation."))
    print("-" * 50 + Style.RESET_ALL)

    vocab_items = list(vocabulary.items())
    used_words = set()
    available_words = set(vocabulary.keys())

    for question_num in range(total_questions):
        if len(available_words) == 0:
            available_words = set(vocabulary.keys())
            used_words.clear()

        # Select word based on level
        if level == 4:
            # Weighted selection based on mastery data
            word_id = weighted_choice(list(available_words), mastery_data)
        else:
            # Random choice for other levels
            word_id = random.choice(list(available_words))

        available_words.remove(word_id)
        used_words.add(word_id)
        word_data = vocabulary[word_id]

        # Get options for multiple choice, using word type for level 3
        if level == 3 or level == 4:
            options, options_id = get_random_options(
                word_data["translation"],
                word_id,
                vocabulary,
                word_data.get("word_type"),
            )

        else:
            options, options_id = get_random_options(
                word_data["translation"], word_id, vocabulary
            )

        # Display question
        print(
            f"\n{Fore.YELLOW}{lang_manager.get('core.question_label', 'Question')} {question_num + 1}/{total_questions}{Style.RESET_ALL}"
        )
        print(
            f"{lang_manager.get('core.latin_word', 'Latin word')}: {Fore.MAGENTA}{word_data['word']} ({word_data['form']}){Style.RESET_ALL}"
        )
        if level == 3:
            print(
                f"{lang_manager.get('core.word_type', 'Word type')}: {word_data.get('word_type', '')}{Style.RESET_ALL}"
            )
        else:
            print(Style.RESET_ALL, end="")

        # Display hint based on level
        if level == 1:
            print(f"{lang_manager.get('core.hint', 'Hint')}: {word_data['hint']}")

        if level == 0:
            print(f"{lang_manager.get('core.hint', 'Hint')}: {word_data['hint']}")
            for i, option_and_id in enumerate(zip(options, options_id), 1):
                translation = lang_manager.translations.get(
                    int(option_and_id[1]), "Unknown"
                )
                print(
                    f"{i}. {option_and_id[0]} - {Fore.CYAN}{translation}{Style.RESET_ALL}"
                )
        else:
            # Normal options display for other levels
            for i, option in enumerate(options, 1):
                print(f"{i}. {option}")

        # Get user answer
        while True:
            try:
                answer = int(
                    input(
                        f"\n{lang_manager.get('core.enter_answer', 'Enter your answer')} (1-4): "
                    )
                )
                if 1 <= answer <= 4:
                    break
                print(
                    lang_manager.get(
                        "core.enter_valid_number",
                        "Please enter a valid number between 1 and 4.",
                    )
                )
            except ValueError:
                print(
                    lang_manager.get(
                        "core.enter_valid_number",
                        "Please enter a valid number between 1 and 4.",
                    )
                )

        # Display hint after answering for levels 2 and 3
        if level in [2, 3, 4]:
            print(f"{lang_manager.get('core.hint', 'Hint')}: {word_data['hint']}")

        # Check answer and display feedback
        is_correct = options[answer - 1] == word_data["translation"]
        if is_correct:
            score += 1
        display_feedback(
            is_correct,
            word_data["translation"],
            word_data["hint"],
            score,
            question_num,
            lang_manager,
        )

        # Update mastery data
        word_id = str(word_id)
        mastery_data[word_id]["total_attempts"] += 1
        if is_correct:
            mastery_data[word_id]["correct_attempts"] += 1

        # Save mastery data
        save_mastery_data(player_name, mastery_data)

    # Final score with color
    percentage = (score / total_questions) * 100
    print(
        f"\n{Fore.CYAN}{lang_manager.get('core.quiz_completed', 'Quiz completed')} {player_name}!"
    )
    print(
        f"{lang_manager.get('core.final_score', 'Final score')}: {score}/{total_questions}"
    )
    print(
        f"{lang_manager.get('core.percentage', 'Percentage')}: {percentage:.1f}%{Style.RESET_ALL}"
    )

    if percentage == 100:
        print(
            f"{Fore.GREEN}{lang_manager.get('core.perfect_score', 'Perfect score! Excellent work!')}{Style.RESET_ALL}"
        )
    elif percentage >= 80:
        print(
            f"{Fore.GREEN}{lang_manager.get('core.great_job', 'Great job!')}{Style.RESET_ALL}"
        )
    elif percentage >= 60:
        print(
            f"{Fore.YELLOW}{lang_manager.get('core.good_effort', 'Good effort! Keep practicing!')}{Style.RESET_ALL}"
        )
    else:
        print(
            f"{Fore.RED}{lang_manager.get('core.keep_studying', 'Keep studying!')}{Style.RESET_ALL}"
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

    config = config_manager("config.yaml")
    language_file = config.get("language_file")
    total_questions = config.get("total_questions", 10)
    lang_manager = LanguageManager(language_file)
    vocab_manager = Vocabulary(lang_manager=lang_manager)

    # Displays the introduction to the game.
    display_roman_intro()
    score_manager = ScoreManager()
    # Load mastery data

    while True:

        # Prompts the player to enter their name.
        player_name = select_player(lang_manager)

        # Load player vocabulary mastery data
        mastery_data = load_mastery_data(player_name)

        # Displays the player's statistics.
        score_manager.display_player_stats(player_name, lang_manager)

        # Loads the vocabulary for the quiz
        vocabulary, vocab_files = vocab_manager.load_vocabulary()

        # Prompts the player to select a difficulty level.
        level = select_level(lang_manager)

        # play_quizz
        score, total_questions = play_quiz(
            player_name, level, vocabulary, lang_manager, mastery_data, total_questions
        )
        percentage = (score / total_questions) * 100

        # Update score with vocabulary information
        score_manager.update_score(player_name, vocab_files, level, percentage)

        # Displays the player's statistics.
        print(
            f"\n{Fore.CYAN}{lang_manager.get('core.updated_statistics').format(player=player_name)}:{Style.RESET_ALL}"
        )
        score_manager.display_player_stats(player_name, lang_manager)

        # Ask the player if they want to play again
        play_again = input(
            f"\n{Fore.CYAN}{lang_manager.get('core.play_again_prompt')} {Style.RESET_ALL}"
        ).lower()
        if play_again not in ["yes", "y", "Y", "o", "O", "oui", "j", "J", "ja"]:
            print(
                f"{Fore.GREEN}{lang_manager.get('core.thanks_for_playing')}{Style.RESET_ALL}"
            )
            break


if __name__ == "__main__":

    main()
