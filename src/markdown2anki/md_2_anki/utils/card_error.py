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


def validate_card_data(card_data) -> None:
    """
    Raise an error if:
        - There are no left tabs in the front side of the card
        - There are no tabs to swap

    "# type: ignore" is needed when using dict keys dinamically, sadly.
    mypy issue: https://github.com/python/mypy/issues/7178
    """
    if not card_data["front"]["left_tabs"]:
        raise CardError("There are no left tabs in the front side of the card.")

    for side in ["left", "right"]:
        for index in card_data["front"][f"{side}_tabs_swap"]:  # type: ignore
            try:
                card_data["back"][f"{side}_tabs"][index]  # type: ignore
            except IndexError as error:
                raise CardError(
                    f"The {make_ordinal(index + 1)} tab on the front-{side} side has no"
                    + f"corresponding tab on the back-{side} side to be swapped with."
                ) from error


# TODO?: maybe move to an helper module
def make_ordinal(number: int) -> str:
    """
    Convert an integer into its ordinal representation:
    https://stackoverflow.com/a/50992575/19144535
    """
    number = int(number)
    if 11 <= (number % 100) <= 13:
        suffix = "th"
    else:
        suffix = ["th", "st", "nd", "rd", "th"][min(number % 10, 4)]
    return str(number) + suffix
