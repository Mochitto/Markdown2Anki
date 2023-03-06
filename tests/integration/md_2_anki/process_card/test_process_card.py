import pytest

from markdown2anki.md_2_anki.process_card import process_card
from markdown2anki.md_2_anki.utils.card_error import CardError


class TestProcessCard:

    # TODO: this calls for more specific errors
    # for each part of the processing (formatting error,
    # extracting error etc.)

    def test_good_case(self):
        md_input = (
        "## [First left tab]\n"
        "Something\n\n"
        "## BR [First right tab]\n"
        "Something else"
        )

        expected_output = {
            "back": '<section class="tab_group"><section class="tab tab--isactive"><span class="tab__label">First left tab</span><div class="tab__body"><p>Something</p></div></section></section><section class="tab_group"><section class="tab tab--isactive"><span class="tab__label">First right tab</span><div class="tab__body"><p>Something else</p></div></section></section>',
            "front": '<section class="tab_group"><section class="tab tab--isactive"><span class="tab__label">First left tab</span><div class="tab__body"><p>Something</p></div></section></section>',
        }

        result = process_card(md_input, "my vault")

        assert result == expected_output

    def test_missing_front_side_case(self):
        md_input = (
        "## BR [First left tab]\n"
        "Something"
        )

        with pytest.raises(CardError):
            process_card(md_input, "my vault")

    def test_tab_without_label_edge_case(self):
        md_input =(
        "## []\n"
        "Not a tab\n\n"
        "## [A tab]\n"
        "Something else"
        )

        with pytest.raises(CardError):
            process_card(md_input, "my vault")

    def test_tab_without_body_edge_case(self):
        md_input =(
        "## [A tab]\n"
        "## [A tab]\n"
        "Something else"
        )

        with pytest.raises(CardError):
            process_card(md_input, "my vault")

    def test_missing_vault_edge_case(self):
        md_input =(
        "## [A tab]\n"
        "With a text\n"
        "## [A tab]\n"
        "Something else"
        )

        with pytest.raises(CardError):
            process_card(md_input, "")
