import logging
from logging.handlers import RotatingFileHandler
import os
import functools
import time
import inspect
from typing import Any, Callable, TypeVar, cast

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
        fmt="%(asctime)s || %(levelname)s || [%(name)s] || %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Handlers
    debug_handler = RotatingFileHandler(
        os.path.join(LOG_DIR, "debug.log"),
        maxBytes=5 * 1024 * 1024,
        backupCount=5
    )
    debug_handler.setLevel(logging.DEBUG)
    debug_handler.setFormatter(formatter)

    info_handler = RotatingFileHandler(
        os.path.join(LOG_DIR, "info.log"),
        maxBytes=5 * 1024 * 1024,
        backupCount=5
    )
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(formatter)

    error_handler = RotatingFileHandler(
        os.path.join(LOG_DIR, "error.log"),
        maxBytes=5 * 1024 * 1024,
        backupCount=5
    )
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


F = TypeVar("F", bound=Callable[..., Any])


def log_execution(func: F) -> F:
    """
    Unified decorator to log function entry, exit, execution time, and exceptions.
    Supports both synchronous and asynchronous functions.

    Usage:
        @log_execution
        def my_func(): ...

        @log_execution
        async def my_async_func(): ...
    """
    func_name = func.__qualname__
    module_name = func.__module__
    custom_logger = logging.getLogger(f"app_logger.{module_name}")

    @functools.wraps(func)
    def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
        custom_logger.debug(f"[{func_name}] STARTED")
        start_time = time.perf_counter()
        try:
            result = func(*args, **kwargs)
            duration = (time.perf_counter() - start_time) * 1000
            custom_logger.info(f"[{func_name}] COMPLETED in {duration:.2f}ms")
            return result
        except Exception as e:
            custom_logger.error(
                f"[{func_name}] FAILED | {type(e).__name__}: {str(e)}",
                exc_info=True
            )
            raise

    @functools.wraps(func)
    async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
        custom_logger.debug(f"[{func_name}] STARTED (async)")
        start_time = time.perf_counter()
        try:
            result = await func(*args, **kwargs)
            duration = (time.perf_counter() - start_time) * 1000
            custom_logger.info(f"[{func_name}] COMPLETED in {duration:.2f}ms")
            return result
        except Exception as e:
            custom_logger.error(
                f"[{func_name}] FAILED | {type(e).__name__}: {str(e)}",
                exc_info=True
            )
            raise

    if inspect.iscoroutinefunction(func):
        return cast(F, async_wrapper)
    return cast(F, sync_wrapper)