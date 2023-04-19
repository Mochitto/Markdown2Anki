import markdown2anki.md_2_anki.process_clozes as clozes


class TestGetClozes:
    def test_basic_case(self):
        content = (
            "This is a string with 2 {{c1::clozes::with hint!}}.\n"
            + "Another line with another {{c2::cloze}}."
        )
        assert clozes.HandleClozes(content)._clozes == [
            "{{c1::clozes::with hint!}}",
            "{{c2::cloze}}",
        ]

    def test_variation_case(self):
        """
        Check for high numbers and uppercase/lowercase "c".
        """
        content = (
            "This is a string with 2 {{C394::cloZe}}.\n"
            + "Another line, same {{C394::cloZe}}."
        )
        assert clozes.HandleClozes(content)._clozes == [
            "{{C394::cloZe}}",
            "{{C394::cloZe}}",
        ]

    def test_false_case(self):
        content = "This is a string with 2 {{c1:clozeS}}.\n" + "Another line."
        assert clozes.HandleClozes(content)._clozes == []
