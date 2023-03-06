import logging
import re
from typing import List, Tuple

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
    filtered_cards = [card.strip() for card in cards if card.strip()]

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


def parse_tab_label(line: Types.MDString) -> Tuple[str, str] | None:
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


def extract_tabs_bodies(
    text: Types.MDString, tab_labels: List[Tuple[int, str, str]]
) -> List[Tuple[str, str, str]]:
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
        if tab_line + 1 > number_of_text_lines - 1:
            raise CardError("A tab without body has been found.")
        elif index < number_of_tabs - 1:
            next_tab_line = tab_labels[index + 1][0]
            tab_body = "\n".join(text_lines[tab_line + 1 : next_tab_line])
        else:
            tab_body = "\n".join(text_lines[tab_line + 1 :])

        if not tab_body:
            raise CardError("A tab without body has been found.")

        result.append((tab_flags, tab_label, tab_body.strip()))

    return result


def extract_tabs(text: Types.MDString) -> List[CardTypes.MDTab]:
    result = []
    tab_labels_information = extract_tabs_labels(text)
    tabs_with_bodies = extract_tabs_bodies(text, tab_labels_information)

    for tab_flags, tab_label, tab_body in tabs_with_bodies:
        card_side, tab_side, swap = parse_flags(tab_flags)
        result.append(
            {
                "card side": card_side,
                "tab side": tab_side,
                "swap": swap,
                "label": tab_label,
                "body": tab_body,
            }
        )

    return result
