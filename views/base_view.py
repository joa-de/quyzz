# views/base_view.py

from abc import ABC, abstractmethod
from models.language_model import LanguageModel


class BaseView(ABC):
    @abstractmethod
    def __init__(self, language_model: LanguageModel):
        self.language_model = language_model

    def set_language_model(self, language_model: LanguageModel):
        """Set the language model for the view."""
        self.language_model = language_model

    @abstractmethod
    def cli_view_warning(self, message: str):
        """Display a warning message in the CLI view."""
        pass

    @abstractmethod
    def display_roman_intro():
        pass

    @abstractmethod
    def display_question_header(self, question_num: int, total_questions: int):
        pass

    @abstractmethod
    def display_welcome_message(self, player_name: str):
        pass

    @abstractmethod
    def display_latin_word(self, word_data: dict):
        pass

    @abstractmethod
    def display_hint(self, hint: str):
        pass

    @abstractmethod
    def display_options(self, options: list, options_id: list = None):
        pass

    @abstractmethod
    def ask_for_answer(self) -> int:
        pass

    @abstractmethod
    def display_feedback(
        self,
        is_correct: bool,
        correct_answer: str,
        hint: str,
        score: int,
        question_num: int,
    ):
        pass

    @abstractmethod
    def display_final_score(self, score: int, total_questions: int, player_name: str):
        pass

    @abstractmethod
    def display_thanks(self):
        pass

    @abstractmethod
    def display_question(
        question_num: int, word_data: dict, options: list[str], level: int
    ):
        pass

    @abstractmethod
    def display_player_stats(self, player_name, player_data, levels):
        pass

    @abstractmethod
    def display_updated_statistics_message(self, player_name: str):
        pass

    @abstractmethod
    def display_menu(title: str, options: list[str]):
        pass

    @abstractmethod
    def display_message(message: str):
        pass

    @abstractmethod
    def display_final_score(self, score, total_questions, player_name):
        pass

    @abstractmethod
    def display_thanks_for_playing(self):
        pass

    @abstractmethod
    def input_player(self) -> str:
        pass

    @abstractmethod
    def select_level(self) -> int:
        pass

    @abstractmethod
    def ask_play_again(self) -> bool:
        pass

    @abstractmethod
    def get_text_input(prompt: str) -> str:
        pass

    @abstractmethod
    def get_numeric_input(prompt: str, min_value: int, max_value: int) -> int:
        pass

    @abstractmethod
    def display_available_files(self, files, min_id, max_id):
        """Display a list of available files."""
        pass

    @abstractmethod
    def get_user_vocabulary_choice(self) -> int:
        """Get the user's choice of vocabulary file."""
        pass
