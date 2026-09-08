import logging
import os
from config import LOG_FOLDER

os.makedirs(LOG_FOLDER, exist_ok=True)

def get_logger():
    # Avoid adding duplicate handlers on repeated calls
    logger = logging.getLogger()
    if logger.handlers:
        return logger
    logging.basicConfig(level=logging.INFO,
                            filename=f"{LOG_FOLDER}/app.log",
                            encoding="utf8",
                            format="%(asctime)s | %(levelname)s | %(filename)s | %(message)s")
    # Also log to console
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
    logger.addHandler(console)
    return logger


