import random


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
    total_questions = 15  # You can adjust the number of questions

    print("\nWelcome to the Latin Vocabulary Quiz!")
    print("Choose the correct Dutch translation for the given Latin word.")
    print("-" * 50)

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
        print(f"\nQuestion {question_num + 1}/{total_questions}")
        print(f"Latin word: {word_data['word']} ({word_data['form']})")

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

        # Check answer
        if options[answer - 1] == word_data["translation"]:
            print("\nCorrect! ✓")
            print(f"Hint: {word_data['hint']}")
            score += 1
        else:
            print("\nIncorrect! ✗")
            print(f"The correct answer was: {word_data['translation']}")
            print(f"Hint: {word_data['hint']}")

        print(f"Current score: {score}/{question_num + 1}")
        print("-" * 50)

    # Final score
    print(f"\nQuiz completed! Final score: {score}/{total_questions}")
    percentage = (score / total_questions) * 100
    print(f"Percentage: {percentage:.1f}%")

    if percentage == 100:
        print("Perfect score! Excellent work!")
    elif percentage >= 80:
        print("Great job!")
    elif percentage >= 60:
        print("Good effort! Keep practicing!")
    else:
        print("Keep studying! You'll improve!")


if __name__ == "__main__":
    # Load vocabulary when the program starts
    vocabulary = load_vocabulary("vocabulary.txt")

    while True:
        play_quiz()
        play_again = input("\nWould you like to play again? (yes/no): ").lower()
        if play_again != "yes":
            print("Thanks for playing! Vale!")
            break
