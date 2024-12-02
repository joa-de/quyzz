from models.player_model import PlayerModel
from views.cli_view import CLIView
from models.language_model import LanguageManager


class PlayerController:
    """Controller for managing player interactions."""

    def __init__(
        self, model: PlayerModel, view: CLIView, lang_manager: LanguageManager
    ):
        """
        Initialize PlayerController.

        Args:
            model (PlayerModel): Player data model
            view (CLIView): Command-line interface view
            lang_manager (LanguageManager): Language translation manager
        """
        self._model = model
        self._view = view
        self._lang = lang_manager

    def select_player(self) -> str:
        """
        Interactive player selection process.

        Returns:
            Selected player name
        """
        players = self._model.get_players()

        while True:
            # Display players
            self._view.display_menu(
                title=self._lang.get("player_management.select_player"),
                options=players + [self._lang.get("player_management.add_new_player")],
            )

            # Get user choice
            choice = self._view.get_numeric_input(
                prompt=self._lang.get("player_management.enter_choice"),
                min_value=1,
                max_value=len(players) + 1,
            )

            # Handle selection
            if choice <= len(players):
                selected_player = self._model.select_player(choice)
                self._view.display_message(
                    self._lang.get("player_management.selected_player").format(
                        player=selected_player
                    )
                )
                return selected_player

            # Add new player
            new_player = self._view.get_text_input(
                prompt=self._lang.get("player_management.enter_player_name")
            )

            added_player = self._model.add_player(new_player)
            if added_player:
                self._view.display_message(
                    self._lang.get("player_management.player_added").format(
                        player=added_player
                    )
                )
            else:
                self._view.display_message(
                    self._lang.get("player_management.empty_name_error")
                )
