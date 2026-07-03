import logging
from logging import Logger

def configLogger(loggerName: str, loggerPath: str) -> Logger:

    logger = logging.getLogger(loggerName)
    logger.setLevel(logging.DEBUG)

    # this is to prevent duplicate handlers if the logger is imported multiple times
    if logger.hasHandlers():
        return logger

    logFormat = logging.Formatter(
        "[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s"
    )

    fileHandler = logging.FileHandler(loggerPath)
    fileHandler.setLevel(logging.DEBUG)
    fileHandler.setFormatter(logFormat)

    streamHandler = logging.StreamHandler()
    streamHandler.setLevel(logging.DEBUG)
    streamHandler.setFormatter(logFormat)

    logger.addHandler(fileHandler)
    logger.addHandler(streamHandler)

    return logger