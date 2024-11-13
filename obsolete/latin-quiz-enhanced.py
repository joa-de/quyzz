import random
from colorama import init, Fore, Style
import platform
import os
from time import sleep

# Initialize colorama
init()


# Determine the operating system and set up sound playing function
def play_sound(is_correct):
    system = platform.system()

    if system == "Windows":
        import winsound

        if is_correct:
            frequency = 1000  # Hz
            duration = 500  # milliseconds
            winsound.Beep(frequency, duration)
        else:
            frequency = 400  # Hz
            duration = 400  # milliseconds
            winsound.Beep(frequency, duration)

    elif system == "Darwin":
        if is_correct:
            os.system("afplay /System/Library/Sounds/Glass.aiff &")
        else:
            os.system("afplay /System/Library/Sounds/Basso.aiff &")

    else:  # Linux or other systems
        if is_correct:
            print("\a")  # Bell sound
        else:
            print("\a")
        sleep(0.3)  # Add a small delay to make the sound noticeable


def load_vocabulary(filename):
    """Load vocabulary from a file."""
    vocabulary = {}
    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                if line.strip():  # Skip empty lines
                    # Split line by | and remove any whitespace
                    parts = [part.strip() for part in line.split("|")]
                    if len(parts) >= 5:  # Ensure all parts are present
                        word_id = int(parts[0])
                        vocabulary[word_id] = {
                            "word": parts[1],
                            "form": parts[2],
                            "translation": parts[3],
                            "hint": parts[4],
                        }
    except FileNotFoundError:
        print(f"Error: Could not find {filename}")
        exit(1)
    except Exception as e:
        print(f"Error loading vocabulary: {e}")
        exit(1)
    return vocabulary


def get_random_options(correct_answer, all_translations):
    """Generate 3 random wrong options plus the correct answer."""
    options = [correct_answer]
    possible_answers = [
        d["translation"]
        for d in vocabulary.values()
        if d["translation"] != correct_answer
    ]
    options.extend(random.sample(possible_answers, 3))
    random.shuffle(options)
    return options


def play_quiz():
    score = 0
    total_questions = 10  # You can adjust the number of questions

    print(f"\n{Fore.CYAN}Welcome to the Latin Vocabulary Quiz!")
    print("Choose the correct Dutch translation for the given Latin word.")
    print("-" * 50 + Style.RESET_ALL)

    # Convert dictionary items to list for random sampling
    vocab_items = list(vocabulary.items())

    # Keep track of used words to avoid repetition
    used_words = set()
    available_words = set(vocabulary.keys())

    for question_num in range(total_questions):
        # If we've used all words, reset the used_words set
        if len(available_words) == 0:
            available_words = set(vocabulary.keys())
            used_words.clear()

        # Select a random word that hasn't been used yet
        word_id = random.choice(list(available_words))
        available_words.remove(word_id)
        used_words.add(word_id)
        word_data = vocabulary[word_id]

        # Get options for multiple choice
        options = get_random_options(word_data["translation"], vocabulary)

        # Display question
        print(f"\n{Fore.YELLOW}Question {question_num + 1}/{total_questions}")
        print(f"Latin word: {word_data['word']} ({word_data['form']}){Style.RESET_ALL}")

        # Display options
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")

        # Get user answer
        while True:
            try:
                answer = int(input("\nEnter your answer (1-4): "))
                if 1 <= answer <= 4:
                    break
                print("Please enter a number between 1 and 4.")
            except ValueError:
                print("Please enter a valid number.")

        # Check answer and display feedback
        is_correct = options[answer - 1] == word_data["translation"]
        if is_correct:
            score += 1
        display_feedback(
            is_correct, word_data["translation"], word_data["hint"], score, question_num
        )

    # Final score with color
    percentage = (score / total_questions) * 100
    print(f"\n{Fore.CYAN}Quiz completed!")
    print(f"Final score: {score}/{total_questions}")
    print(f"Percentage: {percentage:.1f}%{Style.RESET_ALL}")

    if percentage == 100:
        print(f"{Fore.GREEN}Perfect score! Excellent work!{Style.RESET_ALL}")
    elif percentage >= 80:
        print(f"{Fore.GREEN}Great job!{Style.RESET_ALL}")
    elif percentage >= 60:
        print(f"{Fore.YELLOW}Good effort! Keep practicing!{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Keep studying! You'll improve!{Style.RESET_ALL}")


if __name__ == "__main__":
    # Load vocabulary when the program starts
    vocabulary = load_vocabulary("vocabulary.txt")

    while True:
        play_quiz()
        play_again = input(
            f"\n{Fore.CYAN}Would you like to play again? (yes/no): {Style.RESET_ALL}"
        ).lower()
        if play_again not in ["yes", "y", "Y"]:
            print(f"{Fore.GREEN}Thanks for playing! Vale!{Style.RESET_ALL}")
            break
