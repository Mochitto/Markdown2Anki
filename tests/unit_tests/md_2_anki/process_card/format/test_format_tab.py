import pytest

from markdown2anki.md_2_anki.process_card.format.formatters import format_tab
from markdown2anki.md_2_anki.utils.card_types import HTMLTab
from markdown2anki.md_2_anki.utils.card_error import CardError

class TestFormatTab:

    def test_good_case(self):
        tab: HTMLTab = {
            "tab_label": "A label",
            "tab_body": "<p>Hello world</p>"
            }
        expected_tab = (
            '<section class="tab">'
                '<span class="tab__label">A label</span>'
                '<div class="tab__body">'
                    '<p>Hello world</p>'
                '</div>'
            '</section>'
            )

        formatted_tab = format_tab(tab)
        assert formatted_tab == expected_tab

    def test_missing_label(self):
        tab: HTMLTab = {
            "tab_label": "",
            "tab_body": "<p>Hello world</p>"
            }
        with pytest.raises(CardError):
            format_tab(tab)

    def test_missing_body(self):
        tab: HTMLTab = {
            "tab_label": "A label",
            "tab_body": ""
            }
        with pytest.raises(CardError):
            format_tab(tab)

    def test_empty_tab(self):
        tab: HTMLTab = {
            "tab_label": "",
            "tab_body": ""
            }
        with pytest.raises(CardError):
            format_tab(tab)
