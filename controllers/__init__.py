import logging
from pathlib import Path

# Create logs directory if it doesn't exist
LOG_DIR = Path("./logs")
LOG_DIR.mkdir(exist_ok=True)

# Configure logging for the controllers module
logging.basicConfig(
    filename=LOG_DIR / "controllers.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger("controllers")
logger.info("Controllers module initialized.")

# Import controllers
from .vocabulary_controller import VocabularyController

# Future controllers can be added here
