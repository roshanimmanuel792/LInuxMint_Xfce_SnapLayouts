"""Logging configuration for xfce-snap-layouts."""

import logging
import sys
from pathlib import Path

def setup_logging(log_level=logging.INFO):
    """Configure logging for the application."""
    log_dir = Path.home() / ".config" / "xfce-snap-layouts" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "xfce-snap-layouts.log"
    
    # Create formatter
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)-8s [%(name)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Create root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # File handler
    try:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    except Exception as e:
        print(f"Warning: Could not set up file logging: {e}", file=sys.stderr)
    
    # Console handler (only warnings and errors in production)
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    return root_logger
