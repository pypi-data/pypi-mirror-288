import os
import sys
import logging
import contextvars
from pathlib import Path
from loguru import logger


BASE_DIR = Path(__file__).parent.parent.parent.resolve()
LOG_PATH = os.path.expanduser(os.path.join(BASE_DIR, "logs", "log-{time:YYYY-MM-DD}.log"))
LOG_ERROR_PATH = os.path.expanduser(os.path.join(BASE_DIR, "logs", "error-{time:YYYY-MM-DD}.log"))
LOG_FORMAT = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | {trace_id} | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | <level>{message}</level>"
request_id_context = contextvars.ContextVar("request-id")


def trace_filter():
    def trace(record):
        record["trace_id"] = request_id_context.get("root")
        return True
    return trace


logger.remove(0)
logger.add(sys.stderr, backtrace=True, diagnose=True, filter=trace_filter(), format=LOG_FORMAT)
logger.add(
    LOG_PATH,
    level="DEBUG",
    encoding="utf-8",
    rotation="00:00",
    retention="1 week",
    backtrace=True,
    diagnose=True,
    enqueue=True,
    catch=True,
    filter=trace_filter(),
    format=LOG_FORMAT,
)

logger.add(
    LOG_ERROR_PATH,
    level="ERROR",
    encoding="utf-8",
    rotation="00:00",
    retention="1 week",
    backtrace=True,
    diagnose=True,
    enqueue=True,
    catch=True,
    filter=trace_filter(),
    format=LOG_FORMAT,
)


class InterceptHandler(logging.Handler):
    """
    Default handler from examples in loguru documentaion.
    See https://loguru.readthedocs.io/en/stable/overview.html#entirely-compatible-with-standard-logging
    """

    def emit(self, record: logging.LogRecord):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 6
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )

logging.basicConfig(handlers=[InterceptHandler()], level=0)
for name in logging.root.manager.loggerDict:
    _logger = logging.getLogger(name)
    _logger.propagate = False
    _logger.handlers = [InterceptHandler()]

