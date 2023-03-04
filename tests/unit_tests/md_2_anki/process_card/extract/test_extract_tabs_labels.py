import pytest

from markdown2anki.md_2_anki.process_card.extract.extract import extract_tabs_labels

class TestExtractTabsLabels:

    def test_happy_path(self):
        text = (
        "## [label]\n"
        "body\n"
        "## FL [label2]\n"
        "another body\n"
        )

        expected = [(0, "", "label"), (2, "FL", "label2")]

        assert extract_tabs_labels(text) == expected

    def test_no_labels(self):
        text = "something\nsomething else"

        assert extract_tabs_labels(text) == []
