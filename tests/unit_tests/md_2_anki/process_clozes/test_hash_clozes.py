import markdown2anki.md_2_anki.process_clozes as clozes


class TestHashClozes:
    def test_basic_case(self):
        content = (
            "This is a string with 2 {{c1::clozes}}.\n"
            + "Another line with another {{c2::cloze}}."
        )

        expected_hashed_clozes = {
            "something": ("1", "clozes"),
            "something else": ("2", "cloze"),
        }
        expected_length = len(expected_hashed_clozes.values())

        match_clozes = clozes.get_clozes(content)
        hashed_clozes = clozes.hash_clozes(match_clozes)
        length = len(hashed_clozes.values())

        difference = set(expected_hashed_clozes.values()) - set(hashed_clozes.values())

        assert not difference and expected_length == length

    def test_variation_case(self):
        """
        Check for high numbers and uppercase/lowercase "c".
        """
        content = (
            "This is a string with 2 {{C394::cloZe}}.\n"
            + "Another line, same {{C394::cloZe}}."
        )

        expected_hashed_clozes = {"something": ("394", "cloZe")}
        expected_length = len(expected_hashed_clozes.values())

        match_clozes = clozes.get_clozes(content)
        hashed_clozes = clozes.hash_clozes(match_clozes)

        length = len(hashed_clozes.values())
        difference = set(expected_hashed_clozes.values()) - set(
            hashed_clozes.values()
        )  # type:ignore

        assert not difference and expected_length == length

    def test_false_case(self):
        content = "This is a string with 2 {{c1:clozeS}}.\n" + "Another line."
        expected_hashed_clozes = {}
        expected_length = len(expected_hashed_clozes.values())

        match_clozes = clozes.get_clozes(content)
        hashed_clozes = clozes.hash_clozes(match_clozes)

        length = len(hashed_clozes.values())
        difference = set(expected_hashed_clozes.values()) - set(hashed_clozes.values())

        assert not difference and expected_length == length
