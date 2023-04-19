import markdown2anki.md_2_anki.process_clozes as clozes


class TestClozesProcessing:
    def test_basic_case(self):
        content = (
            "This is a string with 2 {{c1::clozes::with hints!}}.\n"
            + "Another line with another {{c2::cloze}}."
        )

        assert clozes.are_clozes_in_card(content)
        cloze_handler = clozes.HandleClozes(content)

        card = {"front": cloze_handler.hashed_markdown, "back": ""}
        processed_card = cloze_handler.inject_clozes(card)

        assert processed_card["front"] == content

    def test_single_letter_case(self):
        content = (
                "This is a cloze with a single letter {c1::a}"
        )

        assert clozes.are_clozes_in_card(content)
        cloze_handler = clozes.HandleClozes(content)

        card = {"front": cloze_handler.hashed_markdown, "back": ""}
        processed_card = cloze_handler.inject_clozes(card)

        assert processed_card["front"] == content

    def test_same_cloze_case(self):
        content = (
            "This is a string with 2 {{c1::clozes}}.\n"
            + "Another line, same {{c1::clozes}}."
        )

        assert clozes.are_clozes_in_card(content)
        cloze_handler = clozes.HandleClozes(content)

        card = {"front": cloze_handler.hashed_markdown, "back": ""}
        processed_card = cloze_handler.inject_clozes(card)

        assert processed_card["front"] == content

    def test_variation_case(self):
        """
        Check for high numbers, uppercase/lowercase "c" and
        uppercase/lowercase similar strings.
        """
        content = (
            "This is a string with 2 {{C394::cloZe}}.\n"
            + "Another line, same {{C394::cloze}}."
        )

        # When clozes are injected back, the "c" should be normalized,
        # so it is always undercase.
        normalized_content = (
            "This is a string with 2 {{c394::cloZe}}.\n"
            + "Another line, same {{c394::cloze}}."
        )

        assert clozes.are_clozes_in_card(content)
        cloze_handler = clozes.HandleClozes(content)

        card = {"front": cloze_handler.hashed_markdown, "back": ""}
        processed_card = cloze_handler.inject_clozes(card)

        assert processed_card["front"] == normalized_content

    def test_false_case(self):
        content = "This is a string with 2 {{c1:clozeS}}.\n" + "Another line."
        assert not clozes.are_clozes_in_card(content)
        cloze_handler = clozes.HandleClozes(content)

        card = {"front": cloze_handler.hashed_markdown, "back": ""}
        processed_card = cloze_handler.inject_clozes(card)

        assert processed_card["front"] == content
