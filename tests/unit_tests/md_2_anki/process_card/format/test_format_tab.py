import pytest

from markdown2anki.md_2_anki.process_card.format.formatters import format_tab
from markdown2anki.md_2_anki.utils.card_types import HTMLTab
from markdown2anki.md_2_anki.utils.card_error import CardError


class TestFormatTab:
    def test_good_case(self):
        tab: HTMLTab = {
            "card side": "front",
            "tab side": "left",
            "swap": True,
            "label": "A label",
            "body": "<p>Hello world</p>",
        }
        expected_tab = {
            "card side": "front",
            "tab side": "left",
            "swap": True,
            "text": (
                '<section class="tab">'
                '<button class="tab__label"><span>A label</span></button>'
                '<div class="tab__body">'
                '<div class="tab__body__content">'
                "<p>Hello world</p>"
                "</div>"
                "</div>"
                "</section>"
            ),
        }

        formatted_tab = format_tab(tab)
        assert formatted_tab == expected_tab

    def test_missing_label(self):
        tab: HTMLTab = {
            "card side": "front",
            "tab side": "left",
            "swap": True,
            "label": "",
            "body": "<p>Hello world</p>",
        }
        with pytest.raises(CardError):
            format_tab(tab)

    def test_missing_body(self):
        tab: HTMLTab = {
            "card side": "front",
            "tab side": "left",
            "swap": True,
            "label": "A label",
            "body": "",
        }
        with pytest.raises(CardError):
            format_tab(tab)

    def test_empty_tab(self):
        tab: HTMLTab = {
            "card side": "front",
            "tab side": "left",
            "swap": True,
            "label": "",
            "body": "",
        }
        with pytest.raises(CardError):
            format_tab(tab)
