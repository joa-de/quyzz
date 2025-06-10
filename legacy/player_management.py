import json
import os
from pathlib import Path
from models.language_model import LanguageModel

# Path to the JSON file
USER_DATA_PATH = Path("./user_data")
PLAYER_FILE = "players.json"


def load_players():
    """Load players from a JSON file."""
    if not os.path.exists(USER_DATA_PATH):
        os.makedirs(USER_DATA_PATH)
    if not os.path.exists(USER_DATA_PATH / PLAYER_FILE):
        # Create a file with default players if it doesn't exist
        save_players(["Zélie"])
    with open(USER_DATA_PATH / PLAYER_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_players(players):
    """Save players to a JSON file."""
    with open(USER_DATA_PATH / PLAYER_FILE, "w", encoding="utf-8") as file:
        json.dump(players, file, indent=4, ensure_ascii=False)


def get_and_display_players_selection(lang_manager: LanguageModel):
    """Display player selection menu and return the list of players."""
    players = load_players()
    print(lang_manager.get("player_management.select_player"))
    for i, player in enumerate(players, 1):
        print(f"{i}. {player}")
    print(f"{len(players) + 1}. {lang_manager.get('player_management.add_new_player')}")
    return players


def select_player(lang_manager: LanguageModel):
    """Handle player selection and creation."""
    players = get_and_display_players_selection(lang_manager)

    while True:
        try:
            choice = int(input(lang_manager.get("player_management.enter_choice")))
            if 1 <= choice <= len(players):
                selected_player = players[choice - 1]
                print(
                    lang_manager.get("player_management.selected_player").format(
                        player=selected_player
                    )
                )
                return selected_player
            elif choice == len(players) + 1:
                new_player = input(
                    lang_manager.get("player_management.enter_player_name")
                ).strip()
                if new_player:
                    players.append(new_player)
                    save_players(players)
                    print(
                        lang_manager.get("player_management.player_added").format(
                            player=new_player
                        )
                    )
                    players = get_and_display_players_selection(lang_manager)
                else:
                    print(lang_manager.get("player_management.empty_name_error"))
            else:
                print(lang_manager.get("player_management.invalid_option"))
        except ValueError:
            print(lang_manager.get("player_management.invalid_number"))
