"""Configuration and logging setup for the RAG Chatbot."""

import sys

from loguru import logger

# Remove default handler
logger.remove()

# Configure loguru with a standard format
log_format = (
    "<level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:"
    "<cyan>{line}</cyan> - <level>{message}</level>"
)
logger.add(
    sys.stdout,
    format=log_format,
    level="INFO",
)

# Optional: Add file logging
# logger.add(
#     "logs/app.log",
#     format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
#     level="DEBUG",
#     rotation="500 MB",
# )


def get_logger(name: str):  # type: ignore[no-untyped-def]
    """Get a logger instance with the given name.

    Args:
        name: The name of the logger (typically __name__ from calling module)

    Returns:
        A configured loguru logger instance
    """
    return logger.bind(name=name)
