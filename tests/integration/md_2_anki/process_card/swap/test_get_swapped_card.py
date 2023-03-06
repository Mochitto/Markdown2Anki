from typing import List

from markdown2anki.md_2_anki.process_card.swap import get_swapped_card
from markdown2anki.md_2_anki.utils.card_types import FormattedTab


class TestGetSwappedCard:
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
        expected = {
            "front": {
                "left": [
                    '<section class="tab"><span class="tab__label">label two</span><div '
                    'class="tab__body"><h1>A great tab</h1>\n'
                    "<ul>\n"
                    "<li>has a great body</li>\n"
                    "</ul>\n"
                    "</div></section>"
                ],
                "right": [
                    '<section class="tab"><span class="tab__label">label '
                    'three</span><div class="tab__body"><p>Another tab</p>\n'
                    "</div></section>",
                ],
            },
            "back": {
                "left": [
                    '<section class="tab"><span class="tab__label">label one</span><div '
                    'class="tab__body"><p>This is the first tab body<br />\n'
                    "which spans two lines</p>\n"
                    "</div></section>"
                ],
                "right": [
                    '<section class="tab"><span class="tab__label">label '
                    'three</span><div class="tab__body"><p>Another tab</p>\n'
                    "</div></section>",
                    '<section class="tab"><span class="tab__label">label four</span><div '
                    'class="tab__body"><p>This tab has a body too</p>\n'
                    "</div></section>",
                ],
            },
        }
        assert get_swapped_card(test_input) == expected
