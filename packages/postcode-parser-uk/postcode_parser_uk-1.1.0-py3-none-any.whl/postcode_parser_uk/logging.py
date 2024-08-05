import logging

logger = logging.getLogger("uk-postcode-parsing")
logger.addHandler(logging.NullHandler())


def get_logger():
    """Get the logger for the package."""
    return logger
