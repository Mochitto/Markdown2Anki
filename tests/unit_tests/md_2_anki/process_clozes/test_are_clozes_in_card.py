import markdown2anki.md_2_anki.process_clozes as clozes


class TestAreClozesInCards:
    def test_basic_case(self):
        content = "This is a string with 2 {{c1::clozes}}.\n" + "Another line."
        assert clozes.are_clozes_in_card(content) == True

    def test_variation_case(self):
        """
        Check for high numbers and uppercase/lowercase "c".
        """
        content = "This is a string with 2 {{C394::clozeS}}.\n" + "Another line."
        assert clozes.are_clozes_in_card(content) == True

    def test_false_case(self):
        content = "This is a string with 2 {{c1:clozeS}}.\n" + "Another line."
        assert clozes.are_clozes_in_card(content) == False
