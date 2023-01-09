import logging
import re
from typing import Dict

import card_types as Types
from debug_tools import expressive_debug

logger = logging.getLogger(__name__)


class CardError(Exception):
    """Errors related to the parsing of the card."""
    def __init__(self, message):
        self.message = message

    def __str__(self):
        error_message = f"{self.message}"
        return error_message

def validate_card_data(card_data: Types.CardWithSwap) -> None:
    """
    Raise an error if:
        - There are no left tabs in the front side of the card
        - There are no tabs to swap

    "# type: ignore" is needed when using dict keys dinamically, sadly.
    mypy issue: https://github.com/python/mypy/issues/7178
    """
    if not (card_data["front"]["left_tabs"]):
        raise CardError("There are no left tabs in the front side of the card.")

    for side in ["left", "right"]:
        for index in card_data["front"][f"{side}_tabs_swap"]: # type: ignore
            try:
                card_data["back"][f"{side}_tabs"][index] # type: ignore
            except IndexError as error:
                raise CardError(
                    f"The {make_ordinal(index + 1)} tab on the front-{side} side has no corresponding "
                    + f"tab on the back-{side} side to be swapped with.") from error

def make_ordinal(n:int) -> str:
    '''
    Convert an integer into its ordinal representation:
    https://stackoverflow.com/a/50992575/19144535
    '''
    #TODO?: maybe move to an helper module
    n = int(n)
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    else:
        suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    return str(n) + suffix

# FIXME maybe?: maybe this is not the best place where to have this function
def are_clozes_in_card(card: Dict[str, Types.HTMLString]) -> bool:
    """
    Check if in the front of the card there is at least one cloze

    Dict:
    "front": HTMLString
    "back": HTMLString

    Pattern:
    {{c1::something}}
    {{C5::something else}}
    """
    clozes_regex = re.compile(r"{{c(\d)::(.+?)}}")
    front = card["front"]

    return bool(clozes_regex.search(front))
    