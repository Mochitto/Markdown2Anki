from markdown2anki.md_2_anki.process_card.compile import tabs_to_html
import pprint

from typing import List

import pytest

from markdown2anki.md_2_anki.process_card.swap import (
    create_back_tabs_list,
    get_swap_mappings,
)
from markdown2anki.md_2_anki.process_card.format.formatters import format_tabs
from markdown2anki.md_2_anki.utils.card_types import FormattedTab
from markdown2anki.md_2_anki.utils.card_error import CardError


class TestCreateFrontTabsList:
    def test_happy_path(self):
        test_input: List[FormattedTab] = [
            {
                "card side": "back",
                "swap": True,
                "tab side": "left",
                "text": '<section class="tab"><span class="tab__label">label one</span><div '
                'class="tab__body"><p>This is the first tab body<br />\n'
                "which spans two lines</p>\n"
                "</div></section>",
            },
            {
                "card side": "front",
                "swap": True,
                "tab side": "left",
                "text": '<section class="tab"><span class="tab__label">label two</span><div '
                'class="tab__body"><h1>A great tab</h1>\n'
                "<ul>\n"
                "<li>has a great body</li>\n"
                "</ul>\n"
                "</div></section>",
            },
            {
                "card side": "front",
                "swap": False,
                "tab side": "right",
                "text": '<section class="tab"><span class="tab__label">label '
                'three</span><div class="tab__body"><p>Another tab</p>\n'
                "</div></section>",
            },
            {
                "card side": "back",
                "swap": True,
                "tab side": "right",
                "text": '<section class="tab"><span class="tab__label">label four</span><div '
                'class="tab__body"><p>This tab has a body too</p>\n'
                "</div></section>",
            },
        ]
        expected = [
            {
                "card side": "back",
                "swap": True,
                "tab side": "left",
                "text": '<section class="tab"><span class="tab__label">label one</span><div '
                'class="tab__body"><p>This is the first tab body<br />\n'
                "which spans two lines</p>\n"
                "</div></section>",
            },
            {
                "card side": "front",
                "swap": False,
                "tab side": "right",
                "text": '<section class="tab"><span class="tab__label">label '
                'three</span><div class="tab__body"><p>Another tab</p>\n'
                "</div></section>",
            },
            {
                "card side": "back",
                "swap": False,
                "tab side": "right",
                "text": '<section class="tab"><span class="tab__label">label four</span><div '
                'class="tab__body"><p>This tab has a body too</p>\n'
                "</div></section>",
            },
        ]
        mappings = get_swap_mappings(test_input)
        assert create_back_tabs_list(test_input, mappings) == expected

    def test_swapping_all_tabs(self):
        test_input: List[FormattedTab] = [
            {
                "card side": "back",
                "swap": True,
                "tab side": "left",
                "text": '<section class="tab"><span class="tab__label">label one</span><div '
                'class="tab__body"><p>This is the first tab body<br />\n'
                "which spans two lines</p>\n"
                "</div></section>",
            },
            {
                "card side": "front",
                "swap": True,
                "tab side": "left",
                "text": '<section class="tab"><span class="tab__label">label two</span><div '
                'class="tab__body"><h1>A great tab</h1>\n'
                "<ul>\n"
                "<li>has a great body</li>\n"
                "</ul>\n"
                "</div></section>",
            },
            {
                "card side": "back",
                "swap": True,
                "tab side": "right",
                "text": '<section class="tab"><span class="tab__label">label four</span><div '
                'class="tab__body"><p>This tab has a body too</p>\n'
                "</div></section>",
            },
            {
                "card side": "front",
                "swap": True,
                "tab side": "right",
                "text": '<section class="tab"><span class="tab__label">label '
                'three</span><div class="tab__body"><p>Another tab</p>\n'
                "</div></section>",
            },
        ]
        expected = [
            {
                "card side": "back",
                "swap": True,
                "tab side": "left",
                "text": '<section class="tab"><span class="tab__label">label one</span><div '
                'class="tab__body"><p>This is the first tab body<br />\n'
                "which spans two lines</p>\n"
                "</div></section>",
            },
            {
                "card side": "back",
                "swap": True,
                "tab side": "right",
                "text": '<section class="tab"><span class="tab__label">label four</span><div '
                'class="tab__body"><p>This tab has a body too</p>\n'
                "</div></section>",
            },
        ]
        mappings = get_swap_mappings(test_input)
        assert create_back_tabs_list(test_input, mappings) == expected

    def test_removing_front_tabs(self):
        test_input: List[FormattedTab] = [
            {
                "card side": "back",
                "swap": True,
                "tab side": "left",
                "text": '<section class="tab"><span class="tab__label">label one</span><div '
                'class="tab__body"><p>This is the first tab body<br />\n'
                "which spans two lines</p>\n"
                "</div></section>",
            },
            {
                "card side": "front",
                "swap": True,
                "tab side": "left",
                "text": '<section class="tab"><span class="tab__label">label two</span><div '
                'class="tab__body"><h1>A great tab</h1>\n'
                "<ul>\n"
                "<li>has a great body</li>\n"
                "</ul>\n"
                "</div></section>",
            },
            {
                "card side": "front",
                "swap": True,
                "tab side": "right",
                "text": '<section class="tab"><span class="tab__label">label '
                'three</span><div class="tab__body"><p>Another tab</p>\n'
                "</div></section>",
            },
            {
                "card side": "back",
                "swap": False,
                "tab side": "right",
                "text": '<section class="tab"><span class="tab__label">label four</span><div '
                'class="tab__body"><p>This tab has a body too</p>\n'
                "</div></section>",
            },
        ]
        expected = [
            {
                "card side": "back",
                "swap": True,
                "tab side": "left",
                "text": '<section class="tab"><span class="tab__label">label one</span><div '
                'class="tab__body"><p>This is the first tab body<br />\n'
                "which spans two lines</p>\n"
                "</div></section>",
            },
            {
                "card side": "back",
                "swap": False,
                "tab side": "right",
                "text": '<section class="tab"><span class="tab__label">label four</span><div '
                'class="tab__body"><p>This tab has a body too</p>\n'
                "</div></section>",
            },
        ]

        mappings = get_swap_mappings(test_input)
        assert create_back_tabs_list(test_input, mappings) == expected

    def test_removing_all_tabs(self):
        test_input: List[FormattedTab] = [
            {
                "card side": "front",
                "swap": True,
                "tab side": "left",
                "text": '<section class="tab"><span class="tab__label">label two</span><div '
                'class="tab__body"><h1>A great tab</h1>\n'
                "<ul>\n"
                "<li>has a great body</li>\n"
                "</ul>\n"
                "</div></section>",
            },
            {
                "card side": "front",
                "swap": True,
                "tab side": "right",
                "text": '<section class="tab"><span class="tab__label">label '
                'three</span><div class="tab__body"><p>Another tab</p>\n'
                "</div></section>",
            },
        ]
        mappings = get_swap_mappings(test_input)
        with pytest.raises(CardError):
            assert create_back_tabs_list(test_input, mappings)


if __name__ == "__main__":
    tabs = [
        {
            "body": "<p>This is the {{C1::first}} tab body<br />\nwhich spans two lines</p>\n",
            "card side": "front",
            "label": "label one",
            "swap": True,
            "tab side": "left",
        },
        {
            "body": "<p>This tab has a body too</p>\n",
            "card side": "front",
            "label": "label four",
            "swap": False,
            "tab side": "right",
        },
    ]

    pprint.pprint(format_tabs(tabs))
