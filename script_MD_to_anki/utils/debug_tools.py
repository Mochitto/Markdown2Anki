"""
This module exposes a function that can be used
to debug objects more easily through  the
pprint and json modules.

It is to be imported in all/most modules in the
source code, to make the use of expressive_debug
easy and quick.
Said imports are to be removed for production.
"""
import inspect
import json
import pprint


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
    module = frames[1][0].f_globals["__name__"]  # Module of the caller
    line_number = frames[1][0].f_lineno  # Line at which the function was called

    if format == "json":
        message = json.dumps(debugMessage, indent=2)
    elif format == "pprint":
        message = pprint.pformat(debugMessage)
    else:
        message = str(debugMessage)

    # log the message at the DEBUG level
    logger.debug(f"From {module}, line: {line_number}: {debugLabel}\n{message}\n")
