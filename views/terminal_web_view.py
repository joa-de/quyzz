# views/terminal_web_view.py

from views.base_view import BaseView
from flask import session


class TerminalWebView(BaseView):
    def __init__(self, lang_model):
        self.lang_model = lang_model

    def _write(self, text):
        history = session.get("history", [])
        history.append(text)
        session["history"] = history

    def display_roman_intro(self):
        self._write("👑 Welcome to the Latin Vocabulary Quiz! 👑")
        self._write("-" * 50)

    def display_question_header(self, question_num, total_questions):
        self._write(f"Question {question_num}/{total_questions}")

    def display_welcome_message(self, player_name):
        self._write(
            f"{self.lang_model.get('core.welcome_message', 'Welcome')} {player_name}!"
        )
        self._write(
            self.lang_model.get("core.quiz_intro", "Choose the correct translation.")
        )

    def display_latin_word(self, word_data):
        self._write(f"Latin word: {word_data['word']} ({word_data['form']})")
        if "word_type" in word_data:
            self._write(f"Type: {word_data['word_type']}")

    def display_hint(self, hint):
        self._write(f"Hint: {hint}")

    def display_options(self, options, options_id=None):
        for i, opt in enumerate(options, 1):
            self._write(f"{i}. {opt}")

    def ask_for_answer(self):
        try:
            return int(session.pop("user_input", "1"))
        except ValueError:
            return 1  # fallback default

    def display_feedback(self, is_correct, correct_answer, hint, score, question_num):
        if is_correct:
            self._write("✅ Correct!")
        else:
            self._write(f"❌ Incorrect. Correct answer: {correct_answer}")
        self._write(f"Hint: {hint}")
        self._write(f"Score: {score}/{question_num + 1}")

    def display_final_score(self, score, total_questions, player_name):
        percentage = (score / total_questions) * 100
        self._write(f"\nQuiz completed, {player_name}!")
        self._write(f"Final score: {score}/{total_questions}")
        self._write(f"Percentage: {percentage:.1f}%")

    def select_level(self):
        return 1  # you could route to a level selection screen later

    def display_updated_statistics_message(self, player_name):
        self._write(f"Updated statistics for {player_name}:")

    def ask_play_again(self):
        return False  # you could support this later

    def display_thanks_for_playing(self):
        self._write("Thanks for playing!")

    def get_history(self):
        return session.get("history", [])

    def clear_history(self):
        session["history"] = []

    # unused methods for now, but could be useful later
    def cli_view_warning(self, *args, **kwargs):
        pass

    def display_menu(self, *args, **kwargs):
        pass

    def display_message(self, *args, **kwargs):
        pass

    def display_player_stats(self, *args, **kwargs):
        pass

    def display_question(self, *args, **kwargs):
        pass

    def display_thanks(self, *args, **kwargs):
        pass

    def get_numeric_input(self, *args, **kwargs):
        return 0

    def get_text_input(self, *args, **kwargs):
        return "placeholder"

    def input_player(self, *args, **kwargs):
        return "anonymous"

    def display_available_files(self, *args, **kwargs):
        pass

    def get_user_vocabulary_choice(self):
        return 1
