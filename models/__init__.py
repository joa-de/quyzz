import logging

# Configure logging to output to a shared logfile
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="../logfile.log",  # Update this path to your shared logfile
    filemode="a",
)  # Append to the logfile

logger = logging.getLogger(__name__)
