"""
Utilities for logging.
"""

import logging
import sys


FORMATTER = logging.Formatter("%(levelname)s: %(message)s")


class ConsoleHandler(logging.StreamHandler):
    """
    A handler that logs to console in the sensible way.
    StreamHandler can log to *one of* sys.stdout or sys.stderr.
    It is more sensible to log to sys.stdout by default with only error
    (logging.ERROR and above) messages going to sys.stderr. This is how
    ConsoleHandler behaves.
    """

    def __init__(self, level, formatter=FORMATTER):
        logging.StreamHandler.__init__(self)
        self.stream = None # reset it; we are not going to use it anyway
        self.setLevel(level)
        self.setFormatter(formatter)

    def emit(self, record):
        if record.levelno >= logging.ERROR:
            self.__emit(record, sys.stderr)
        else:
            self.__emit(record, sys.stdout)

    def __emit(self, record, strm):
        self.stream = strm
        logging.StreamHandler.emit(self, record)

    def flush(self):
        # Workaround a bug in logging module
        # See:
        #   http://bugs.python.org/issue6333
        if self.stream and hasattr(self.stream, 'flush') and not self.stream.closed:
            logging.StreamHandler.flush(self)