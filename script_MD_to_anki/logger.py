import logging
import sys

from config_handle import LOG_FILE

# Create a logger object
class SingleLevelFilter(logging.Filter):
    def __init__(self, passlevel, reject):
        self.passlevel = passlevel
        self.reject = reject

    def filter(self, record):
        if self.reject:
            return (record.levelno != self.passlevel)
        else:
            return (record.levelno == self.passlevel)

# Create a stream handler for STDOUT
stdout_handler = logging.StreamHandler(stream=sys.stdout)
stdout_handler.addFilter(SingleLevelFilter(logging.INFO, False))
stdout_handler.setFormatter(logging.Formatter("%(message)s"))

stderr_handler = logging.StreamHandler(stream=sys.stderr)
stderr_handler.addFilter(SingleLevelFilter(logging.INFO, True))
stderr_handler.setFormatter(logging.Formatter("❌ %(module)s - %(levelname)s: %(message)s"))

file_handler = logging.FileHandler(LOG_FILE, mode="w", encoding="utf-8", errors="replace")
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s (line %(lineno)d from %(module)s.py): %(message)s"))

logging.basicConfig(handlers=[
    stdout_handler,
    stderr_handler,
    file_handler
], level=logging.INFO)
