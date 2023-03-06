import markdown2anki.md_2_anki.process_clozes as clozes


class TestCleanCodeFromClozes:
    def test_basic_case(self):
        content = (
            "This is a string with 2 {{c1::clozes}}.\n"
            + "Another line with another {{c2::cloze}}."
        )
        cleaned_content = (
            "This is a string with 2 clozes.\n" + "Another line with another cloze."
        )

        assert clozes.clean_code_from_clozes(content) == cleaned_content

    def test_variation_case(self):
        """
        Check for high numbers and uppercase/lowercase "c".
        """
        content = (
            "This is a string with 2 {{C394::cloZe}}.\n"
            + "Another line, same {{C394::cloZe}}."
        )
        cleaned_content = (
            "This is a string with 2 cloZe.\n" + "Another line, same cloZe."
        )
        assert clozes.clean_code_from_clozes(content) == cleaned_content

    def test_false_case(self):
        content = "This is a string with 2 {{c1:clozeS}}.\n" + "Another line."
        assert clozes.clean_code_from_clozes(content) == content
