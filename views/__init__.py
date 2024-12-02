import logging
from pathlib import Path

# Create logs directory if it doesn't exist
LOG_DIR = Path("./logs")
LOG_DIR.mkdir(exist_ok=True)

# Configure logging for the views module
logging.basicConfig(
    filename=LOG_DIR / "views.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger("views")
logger.info("Views module initialized.")

# Import views
from .cli_view import CLIView

# Future imports for web views can be added here
