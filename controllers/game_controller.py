import random
from typing import Dict, Tuple

from models.vocabulary import Vocabulary
from views.cli_view import CLIView
from controllers.vocabulary_controller import VocabularyController
from language_manager import LanguageManager
from mastery_management import load_mastery_data, save_mastery_data, weighted_choice
from score_manager import ScoreManager
from config_manager import config_manager
from logging_util import logger  # Import the logger we just created

class GameController:
    def __init__(
        self, 
        view: CLIView, 
        lang_manager: LanguageManager, 
        vocabulary_controller: VocabularyController,
        score_manager: ScoreManager,
        config: config_manager
    ):
        self.view = view
        self.lang_manager = lang_manager
        self.vocabulary_controller = vocabulary_controller
        self.score_manager = score_manager
        self.config = config
        
        # Game configuration
        self.total_questions = config.get('total_questions', 10)
        
        logger.info("GameController initialized")

    def play_quiz(self, player_name: str, level: int) -> Tuple[int, int]:
        """
        Conduct the Latin vocabulary quiz for the player.
        
        Args:
            player_name (str): Name of the player
            level (int): Difficulty level of the quiz
        
        Returns:
            Tuple of (score, total_questions)
        """
        try:
            logger.info(f"Starting quiz for {player_name} at level {level}")
            
            # Load vocabulary and mastery data
            vocabulary, vocab_files = self.vocabulary_controller.load_vocabulary()
            mastery_data = load_mastery_data(player_name)
            
            score = 0
            used_words = set()
            available_words = set(vocabulary.keys())

            for question_num in range(self.total_questions):
                # Word selection logic (similar to original implementation)
                word_id = self._select_word(level, available_words, mastery_data)
                available_words.remove(word_id)
                used_words.add(word_id)
                
                word_data = vocabulary[word_id]
                
                # Get multiple choice options
                options = self._get_quiz_options(level, word_data, vocabulary)
                
                # Display question and get user answer
                user_answer = self.view.display_question(
                    question_num + 1, 
                    word_data, 
                    options, 
                    level
                )
                
                # Check answer
                is_correct = options[user_answer - 1] == word_data["translation"]
                if is_correct:
                    score += 1
                
                # Display feedback
                self.view.display_feedback(
                    is_correct, 
                    word_data["translation"], 
                    word_data["hint"], 
                    score, 
                    question_num
                )
                
                # Update mastery data
                self._update_mastery_data(str(word_id), is_correct, mastery_data, player_name)
            
            # Calculate and log final score
            percentage = (score / self.total_questions) * 100
            logger.info(f"{player_name} completed quiz with score: {score}/{self.total_questions} ({percentage:.1f}%)")
            
            return score, self.total_questions

        except Exception as e:
            logger.error(f"Error in play_quiz: {e}", exc_info=True)
            raise

    def _select_word(self, level: int, available_words: set, mastery_data: Dict):
        """Select a word based on the difficulty level."""
        if level == 4:
            return weighted_choice(list(available_words), mastery_data)
        return random.choice(list(available_words))

    def _get_quiz_options(self, level: int, word_data: Dict, vocabulary: Dict):
        """Generate multiple choice options based on level."""
        # Implement option generation logic here
        # Similar to original get_random_options function
        pass

    def _update_mastery_data(self, word_id: str, is_correct: bool, mastery_data: Dict, player_name: str):
        """Update mastery data for a specific word."""
        mastery_data[word_id]["total_attempts"] += 1
        if is_correct:
            mastery_data[word_id]["correct_attempts"] += 1
        
        save_mastery_data(player_name, mastery_data)

    def run_game_loop(self):
        """Main game loop managing multiple quiz rounds."""
        while True:
            try:
                # Player selection
                player_name = self.view.select_player()
                
                # Display player stats
                self.score_manager.display_player_stats(player_name, self.lang_manager)
                
                # Select quiz level
                level = self.view.select_level()
                
                # Play quiz
                score, total_questions = self.play_quiz(player_name, level)
                
                # Update and display scores
                percentage = (score / total_questions) * 100
                self.score_manager.update_score(player_name, None, level, percentage)
                
                # Ask to play again
                if not self.view.play_again():
                    logger.info("Game session ended")
                    break
            
            except Exception as e:
                logger.error(f"Error in game loop: {e}", exc_info=True)
                break

def main():
    """Initialize and start the game."""
    config = config_manager("config.yaml")
    lang_manager = LanguageManager(config.get('language_file'))
    view = CLIView(lang_manager)
    
    vocabulary_model = Vocabulary()
    vocabulary_controller = VocabularyController(vocabulary_model, view, lang_manager)
    score_manager = ScoreManager()
    
    game_controller = GameController(
        view, 
        lang_manager, 
        vocabulary_controller, 
        score_manager, 
        config
    )
    
    game_controller.run_game_loop()

if __name__ == "__main__":
    main()
