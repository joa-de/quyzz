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
