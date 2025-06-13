# controllers/game_controller.py

from colorama import Fore, Style
from legacy.level_management import select_level
from legacy.get_random_options import get_random_options

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
        # TODO move lang_model use to view
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

    def run(self):
        """Main game loop."""
        self.view.display_roman_intro()

        while True:
            self.player_controller.select_player()
            player_name = self.player_controller.get_current_player()

            self.score_controller.show_player_statistics(player_name)

            vocabulary, vocab_files = self.vocab_controller.load_vocabulary()
            level = select_level(self.lang_model)

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

        #####TODO: Move this to the view
        print(
            f"\n{Fore.CYAN}{self.lang_model.get('core.welcome_message', 'Welcome')} {player_name}!"
        )
        print(self.lang_model.get("core.quiz_intro", "Choose the correct translation."))
        print("-" * 50 + Style.RESET_ALL)
        #####

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
