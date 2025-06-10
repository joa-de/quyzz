#!/usr/bin/env python3
"""
Main entry point for the Latin Quiz application.
This script initializes and starts the game.
"""

import sys
import os

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from views.cli_view import CLIView

from controllers.game_controller import GameController
from controllers.vocabulary_controller import VocabularyController

from models.language_model import LanguageModel
from models.vocabulary_model import VocabularyModel
from legacy.score_manager import ScoreManager
from legacy.config_manager import config_manager

from utilities.logging_util import logger


def main():
    """
    Initialize and start the Latin Quiz game.

    This function sets up all necessary components and starts the game loop.
    """
    try:
        # Load configuration
        config = config_manager("config.yaml")

        # Initialize language manager
        lang_manager = LanguageModel(config.get("language_file"))

        # Create view
        view = CLIView(lang_manager)

        # Initialize models and controllers
        vocabulary_model = VocabularyModel()
        vocabulary_controller = VocabularyController(
            vocabulary_model, view, lang_manager
        )
        score_manager = ScoreManager()

        # Create game controller
        game_controller = GameController(
            view, lang_manager, vocabulary_controller, score_manager, config
        )

        # Log game start
        logger.info("Latin Quiz Application Started")

        # Run the game
        game_controller.run_game_loop()

        # Log game exit
        logger.info("Latin Quiz Application Exited")

    except Exception as e:
        # Log any unexpected errors
        logger.critical(f"Unhandled exception in main: {e}", exc_info=True)
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
