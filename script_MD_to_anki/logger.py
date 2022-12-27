import logging
import sys
import json 
import pprint

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

class DebugFormatter(logging.Formatter):
    def format(self, record):
        # get the format value from the extra dictionary
        format = record.__dict__.get('format', 'print')

        

        # format the message based on the format value
        if format == 'pprint':
            message = pprint.pformat(record.msg)
        elif format == 'json':
            message = json.dumps(record.msg)
        else:
            message = record.msg

        # format the log record using the original formatter
        record.msg = message
        return super().format(record)

# Create a stream handler for STDOUT
info_handler = logging.StreamHandler(stream=sys.stdout)
info_handler.addFilter(SingleLevelFilter(logging.INFO, False))
info_handler.setFormatter(logging.Formatter("%(message)s"))

stderr_handler = logging.StreamHandler(stream=sys.stderr)
stderr_handler.addFilter(SingleLevelFilter(logging.INFO, True))
stderr_handler.addFilter(SingleLevelFilter(logging.DEBUG, True))
stderr_handler.setFormatter(logging.Formatter("❌ %(levelname)s (line %(lineno)d from %(module)s.py): %(message)s"))

debug_handler = logging.StreamHandler()
debug_handler.addFilter(SingleLevelFilter(logging.DEBUG, False))
debug_handler.setFormatter(logging.Formatter("🔧 Debugging from: %(module)s, line: %(lineno)d\n%(message)s"))

file_handler = logging.FileHandler(LOG_FILE, mode="w", encoding="utf-8", errors="replace")
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s (line %(lineno)d from %(module)s.py): %(message)s"))
file_handler.setLevel(logging.DEBUG)

logging.basicConfig(handlers=[
    debug_handler,
    info_handler,
    stderr_handler,
    file_handler
], level=logging.DEBUG)


# Debug logger
def expressive_debug(logger, debugLabel, debugMessage, format=None):
    """
    Call logger.debug, after appending the debugLabel to the debugMessage;
    If the message is an object, you can format it using json.dumps or pprint.pformat:
    format=
        "pprint" - pprint.pformat
        "json" - json.dumps, indent=2
    """
    if format == 'json':
        message = json.dumps(debugMessage, indent=2)
    elif format == 'pprint':
        message = pprint.pformat(debugMessage)
    else:
        message = str(debugMessage)

    # log the message at the DEBUG level
    logger.debug(f"🔧 LABEL: {debugLabel}\n{message}")