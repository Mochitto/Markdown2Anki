import logging

from typing import List, Tuple, Dict

import markdown2anki.md_2_anki.utils.card_types as CardTypes
from markdown2anki.md_2_anki.utils.card_error import CardError
from markdown2anki.utils.debug_tools import expressive_debug
from markdown2anki.md_2_anki.process_clozes.process_clozes import are_clozes_in_card

logger = logging.getLogger(__name__)


def create_front_tabs_list(tabs: List[CardTypes.HTMLTab]) -> List[CardTypes.HTMLTab]:
    front_tabs = [tab for tab in tabs if tab["card side"] == "front"]
    if not front_tabs:
        raise CardError("A card without front tabs has been found.")
    return front_tabs

def get_swap_mappings(tabs: List[CardTypes.HTMLTab]) -> CardTypes.SwapMappings:
    front_swap = []
    back_swap = []

    for index, tab in enumerate(tabs):
        if tab["card side"] == "front" and tab["swap"]:
            if are_clozes_in_card(tab["body"]):
                raise CardError("You can't swap a tab that has a cloze in it.")

            front_swap.append(index)
        elif tab["card side"] == "back" and tab["swap"]:
            back_swap.append(index)
    
    smallest_list = min(front_swap, back_swap, key=len)
    common_length = len(smallest_list)

    to_replace: List[Tuple[int, int]] = [
        (front_swap[index], back_swap[index]) 
        for index in range(common_length)
        ]
    to_remove = front_swap[:] + back_swap[:common_length]
    to_restore = back_swap[common_length:]

    return {
            "restore": to_restore,
            "replace": to_replace,
            "remove": to_remove
        }

# def create_back_tabs_list(tabs: List[CardTypes.HTMLTab], swap_mappings: CardTypes.SwapMappings):
#     tabs_copy = tabs.copy()
#     for index_of_tab_to_replace, index_of_tab_that_replaces in swap_mappings["replace"]:
#         tabs_copy[index_of_tab_to_replace] = tabs_copy[index_of_tab_that_replaces]

#     for index_of_tab_to_restore in swap_mappings["restore"]:
#         tabs_copy[index_of_tab_to_restore]["swap"] = False

#     for index_of_tab_to_remove in swap_mappings["remove"]:
#         del tabs_copy[index_of_tab_to_remove]
#         
#     return tabs_copy


