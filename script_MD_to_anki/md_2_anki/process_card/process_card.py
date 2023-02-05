import logging
from dataclasses import asdict
from typing import Dict, List

import md_2_anki.utils.card_types as Types
from md_2_anki.process_card.compile.text_to_html import tabs_to_html
from md_2_anki.process_card.extract.extract import (
    extract_card_sides,
    extract_tabs,
    extract_tabs_sides,
)
from md_2_anki.process_card.format.formatters import format_tab_group, format_tabs
from md_2_anki.process_card.swap.tab_swapping import get_swapped_tabs
from md_2_anki.utils.card_error import validate_card_data

from md_2_anki.utils.debug_tools import expressive_debug

logger = logging.getLogger(__name__)


def process_card(
    markdown: Types.MDString, vault, **options
) -> Dict[str, Types.HTMLString]:
    """
    Process a card in markdown to HTML.

    **options kwargs:
        linenos=True: add line numbers to the highlighted code

    The steps are:
    1. Extraction of data (matching with regex, from the extract module)
    2. Parsing each Tab's md and compiling to HTML (text_to_html module)
    3. Formatting the HTML Tab/s to match front-end specs (formatters module)
    4. Swapping tabs (tab_swapping module)
    5. Formatting tab groups to match front-end specs (formatters module)

    Returning dict:
    "front": HTMLString
    "back": HTMLString

    "# type: ignore" is needed when using dict keys dinamically, sadly.
    mypy issue: https://github.com/python/mypy/issues/7178
    """

    linenos_in_highlight = options.get("linenos", True)

    card_sides = extract_card_sides(markdown)

    card_data: Types.CardWithSwap = {
        "front": {
            "left_tabs": [],
            "left_tabs_swap": [],
            "right_tabs": [],
            "right_tabs_swap": [],
        },
        "back": {
            "left_tabs": [],
            "left_tabs_swap": [],
            "right_tabs": [],
            "right_tabs_swap": [],
        },
    }

    for side, side_content in asdict(card_sides).items():
        tabs_sides = extract_tabs_sides(side_content)

        for tab_side, tab_side_content in tabs_sides.items():
            if not tab_side_content:  # Non-empty tab side
                continue
            tabs_info = extract_tabs(tab_side_content)
            tabs: List[Types.MDTab] = tabs_info["tabs"]  # type: ignore
            html_tabs = tabs_to_html(tabs, vault, linenos_in_highlight)
            formatted_tabs = format_tabs(html_tabs)

            card_data[side][tab_side] = formatted_tabs  # type: ignore
            card_data[side][f"{tab_side}_swap"] = tabs_info["tabs_to_swap"]  # type: ignore

    validate_card_data(card_data)

    card_with_swapped_tabs = get_swapped_tabs(card_data)

    formatted_card = {"front": "", "back": ""}

    for side in asdict(card_sides).keys():
        formatted_card[side] += format_tab_group(card_with_swapped_tabs[side]["left_tabs"])  # type: ignore
        formatted_card[side] += format_tab_group(card_with_swapped_tabs[side]["right_tabs"])  # type: ignore

    return formatted_card
