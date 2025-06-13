import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import sys


def setup_logging(
    log_dir="logs",
    log_file="latin_quiz.log",
    console_level=logging.CRITICAL,
    file_level=logging.DEBUG,
):
    """
    Set up comprehensive logging with more advanced features.

    Args:
        log_dir (str): Directory to store log files
        log_file (str): Name of the log file
        console_level (int): Logging level for console output
        file_level (int): Logging level for file output

    Returns:
        logging.Logger: Configured logger instance
    """
    # Ensure log directory exists
    log_path = Path(__file__).parent / log_dir
    log_path.mkdir(exist_ok=True)

    # Full path to log file
    full_log_path = log_path / log_file

    # Create a formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Create a root logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # Capture all log levels

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(console_level)
    console_handler.setFormatter(formatter)

    # File Handler with log rotation
    file_handler = RotatingFileHandler(
        full_log_path,
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5,  # Keep 5 backup files
    )
    file_handler.setLevel(file_level)
    file_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


# Convenience function to get a module-specific logger
def get_logger(name=None):
    """
    Get a logger for a specific module or the root logger.

    Args:
        name (str, optional): Name of the logger. Defaults to root logger.

    Returns:
        logging.Logger: Logger instance
    """
    return logging.getLogger(name)


# Initialize logging when the module is imported
logger = setup_logging()
