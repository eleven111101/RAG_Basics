import logging
import os

LOG_DIR = "logs"

os.makedirs(LOG_DIR, exist_ok=True)


def setup_logger(name: str):

    logger = logging.getLogger(name)

    logger.setLevel(logging.INFO)

    if not logger.handlers:

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )

        file_handler = logging.FileHandler(
            f"{LOG_DIR}/application.log",
            encoding="utf-8"
        )

        file_handler.setFormatter(formatter)

        # ONLY FILE LOGGER
        logger.addHandler(file_handler)

    return logger