from typing import List

import pytest

from markdown2anki.md_2_anki.process_card.format.formatters import (
    format_tabs,
    format_tab_group,
)
from markdown2anki.md_2_anki.process_card.swap import get_swapped_card
from markdown2anki.md_2_anki.utils.card_types import HTMLTab
from markdown2anki.md_2_anki.utils.card_error import CardError


class TestFormatting:
    def test_good_case(self):
        tabs_list: List[HTMLTab] = [
            {
                "card side": "front",
                "tab side": "left",
                "swap": False,
                "label": "A label",
                "body": "<p>Hello world</p>",
            },
            {
                "card side": "front",
                "tab side": "left",
                "swap": False,
                "label": "Another label",
                "body": "<p>Hello world</p>",
            },
        ]

        expected_formatted_tab_group = (
            '<section class="tab_group">'
            '<section class="tab tab--isactive">'
            '<button class="tab__label"><span>A label</span></button>'
            '<div class="tab__body"><div class="tab__body__content"><p>Hello world</p></div></div>'
            "</section>"
            '<section class="tab">'
            '<button class="tab__label"><span>Another label</span></button>'
            '<div class="tab__body"><div class="tab__body__content"><p>Hello world</p></div></div>'
            "</section>"
            "</section>"
        )

        formatted_tabs = format_tabs(tabs_list)
        swapped_tabs = get_swapped_card(formatted_tabs)
        tab_group = format_tab_group(swapped_tabs["front"]["left"])
        assert tab_group == expected_formatted_tab_group

    def test_broken_tab(self):
        tabs_list: List[HTMLTab] = [
            {
                "card side": "front",
                "tab side": "left",
                "swap": True,
                "label": "",
                "body": "<p>Hello world</p>",
            },
            {
                "card side": "front",
                "tab side": "left",
                "swap": True,
                "label": "Another label",
                "body": "<p>Hello world</p>",
            },
        ]

        with pytest.raises(CardError):
            format_tabs(tabs_list)
