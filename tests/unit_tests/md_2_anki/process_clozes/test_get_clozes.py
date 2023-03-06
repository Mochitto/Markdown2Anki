import markdown2anki.md_2_anki.process_clozes as clozes


class TestGetClozes:
    def test_basic_case(self):
        content = (
            "This is a string with 2 {{c1::clozes}}.\n"
            + "Another line with another {{c2::cloze}}."
        )
        assert clozes.get_clozes(content) == [("1", "clozes"), ("2", "cloze")]

    def test_variation_case(self):
        """
        Check for high numbers and uppercase/lowercase "c".
        """
        content = (
            "This is a string with 2 {{C394::cloZe}}.\n"
            + "Another line, same {{C394::cloZe}}."
        )
        assert clozes.get_clozes(content) == [("394", "cloZe"), ("394", "cloZe")]

    def test_false_case(self):
        content = "This is a string with 2 {{c1:clozeS}}.\n" + "Another line."
        assert clozes.get_clozes(content) == []
