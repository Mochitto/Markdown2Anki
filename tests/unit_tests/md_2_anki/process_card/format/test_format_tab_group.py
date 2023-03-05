from typing import List

import pytest

from markdown2anki.md_2_anki.process_card.format.formatters import format_tab_group
from markdown2anki.md_2_anki.utils.common_types import HTMLString
from markdown2anki.md_2_anki.utils.card_error import CardError


class TestFormatTabGroup:
    def test_good_case(self):
        formatted_tabs: List[HTMLString] = [
            (
                '<section class="tab">'
                '<span class="tab__label">A label</span>'
                '<div class="tab__body">'
                "<p>Hello world</p>"
                "</div>"
                "</section>"
            ),
            (
                '<section class="tab">'
                '<span class="tab__label">Another label</span>'
                '<div class="tab__body">'
                "<p>Hello world</p>"
                "</div>"
                "</section>"
            ),
        ]
        expected_grouped_tabs = (
            '<section class="tab_group">'
            '<section class="tab tab--isactive">'
            '<span class="tab__label">A label</span>'
            '<div class="tab__body"><p>Hello world</p></div>'
            "</section>"
            '<section class="tab">'
            '<span class="tab__label">Another label</span>'
            '<div class="tab__body"><p>Hello world</p></div>'
            "</section>"
            "</section>"
        )

        grouped_tabs = format_tab_group(formatted_tabs)
        assert grouped_tabs == expected_grouped_tabs

    def test_empty_case(self):
        formatted_tabs: List[HTMLString] = []
        expected_grouped_tabs = ""

        grouped_tabs = format_tab_group(formatted_tabs)
        assert grouped_tabs == expected_grouped_tabs

    def test_first_empty_corner_case(self):
        formatted_tabs: List[HTMLString] = [
            "",
            (
                '<section class="tab">'
                '<span class="tab__label">A label</span>'
                '<div class="tab__body">'
                "<p>Hello world</p>"
                "</div>"
                "</section>"
            ),
            (
                '<section class="tab">'
                '<span class="tab__label">Another label</span>'
                '<div class="tab__body">'
                "<p>Hello world</p>"
                "</div>"
                "</section>"
            ),
        ]
        expected_grouped_tabs = (
            '<section class="tab_group">'
            '<section class="tab tab--isactive">'
            '<span class="tab__label">A label</span>'
            '<div class="tab__body"><p>Hello world</p></div>'
            "</section>"
            '<section class="tab">'
            '<span class="tab__label">Another label</span>'
            '<div class="tab__body"><p>Hello world</p></div>'
            "</section>"
            "</section>"
        )

        grouped_tabs = format_tab_group(formatted_tabs)
        assert grouped_tabs == expected_grouped_tabs

    def test_empty_tabs_corner_case(self):
        formatted_tabs: List[HTMLString] = [
            "",
            (
                '<section class="tab">'
                '<span class="tab__label">A label</span>'
                '<div class="tab__body">'
                "<p>Hello world</p>"
                "</div>"
                "</section>"
            ),
            "",
            (
                '<section class="tab">'
                '<span class="tab__label">Another label</span>'
                '<div class="tab__body">'
                "<p>Hello world</p>"
                "</div>"
                "</section>"
            ),
            "",
            "",
        ]
        expected_grouped_tabs = (
            '<section class="tab_group">'
            '<section class="tab tab--isactive">'
            '<span class="tab__label">A label</span>'
            '<div class="tab__body"><p>Hello world</p></div>'
            "</section>"
            '<section class="tab">'
            '<span class="tab__label">Another label</span>'
            '<div class="tab__body"><p>Hello world</p></div>'
            "</section>"
            "</section>"
        )

        grouped_tabs = format_tab_group(formatted_tabs)
        assert grouped_tabs == expected_grouped_tabs
