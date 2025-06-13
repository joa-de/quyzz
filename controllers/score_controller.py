# controller/score_controller.py

from models.score_model import ScoreModel
from views.base_view import BaseView


class ScoreController:
    def __init__(self, view: BaseView, score_model: ScoreModel = None):
        self.score_model = score_model or ScoreModel()
        self.view = view

    def show_player_statistics(self, player_name):
        player_data, levels = self.score_model.get_display_data(player_name)

        self.view.display_player_stats(player_name, player_data, levels)

    def update_player_score(
        self, player_name, vocab_files, level, new_score, period=None
    ):
        """
        Update the player's score in the score model.

        Args:
            player_name (str): Name of the player.
            score (int): Score achieved by the player.
            total_questions (int): Total number of questions in the quiz.
            level (str): Level of the quiz.
        """
        self.score_model.update_score(
            player_name, vocab_files, level, new_score, period=period
        )
