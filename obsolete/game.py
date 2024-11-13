import random

# Dictionary to store the vocabulary
vocabulary = {
    189: {
        "word": "capillus",
        "form": "capilli",
        "translation": "het haar",
        "hint": "caput, capillaire",
    },
    190: {
        "word": "porta",
        "form": "portae",
        "translation": "de poort",
        "hint": "Fr. la porte, portaal",
    },
    191: {
        "word": "provincia",
        "form": "provinciae",
        "translation": "de provincie",
        "hint": "Fr. province",
    },
    192: {
        "word": "terra",
        "form": "terrae",
        "translation": "de aarde; het land",
        "hint": "Fr. la terre, terres",
    },
    193: {
        "word": "fōns",
        "form": "font-is, m.",
        "translation": "de bron",
        "hint": "Ndl. fontein",
    },
    194: {
        "word": "pēs",
        "form": "ped-is, m.",
        "translation": "de voet",
        "hint": "Ndl. de pedicure, Fr. le pied, Pes",
    },
    195: {
        "word": "vigilāre",
        "form": "vigilō",
        "translation": "waken",
        "hint": "vigilant",
    },
    196: {
        "word": "terrēre",
        "form": "terreō",
        "translation": "bang maken",
        "hint": "Ndl. de terreur, terrorist",
    },
    197: {
        "word": "timēre",
        "form": "timeō",
        "translation": "vrezen; bang zijn",
        "hint": "Lat. timidus",
    },
    # ... add more words as needed
}


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
    total_questions = 5  # You can adjust the number of questions

    print("\nWelcome to the Latin Vocabulary Quiz!")
    print("Choose the correct Dutch translation for the given Latin word.")
    print("-" * 50)

    # Convert dictionary items to list for random sampling
    vocab_items = list(vocabulary.items())

    for question_num in range(total_questions):
        # Select a random word
        word_id, word_data = random.choice(vocab_items)

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
    while True:
        play_quiz()
        play_again = input("\nWould you like to play again? (yes/no): ").lower()
        if play_again != "yes":
            print("Thanks for playing! Vale!")
            break
