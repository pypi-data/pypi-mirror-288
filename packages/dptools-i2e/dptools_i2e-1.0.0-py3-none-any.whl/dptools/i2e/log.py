import logging
import functools
from typing import List


HANDLES: List[logging.Handler] = []


@functools.lru_cache(maxsize=None)
def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    for hdlr in HANDLES:
        logger.addHandler(hdlr)
    return logger


def setup(file: str = None):
    HANDLES.clear()

    formatter = logging.Formatter('%(asctime)s | %(levelname)-7s | %(name)s | %(message)s')
    HANDLES.append(logging.StreamHandler())

    if file is not None:
        HANDLES.append(logging.FileHandler(file, mode='w'))

    for handler in HANDLES:
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(formatter)
