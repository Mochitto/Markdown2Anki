import logging

from typing import List, Dict

import markdown2anki.md_2_anki.utils.card_types as CardTypes
from markdown2anki.md_2_anki.utils.card_error import CardError
from markdown2anki.utils.debug_tools import expressive_debug

logger = logging.getLogger(__name__)


def create_front_tabs_list(tabs: List[CardTypes.HTMLTab]) -> List[CardTypes.HTMLTab]:
    front_tabs = [tab for tab in tabs if tab["card side"] == "front"]
    if not front_tabs:
        raise CardError("A card without front tabs has been found.")
    return front_tabs

def get_swap_mappings(tabs: List[CardTypes.HTMLTab]) -> Dict[str, List[int]|Dict[int, int]]:
    return
