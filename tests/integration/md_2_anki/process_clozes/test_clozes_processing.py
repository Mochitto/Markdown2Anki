import markdown2anki.md_2_anki.process_clozes as clozes


class TestClozesProcessing:
    def test_basic_case(self):
        content = (
            "This is a string with 2 {{c1::clozes}}.\n"
            + "Another line with another {{c2::cloze}}."
        )

        assert clozes.are_clozes_in_card(content)
        match_clozes = clozes.get_clozes(content)
        hashed_clozes = clozes.hash_clozes(match_clozes)
        cleaned_content = clozes.clean_code_from_clozes(content)
        hashed_content = clozes.replace_cloze_text_with_hashes(
            cleaned_content, hashed_clozes
        )

        card = {"front": hashed_content, "back": ""}
        processed_card = clozes.inject_clozes(card, hashed_clozes)

        assert processed_card["front"] == content

    def test_variation_case(self):
        """
        Check for high numbers and uppercase/lowercase "c".

        """
        content = (
            "This is a string with 2 {{C394::cloZe}}.\n"
            + "Another line, same {{C394::cloZe}}."
        )

        # When clozes are injected back, the c normalized,
        # so it is always undercase.
        normalized_content = (
            "This is a string with 2 {{c394::cloZe}}.\n"
            + "Another line, same {{c394::cloZe}}."
        )

        assert clozes.are_clozes_in_card(content)
        match_clozes = clozes.get_clozes(content)
        hashed_clozes = clozes.hash_clozes(match_clozes)
        cleaned_content = clozes.clean_code_from_clozes(content)
        hashed_content = clozes.replace_cloze_text_with_hashes(
            cleaned_content, hashed_clozes
        )

        card = {"front": hashed_content, "back": ""}
        processed_card = clozes.inject_clozes(card, hashed_clozes)

        assert processed_card["front"] == normalized_content

    def test_false_case(self):
        content = "This is a string with 2 {{c1:clozeS}}.\n" + "Another line."
        assert not clozes.are_clozes_in_card(content)
        match_clozes = clozes.get_clozes(content)
        hashed_clozes = clozes.hash_clozes(match_clozes)
        cleaned_content = clozes.clean_code_from_clozes(content)
        hashed_content = clozes.replace_cloze_text_with_hashes(
            cleaned_content, hashed_clozes
        )

        card = {"front": hashed_content, "back": ""}
        processed_card = clozes.inject_clozes(card, hashed_clozes)

        assert processed_card["front"] == content
