# Logging configuration module

import logging
import sys
from pathlib import Path
from config import LOG_FILE, LOG_LEVEL, LOG_FORMAT

def setup_logger(name: str) -> logging.Logger:
    """Setup logger with both file and console handlers."""
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, LOG_LEVEL))

    # File handler
    LOG_FILE.parent.mkdir(exist_ok=True)
    file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
    file_handler.setLevel(getattr(logging, LOG_LEVEL))

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, LOG_LEVEL))

    # Formatter
    formatter = logging.Formatter(LOG_FORMAT)
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

# Main logger
logger = setup_logger("NewsAgent")
