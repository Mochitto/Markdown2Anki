import logging

from typing import List, Tuple

import markdown2anki.md_2_anki.utils.card_types as CardTypes
from markdown2anki.md_2_anki.utils.card_error import CardError
from markdown2anki.utils.debug_tools import expressive_debug
from markdown2anki.md_2_anki.process_clozes import are_clozes_in_card

logger = logging.getLogger(__name__)


def create_front_tabs_list(
    tabs: List[CardTypes.FormattedTab],
) -> List[CardTypes.FormattedTab]:
    front_tabs = [tab for tab in tabs if tab["card side"] == "front"]
    if not front_tabs:
        raise CardError("A card without front tabs has been found.")
    return front_tabs


def get_swap_mappings(tabs: List[CardTypes.FormattedTab]) -> CardTypes.SwapMappings:
    """
    Create a dictionary with useful information on how
    to swap the tabs.

    Restore: back tabs that had the swap flag as True
        but have no matching front tab, so can't be swapped.
    Replace: A mapping (front tab: back tab) to replace the
        swapped front tab with the back tab.
    Remove: Unmatched front tabs or back tabs that replace
        front tabs (since these last ones are doubled,
        after replacing the front tab).
    """
    front_swap = []
    back_swap = []

    for index, tab in enumerate(tabs):
        if tab["card side"] == "front" and tab["swap"]:
            if are_clozes_in_card(tab["text"]):
                raise CardError("A tab that is to be swapped has a cloze in it.")

            front_swap.append(index)
        elif tab["card side"] == "back" and tab["swap"]:
            back_swap.append(index)

    smallest_list = min(front_swap, back_swap, key=len)
    common_length = len(smallest_list)

    to_replace: List[Tuple[int, int]] = [
        (front_swap[index], back_swap[index]) for index in range(common_length)
    ]

    # Sorted in reverse so that when you remove tabs, you start from the end of the list
    # and don't change the index of the tabs yet-to-be-removed
    to_remove = sorted(
        front_swap[common_length:] + back_swap[:common_length], reverse=True
    )

    # Keep the tabs that haven't been matched with a front-tab
    to_restore = back_swap[common_length:]

    return {"restore": to_restore, "replace": to_replace, "remove": to_remove}


def create_back_tabs_list(
    tabs: List[CardTypes.FormattedTab], swap_mappings: CardTypes.SwapMappings
) -> List[CardTypes.FormattedTab]:
    tabs_copy = tabs.copy()

    for index_of_tab_to_replace, index_of_tab_that_replaces in swap_mappings["replace"]:
        tabs_copy[index_of_tab_to_replace] = tabs_copy[index_of_tab_that_replaces]

    for index_of_tab_to_restore in swap_mappings["restore"]:
        tabs_copy[index_of_tab_to_restore]["swap"] = False

    for index_of_tab_to_remove in swap_mappings["remove"]:
        del tabs_copy[index_of_tab_to_remove]

    if not tabs_copy:
        raise CardError(
            "All front tabs have been swapped and the back side has no tabs left."
        )

    return tabs_copy


def format_tab_sides(tabs: List[CardTypes.FormattedTab]) -> CardTypes.TabSides:
    left_tabs = []
    right_tabs = []
    for tab in tabs:
        if tab["tab side"] == "left":
            left_tabs.append(tab["text"])
        else:
            right_tabs.append(tab["text"])

    return {"left": left_tabs, "right": right_tabs}


def get_swapped_card(tabs: List[CardTypes.FormattedTab]) -> CardTypes.CardWithTabs:
    front_tabs = create_front_tabs_list(tabs)
    swap_mappings = get_swap_mappings(tabs)
    back_tabs = create_back_tabs_list(tabs, swap_mappings)
    front_tabs_sides = format_tab_sides(front_tabs)
    back_tabs_sides = format_tab_sides(back_tabs)
    return {"front": front_tabs_sides, "back": back_tabs_sides}
