import logging
import sys
import json 
import pprint
import inspect

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
info_handler = logging.StreamHandler(stream=sys.stdout)
info_handler.addFilter(SingleLevelFilter(logging.INFO, False))
info_handler.setFormatter(logging.Formatter("%(message)s"))

stderr_handler = logging.StreamHandler(stream=sys.stderr)
stderr_handler.addFilter(SingleLevelFilter(logging.INFO, True))
stderr_handler.addFilter(SingleLevelFilter(logging.DEBUG, True))
stderr_handler.setFormatter(logging.Formatter("❌ %(levelname)s (line %(lineno)d from %(module)s.py): %(message)s"))

debug_handler = logging.StreamHandler()
debug_handler.addFilter(SingleLevelFilter(logging.DEBUG, False))
debug_handler.setFormatter(logging.Formatter("🔧 %(message)s")) # Should be used with "expressive_debug"

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
    Call logger.debug, after prepending the debugLabel to the debugMessage;
    If the message is an object, you can format it using json.dumps or pprint.pformat:
    format=
        "pprint" -> pprint.pformat
        "json" -> json.dumps, indent=2
    """
    frames = inspect.getouterframes(inspect.currentframe())
    # getouterframes gives back a list of frames.
    # frames[1] represents the previous frame (call on the call-stack), which is the caller of the function
    # frames[1][0] frame object; contains information on the frame (such as globals or the line number)
    module = frames[1][0].f_globals['__name__'] # Module of the caller
    line_number = frames[1][0].f_lineno # Line at which the function was called

    if format == 'json':
        message = json.dumps(debugMessage, indent=2)
    elif format == 'pprint':
        message = pprint.pformat(debugMessage)
    else:
        message = str(debugMessage)

    # log the message at the DEBUG level
    logger.debug(f"From {module}, line: {line_number}: {debugLabel}\n{message}\n")