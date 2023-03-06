import pytest

from markdown2anki.md_2_anki.process_card.extract import (
    extract_tabs_bodies,
    extract_tabs_labels,
)
from markdown2anki.md_2_anki.utils.card_error import CardError


class TestExtractTabBody:
    def test_happy_path(self):
        text = (
            "## B [label]\n"
            "This is the first tab body\n"
            "which spans two lines\n\n"
            "## - [label]\n"
            "# A great tab\n"
            "- has great body\n"
            "## R [label]\n"
            "Another tab\n\n"
            "## BR [label]\n"
            "This tab has a body too\n\n"
        )
        labels = [
            (0, "B", "label"),
            (4, "-", "label"),
            (7, "R", "label"),
            (10, "BR", "label"),
        ]
        expected_output = [
            ("B", "label", "This is the first tab body\nwhich spans two lines"),
            ("-", "label", "# A great tab\n- has great body"),
            ("R", "label", "Another tab"),
            ("BR", "label", "This tab has a body too"),
        ]

        assert extract_tabs_bodies(text, labels) == expected_output

    def test_tab_without_body(self):
        text = "## BL [label]\n" "## FL [label]\n" "This tab has a body"
        labels = [(0, "BL", "label"), (1, "FL", "label")]

        with pytest.raises(CardError):
            extract_tabs_bodies(text, labels)

    def test_single_tab(self):
        text = "## FL [label]\n" "This is the {{C1::body}}"
        labels = [(0, "FL", "label")]

        expected_output = [("FL", "label", "This is the {{C1::body}}")]

        assert extract_tabs_bodies(text, labels) == expected_output

    def test_trimming(self):
        text = (
            "## BL [label]\n\n\r\n                  "
            "This is the tab body\n         \n"
            "## FL [label]\n\n"
            "This tab has a body\n\n               "
        )
        labels = [(0, "BL", "label"), (5, "FL", "label")]
        expected_output = [
            ("BL", "label", "This is the tab body"),
            ("FL", "label", "This tab has a body"),
        ]

        assert extract_tabs_bodies(text, labels) == expected_output

    def test_empty_single_tab_edge_case(self):
        text = "## [label]"
        labels = [(0, "", "label")]

        with pytest.raises(CardError):
            extract_tabs_bodies(text, labels)

    def test_empty(self):
        text = ""
        labels = []
        expected_output = []

        assert extract_tabs_bodies(text, labels) == expected_output


if __name__ == "__main__":
    """
    When adding new tests, you can run the script
    as main to generate the labels input.
    """
    text = (
        "## BL [label]\n\n\r\n                  "
        "This is the tab body\n         \n"
        "## FL [label]\n\n"
        "This tab has a body\n\n               "
    )

    print(extract_tabs_labels(text))
