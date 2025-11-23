"""
logger that will write to ``logs/debug.log`` from the execution dir
"""
import logging
import os


logger = logging.getLogger("debug")
logger.setLevel(logging.DEBUG)

OUTPUT_DIR = "logs"

if not logger.handlers:
    if not os.path.exists(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)

    formatter = logging.Formatter(
        "%(asctime)s - %(filename)s - %(levelname)s - %(message)s"
    )

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(os.path.join(OUTPUT_DIR, "debug.log"))
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
