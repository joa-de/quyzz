from colorama import Fore, Style
from models.language_model import LanguageManager
from tabulate import tabulate
from colorama import Fore, Style


class CLIView:
    @staticmethod
    def display_available_files(files, min_id, max_id, lang_manager):
        print(f"\n{lang_manager.get('vocabulary_management.available_lists')}")
        print(
            f"-1: {lang_manager.get('vocabulary_management.custom_range').format(min_id=min_id, max_id=max_id)}"
        )
        print(f"0: {lang_manager.get('vocabulary_management.all_chapters')}")
        for i, file in enumerate(files):
            print(f"{i + 1}: {file[:-4]}")

    @staticmethod
    def get_user_vocabulary_choice(lang_manager):
        try:
            return int(input(lang_manager.get("vocabulary_management.file_selection")))
        except ValueError:
            print(lang_manager.get("vocabulary_management.enter_valid_number"))
            return None

    @staticmethod
    def get_custom_range(min_id, max_id, lang_manager):
        range_input = input(
            lang_manager.get("vocabulary_management.enter_range").format(
                min_id=min_id, max_id=max_id
            )
        )
        try:
            start, end = map(int, range_input.split("-"))
            if start < min_id or end > max_id:
                print(
                    lang_manager.get("vocabulary_management.invalid_range").format(
                        min_id=min_id, max_id=max_id
                    )
                )
            elif start > end:
                print(lang_manager.get("vocabulary_management.invalid_range_order"))
            else:
                return start, end
        except ValueError:
            print(lang_manager.get("vocabulary_management.invalid_range_format"))
        return None

    @staticmethod
    def display_roman_intro():
        GREEN = Fore.GREEN
        RESET = Style.RESET_ALL
        YELLOW = Fore.YELLOW + Style.BRIGHT
        roman_intro = rf"""
-:::::::::::::-:-::::::::::::::::::::::-::::::::::::-:::::::::::::::::::::::::::::::::::::::::::::::
=:::---::-:-:::::---::::::-------::--:--::-:-::::::--:::::::::::::::::::::::::::::::::::::::::::::::
=::::::::::::{YELLOW}   _         _   _____  ___  _   _    ___   _   _  ___  _____ _____ {RESET}:::::::::::::::::::
=::::::::::::{YELLOW}  | |       / \ |_   _||_ _|| \ | |  / _ \ | | | ||_ _||__  /|__  /{RESET} :::::::::::::::::::
=::::::::::::{YELLOW}  | |      / _ \  | |   | | |  \| | | | | || | | | | |   / /   / / {RESET} :::::::::::::::::::
=::::::::::::{YELLOW}  | |___  / ___ \ | |   | | | |\  | | |_| || |_| | | |  / /_  / /_ {RESET} :::::::::::::::::::
=::::::::::::{YELLOW}  |_____|/_/   \_\|_|  |___||_| \_|  \__\_\ \___/ |___|/____|/____|{RESET} :::::::::::::::::::
=::::::::::::{YELLOW}                                                                   {RESET} :::::::::::::::::::
=:::::::::-:::--:::--::::::::-:-:{GREEN}*{RESET}:.::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
=::::::::::::-::::::::::::-:{GREEN}+####-{RESET}::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
=:::::::::::-----::::::::{GREEN}+########{RESET}::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
=::::::::::::::-:-:-{GREEN}*-:+###########-{RESET}:............::::::::::::::::::::::::::::::::..::.::::::::::::::
=:::::::::::::-{GREEN}+##==*###############{RESET}:::..............::::::::::::::::::::::::::.:-::..::::::::::::::
=:::::::::::::::{GREEN}=##################{RESET}.::{GREEN}+*+{RESET}............:::::::::::::::::::......:-::::.:::::::::::::::
=::::::::::::::-:--{GREEN}################-+####={RESET}......{GREEN}:####{RESET}::::::::::::::::::.--:::...::-:::::::::::::::::
=::::::::::::::::::{GREEN}+##########################+.-{GREEN}####{RESET}:::::::::::::::::.--:::-:.-::::--:--:::::::::::
=:::::::::::::::::--{GREEN}#################################{RESET}::::::::::::::::.:---:::::-::::::::::-:-:::::::
=::::-:-:-:-:-::::-{GREEN}*###########.:#########--*##########={RESET}::.:::::::::::-::::::::::::::::-:::--{GREEN}#-{RESET}:::::
=:::-{GREEN}#######=:-::--{GREEN}############*:#########:-:-+#############={RESET}:::::::::--:-::::::----:-::-{GREEN}+###*{RESET}::::::
=:::-{GREEN}######################*#####*+{RESET}:-:{GREEN}+####{RESET}-:-:{GREEN}=############+{RESET}.......:-:-:::-:{GREEN}+##############-{RESET}:::::::
=:-:-{GREEN}#####################{RESET}:-:-:-::::---{GREEN}#####*{RESET}:-:---{GREEN}+#########{RESET}.........:-:---{GREEN}##############-{RESET}:::::::::
=-::{GREEN}*#####################{RESET}-::::::--{GREEN}=#{RESET}----{GREEN}*####={RESET}::---::{GREEN}=########+{RESET}.....:{GREEN}--=#################+{RESET}:::::::::
=::{GREEN}*#################*={RESET}-::-::::::::-{GREEN}+{RESET}:--::-{GREEN}*#####={RESET}::::{GREEN}-########=={RESET}:--{GREEN}**#####################*{RESET}-:::::::
=-{GREEN}##################{RESET}--::::::-::::-{GREEN}-##*{RESET}-:::-:--{GREEN}+###*#*{RESET}-:{GREEN}*#####-{RESET}=---:{GREEN}=+#####################={RESET}:::::::::
=::{GREEN}################:{RESET}-:::{GREEN}**{RESET}:--::::-:{GREEN}*#={RESET}:::-:::----{GREEN}#{RESET}:-:::-{GREEN}=#####+{RESET}---:--{GREEN}+#################+###*{RESET}::::.:::
=:{GREEN}*###############*{RESET}-::-::-:-:::::--{GREEN}*={RESET}::::::::::::{GREEN}+*{RESET}-:-:::{GREEN}-+####++{RESET}::-:-{GREEN}+#############{RESET}---{GREEN}=#####+{RESET}--::::
=:::::-{GREEN}*########**{RESET}:::-::::::-::--:---::-:-::--:-{GREEN}+*{RESET}::::::::{GREEN}=####={RESET}--:::--{GREEN}+*#-{RESET}..::::=:-:-:{GREEN}:#######*{RESET}::::
=::::--{GREEN}*+:{RESET}::---:-::---:::--::-----:-::--:::{GREEN}=###*{RESET}--::::::::-:{GREEN}**#:{RESET}------{GREEN}:-#-:{RESET}--::---{GREEN}+#+{RESET}::{GREEN}-+#####-{RESET}:::::
=::-:{GREEN}-+#{RESET}---::-:::::{GREEN}+########*#########**{RESET}:::-:--=::::::::::::::--------:-:::::::::::::::-{GREEN}*###{RESET}::::::::
=:::{GREEN}-*{RESET}-......:::..........::-{GREEN}+#########{RESET}::---::=:-:-::::::::::::-{GREEN}==+*={RESET}-:--:::::::::::::::{GREEN}####{RESET}::::::::
=::::::...........:::::::::::{GREEN}+##########{RESET}-::-::::::::::::::::::::::::::::::::::::::::::::{GREEN}###*{RESET}::::::::
-::::::::::::::::::::::::::::{GREEN}#########+{RESET}--:::::::::::::::::::::::::::::::::::::::::::::::{GREEN}###{RESET}:::::::::
-::::::::::::::::::::::::::::::::::{GREEN}=##**{RESET}-::--:::::-:::::::-::---::::::::::::-:::-{GREEN}+*=-**###-{RESET}:::::::::
-:::::::::::::::::::::::::::::::::::::{GREEN}####==+={RESET}-::-::::::::-{GREEN}*#####***+:{RESET}----::::{GREEN}+########{RESET}:::::::::::::
-:::::::::::::::::::::::::::::::::::::::{GREEN}==+######{RESET}::--::::-{GREEN}*##########################-{RESET}::::::::::::::
-:::::::::::::::::::::::::::::::::::::::::::::{GREEN}#*##*+={RESET}::--:{GREEN}-###########################={RESET}:::-:::::::::
-::::::::::::::::::::::::::::::::::::::::::::::.{GREEN}-#######**#####+{RESET}.::::::::::::.:{GREEN}+########=-v{RESET}::-::::::
-::::::::::::::::::::::::::::::::::::::::::::::::::::::={GREEN}++{RESET}::::::::::::::::::::::{GREEN}-#########-{RESET}:::--::::     
"""
        print(roman_intro)
        print("\n")
        print("QUYZZ Copyright (C) 2024 Denis Joassin")
        print("\n")

    @staticmethod
    def select_player(lang_manager) -> str:
        """Prompt and return player name"""
        print(
            f"\n{Fore.CYAN}{lang_manager.get('core.welcome_message', 'Welcome to Latin Quiz!')}{Style.RESET_ALL}"
        )
        while True:
            player_name = input(
                lang_manager.get("core.enter_name", "Enter your name: ")
            ).strip()
            if player_name:
                return player_name
            print(lang_manager.get("core.invalid_name", "Please enter a valid name."))

    @staticmethod
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

        if lang_manager.language != "dutch":
            print(f"0. {lang_manager.get('level_management.level_0_name')}")
            levels = [0, 1, 2, 3, 4]
        else:
            levels = [1, 2, 3, 4]

        print(f"1. {lang_manager.get('level_management.level_1_name')}")
        print(f"2. {lang_manager.get('level_management.level_2_name')}")
        print(f"3. {lang_manager.get('level_management.level_3_name')}")
        print(f"4. {lang_manager.get('level_management.level_4_name')}")

        while True:
            try:
                level = int(
                    input(lang_manager.get("level_management.enter_level_number"))
                )
                if level in levels:
                    print(
                        lang_manager.get("level_management.selected_level").format(
                            level=level
                        )
                    )
                    return level
                print(lang_manager.get("level_management.invalid_level_number"))
            except ValueError:
                print(lang_manager.get("level_management.invalid_input"))

    @staticmethod
    def display_feedback(
        is_correct: bool,
        correct_answer: str,
        hint: str,
        current_score: int,
        question_num: int,
        lang: LanguageManager,
    ):
        """Display feedback with colors."""

        if is_correct:
            print(f"\n{Fore.GREEN}{lang.get('feedback.correct')} ✓{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.RED}{lang.get('feedback.incorrect')} ✗")
            print(
                f"{lang.get('feedback.correct_answer_was')}: {correct_answer}{Style.RESET_ALL}"
            )

        print(f"{lang.get('feedback.hint')}: {hint}")
        print(
            f"{lang.get('feedback.current_score')}: {current_score}/{question_num + 1}"
        )
        print("-" * 50)

    @staticmethod
    def play_again(lang_manager: LanguageManager) -> bool:
        """Ask if player wants to play again"""
        play_again = input(
            f"\n{Fore.CYAN}{lang_manager.get('core.play_again_prompt')} {Style.RESET_ALL}"
        ).lower()
        return play_again in ["yes", "y", "Y", "o", "O", "oui", "j", "J", "ja"]

    @staticmethod
    def display_thanks(lang_manager: LanguageManager):
        print(
            f"{Fore.GREEN}{lang_manager.get('core.thanks_for_playing')}{Style.RESET_ALL}"
        )

    @staticmethod
    def display_question(
        question_num: int, word_data: dict, options: list[str], level: int
    ) -> int:
        """Display a quiz question and get user's answer"""
        print(f"\n{Fore.YELLOW}Question {question_num}/10{Style.RESET_ALL}")
        print(
            f"Latin word: {Fore.MAGENTA}{word_data['word']} ({word_data['form']}){Style.RESET_ALL}"
        )

        if level == 3:
            print(f"Word type: {word_data.get('word_type', '')}")

        # Display options
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")

        # Get user answer
        while True:
            try:
                answer = int(input("\nEnter your answer (1-4): "))
                if 1 <= answer <= 4:
                    return answer
                print("Please enter a valid number between 1 and 4.")
            except ValueError:
                print("Please enter a valid number between 1 and 4.")

    @staticmethod
    def display_player_stats(
        self,
        player_name,
        player_data,
        players_with_scores,
        player_levels,
        lang_manager: LanguageManager,
    ):
        """Display player's statistics in a formatted table with levels as rows, vocabularies as columns, and averages."""

        if player_name not in players_with_scores:
            print(
                f"{Fore.CYAN}{lang_manager.get('score.no_score_available', 'No score avalaible')}{Style.RESET_ALL}"
            )
            return

        print(
            f"\n{Fore.CYAN}{lang_manager.get('score.statistics_for')} {player_name}:{Style.RESET_ALL}"
        )
        if player_data["last_played"]:
            print(
                f"{lang_manager.get('score.last_played')}: {player_data['last_played']}"
            )
        print()

        # Prepare table headers
        vocabularies = sorted(player_data["vocabularies"].keys())
        headers = (
            [lang_manager.get("score.level")]
            + vocabularies
            + [lang_manager.get("score.average")]
        )
        table_data = []

        # Collect totals for calculating averages
        vocabulary_totals = {vocab_id: 0 for vocab_id in vocabularies}
        vocabulary_counts = {vocab_id: 0 for vocab_id in vocabularies}

        for level in player_levels[player_name]:
            row = [f"{lang_manager.get('score.level')} {level}"]
            level_total = 0
            level_count = 0

            for vocab_id in vocabularies:
                vocab_data = player_data["vocabularies"][vocab_id]
                # self.ensure_level_scores(vocab_data, level)
                level_data = vocab_data["levels"][level]
                ema = level_data["ema"]
                played = level_data["games_played"]

                level_total += ema
                level_count += 1
                vocabulary_totals[vocab_id] += ema
                if ema > 0:
                    vocabulary_counts[vocab_id] += 1

                if ema >= 80:
                    score_str = f"{Fore.GREEN}{ema:.1f}%{Style.RESET_ALL} ({played})"
                elif ema >= 60:
                    score_str = f"{Fore.YELLOW}{ema:.1f}%{Style.RESET_ALL} ({played})"

                if ema == 0:
                    score_str = f"{Fore.WHIAT}--{Style.RESET_ALL} ({played})"
                else:
                    score_str = f"{Fore.RED}{ema:.1f}%{Style.RESET_ALL} ({played})"

                row.append(score_str)

            table_data.append(row)

        avg_row = [lang_manager.get("score.average")]
        for vocab_id in vocabularies:

            vocab_avg = vocabulary_totals[vocab_id] / vocabulary_counts[vocab_id]
            avg_color = (
                f"{Fore.GREEN}{vocab_avg:.1f}%{Style.RESET_ALL}"
                if vocab_avg >= 80
                else (
                    f"{Fore.YELLOW}{vocab_avg:.1f}%{Style.RESET_ALL}"
                    if vocab_avg >= 60
                    else f"{Fore.RED}{vocab_avg:.1f}%{Style.RESET_ALL}"
                )
            )
            avg_row.append(avg_color)

        table_data.append(avg_row)

        print(tabulate(table_data, headers=headers, tablefmt="grid", stralign="center"))
