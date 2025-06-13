# controllers/game_controller.py
import random

from views.base_view import BaseView
from controllers.vocabulary_controller import VocabularyController
from controllers.config_controller import ConfigController
from controllers.player_controller import PlayerController
from controllers.score_controller import ScoreController
from models.language_model import LanguageModel


class GameController:
    def __init__(
        self,
        view: BaseView,
        lang_model: LanguageModel,
        config_controller: ConfigController,
        player_controller: PlayerController,
        vocab_controller: VocabularyController,
        score_controller: ScoreController,
    ):
        # Initialize the GameController with all required controllers and view
        self.view = view
        self.lang_model = lang_model
        self.config_controller = config_controller
        self.player_controller = player_controller
        self.vocab_controller = vocab_controller
        self.score_controller = score_controller

    @staticmethod
    def get_random_options(
        correct_answer, correct_answer_id, vocabulary, word_type=None
    ):
        """
        Generate a randomized list of multiple-choice options for a vocabulary quiz.

        Args:
            correct_answer (str): The correct translation to be included among the options.
            correct_answer_id (Any): The identifier for the correct answer in the vocabulary.
            vocabulary (dict): The complete vocabulary dictionary, mapping IDs to word data.
            word_type (str, optional): If provided, ensures distractors are of the same word type.

        Returns:
            tuple: A tuple containing two lists:
            - options (list of str): The randomized answer choices, including the correct answer.
            - options_id (list): The corresponding IDs for each option.
        """
        options = [correct_answer]  # Start with the correct answer
        options_id = [correct_answer_id]
        vocab_items = list(vocabulary.items())

        if word_type:
            # Filter vocabulary items to only include words of the same type
            same_type_items = [
                item
                for item in vocab_items
                if item[1]["word_type"] == word_type
                and item[1]["translation"] != correct_answer
            ]

            # If not enough words of the same type, fall back to random words
            if len(same_type_items) < 3:
                different_items = [
                    item
                    for item in vocab_items
                    if item[1]["translation"] != correct_answer
                ]
                while len(options) < 4:
                    random_item = random.choice(different_items)
                    if random_item[1]["translation"] not in options:
                        options.append(random_item[1]["translation"])
                        options_id.append(random_item[0])
            else:
                # Add three random words of the same type
                while len(options) < 4:
                    random_item = random.choice(same_type_items)
                    if random_item[1]["translation"] not in options:
                        options.append(random_item[1]["translation"])
                        options_id.append(random_item[0])
        else:
            # Original behavior for levels 1 and 2: just pick random distractors
            different_items = [
                item for item in vocab_items if item[1]["translation"] != correct_answer
            ]
            while len(options) < 4:
                random_item = random.choice(different_items)
                if random_item[1]["translation"] not in options:
                    options.append(random_item[1]["translation"])
                    options_id.append(random_item[0])

        # Shuffle the options and their IDs together
        combined = list(zip(options, options_id))
        random.shuffle(combined)
        options, options_id = map(list, zip(*combined))

        return options, options_id

    def run(self):
        """
        Main game loop.
        Executes the main game loop for the Latin vocabulary quiz game.
        This method manages the overall game flow, including:
            - Displaying the introductory message.
            - Allowing the user to select or switch players.
            - Showing current player statistics.
            - Loading vocabulary and available vocabulary files.
            - Prompting the user to select a difficulty level.
            - Running the quiz for the selected level and vocabulary.
            - Calculating and updating the player's score and statistics.
            - Displaying updated statistics and feedback messages.
            - Asking the user if they wish to play another round.
            - Exiting the loop and displaying a farewell message if the user chooses not to continue.
        The loop continues until the player opts not to play again.
        """

        self.view.display_roman_intro()  # Show intro message

        while True:
            self.player_controller.select_player()  # Select or switch player
            player_name = self.player_controller.get_current_player()

            self.score_controller.show_player_statistics(player_name)  # Show stats

            vocabulary, vocab_files = (
                self.vocab_controller.load_vocabulary()
            )  # Load vocab
            level = self.view.select_level()  # Choose difficulty

            # Run the quiz and get score
            score, total_questions = self.play_quiz(
                level,
                vocabulary,
                total_questions=self.config_controller.get_total_questions(),
            )
            percentage = (score / total_questions) * 100 if total_questions != 0 else 0

            # Update player score and stats
            self.score_controller.update_player_score(
                player_name, vocab_files, level, percentage
            )

            self.view.display_updated_statistics_message(player_name)

            self.score_controller.show_player_statistics(player_name)

            # Ask if the user wants to play again
            if not self.view.ask_play_again():
                self.view.display_thanks_for_playing()
                break

    def play_quiz(self, level, vocabulary, total_questions=10):
        """Run the quiz for the given level and vocabulary."""
        score = 0
        player_name = self.player_controller.get_current_player()
        self.view.display_welcome_message(player_name)

        used_words = set()
        available_words = set(vocabulary.keys())

        for question_num in range(total_questions):
            # Reset available words if all have been used
            if not available_words:
                available_words = set(vocabulary.keys())
                used_words.clear()

            # Choose a word ID based on level
            if level == 4:
                word_id = self.player_controller.weighted_choice(list(available_words))
            else:
                word_id = self.player_controller.unplayed_first_choice(
                    list(available_words)
                )

            available_words.remove(word_id)
            used_words.add(word_id)
            word_data = vocabulary[word_id]

            # Generate options for the question
            if level in [3, 4]:
                options, options_id = self.get_random_options(
                    word_data["translation"],
                    word_id,
                    vocabulary,
                    word_data.get("word_type"),
                )
            else:
                options, options_id = self.get_random_options(
                    word_data["translation"], word_id, vocabulary
                )

            self.view.display_question_header(question_num + 1, total_questions)
            self.view.display_latin_word(word_data)

            # Show hint for easier levels
            if level in [0, 1]:
                self.view.display_hint(word_data["hint"])

            self.view.display_options(options, options_id if level == 0 else None)

            answer = self.view.ask_for_answer()

            # Show hint after answering for harder levels
            if level in [2, 3, 4]:
                self.view.display_hint(word_data["hint"])

            # Check if the answer is correct
            if 1 <= answer <= len(options):
                is_correct = options[answer - 1] == word_data["translation"]
            else:
                is_correct = False  # Treat invalid input as incorrect

            if is_correct:
                score += 1

            # Show feedback for the answer
            self.view.display_feedback(
                is_correct,
                word_data["translation"],
                word_data["hint"],
                score,
                question_num,
            )

            # Update mastery data for the player
            self.player_controller.update_mastery_data(word_id, is_correct)
            self.player_controller.save_mastery_data()

        # Final feedback after the quiz
        self.view.display_final_score(score, total_questions, player_name)
        return score, total_questions
