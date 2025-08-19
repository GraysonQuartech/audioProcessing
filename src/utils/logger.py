"""
Logging configuration for the Courtroom Audio Processor.
"""

import logging
import sys
from pathlib import Path

from ..config.settings import LOG_FILE, LOG_FORMAT, LOG_LEVEL

def setup_logging(verbose: bool = False) -> None:
    """
    Set up logging configuration.
    
    Args:
        verbose: Enable verbose logging if True
    """
    # Determine log level
    level = logging.DEBUG if verbose else getattr(logging, LOG_LEVEL.upper())
    
    # Create formatter
    formatter = logging.Formatter(LOG_FORMAT)
    
    # Ensure logs directory exists
    log_path = Path(LOG_FILE)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Create file handler
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    
    # Remove existing handlers to avoid duplicates
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Add handlers
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    logger = logging.getLogger(__name__)
    logger.debug("Logging configured successfully")

def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a specific module.
    
    Args:
        name: Logger name (usually __name__)
        
    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)

