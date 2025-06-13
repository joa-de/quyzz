# Description: A Latin vocabulary quiz game with multiple levels and feedback.
# Copyright (c) 2024 Denis Joassin
# All rights reserved.

# MVC imports
from models.language_model import LanguageModel
from models.vocabulary_model import VocabularyModel
from models.player_model import PlayerModel
from models.mastery_model import MasteryModel
from models.score_model import ScoreModel

from views.cli_view import CLIView

from controllers.vocabulary_controller import VocabularyController
from controllers.config_controller import ConfigController
from controllers.player_controller import PlayerController
from controllers.score_controller import ScoreController
from controllers.game_controller import GameController


# Initialize colorama


def main():
    """
    Main function to run the Latin quiz game.
    This function displays the Roman introduction, initializes the score manager,
    and enters a loop where the player can select their name, load vocabulary,
    select a level, and play the quiz. After each quiz, the player's score is
    updated and displayed. The player is then asked if they want to play again.
    The loop continues until the player chooses not to play again.
    """

    config_controller = ConfigController()

    lang_model = LanguageModel(config_controller.get_language_file())
    vocabulary_model = VocabularyModel()
    player_model = PlayerModel()
    mastery_model = MasteryModel()
    score_model = ScoreModel()

    view = CLIView(lang_model)
    player_controller = PlayerController(player_model, mastery_model, view, lang_model)
    vocab_controller = VocabularyController(vocabulary_model, view, lang_model)
    score_controller = ScoreController(view, score_model)

    game = GameController(
        view,
        lang_model,
        config_controller,
        player_controller,
        vocab_controller,
        score_controller,
    )
    game.run()


if __name__ == "__main__":
    main()
    input("Press Enter to exit...")
