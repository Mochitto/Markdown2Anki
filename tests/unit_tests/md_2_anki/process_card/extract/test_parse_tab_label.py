import pytest

from markdown2anki.md_2_anki.process_card.extract import parse_tab_label
from markdown2anki.md_2_anki.utils.card_error import CardError


class TestExtractTabLabel:
    def test_happy_path(self):
        text = "## BL [label with words]"

        assert parse_tab_label(text) == ("BL", "label with words")

    def test_trimming(self):
        text = "## BL [           label with words         ]"

        assert parse_tab_label(text) == ("BL", "label with words")

    def test_multiline(self):
        text = "## BL [\nSomething]"

        with pytest.raises(TypeError):
            parse_tab_label(text)

    def test_empty_label(self):
        text = "## L- []"

        with pytest.raises(CardError):
            parse_tab_label(text)

    def test_label_with_sq_brackets(self):
        text = "## FL- [[label]]]"

        assert parse_tab_label(text) == ("FL-", "[label]]")

    def test_double_label(self):
        text = "## FL- [label] ## [label]"

        assert parse_tab_label(text) == ("FL-", "label] ## [label")

    def test_normal_line(self):
        text = "Something"

        assert parse_tab_label(text) == None

    def test_h3(self):
        text = "### FL [label]"

        assert parse_tab_label(text) == None

    def test_no_brackets(self):
        text = "## FL label"

        assert parse_tab_label(text) == None

    def test_missing_closing_bracket(self):
        text = "## FL [label"

        assert parse_tab_label(text) == None

    def test_h2(self):
        text = "##"

        assert parse_tab_label(text) == None

    def test_words_after_label(self):
        text = "## FL [label] something"

        assert parse_tab_label(text) == ("FL", "label")
