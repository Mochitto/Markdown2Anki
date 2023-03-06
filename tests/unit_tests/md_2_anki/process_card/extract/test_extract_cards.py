import pytest

from markdown2anki.md_2_anki.process_card.extract import extract_cards


class TestExtractCards:
    def test_cards_extraction(self):
        text = (
            "one card\n"
            "---\n"
            "another card\n"
            "--------------\n"
            "This is a card ---                \n"
            "---------\n"
            "------------\n"
            "                last card"
        )
        expected_output = [
            "one card",
            "another card",
            "This is a card ---",
            "last card",
        ]

        assert extract_cards(text) == expected_output

    def test_other_hr(self):
        text = "***\n" "------\n" "****"

        expected_output = ["***", "****"]

        assert extract_cards(text) == expected_output
