import logging
import sys

from markdown2anki.utils import common_types as Types
from markdown2anki.utils.debug_tools import expressive_debug

# Create a logger object
class SingleLevelFilter(logging.Filter):
    def __init__(self, passlevel, reject):
        self.passlevel = passlevel
        self.reject = reject

    def filter(self, record):
        if self.reject:
            return record.levelno != self.passlevel
        return record.levelno == self.passlevel

def setup_logging(console_debug=False) -> None:
    """
    Take a logging level from the logging module,
    set-up different handlers for the various messages levels and
    call a basicConfig with the level and the handlers.
    """
    info_handler = logging.StreamHandler(stream=sys.stdout)
    info_handler.addFilter(SingleLevelFilter(logging.INFO, False))
    info_handler.setFormatter(logging.Formatter("%(message)s"))
    info_handler.setLevel(logging.INFO)

    stderr_handler = logging.StreamHandler(stream=sys.stderr)
    stderr_handler.addFilter(SingleLevelFilter(logging.INFO, True))
    stderr_handler.addFilter(SingleLevelFilter(logging.DEBUG, True))
    stderr_handler.setFormatter(logging.Formatter("%(message)s"))
    stderr_handler.setLevel(logging.INFO)
    
    debug_handler = logging.StreamHandler()
    debug_handler.addFilter(SingleLevelFilter(logging.DEBUG, False))
    debug_handler.setFormatter(
        logging.Formatter("🔧 %(message)s")
    )  # Should be used with "expressive_debug"

    if console_debug:
        logging.basicConfig(
            handlers=[info_handler, stderr_handler, debug_handler],
            level=logging.DEBUG,
        )
    else:
        logging.basicConfig(
            handlers=[info_handler, stderr_handler],
            level=logging.DEBUG,
        )


def setup_file_logging(logger: logging.Logger, log_file_path: Types.PathString):
    file_handler = logging.FileHandler(
        log_file_path, mode="w", encoding="utf-8", errors="replace"
    )
    file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s - %(levelname)s (line %(lineno)d from %(module)s.py) %(levelname)s: %(message)s"
        )
    )
    file_handler.setLevel(logging.DEBUG)

    logger.addHandler(file_handler)
