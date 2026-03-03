import functools
import logging
import time
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path

import requests
from colorlog import ColoredFormatter


def get_logger(name:str) -> logging.Logger:
    
     # Creeaza si intoarce un logger configurat
     # -log in fisier: logs/api_framework.log
     # -log in consola
     # -format

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        # Dacă logger-ul are deja handleri, nu mai adăugăm alții
        return logger
    #logger.handlers.clear()

    project_root = Path(__file__).resolve().parents[2]
    logs_dir = project_root / "logs"
    logs_dir.mkdir(exist_ok=True)

    log_format = "%(asctime)s | %(levelname)s | %(message)s | %(name)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    file_formatter = logging.Formatter(
        log_format,
        datefmt=date_format,
    )

    console_formatter = ColoredFormatter(
        f"%(log_color)s{log_format}",
        datefmt=date_format,
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red",
        },
    )

    # Handler pentru fișier
    # the classic way with a static file that saves all logs
    # file_handler = logging.FileHandler(logs_dir / "api_framework.log", encoding="utf-8")

    # advanced way with a file that saves max 1MB of logs and keeps the last 5 files
    file_handler = RotatingFileHandler(
        logs_dir / "api_framework.log",
        maxBytes=1 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)
    file_handler.terminator = "\n"  # ensure newline terminator (defensive)

    # Handler for error file
    # the same thing as file_handler
    # file_error_handler = logging.FileHandler(logs_dir / "errors.log", encoding="utf-8")
    file_error_handler = RotatingFileHandler(
        logs_dir / "errors.log",
        maxBytes=1 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8"
    )
    file_error_handler.setLevel(logging.ERROR)
    file_error_handler.setFormatter(file_formatter)
    file_error_handler.terminator = "\n"

    # Handler pentru consolă
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)

    logger.addHandler(file_handler)
    logger.addHandler(file_error_handler)
    logger.addHandler(console_handler)

    return logger


# decorator measure_time for measuring time per request
logger_time = get_logger("http-request.timing")  # set the name of the log in file, at the end of the log line
# the decorator is used before every http request that is sent in clients


def measure_time(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        response = None
        try:
            response = func(*args, **kwargs)
            return response
        finally:
            elapsed = time.perf_counter() - start

            method = None
            url = None

            # Common patterns
            if isinstance(response, requests.Response):
                method = response.request.method
                url = response.request.url
            else:
                # fallback: try to infer from args
                if args:
                    method = getattr(args[0], "method", None)
                    url = getattr(args[0], "url", None)

            if method and url:
                logger_time.info("%s %s took %.3fs", method, url, elapsed)
            else:
                logger_time.info("%s took %.3fs", func.__name__, elapsed)
    return wrapper

