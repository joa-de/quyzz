import json
import os

# Path to the JSON file
PLAYER_FILE = "players.json"


def load_players():
    """Load players from a JSON file."""
    if not os.path.exists(PLAYER_FILE):
        # Create a file with default players if it doesn't exist
        save_players(["Zélie"])
    with open(PLAYER_FILE, "r") as file:
        return json.load(file)


def save_players(players):
    """Save players to a JSON file."""
    with open(PLAYER_FILE, "w") as file:
        json.dump(players, file, indent=4)


def get_and_display_players_selection():

    players = load_players()
    print("Select a player:")
    for i, player in enumerate(players, 1):
        print(f"{i}. {player}")
    print(f"{len(players) + 1}. Add a new player")
    return players


def select_player():

    players = get_and_display_players_selection()

    while True:
        try:
            choice = int(input("Enter your choice: "))
            if 1 <= choice <= len(players):
                selected_player = players[choice - 1]
                print(f"Selected player: {selected_player}\n")
                return selected_player
            elif choice == len(players) + 1:
                new_player = input("Enter the new player's name: ").strip()
                if new_player:
                    players.append(new_player)
                    save_players(players)
                    print(f"Player {new_player} added successfully!")
                    players = get_and_display_players_selection()
                else:
                    print("Player name cannot be empty.")
            else:
                print("Please select a valid option.")
        except ValueError:
            print("Please enter a valid number.")
