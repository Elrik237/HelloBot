import logging


def initialize_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    handler_s = logging.StreamHandler()
    handler_s.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - [%(levelname)s] - %(name)s - %(message)s")
    handler_s.setFormatter(formatter)
    logger.addHandler(handler_s)

    handler_f = logging.FileHandler("file.log", "w")
    handler_f.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - [%(levelname)s] - %(name)s - %(message)s")
    handler_f.setFormatter(formatter)
    logger.addHandler(handler_f)
