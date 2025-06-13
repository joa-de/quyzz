from models.player_model import PlayerModel
from models.mastery_model import MasteryModel
from views.cli_view import BaseView
from models.language_model import LanguageModel
from models.score_model import ScoreModel


class PlayerController:
    """Controller for managing player interactions."""

    def __init__(
        self,
        model: PlayerModel,
        mastery_model: MasteryModel,
        view: BaseView,
        lang_manager: LanguageModel,
    ):
        """
        Initialize PlayerController.

        Args:
            model (PlayerModel): Player data model
            view (CLIView): Command-line interface view
            lang_manager (LanguageManager): Language translation manager
        """
        self.player_model = model
        self._mastery_model = mastery_model
        self._view = view
        self._lang = lang_manager
        self.current_player = None
        self.mastery_data = None

    def select_player(self) -> str:
        """
        Interactive player selection process.

        Returns:
            Selected player name
        """
        players = self.player_model.get_players()

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
                selected_player = self.player_model.select_player(choice)
                self._view.display_message(
                    self._lang.get("player_management.selected_player").format(
                        player=selected_player
                    )
                )
                self.current_player = selected_player
                self.mastery_data = self.load_mastery_data()

            elif choice == len(players) + 1:

                # Add new player
                new_player = self._view.get_text_input(
                    prompt=self._lang.get("player_management.enter_player_name")
                )

                self.current_player = self.player_model.add_player(new_player)
                self.mastery_data = self.load_mastery_data()

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

    def load_mastery_data(self) -> dict:
        """
        Load mastery data for the current player.

        Returns:
            Mastery data dictionary
        """
        if self.current_player is None:
            raise ValueError("No player selected. Please select a player first.")

        self.mastery_data = self._mastery_model.load_mastery_data(self.current_player)

    def get_mastery_data(self) -> dict:
        """
        Get the mastery data for the current player.

        Returns:
            dict: Mastery data for the current player.
        """
        if self.current_player is None:
            raise ValueError("No player selected. Please select a player first.")

        if self.mastery_data is None:
            self.load_mastery_data()

        return self.mastery_data

    def update_mastery_data(self, word_id, is_correct):

        if self.mastery_data is None:
            self.load_mastery_data()

        word_id = str(word_id)
        self.mastery_data[word_id]["total_attempts"] += 1
        if is_correct:
            self.mastery_data[word_id]["correct_attempts"] += 1

    def save_mastery_data(self):
        """
        Save the mastery data for the given user.

        Args:
            user_name (str): Name of the user.
            mastery_data (dict): Mastery data to save.
        """
        if self.current_player is None:
            raise ValueError("No player selected. Please select a player first.")

        if self.mastery_data is None:
            self.load_mastery_data()

        self._mastery_model.save_mastery_data(self.current_player, self.mastery_data)
        self._view.display_message(
            self._lang.get("player_management.mastery_data_saved").format(
                user=self.current_player
            )
        )

    def unplayed_first_choice(self, available_words):
        """
        Select the first unplayed word from the available words.

        Args:
            available_words (list): List of available words.
            mastery_data (dict): Mastery data for the current player.

        Returns:
            str: The first unplayed word ID.
        """

        if self.mastery_data is None:
            self.load_mastery_data()

        return self._mastery_model.unplayed_first_choice(
            available_words, self.mastery_data
        )

    def weighted_choice(self, available_words):
        """
        Select a word ID based on mastery data with weighting.

        Args:
            available_words (set): Set of available word IDs.
            mastery_data (dict): User performance data.

        Returns:
            str: Selected word ID.
        """

        if self.mastery_data is None:
            self.load_mastery_data()

        return self._mastery_model.weighted_choice(available_words, self.mastery_data)
