import pytest

from markdown2anki.md_2_anki.process_card.process_card import process_card
from markdown2anki.md_2_anki.utils.card_error import CardError


class TestProcessCard:

    # TODO: this calls for more specific errors
    # for each part of the processing (formatting error,
    # extracting error etc.)

    def test_good_case(self):
        md_input = """
        #Front side

        ## Left tabs

        ### First left tab
        Something

        # Back side

        ## Right tabs

        ### First right tab
        Something else
        """

        expected_output = {
            "back": '<section class="tab_group"><section class="tab tab--isactive"><span class="tab__label">First left tab</span><div class="tab__body"><p>Something</p></div></section></section><section class="tab_group"><section class="tab tab--isactive"><span class="tab__label">First right tab</span><div class="tab__body"><p>Something else</p></div></section></section>',
            "front": '<section class="tab_group"><section class="tab tab--isactive"><span class="tab__label">First left tab</span><div class="tab__body"><p>Something</p></div></section></section>',
        }

        result = process_card(md_input, "my vault")

        assert result == expected_output

    def test_missing_front_left_tabs(self):
        md_input = """
        #Front side

        ## Right tabs

        ### First left tab
        Something
        """

        with pytest.raises(CardError):
            process_card(md_input, "my vault")

    def test_missing_front_side_case(self):
        md_input = """
        #Right side

        ## Left tabs

        ### First left tab
        Something
        """

        with pytest.raises(CardError):
            process_card(md_input, "my vault")

    def test_tab_without_label_edge_case(self):
        md_input = """
        #Front side
        #Left side

        ## Left tabs

        ###
        Not a tab

        ### A tab
        Something else
        """

        with pytest.raises(CardError):
            # Notice: the current extraction makes it so that
            # This pattern considers "### Not a tab" a tab, so
            # the error is that of a tab without a body (which is wrong).
            # The right error would be a tab without label.
            process_card(md_input, "my vault")

    def test_tab_without_body_edge_case(self):
        md_input = """
        #Front side
        #Left side

        ## Left tabs

        ### A tab

        ### A tab
        Something else
        """

        with pytest.raises(CardError):
            process_card(md_input, "my vault")

    def test_missing_vault_edge_case(self):
        md_input = """
        #Front side

        ## Left tabs

        ### First left tab
        Something
        """

        with pytest.raises(CardError):
            process_card(md_input, "")
