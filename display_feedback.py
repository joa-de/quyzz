# This file contains the display_feedback function which displays feedback to the user after each question.
# Denis Joassin 2024


from colorama import Fore, Style


def display_feedback(is_correct, correct_answer, hint, current_score, question_num):
    """Display feedback with colors and play sound."""
    if is_correct:
        # play_sound(True)
        print(f"\n{Fore.GREEN}Correct! ✓{Style.RESET_ALL}")
    else:
        # play_sound(False)
        print(f"\n{Fore.RED}Incorrect! ✗")
        print(f"The correct answer was: {correct_answer}{Style.RESET_ALL}")

    print(f"Hint: {hint}")
    print(f"Current score: {current_score}/{question_num + 1}")
    print("-" * 50)
