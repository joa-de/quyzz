# Description: A Latin vocabulary quiz game with multiple levels and feedback.
# Copyright (c) 2024 Denis Joassin
# All rights reserved.

from colorama import init, Fore, Style

# Legacy imports
from legacy.get_random_options import get_random_options
from legacy.level_management import select_level

# MVC imports
from models.language_model import LanguageModel
from models.vocabulary_model import VocabularyModel
from models.player_model import PlayerModel
from models.mastery_model import MasteryModel
from models.score_model import ScoreModel

from views.cli_view import CLIView

from controllers.vocabulary_controller import VocabularyController
from controllers.config_controller import ConfigController
from controllers.player_controller import PlayerController
from controllers.score_controller import ScoreController


# Initialize colorama
init()


def play_quiz(
    view: CLIView,
    level,
    vocabulary,
    lang_model: LanguageModel,
    player_controller: PlayerController,
    total_questions=10,
):
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

    player_name = player_controller.get_current_player()

    print(
        f"\n{Fore.CYAN}{lang_model.get('core.welcome_message', 'Welcome')} {player_name}!"
    )
    print(lang_model.get("core.quiz_intro", "Choose the correct translation."))
    print("-" * 50 + Style.RESET_ALL)

    used_words = set()
    available_words = set(vocabulary.keys())

    for question_num in range(total_questions):
        if len(available_words) == 0:
            available_words = set(vocabulary.keys())
            used_words.clear()

        # Select word based on level
        if level == 4:
            # Weighted selection based on mastery data
            word_id = player_controller.weighted_choice(list(available_words))
        else:
            # Random choice for other levels
            word_id = player_controller.unplayed_first_choice(list(available_words))

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
            f"\n{Fore.YELLOW}{lang_model.get('core.question_label', 'Question')} {question_num + 1}/{total_questions}{Style.RESET_ALL}"
        )
        print(
            f"{lang_model.get('core.latin_word', 'Latin word')}: {Fore.MAGENTA}{word_data['word']} ({word_data['form']}){Style.RESET_ALL}"
        )
        if level == 3:
            print(
                f"{lang_model.get('core.word_type', 'Word type')}: {word_data.get('word_type', '')}{Style.RESET_ALL}"
            )
        else:
            print(Style.RESET_ALL, end="")

        # Display hint based on level
        if level == 1:
            print(f"{lang_model.get('core.hint', 'Hint')}: {word_data['hint']}")

        if level == 0:
            print(f"{lang_model.get('core.hint', 'Hint')}: {word_data['hint']}")
            for i, option_and_id in enumerate(zip(options, options_id), 1):
                translation = lang_model.translations.get(
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
                        f"\n{lang_model.get('core.enter_answer', 'Enter your answer')} (1-4): "
                    )
                )
                if 1 <= answer <= 4:
                    break
                print(
                    lang_model.get(
                        "core.enter_valid_number",
                        "Please enter a valid number between 1 and 4.",
                    )
                )
            except ValueError:
                print(
                    lang_model.get(
                        "core.enter_valid_number",
                        "Please enter a valid number between 1 and 4.",
                    )
                )

        # Display hint after answering for levels 2 and 3
        if level in [2, 3, 4]:
            print(f"{lang_model.get('core.hint', 'Hint')}: {word_data['hint']}")

        # Check answer and display feedback
        is_correct = options[answer - 1] == word_data["translation"]
        if is_correct:
            score += 1
        view.display_feedback(
            is_correct,
            word_data["translation"],
            word_data["hint"],
            score,
            question_num,
            lang_model,
        )

        player_controller.update_mastery_data(word_id, is_correct)
        player_controller.save_mastery_data()

    # Final score with color
    percentage = (score / total_questions) * 100
    print(
        f"\n{Fore.CYAN}{lang_model.get('core.quiz_completed', 'Quiz completed')} {player_name}!"
    )
    print(
        f"{lang_model.get('core.final_score', 'Final score')}: {score}/{total_questions}"
    )
    print(
        f"{lang_model.get('core.percentage', 'Percentage')}: {percentage:.1f}%{Style.RESET_ALL}"
    )

    if percentage == 100:
        print(
            f"{Fore.GREEN}{lang_model.get('core.perfect_score', 'Perfect score! Excellent work!')}{Style.RESET_ALL}"
        )
    elif percentage >= 80:
        print(
            f"{Fore.GREEN}{lang_model.get('core.great_job', 'Great job!')}{Style.RESET_ALL}"
        )
    elif percentage >= 60:
        print(
            f"{Fore.YELLOW}{lang_model.get('core.good_effort', 'Good effort! Keep practicing!')}{Style.RESET_ALL}"
        )
    else:
        print(
            f"{Fore.RED}{lang_model.get('core.keep_studying', 'Keep studying!')}{Style.RESET_ALL}"
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

    view = CLIView()

    config_controller = ConfigController()

    lang_model = LanguageModel(config_controller.get_language_file())
    vocabulary_model = VocabularyModel()
    player_model = PlayerModel()
    mastery_model = MasteryModel()

    player_controller = PlayerController(player_model, mastery_model, view, lang_model)
    vocab_controller = VocabularyController(vocabulary_model, view, lang_model)

    score_model = ScoreModel()
    score_controller = ScoreController(view, score_model)

    # Displays the introduction to the game.
    view.display_roman_intro()

    while True:

        # Prompts the player to enter their name.
        player_controller.select_player()

        # Displays the player's statistics.
        score_controller.show_player_statistics(
            player_controller.get_current_player(), lang_model
        )

        # Loads the vocabulary for the quiz
        vocabulary, vocab_files = vocab_controller.load_vocabulary()

        # Prompts the player to select a difficulty level.
        level = select_level(lang_model)

        # play_quizz
        score, total_questions = play_quiz(
            view,
            level,
            vocabulary,
            lang_model,
            player_controller,
            total_questions=config_controller.get_total_questions(),
        )
        percentage = (score / total_questions) * 100

        # Update score with vocabulary information
        score_controller.update_player_score(
            player_controller.get_current_player(), vocab_files, level, percentage
        )

        # Displays the player's statistics.
        print(
            f"\n{Fore.CYAN}{lang_model.get('core.updated_statistics').format(player=player_controller.get_current_player())}:{Style.RESET_ALL}"
        )
        score_controller.show_player_statistics(
            player_controller.get_current_player(), lang_model
        )

        # Ask the player if they want to play again
        play_again = input(
            f"\n{Fore.CYAN}{lang_model.get('core.play_again_prompt')} {Style.RESET_ALL}"
        ).lower()
        if play_again not in ["yes", "y", "Y", "o", "O", "oui", "j", "J", "ja"]:
            print(
                f"{Fore.GREEN}{lang_model.get('core.thanks_for_playing')}{Style.RESET_ALL}"
            )
            break


if __name__ == "__main__":

    main()
