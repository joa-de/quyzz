# Description: A Latin vocabulary quiz game with multiple levels and feedback.
# Copyright (c) 2024 Denis Joassin
# All rights reserved.

# MVC imports: Importing models, views, and controllers for the application
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


def main():
    """
    Entry point for the Latijn Game application.
    This function initializes all necessary controllers, models, and views required for the game.
    It sets up configuration management, language and vocabulary models, player and score tracking,
    and the command-line interface for user interaction. After all dependencies are initialized,
    it starts the main game loop by invoking the GameController.
    Steps performed:
        1. Initialize configuration controller for managing settings and config files.
        2. Set up models for language, vocabulary, player, mastery, and score.
        3. Initialize the CLI view for user interaction.
        4. Create controllers for player, vocabulary, and score management.
        5. Instantiate the main GameController with all dependencies.
        6. Start the game loop.
    """

    # Initialize configuration controller to manage config files and settings
    config_controller = ConfigController()

    # Initialize models for language, vocabulary, player, mastery, and score
    lang_model = LanguageModel(config_controller.get_language_file())
    vocabulary_model = VocabularyModel()
    player_model = PlayerModel()
    mastery_model = MasteryModel()
    score_model = ScoreModel()

    # Initialize the CLI view with the language model for user interaction
    view = CLIView(lang_model)

    # Initialize controllers for player, vocabulary, and score management
    player_controller = PlayerController(player_model, mastery_model, view, lang_model)
    vocab_controller = VocabularyController(vocabulary_model, view, lang_model)
    score_controller = ScoreController(view, score_model)

    # Initialize the main game controller with all dependencies
    game = GameController(
        view,
        lang_model,
        config_controller,
        player_controller,
        vocab_controller,
        score_controller,
    )
    # Start the game loop
    game.run()


if __name__ == "__main__":
    # Entry point: run the main function if this script is executed directly
    main()
