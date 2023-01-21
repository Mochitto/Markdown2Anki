import logging
import re
from typing import Dict, List

import card_dataclasses as Dataclasses
import card_types as Types
from debug_tools import expressive_debug

logger = logging.getLogger(__name__)


def extract_card_sides(card: Types.MDString) -> Dataclasses.MDCard:
    """
    Extract the text that is under the "Front side" and "Back side",
    return a dictionary with the two text blocks.
    "Back side" is optional.

    Pattern (same for backside):
    # frontside
    something

    #fRoNtSiDe
    something

    # Front Side
    something
    """
    stripped_card = card.strip()

    front_side_regex = re.compile(r"(?si)#\s*front\s*side\s*\n(.*?)(?:\#\s*back\s*side\s*\n|$)")
    back_side_regex = re.compile(r"(?si)#\s*back\s*side\s*\n(.*)")

    front_side_match = front_side_regex.search(stripped_card)
    back_side_match = back_side_regex.search(stripped_card)

    return Dataclasses.MDCard(
        front=front_side_match[1] if front_side_match else "", back=back_side_match[1] if back_side_match else ""
    )


def extract_tabs_sides(side_fragment: Types.MDString) -> Dict[str, Types.MDString]:
    """
    Extract the text that is under the "left tabs" and "right tabs".

    Dict:
    "left_tabs": MDString
    "right_tabs": MDString

    Pattern (same for right tabs):
    ## lefttabs
    something

    ##LeFtTabS
    something

    ## Left Tabs
    something
    """
    stripped_fragment = side_fragment.strip()

    left_tabs_regex = re.compile(r"(?si)##\s*left\s*tabs\s*\n(.*?)(?=##\s*right\s*tabs|$)")
    right_tabs_regex = re.compile(r"(?si)##\s*right\s*tabs\s*\n(.*)")

    left_tabs_block = re.search(left_tabs_regex, stripped_fragment)
    right_tabs_block = re.search(right_tabs_regex, stripped_fragment)

    return {
        "left_tabs": left_tabs_block[1] if left_tabs_block else "",
        "right_tabs": right_tabs_block[1] if right_tabs_block else "",
    }


def extract_tabs(left_or_right_block: Types.MDString) -> Dict[str, List[Types.MDTab] | List[int]]:
    """
    Extact tabs and the indexes of those to be swapped.

    Dict:
    "tabs": List[MDTab]
    "tabs_to_swap: list[int]

    Pattern:
    ### Something
    something

    ### -Something
    something

    ###-Something
    something

    Match until: ### | ## | $
    """

    tabs_regex = re.compile(r"(?s)###\s*(-)?(.+?)\n(.+?)(?=###|##|$)")

    tabs_matches = tabs_regex.findall(left_or_right_block)

    tabs: List[Types.MDTab] = []
    tabs_to_switch: List[int] = []
    for index, match in enumerate(tabs_matches):
        switch_flag = match[0]
        if switch_flag:
            tabs_to_switch.append(index)

        tab_label = match[1]
        tab_body = match[2]

        tabs.append({"tab_label": tab_label.strip(), "tab_body": tab_body.strip()})

    return {"tabs": tabs, "tabs_to_swap": tabs_to_switch}
