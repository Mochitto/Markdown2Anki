import logging
import re
import typing
from typing import List, Dict


import markdown2anki.md_2_anki.utils.common_types as Types
import markdown2anki.md_2_anki.utils.card_types as CardTypes
from markdown2anki.md_2_anki.utils.card_error import CardError
from markdown2anki.md_2_anki.process_card.format.wrappers import (
    wrap_tab,
    wrap_tab_body,
    wrap_tab_group,
    wrap_tab_label,
)
from markdown2anki.utils.debug_tools import expressive_debug

logger = logging.getLogger(__name__)


def format_tabs(tabs: List[CardTypes.HTMLTab]) -> List[CardTypes.FormattedTab]:
    formatted_tabs = [format_tab(tab) for tab in tabs]
    return formatted_tabs


def format_tab(tab: CardTypes.HTMLTab) -> CardTypes.FormattedTab:
    tab_copy = typing.cast(Dict, tab.copy())
    tab_label = tab_copy.pop("label")
    tab_body = tab_copy.pop("body")

    if not tab_label:
        raise CardError("There is a missing tab label.")
    if not tab_body:
        raise CardError("There is a tab without a body.")

    wrapped_label = wrap_tab_label(tab_label)
    wrapped_body = wrap_tab_body(tab_body)

    wrapped_tab = wrap_tab(wrapped_label, wrapped_body)

    tab_copy = typing.cast(CardTypes.FormattedTab, tab_copy)
    tab_copy["text"] = wrapped_tab

    return tab_copy


def format_tab_group(
    tabs_list: List[Types.HTMLString]
) -> Types.HTMLString:
    # Filter out empty tabs and copy the list
    tabs = [tab for tab in tabs_list if tab]

    if tabs:
        activated_tabs = activate_first_tab(tabs)
        joined_tabs = "".join(activated_tabs)

        tab_group = wrap_tab_group(joined_tabs)
        cleaned_tab_group = remove_newlines(tab_group)
    else:
        return ""

    return cleaned_tab_group


def activate_first_tab(tabs: List[Types.HTMLString]) -> List[Types.HTMLString]:
    new_tabs = tabs.copy()

    new_tabs[0] = re.sub(r'(class="tab)"', r'\1 tab--isactive"', new_tabs[0])
    return new_tabs


def remove_newlines(text: Types.HTMLString) -> Types.HTMLString:
    """Remove newlines from the text.
    This is needed because all the newlines INSIDE tags will become <br>, when needed.
    The remaining newlines are linked to the markdown input
    and become useless as block elements do not need them.
    """
    return re.sub(r"\n", "", text)
