import logging
import re
from typing import Dict, List, Tuple

import markdown2anki.md_2_anki.utils.card_dataclasses as Dataclasses
import markdown2anki.md_2_anki.utils.common_types as Types
import markdown2anki.md_2_anki.utils.card_types as CardTypes
from markdown2anki.md_2_anki.utils.card_error import CardError
from markdown2anki.utils.debug_tools import expressive_debug

logger = logging.getLogger(__name__)

def extract_cards(text: Types.MDString) -> List[str]:
    """
    Extract cards from the given text, by splitting
    it at each occurrance of the markdown hr (only with -).
    Return a list of what is between the hrs, after it has
    been stripped.
    """
    regex_pattern = r"(?m)^(?:---+?)$"  # Match hr in markdown

    cards = re.split(regex_pattern, text)

    # Remove empty cards
    filtered_cards = [
            card.strip() 
            for card in cards 
            if card.strip()
            ] 

    return filtered_cards

def parse_flags(flags: str) -> Tuple[str, str, bool]:
    """
    Parse the given tab flags and return a
    tuple containing (card side, tab side, swap?).
    """
    card_side = "front"
    tab_side = "left"
    swap = False

    normalized_flags = flags.upper()
    if "B" in normalized_flags and "F" not in normalized_flags:
        card_side = "back"
    if "R" in normalized_flags and "L" not in normalized_flags:
        tab_side = "right"
    if "-" in normalized_flags or "+" in normalized_flags:
        swap = True

    return (card_side, tab_side, swap)
    
def parse_tab_label(line: Types.MDString) -> Tuple[str, str]|None:
    """
    Parse out flags and tab label from the given line.
    The given string MUST NOT be multiline.
    Return (flags, label).
    If the line doesn't match the pattern, return None.
    """
    # Make sure the input is not multiline
    newline_regex = re.compile(r"(\r\n|\r|\n)")
    if re.search(newline_regex, line): 
        raise TypeError("A multiline line has been fed to parse_tab_label.")

    flags = ""
    label = ""
    
    # Parser --- 
    is_octothorpe = lambda char: char == "#"
    is_open_sq_bracket = lambda char: char == "["
    if_closed_sq_bracket = lambda char: char == "]"

    found_open_sq_bracket = False
    found_closed_sq_bracket = False
    temporary_label = ""
    # This allows multiple ] to be present and to
    # keep just the last, while throwing away
    # what could come after the last ].

    for index, letter in enumerate(line):
        if index < 2:
            if not is_octothorpe(letter):
                return None
        elif index == 2:
            if is_octothorpe(letter):
                return None
        elif not found_open_sq_bracket:
            if is_open_sq_bracket(letter):
                found_open_sq_bracket = True
                continue
            flags += letter
        else:
            if if_closed_sq_bracket(letter):
                found_closed_sq_bracket = True
                label += temporary_label 
                temporary_label = "]"
                # This ensures that if there are
                # extra ], they are added to label.
                continue
            temporary_label += letter

    cleaned_flags = flags.strip()
    cleaned_label = label.strip()

    # There was nothing between the [] (or only whitespaces).
    if not cleaned_label and found_closed_sq_bracket:
        raise CardError("A tab without label has been found.")
    # There was no label block/no closing bracket
    if not cleaned_label:
        return None 

    return cleaned_flags, cleaned_label

def extract_tabs_labels(text: Types.MDString) -> List[Tuple[int, str, str]]:
    result = [] 
    
    for line_number, line in enumerate(text.splitlines()):
        tab = parse_tab_label(line)
        if tab:
            result.append((line_number, tab[0], tab[1]))

    return result

def extract_tabs_bodies(text: Types.MDString, tab_labels: List[Tuple[int, str, str]]) -> List[Tuple[str, str, str]]:
    """
    Use the tab labels line numbers to get
    the text between tabs (tab bodies).
    Return a list of (tab_flags, tab_label, tab_body).
    """
    result = []
    text_lines = text.splitlines()

    number_of_text_lines = len(text_lines)
    number_of_tabs = len(tab_labels)

    for index, (tab_line, tab_flags, tab_label) in enumerate(tab_labels):
        if tab_line+1 > number_of_text_lines-1:
            raise CardError("A tab without body has been found.")
        elif index < number_of_tabs-1:
            next_tab_line = tab_labels[index+1][0]
            tab_body = "\n".join(text_lines[tab_line+1: next_tab_line])
        else:
            tab_body = "\n".join(text_lines[tab_line+1:])

        if not tab_body:
            raise CardError("A tab without body has been found.")

        result.append((
            tab_flags,
            tab_label,
            tab_body.strip()
            ))

    return result


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

    front_side_regex = re.compile(
        r"(?si)#\s*front\s*side\s*\n(.*?)(?:\#\s*back\s*side\s*\n|$)"
    )
    back_side_regex = re.compile(r"(?si)#\s*back\s*side\s*\n(.*)")

    front_side_match = front_side_regex.search(stripped_card)
    back_side_match = back_side_regex.search(stripped_card)

    return Dataclasses.MDCard(
        front=front_side_match[1] if front_side_match else "",
        back=back_side_match[1] if back_side_match else "",
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

    left_tabs_regex = re.compile(
        r"(?si)##\s*left\s*tabs\s*\n(.*?)(?=##\s*right\s*tabs|$)"
    )
    right_tabs_regex = re.compile(r"(?si)##\s*right\s*tabs\s*\n(.*)")

    left_tabs_block = re.search(left_tabs_regex, stripped_fragment)
    right_tabs_block = re.search(right_tabs_regex, stripped_fragment)

    return {
        "left_tabs": left_tabs_block[1] if left_tabs_block else "",
        "right_tabs": right_tabs_block[1] if right_tabs_block else "",
    }


def extract_tabs(
    left_or_right_block: Types.MDString,
) -> Dict[str, List[CardTypes.MDTab] | List[int]]:
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

    tabs: List[CardTypes.MDTab] = []
    tabs_to_switch: List[int] = []
    for index, match in enumerate(tabs_matches):
        switch_flag = match[0]
        if switch_flag:
            tabs_to_switch.append(index)

        tab_label = match[1]
        tab_body = match[2]

        tabs.append({"tab_label": tab_label.strip(), "tab_body": tab_body.strip()})

    return {"tabs": tabs, "tabs_to_swap": tabs_to_switch}
