# controllers/game_controller.py
import random
from colorama import Fore, Style

from views.cli_view import CLIView
from controllers.vocabulary_controller import VocabularyController
from controllers.config_controller import ConfigController
from controllers.player_controller import PlayerController
from controllers.score_controller import ScoreController
from models.language_model import LanguageModel


class GameController:
    def __init__(
        self,
        view: CLIView,
        lang_model: LanguageModel,
        config_controller: ConfigController,
        player_controller: PlayerController,
        vocab_controller: VocabularyController,
        score_controller: ScoreController,
    ):
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
        Get random options for multiple choice, with support for word type matching.

        Args:
            correct_answer: The correct translation
            vocabulary: The complete vocabulary dictionary
            word_type: The type of word to match (for level 3)
        """
        options = [correct_answer]
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

            # If we don't have enough words of the same type, fall back to random words
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
            # Original behavior for levels 1 and 2
            different_items = [
                item for item in vocab_items if item[1]["translation"] != correct_answer
            ]
            while len(options) < 4:
                random_item = random.choice(different_items)
                if random_item[1]["translation"] not in options:
                    options.append(random_item[1]["translation"])
                    options_id.append(random_item[0])

        # Shuffle the options
        combined = list(zip(options, options_id))
        random.shuffle(combined)
        options, options_id = zip(*combined)

        return options, options_id

    def run(self):
        """Main game loop."""
        self.view.display_roman_intro()

        while True:
            self.player_controller.select_player()
            player_name = self.player_controller.get_current_player()

            self.score_controller.show_player_statistics(player_name)

            vocabulary, vocab_files = self.vocab_controller.load_vocabulary()
            level = self.view.select_level()

            score, total_questions = self.play_quiz(
                level,
                vocabulary,
                total_questions=self.config_controller.get_total_questions(),
            )
            percentage = (score / total_questions) * 100

            self.score_controller.update_player_score(
                player_name, vocab_files, level, percentage
            )

            self.view.display_updated_statistics_message(player_name)

            self.score_controller.show_player_statistics(player_name)

            if not self.view.ask_play_again():
                self.view.display_thanks_for_playing()
                break

    def play_quiz(self, level, vocabulary, total_questions=10):
        """Refactored play_quiz logic inside GameController."""
        score = 0
        player_name = self.player_controller.get_current_player()

        self.view.display_welcome_message(player_name)

        used_words = set()
        available_words = set(vocabulary.keys())

        for question_num in range(total_questions):
            if not available_words:
                available_words = set(vocabulary.keys())
                used_words.clear()

            if level == 4:
                word_id = self.player_controller.weighted_choice(list(available_words))
            else:
                word_id = self.player_controller.unplayed_first_choice(
                    list(available_words)
                )

            available_words.remove(word_id)
            used_words.add(word_id)
            word_data = vocabulary[word_id]

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

            if level == 1 or level == 0:
                print(
                    f"{self.lang_model.get('core.hint', 'Hint')}: {word_data['hint']}"
                )

            if level == 0:
                for i, (opt, opt_id) in enumerate(zip(options, options_id), 1):
                    translation = self.lang_model.translations.get(
                        int(opt_id), "Unknown"
                    )
                    print(f"{i}. {opt} - {Fore.CYAN}{translation}{Style.RESET_ALL}")
            else:
                for i, opt in enumerate(options, 1):
                    print(f"{i}. {opt}")

            # Get user input
            while True:
                try:
                    answer = int(
                        input(
                            f"\n{self.lang_model.get('core.enter_answer', 'Enter your answer')} (1-4): "
                        )
                    )
                    if 1 <= answer <= 4:
                        break
                except ValueError:
                    pass
                print(
                    self.lang_model.get(
                        "core.enter_valid_number",
                        "Please enter a valid number between 1 and 4.",
                    )
                )

            if level in [2, 3, 4]:
                print(
                    f"{self.lang_model.get('core.hint', 'Hint')}: {word_data['hint']}"
                )

            is_correct = options[answer - 1] == word_data["translation"]
            if is_correct:
                score += 1

            self.view.display_feedback(
                is_correct,
                word_data["translation"],
                word_data["hint"],
                score,
                question_num,
            )

            self.player_controller.update_mastery_data(word_id, is_correct)
            self.player_controller.save_mastery_data()

        # Final feedback
        self.view.display_final_score(score, total_questions, player_name)
        return score, total_questions
