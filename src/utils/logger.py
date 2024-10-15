import logging
import os
import time
from enum import Enum
from typing import Optional, Callable, Any, Literal


class LogLevel(Enum):
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs) -> Any:
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Logger(metaclass=Singleton):
    def __init__(
            self,
            log_lvl: LogLevel = LogLevel.INFO,
            log_base_directory: Optional[str] = None,
            log_mode: str = 'w',  # 'w' for overwrite, 'a' for append
            console_logging: bool = True,
    ) -> None:
        self._log = logging.getLogger("playwrite")
        self._log.setLevel(LogLevel.DEBUG.value)

        self.log_base_directory = log_base_directory or os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../.."))
        self.log_file = self._create_log_file()
        self._initialize_logging(log_lvl, log_mode, console_logging)

    def _create_log_file(self) -> str:
        current_time = time.strftime("%Y-%m-%d")
        log_directory = os.path.join(self.log_base_directory, "reports/logs")

        os.makedirs(log_directory, exist_ok=True)  # Create directory if it doesn't exist

        return os.path.join(log_directory, f"log_{current_time}.log")

    def _initialize_logging(self, log_lvl: LogLevel, log_mode: str, console_logging: bool) -> None:
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        # File handler
        fh = logging.FileHandler(self.log_file, mode=log_mode)
        fh.setFormatter(formatter)
        fh.setLevel(log_lvl.value)
        self._log.addHandler(fh)

        # Console handler
        if console_logging:
            ch = logging.StreamHandler()
            ch.setFormatter(formatter)
            ch.setLevel(log_lvl.value)
            self._log.addHandler(ch)

    def get_instance(self) -> logging.Logger:
        return self._log

    def annotate(self, message: str, level: Literal["info", "warn", "debug", "error"] = "info") -> None:
        """Log a message at the specified level."""
        log_methods = {
            "info": self._log.info,
            "warn": self._log.warning,
            "debug": self._log.debug,
            "error": self._log.error,
        }

        if level not in log_methods:
            raise ValueError(f"Invalid log level: {level}")

        log_methods[level](message)


def log(data: Optional[str] = None, level: Literal["info", "warn", "debug", "error"] = "info") -> Callable:
    """Decorator to log the current method's execution.

    :param data: Custom log message to use if no docstring is provided.
    :param level: Level of the logs, e.g., info, warn, debug, error.
    """
    logger_instance = Logger()

    def decorator(func: Callable) -> Callable:
        def wrapper(self, *args, **kwargs) -> Any:
            # Get the method's docstring
            method_docs = format_method_doc_str(func.__doc__)

            if method_docs is None and data is None:
                raise ValueError(f"No documentation available for :: {func.__name__}")

            # Construct the parameter string for logging
            params_str = ", ".join(repr(arg) for arg in args)
            kwargs_str = ", ".join(f"{k}={v!r}" for k, v in kwargs.items())
            all_params_str = ", ".join(filter(None, [params_str, kwargs_str]))

            # Filter out unwanted <Locator> information
            filtered_params_str = filter_locator_info(all_params_str)

            logs = (
                f"{method_docs + '.' if method_docs else data} "
                f"Method :: {func.__name__}() "
                f"with parameters: {filtered_params_str}"
            )

            logger_instance.annotate(logs, level)

            # Call the original method, passing *args and **kwargs
            return func(self, *args, **kwargs)

        return wrapper

    return decorator


def format_method_doc_str(doc_str: Optional[str]) -> Optional[str]:
    """Add a dot to the docs string if it doesn't exist."""
    if doc_str and not doc_str.endswith("."):
        return doc_str + "."
    return doc_str


def filter_locator_info(param_str: str) -> str:
    """Filter out unwanted <Locator> details from the parameters string."""
    # Example regex to filter out the specific Locator format, modify as needed
    import re
    filtered = re.sub(r"<Locator.*?>", "", param_str)
    return filtered.strip()
