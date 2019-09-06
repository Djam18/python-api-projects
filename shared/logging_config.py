"""Shared logging configuration for all Flask apps."""
import logging


def setup_logging(name: str) -> logging.Logger:
    """Setup logging for a Flask app."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(name)
