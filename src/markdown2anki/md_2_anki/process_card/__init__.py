import logging
from typing import Dict

import markdown2anki.md_2_anki.utils.common_types as Types
from markdown2anki.md_2_anki.utils.card_error import CardError
from markdown2anki.md_2_anki.process_card.compile import tabs_to_html
from markdown2anki.md_2_anki.process_card.extract import extract_tabs
from markdown2anki.md_2_anki.process_card.format.formatters import (
    format_tab_group,
    format_tabs,
)
from markdown2anki.md_2_anki.process_card.swap import get_swapped_card

from markdown2anki.utils.debug_tools import expressive_debug

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
    4. Swapping tabs (swap module)
    5. Formatting tab groups to match front-end specs (formatters module)
        and turning the tabs into one HTML string for each side.
    """

    if not vault:
        raise CardError("Missing obsidian vault name.")

    linenos_in_highlight = options.get("linenos", True)

    tabs = extract_tabs(markdown)
    compiled_tabs = tabs_to_html(tabs, vault, linenos=linenos_in_highlight)
    formatted_tabs = format_tabs(compiled_tabs)
    swapped_card = get_swapped_card(formatted_tabs)

    formatted_card = {"front": "", "back": ""}
    for card_side in swapped_card.keys():
        formatted_card[card_side] += format_tab_group(
            swapped_card[card_side]["left"]
        )
        formatted_card[card_side] += format_tab_group(
            swapped_card[card_side]["right"]
        )

    expressive_debug(logger, "Formatted card", formatted_card)
    return formatted_card
