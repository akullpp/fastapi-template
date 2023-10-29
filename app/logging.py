import logging
import logging.config
from sys import stdout

from loguru import logger

from app.config import config


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def start_logging():
    log_level = config["LOG_LEVEL"]
    log_level_name = logging.getLevelName(log_level)
    log_json = config["LOG_JSON"] == "1"

    # Intercept everything at the root logger
    logging.root.handlers = [InterceptHandler()]
    logging.root.setLevel(log_level_name)

    # Remove every other logger's handlers and propagate to root logger
    for name in logging.root.manager.loggerDict:
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True

    # Configure loguru
    logger.configure(handlers=[
        {
            "sink": stdout,
            "serialize": log_json,
            "level": log_level_name,
            "enqueue": True,
        },
    ])
    logger.info(f"LOG_LEVEL={log_level}")


def stop_logging():
    logging.shutdown()
