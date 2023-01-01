import re
import logging

from typing import List

from card_error import CardError
import card_types as CardTypes
from logger import expressive_debug

logger = logging.getLogger(__name__)

def extract_cards(markdown_text: str) -> list[str]:
    """
    Extract the cards from the markdown file.
    The break points are "---+" and "***+". Return an array of strings (cards).
    """
    regex_pattern = r"\n(?:(?:---+?)|(?:\*\*\*+?))\n" # Match hr in markdown

    cards = re.split(regex_pattern, markdown_text)

    return cards

def extract_card_sides(card: str) -> CardTypes.CardSides:
    """
    Extract the text that is under the "Front side" and "Back side",
    return a dictionary with the two text blocks.
    "Back side" is optional.
    """
    stripped_card = card.strip()

    front_side_regex = re.compile(r"(?si)#\s*front\s*side\s*\n(.*?)(?:\#\s*back\s*side\s*\n|$)")
    back_side_regex = re.compile(r"(?si)#\s*back\s*side\s*\n(.*)")

    front_side_match = front_side_regex.search(stripped_card)
    back_side_match = back_side_regex.search(stripped_card)

    if not front_side_match[1]:
        raise CardError(f"A card without front-side has been found.")

    return {
        "front": front_side_match[1],
        "back": back_side_match[1] if back_side_match else ""
    }

def extract_tabs_sides(side_fragment: str) -> CardTypes.TabsSides:
    """Extract the text that is under the "left tabs" and "right tabs"."""
    stripped_fragment = side_fragment.strip()

    left_tabs_regex = re.compile(r"(?si)##\s*left\s*tabs\s*\n(.*?)(?=##\s*right\s*tabs|$)")
    right_tabs_regex = re.compile(r"(?si)##\s*right\s*tabs\s*\n(.*)")

    # The or is used to avoid IndexErrors and adding a try: except block
    left_tabs_block = re.search(left_tabs_regex, stripped_fragment) or [""] 
    right_tabs_block = re.search(right_tabs_regex, stripped_fragment) or [""]

    return {
        "left_tabs": left_tabs_block[0],
        "right_tabs": right_tabs_block[0] if right_tabs_block else ""
        }

def extract_tabs(left_or_right_block: str) -> CardTypes.TabsList:
    """Extact the tabs, their text and the indexes of tabs to be swapped."""

    tabs_regex = re.compile(r"###\s*(-)?(.+?)\n(.+?)(?=###|##|$)", re.S)

    tabs_matches = tabs_regex.findall(left_or_right_block)

    tabs = []
    tabs_to_switch = []
    for index, match in enumerate(tabs_matches):
        switch_flag = match[0]
        if switch_flag:
            tabs_to_switch.append(index)

        tab_label = match[1]
        tab_body = match[2]

        tabs.append({"tab_label": tab_label.strip(), "tab_body": tab_body.strip()})

    return {"tabs": tabs, "tabs_to_swap": tabs_to_switch}

def extract_clozes(text: str) -> List[CardTypes.ClozeType]:
    clozes_regex = re.compile(r"{{c(\d)::(.+?)}}", re.IGNORECASE)
    
    clozes_matches = clozes_regex.findall(text)

    return clozes_matches
