import logging
import sys
from pathlib import Path

# Add project root to sys.path to ensure config can be imported if running from src
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from config.settings import LOG_FILE

def setup_logger(name=__name__, log_file=LOG_FILE, level=logging.INFO):
    """Function to setup as many loggers as you want"""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        # Create handlers
        c_handler = logging.StreamHandler()
        f_handler = logging.FileHandler(log_file)
        c_handler.setLevel(level)
        f_handler.setLevel(level)

        # Create formatters and add it to handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        c_handler.setFormatter(formatter)
        f_handler.setFormatter(formatter)

        # Add handlers to the logger
        logger.addHandler(c_handler)
        logger.addHandler(f_handler)

    return logger
