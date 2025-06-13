from colorama import init, Fore, Style
from models.language_model import LanguageModel
from tabulate import tabulate


from views.base_view import BaseView


class CLIView(BaseView):

    def __init__(self, language_model: LanguageModel):
        super().__init__(language_model)
        init()

    @staticmethod
    def cli_view_warning(message: str):
        """Display a warning message in the CLI."""
        print(Fore.RED + Style.BRIGHT + message + Style.RESET_ALL)

    @staticmethod
    def display_message(message: str):
        """Display a message to the user."""
        print(f"{Fore.CYAN}{message}{Style.RESET_ALL}")

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

    def display_available_files(self, files, min_id, max_id):
        print(f"\n{self.language_model.get('vocabulary_management.available_lists')}")
        print(
            f"-1: {self.language_model.get('vocabulary_management.custom_range').format(min_id=min_id, max_id=max_id)}"
        )
        print(f"0: {self.language_model.get('vocabulary_management.all_chapters')}")
        for i, file in enumerate(files):
            print(f"{i + 1}: {file[:-4]}")

    def get_user_vocabulary_choice(self):
        try:
            return int(
                input(self.language_model.get("vocabulary_management.file_selection"))
            )
        except ValueError:
            print(self.language_model.get("vocabulary_management.enter_valid_number"))
            return None

    def get_custom_range(self, min_id, max_id):
        range_input = input(
            self.language_model.get("vocabulary_management.enter_range").format(
                min_id=min_id, max_id=max_id
            )
        )
        try:
            start, end = map(int, range_input.split("-"))
            if start < min_id or end > max_id:
                print(
                    self.language_model.get(
                        "vocabulary_management.invalid_range"
                    ).format(min_id=min_id, max_id=max_id)
                )
            elif start > end:
                print(
                    self.language_model.get("vocabulary_management.invalid_range_order")
                )
            else:
                return start, end
        except ValueError:
            print(self.language_model.get("vocabulary_management.invalid_range_format"))
        return None

    def display_question_header(self, question_num, total_questions):
        print(
            f"\n{Fore.YELLOW}{self.language_model.get('core.question_label', 'Question')} {question_num}/{total_questions}{Style.RESET_ALL}"
        )

    def display_welcome_message(self, player_name):
        print(
            f"\n{Fore.CYAN}{self.language_model.get('core.welcome_message', 'Welcome')} {player_name}!"
        )
        print(
            self.language_model.get(
                "core.quiz_intro", "Choose the correct translation."
            )
        )
        print("-" * 50 + Style.RESET_ALL)

    def display_latin_word(self, word_data):
        print(
            f"{self.language_model.get('core.latin_word', 'Latin word')}: {Fore.MAGENTA}{word_data['word']} ({word_data['form']}){Style.RESET_ALL}"
        )
        if "word_type" in word_data:
            print(
                f"{self.language_model.get('core.word_type', 'Word type')}: {word_data['word_type']}{Style.RESET_ALL}"
            )

    def display_hint(self, hint):
        print(f"{self.language_model.get('core.hint', 'Hint')}: {hint}")

    def display_options(self, options, options_id=None):
        if options_id:
            for i, (opt, opt_id) in enumerate(zip(options, options_id), 1):
                translation = self.language_model.translations.get(
                    int(opt_id), "Unknown"
                )
                print(f"{i}. {opt} - {Fore.CYAN}{translation}{Style.RESET_ALL}")
        else:
            for i, opt in enumerate(options, 1):
                print(f"{i}. {opt}")

    def ask_for_answer(self):
        while True:
            try:
                answer = int(
                    input(
                        f"\n{self.language_model.get('core.enter_answer', 'Enter your answer')} (1-4): "
                    )
                )
                if 1 <= answer <= 4:
                    return answer
            except ValueError:
                pass
            print(
                self.language_model.get(
                    "core.enter_valid_number",
                    "Please enter a valid number between 1 and 4.",
                )
            )

    def display_feedback(
        self,
        is_correct: bool,
        correct_answer: str,
        hint: str,
        current_score: int,
        question_num: int,
    ):
        """Display feedback with colors."""

        if is_correct:
            print(
                f"\n{Fore.GREEN}{self.language_model.get('feedback.correct')} ✓{Style.RESET_ALL}"
            )
        else:
            print(f"\n{Fore.RED}{self.language_model.get('feedback.incorrect')} ✗")
            print(
                f"{self.language_model.get('feedback.correct_answer_was')}: {correct_answer}{Style.RESET_ALL}"
            )

        print(f"{self.language_model.get('feedback.hint')}: {hint}")
        print(
            f"{self.language_model.get('feedback.current_score')}: {current_score}/{question_num + 1}"
        )
        print("-" * 50)

    def display_thanks(self):
        print(
            f"{Fore.GREEN}{self.language_model.get('core.thanks_for_playing')}{Style.RESET_ALL}"
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

    def display_player_stats(self, player_name, player_data, levels):
        if not player_data:
            print(
                f"{Fore.CYAN}{self.language_model.get('core.no_score_available', 'No score available')}{Style.RESET_ALL}"
            )
            return

        print(
            f"\n{Fore.CYAN}{self.language_model.get('core.statistics_for')} {player_name}:{Style.RESET_ALL}"
        )
        if player_data["last_played"]:
            print(
                f"{self.language_model.get('core.last_played')}: {player_data['last_played']}"
            )
        print()

        vocabularies = sorted(player_data["vocabularies"].keys())
        headers = (
            [self.language_model.get("core.level")]
            + vocabularies
            + [self.language_model.get("core.average")]
        )
        table_data = []
        vocabulary_totals = {vocab_id: 0 for vocab_id in vocabularies}
        vocabulary_counts = {vocab_id: 0 for vocab_id in vocabularies}

        for level in levels:
            row = [f"{self.language_model.get('core.level')} {level}"]
            level_total = 0
            level_count = 0

            for vocab_id in vocabularies:
                vocab_data = player_data["vocabularies"][vocab_id]
                if str(level) not in vocab_data["levels"]:
                    vocab_data["levels"][str(level)] = {"ema": 0.0, "games_played": 0}

                level_data = vocab_data["levels"][str(level)]
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
                elif ema == 0:
                    score_str = f"{Fore.RED}--{Style.RESET_ALL} ({played})"
                else:
                    score_str = f"{Fore.RED}{ema:.1f}%{Style.RESET_ALL} ({played})"

                row.append(score_str)

            table_data.append(row)

        avg_row = [self.language_model.get("core.average")]
        for vocab_id in vocabularies:
            count = vocabulary_counts[vocab_id] or 1  # avoid div by 0
            vocab_avg = vocabulary_totals[vocab_id] / count
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

    @staticmethod
    def display_menu(title: str, options: list[str]):
        """Display a menu with a title and options."""
        print(f"\n{Fore.CYAN}{title}{Style.RESET_ALL}")
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        print("-" * 50)

    def display_final_score(self, score, total_questions, player_name):
        percentage = (score / total_questions) * 100
        print(
            f"\n{Fore.CYAN}{self.language_model.get('core.quiz_completed', 'Quiz completed')} {player_name}!"
        )
        print(
            f"{self.language_model.get('core.final_score', 'Final score')}: {score}/{total_questions}"
        )
        print(
            f"{self.language_model.get('core.percentage', 'Percentage')}: {percentage:.1f}%{Style.RESET_ALL}"
        )

        if percentage == 100:
            print(
                f"{Fore.GREEN}{self.language_model.get('core.perfect_score', 'Perfect score! Excellent work!')}{Style.RESET_ALL}"
            )
        elif percentage >= 80:
            print(
                f"{Fore.GREEN}{self.language_model.get('core.great_job', 'Great job!')}{Style.RESET_ALL}"
            )
        elif percentage >= 60:
            print(
                f"{Fore.YELLOW}{self.language_model.get('core.good_effort', 'Good effort! Keep practicing!')}{Style.RESET_ALL}"
            )
        else:
            print(
                f"{Fore.RED}{self.language_model.get('core.keep_studying', 'Keep studying!')}{Style.RESET_ALL}"
            )

    def display_updated_statistics_message(self, player_name):
        print(
            f"\n{Fore.CYAN}{self.language_model.get('core.updated_statistics').format(player=player_name)}:{Style.RESET_ALL}"
        )

    def display_thanks_for_playing(self):
        print(
            f"{Fore.GREEN}{self.language_model.get('core.thanks_for_playing')}{Style.RESET_ALL}"
        )

    def input_player(self) -> str:
        """Prompt and return player name"""
        print(
            f"\n{Fore.CYAN}{self.language_model.get('core.welcome_message', 'Welcome to Latin Quiz!')}{Style.RESET_ALL}"
        )
        while True:
            player_name = input(
                self.language_model.get("core.enter_name", "Enter your name: ")
            ).strip()
            if player_name:
                return player_name
            print(
                self.language_model.get(
                    "core.invalid_name", "Please enter a valid name."
                )
            )

    def select_level(self):
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

        print(f"\n{self.language_model.get('level_management.select_level_prompt')}")

        if self.language_model.language != "dutch":
            print(f"0. {self.language_model.get('level_management.level_0_name')}")
            levels = [0, 1, 2, 3, 4]
        else:
            levels = [1, 2, 3, 4]

        print(f"1. {self.language_model.get('level_management.level_1_name')}")
        print(f"2. {self.language_model.get('level_management.level_2_name')}")
        print(f"3. {self.language_model.get('level_management.level_3_name')}")
        print(f"4. {self.language_model.get('level_management.level_4_name')}")

        while True:
            try:
                level = int(
                    input(
                        self.language_model.get("level_management.enter_level_number")
                    )
                )
                if level in levels:
                    print(
                        self.language_model.get(
                            "level_management.selected_level"
                        ).format(level=level)
                    )
                    return level
                print(self.language_model.get("level_management.invalid_level_number"))
            except ValueError:
                print(self.language_model.get("level_management.invalid_input"))

    def ask_play_again(self) -> bool:
        """Ask if player wants to play again"""
        play_again = input(
            f"\n{Fore.CYAN}{self.language_model.get('core.play_again_prompt')} {Style.RESET_ALL}"
        ).lower()
        return play_again in ["yes", "y", "Y", "o", "O", "oui", "j", "J", "ja"]

    @staticmethod
    def get_text_input(prompt: str) -> str:
        """Get a text input from the user."""
        return input(f"{prompt}: ").strip()

    @staticmethod
    def get_numeric_input(prompt: str, min_value: int, max_value: int) -> int:
        """Get a numeric input from the user within a specified range."""
        while True:
            try:
                choice = int(input(f"{prompt} ({min_value}-{max_value}): "))
                if min_value <= choice <= max_value:
                    return choice
                print(f"Please enter a number between {min_value} and {max_value}.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")
