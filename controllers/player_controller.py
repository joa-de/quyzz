from models.player_model import PlayerModel
from views.cli_view import CLIView
from models.language_model import LanguageModel


class PlayerController:
    """Controller for managing player interactions."""

    def __init__(self, model: PlayerModel, view: CLIView, lang_manager: LanguageModel):
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
        self.current_player = None

    def select_player(self) -> str:
        """
        Interactive player selection process.

        Returns:
            Selected player name
        """
        players = self._model.get_players()

        while self.current_player is None:
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
                self.current_player = selected_player

            if choice == len(players) + 1:

                # Add new player
                new_player = self._view.get_text_input(
                    prompt=self._lang.get("player_management.enter_player_name")
                )

                self.current_player = self._model.add_player(new_player)

                if self.current_player is not None:
                    self._view.display_message(
                        self._lang.get("player_management.player_added").format(
                            player=self.current_player
                        )
                    )

            else:
                self._view.display_message(
                    self._lang.get("player_management.empty_name_error")
                )

    def get_current_player(self) -> str:
        """
        Get the currently selected player.

        Returns:
            Name of the current player
        """
        return self.current_player if hasattr(self, "current_player") else None
