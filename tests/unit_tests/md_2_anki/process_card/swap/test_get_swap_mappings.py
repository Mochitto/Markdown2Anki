from typing import List

import pytest

from markdown2anki.md_2_anki.process_card.swap import get_swap_mappings
from markdown2anki.md_2_anki.utils.card_types import FormattedTab
from markdown2anki.md_2_anki.utils.card_error import CardError


class TestGetSwapMappings:
    def test_happy_path(self):
        test_input: List[FormattedTab] = [
            {
                "card side": "back",
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
                "card side": "front",
                "swap": False,
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
                "text": '<section class="tab"><span class="tab__label">label '
                'three</span><div class="tab__body"><p>Another tab</p>\n'
                "</div></section>",
            },
        ]
        expected = {"remove": [0], "replace": [(1, 0)], "restore": [3]}
        assert get_swap_mappings(test_input) == expected

    def test_all_front_swap(self):
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

        expected = {"remove": [1, 0], "replace": [], "restore": []}
        assert get_swap_mappings(test_input) == expected

    def test_remove_cloze(self):
        test_input: List[FormattedTab] = [
            {
                "card side": "front",
                "swap": True,
                "tab side": "left",
                "text": '<section class="tab"><span class="tab__label">label one</span><div '
                'class="tab__body"><p>This is the {{C1::first}} tab body<br />\n'
                "which spans two lines</p>\n"
                "</div></section>",
            },
            {
                "card side": "front",
                "swap": False,
                "tab side": "right",
                "text": '<section class="tab"><span class="tab__label">label four</span><div '
                'class="tab__body"><p>This tab has a body too</p>\n'
                "</div></section>",
            },
        ]
        with pytest.raises(CardError):
            get_swap_mappings(test_input)
