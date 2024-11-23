from language_manager import LanguageManager


def select_level(lang_manager: LanguageManager):
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

    # note : update to use the language manager
    """

    print(f"\n{lang_manager.get('level_management.select_level_prompt')}")
    print(f"1. {lang_manager.get('level_management.level_1_name')}")
    print(f"2. {lang_manager.get('level_management.level_2_name')}")
    print(f"3. {lang_manager.get('level_management.level_3_name')}")
    print(f"4. {lang_manager.get('level_management.level_4_name')}")

    while True:
        try:
            level = int(input(lang_manager.get("level_management.enter_level_number")))
            if level in [1, 2, 3, 4]:
                print(
                    lang_manager.get("level_management.selected_level").format(
                        level=level
                    )
                )
                return level
            print(lang_manager.get("level_management.invalid_level_number"))
        except ValueError:
            print(lang_manager.get("level_management.invalid_input"))
