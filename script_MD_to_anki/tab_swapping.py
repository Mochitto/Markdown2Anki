from typing import List

from card_error import CardError
import card_types as CardTypes 

def get_swapped_tabs(
    card_data: CardTypes.CardWithSwap) ->  CardTypes.CardWithTabs:
    """
    Take in card_data and return the swapped tabs.
    """

    front_left_tabs = card_data["front"]["left_tabs"]
    back_left_tabs = card_data["back"]["left_tabs"]
    left_tabs_to_swap = card_data["front"]["left_tabs_swap"]
    swapped_left_tabs = swap_tabs(front_left_tabs, back_left_tabs, left_tabs_to_swap, "left_tabs")


    front_right_tabs = card_data["front"]["right_tabs"]
    back_right_tabs = card_data["back"]["right_tabs"]
    right_tabs_to_swap = card_data["front"]["right_tabs_swap"]
    swapped_right_tabs = swap_tabs(front_right_tabs, back_right_tabs, right_tabs_to_swap, "right_tabs")

    return {
        "front": {
            "left_tabs": front_left_tabs,
            "right_tabs": front_right_tabs
        },
        "back": {
            "left_tabs": swapped_left_tabs,
            "right_tabs": swapped_right_tabs
        }
    }

def swap_tabs(
    front_tabs: List[str], 
    back_tabs: List[str], 
    tab_indices_to_swap: List[int], 
    side: str):
    # FIXME: Should tabs be swapped with one of the same index or with the first tab possible?
    # If you change this, make sure you also fix the back_left and back_right variables.

    front_tabs = front_tabs.copy()

    swapped_tabs = None
    if tab_indices_to_swap:
        if not back_tabs:
            tabs_to_swap = ', '.join(str(value) for value in tab_indices_to_swap)
            raise CardError(
                f"Supposed to swap a {side} tab (To swap: {tabs_to_swap}),"
                + f"but there's no tabs in the BACK {side} side.")

        try:
            swapped_front_tabs = [tab if tab_index not in tab_indices_to_swap 
                                else back_tabs[tab_index]
                                for tab_index, tab in enumerate(front_tabs)]
        except IndexError as err: # No matching index
            tabs_to_swap = ', '.join(str(value) for value in tab_indices_to_swap)
            raise CardError(
                f"Supposed to swap a {side} tab (To swap: {tabs_to_swap}),"
                + f"but there's no counterpart in the BACK {side} tabs.") from err

        back_tabs_remaining = [
            tab for tab_index, tab in enumerate(back_tabs)
            if tab_index not in tab_indices_to_swap
            ]

        swapped_tabs = swapped_front_tabs + back_tabs_remaining

    return swapped_tabs if swapped_tabs else front_tabs
