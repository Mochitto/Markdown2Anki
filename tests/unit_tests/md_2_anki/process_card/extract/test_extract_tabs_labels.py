import pytest

from markdown2anki.md_2_anki.process_card.extract import extract_tabs_labels


class TestExtractTabsLabels:
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
        expected = [
            (0, "B", "label"),
            (4, "-", "label"),
            (7, "R", "label"),
            (10, "BR", "label"),
        ]

        assert extract_tabs_labels(text) == expected

    def test_no_labels(self):
        text = "something\nsomething else"

        assert extract_tabs_labels(text) == []
