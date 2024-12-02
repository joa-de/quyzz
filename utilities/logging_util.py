import logging
from pathlib import Path
import os

def setup_logging(log_dir='logs', log_file='latin_quiz.log'):
    """
    Set up logging configuration for the application.
    
    Args:
        log_dir (str): Directory to store log files
        log_file (str): Name of the log file
    
    Returns:
        logging.Logger: Configured logger instance
    """
    # Ensure log directory exists
    log_path = Path(__file__).parent / log_dir
    log_path.mkdir(exist_ok=True)
    
    # Full path to log file
    full_log_path = log_path / log_file
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(full_log_path, encoding='utf-8'),
            logging.StreamHandler()  # Optional: also log to console
        ]
    )
    
    # Create and return a logger
    return logging.getLogger('LatinQuizApp')

# Global logger that can be imported and used across the application
logger = setup_logging()
