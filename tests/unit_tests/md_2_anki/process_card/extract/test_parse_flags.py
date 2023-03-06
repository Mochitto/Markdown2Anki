import pytest

from markdown2anki.md_2_anki.process_card.extract import parse_flags


class TestParseFlags:
    def test_no_flags(self):
        assert parse_flags("") == ("front", "left", False)

    def test_no_card_side(self):
        assert parse_flags("L") == ("front", "left", False)
        assert parse_flags("R") == ("front", "right", False)

    def test_no_tab_side(self):
        assert parse_flags("F") == ("front", "left", False)
        assert parse_flags("B") == ("back", "left", False)

    def test_case_insensitive(self):
        assert parse_flags("-Fl") == ("front", "left", True)
        assert parse_flags("+rB") == ("back", "right", True)

    def test_repeated_flags(self):
        assert parse_flags("-----------BBBBBBBBBBBBLLLLLLLLLLL") == (
            "back",
            "left",
            True,
        )

    def test_random_extra_letters(self):
        assert parse_flags("AJASDKJB_+ASL") == ("back", "left", True)

    def test_flags_precendence(self):
        assert parse_flags("+-FBLR") == ("front", "left", True)
