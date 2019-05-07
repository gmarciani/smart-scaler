"""
Utilities for logging.
"""

import logging


FORMAT = "%(asctime)-15s [%(levelname)s] %(message)s"
LEVEL = logging._nameToLevel['INFO']
logging.basicConfig(format=FORMAT, level=LEVEL)

def get_logger(name):
    return logging.getLogger(name)