import logging

def createLogger(file_name: str):
    logger = logging.getLogger(file_name)
    logger.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s | %(name)s - %(levelname)s: %(message)s"
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    logger.propagate = False
    return logger
