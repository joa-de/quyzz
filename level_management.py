def select_level():
    """
    Prompts the user to select a difficulty level for the quiz.

    Levels:
    1. Level 1 (hint displayed before answering)
    2. Level 2 (hint displayed after answering)
    3. Level 3 (options of the same word type, hint after answering)
    4. Level 4 (options of the same word type, word prioritized by user mastery)
    5. Level 5 (options of the same word type, word and options by user mastery) - not implemented

    Returns:
        int: The selected level (1, 2, 3, 4 or 5).
    """

    print("\nSelect a level:")
    print("1. Level 1 GALLEY SLAVE")
    print("2. Level 2 LEGIONARY")
    print("3. Level 3 CENTURION")
    print("4. Level 4 SENATOR")

    while True:
        try:
            level = int(input("Enter the level number (1, 2, 3, or 4): "))
            if level in [1, 2, 3, 4]:
                print(f"Selected level: {level}\n")
                return level
            print("Please enter 1, 2, 3, or 4.")
        except ValueError:
            print("Please enter a valid number.")
