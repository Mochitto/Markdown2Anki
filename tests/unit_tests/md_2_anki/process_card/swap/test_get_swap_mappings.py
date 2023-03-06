from typing import List

import pytest

from markdown2anki.md_2_anki.process_card.swap import get_swap_mappings
from markdown2anki.md_2_anki.utils.card_types import HTMLTab
from markdown2anki.md_2_anki.utils.card_error import CardError


class TestGetSwapMappings:

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
        expected = {
            "remove": [1],
            "replace": [(1, 0)],
            "restore": [3]
            }
        assert get_swap_mappings(test_input) == expected

    def test_more_front_swap(self):
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
                "swap": False,
                "tab side": "right",
            },
        ]
        expected = {
            "remove": [0],
            "replace": [],
            "restore": []
            }
        assert get_swap_mappings(test_input) == expected

    # def test_remove_all_without_replace(self):
    #     test_input: List[HTMLTab] = [
    #         {
    #             "body": "<p>This is the first tab body<br />\nwhich spans two lines</p>\n",
    #             "card side": "front",
    #             "label": "label one",
    #             "swap": True,
    #             "tab side": "left",
    #         },
    #         {
    #             "body": "<p>This tab has a body too</p>\n",
    #             "card side": "front",
    #             "label": "label four",
    #             "swap": True,
    #             "tab side": "right",
    #         },
    #     ]

    #     with pytest.raises(CardError):
    #         get_swap_mappings(test_input)

    def test_remove_cloze(self):
        test_input: List[HTMLTab] = [
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

        with pytest.raises(CardError):
            get_swap_mappings(test_input)
