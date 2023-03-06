from markdown2anki.md_2_anki.process_card.compile.text_to_html import tabs_to_html
import pprint

from typing import List

import pytest

from markdown2anki.md_2_anki.process_card.swap import create_back_tabs_list, get_swap_mappings
from markdown2anki.md_2_anki.utils.card_types import HTMLTab
from markdown2anki.md_2_anki.utils.card_error import CardError


class TestCreateFrontTabsList:

    def test_happy_path(self):
        test_input: List[HTMLTab] = [
            {
                "body": "<p>This is the first tab body<br />\nwhich spans two lines</p>\n",
                "card side": "back",
                "label": "label one",
                "swap": True,
                "tab side": "left",
            },
            {
                "body": "<h1>A great tab</h1>\n<ul>\n<li>has a great body</li>\n</ul>\n",
                "card side": "front",
                "label": "label two",
                "swap": True,
                "tab side": "left",
            },
            {
                "body": "<p>Another tab</p>\n",
                "card side": "front",
                "label": "label three",
                "swap": False,
                "tab side": "right",
            },
            {
                "body": "<p>This tab has a body too</p>\n",
                "card side": "back",
                "label": "label four",
                "swap": True,
                "tab side": "right",
            },
        ]
        expected = [
            {
                "body": "<p>This is the first tab body<br />\nwhich spans two lines</p>\n",
                "card side": "back",
                "label": "label one",
                "swap": True,
                "tab side": "left",
            },
            {
                "body": "<p>Another tab</p>\n",
                "card side": "front",
                "label": "label three",
                "swap": False,
                "tab side": "right",
            },
            {
                "body": "<p>This tab has a body too</p>\n",
                "card side": "back",
                "label": "label four",
                "swap": False,
                "tab side": "right",
            },
        ]        
        mappings = get_swap_mappings(test_input)
        assert create_back_tabs_list(test_input, mappings) == expected

    def test_swapping_all_tabs(self):
        test_input: List[HTMLTab] = [
            {
                "body": "<p>This is the first tab body<br />\nwhich spans two lines</p>\n",
                "card side": "back",
                "label": "label one",
                "swap": True,
                "tab side": "left",
            },
            {
                "body": "<h1>A great tab</h1>\n<ul>\n<li>has a great body</li>\n</ul>\n",
                "card side": "front",
                "label": "label two",
                "swap": True,
                "tab side": "left",
            },
            {
                "body": "<p>This tab has a body too</p>\n",
                "card side": "back",
                "label": "label four",
                "swap": True,
                "tab side": "right",
            },
            {
                "body": "<p>Another tab</p>\n",
                "card side": "front",
                "label": "label three",
                "swap": True,
                "tab side": "right",
            },
        ]
        expected = [
            {
                "body": "<p>This is the first tab body<br />\nwhich spans two lines</p>\n",
                "card side": "back",
                "label": "label one",
                "swap": True,
                "tab side": "left",
            },
            {
                "body": "<p>This tab has a body too</p>\n",
                "card side": "back",
                "label": "label four",
                "swap": True,
                "tab side": "right",
            },
        ]        
        mappings = get_swap_mappings(test_input)
        assert create_back_tabs_list(test_input, mappings) == expected

    def test_removing_front_tabs(self):
        test_input: List[HTMLTab] = [
            {
                "body": "<p>This is the first tab body<br />\nwhich spans two lines</p>\n",
                "card side": "back",
                "label": "label one",
                "swap": True,
                "tab side": "left",
            },
            {
                "body": "<h1>A great tab</h1>\n<ul>\n<li>has a great body</li>\n</ul>\n",
                "card side": "front",
                "label": "label two",
                "swap": True,
                "tab side": "left",
            },
            {
                "body": "<p>Another tab</p>\n",
                "card side": "front",
                "label": "label three",
                "swap": True,
                "tab side": "right",
            },
            {
                "body": "<p>This tab has a body too</p>\n",
                "card side": "back",
                "label": "label four",
                "swap": False,
                "tab side": "right",
            },
        ]
        expected = [
            {
                "body": "<p>This is the first tab body<br />\nwhich spans two lines</p>\n",
                "card side": "back",
                "label": "label one",
                "swap": True,
                "tab side": "left",
            },
            {
                "body": "<p>This tab has a body too</p>\n",
                "card side": "back",
                "label": "label four",
                "swap": False,
                "tab side": "right",
            },
        ]
        
        mappings = get_swap_mappings(test_input)
        assert create_back_tabs_list(test_input, mappings) == expected

    def test_removing_all_tabs(self):
        test_input: List[HTMLTab] = [
            {
                "body": "<h1>A great tab</h1>\n<ul>\n<li>has a great body</li>\n</ul>\n",
                "card side": "front",
                "label": "label two",
                "swap": True,
                "tab side": "left",
            },
            {
                "body": "<p>Another tab</p>\n",
                "card side": "front",
                "label": "label three",
                "swap": True,
                "tab side": "right",
            },
        ]
        mappings = get_swap_mappings(test_input)
        with pytest.raises(CardError):
            assert create_back_tabs_list(test_input, mappings)

if __name__ == "__main__":
    text = []

    pprint.pprint(tabs_to_html(text, ""))
