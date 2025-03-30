import os
import logging


def init_logging() -> None:
    log_folder = os.path.join("logs")
    log_file = os.path.join(log_folder, "app.log")
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.DEBUG,
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(),
        ],
    )
