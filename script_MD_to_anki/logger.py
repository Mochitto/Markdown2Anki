import logging
import sys

import md_2_anki.utils.card_types as Types
from md_2_anki.utils.debug_tools import expressive_debug

# Create a logger object
class SingleLevelFilter(logging.Filter):
    def __init__(self, passlevel, reject):
        self.passlevel = passlevel
        self.reject = reject

    def filter(self, record):
        if self.reject:
            return record.levelno != self.passlevel
        return record.levelno == self.passlevel


def setup_logging(log_file_path: Types.PathString)-> None:
    info_handler = logging.StreamHandler(stream=sys.stdout)
    info_handler.addFilter(SingleLevelFilter(logging.INFO, False))
    info_handler.setFormatter(logging.Formatter("%(message)s"))

    stderr_handler = logging.StreamHandler(stream=sys.stderr)
    stderr_handler.addFilter(SingleLevelFilter(logging.INFO, True))
    stderr_handler.addFilter(SingleLevelFilter(logging.DEBUG, True))
    stderr_handler.setFormatter(logging.Formatter("%(message)s"))

    debug_handler = logging.StreamHandler()
    debug_handler.addFilter(SingleLevelFilter(logging.DEBUG, False))
    debug_handler.setFormatter(logging.Formatter("🔧 %(message)s"))  # Should be used with "expressive_debug"

    file_handler = logging.FileHandler(log_file_path, mode="w", encoding="utf-8", errors="replace")
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(levelname)s (line %(lineno)d from %(module)s.py) %(levelname)s: %(message)s")
    )
    file_handler.setLevel(logging.DEBUG)

    logging.basicConfig(handlers=[debug_handler, info_handler, stderr_handler, file_handler], level=logging.DEBUG)
