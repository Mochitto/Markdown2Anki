import logging

import markdown2anki.md_2_anki.utils.card_types as CardTypes
from markdown2anki.utils.debug_tools import expressive_debug

logger = logging.getLogger(__name__)


class CardError(Exception):
    """Errors related to the parsing of the card."""

    def __init__(self, message):
        self.message = message

    def __str__(self):
        error_message = f"{self.message}"
        return error_message
