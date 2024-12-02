import logging
from pathlib import Path

# Create logs directory if it doesn't exist
LOG_DIR = Path("./logs")
LOG_DIR.mkdir(exist_ok=True)

# Configure logging for the models module
logging.basicConfig(
    filename=LOG_DIR / "models.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger("models")
logger.info("Models module initialized.")

# Import models
from .vocabulary import Vocabulary

# from .mastery import Mastery
# from .score import Score
