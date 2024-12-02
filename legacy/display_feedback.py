# This file contains the display_feedback function which displays feedback to the user after each question.
# Denis Joassin 2024

from colorama import Fore, Style
from models.language_manager import LanguageManager


def display_feedback(
    is_correct, correct_answer, hint, current_score, question_num, lang: LanguageManager
):
    """Display feedback with colors."""

    if is_correct:
        # play_sound(True)
        print(f"\n{Fore.GREEN}{lang.get('feedback.correct')} ✓{Style.RESET_ALL}")
    else:
        # play_sound(False)
        print(f"\n{Fore.RED}{lang.get('feedback.incorrect')} ✗")
        print(
            f"{lang.get('feedback.correct_answer_was')}: {correct_answer}{Style.RESET_ALL}"
        )

    print(f"{lang.get('feedback.hint')}: {hint}")
    print(f"{lang.get('feedback.current_score')}: {current_score}/{question_num + 1}")
    print("-" * 50)
