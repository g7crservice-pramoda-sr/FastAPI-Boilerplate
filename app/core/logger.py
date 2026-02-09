import logging
import os

LOG_DIR = "./logs"


def setup_logger() -> logging.Logger:
    """
    Configure and return the application logger (singleton).
    """
    os.makedirs(LOG_DIR, exist_ok=True)

    logger = logging.getLogger("app_logger")

    # If logger already configured, return it
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        fmt="%(asctime)s || %(levelname)s || %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Handlers
    debug_handler = logging.FileHandler(os.path.join(LOG_DIR, "debug.log"))
    debug_handler.setLevel(logging.DEBUG)
    debug_handler.setFormatter(formatter)

    info_handler = logging.FileHandler(os.path.join(LOG_DIR, "info.log"))
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(formatter)

    error_handler = logging.FileHandler(os.path.join(LOG_DIR, "error.log"))
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Add handlers only once
    logger.addHandler(debug_handler)
    logger.addHandler(info_handler)
    logger.addHandler(error_handler)
    logger.addHandler(console_handler)

    return logger


# Create a single shared logger instance
logger = setup_logger()
