import markdown2anki.md_2_anki.process_clozes as clozes


class TestReplaceClozeTextWithHashes:
    def test_basic_case(self):
        content = (
            "This is a string with 2 {{c1::clozes}}.\n"
            + "Another line with another {{c2::cloze}}."
        )
        expected_hashed_content = (
            "This is a string with 2 HIIDAJIGJADFBDBJJDF.\n"
            + "Another line with another ZEJDDDHDEBDEICGIHBGF."
        )

        hashed_clozes = {
            "HIIDAJIGJADFBDBJJDF": ("1", "clozes"),
            "ZEJDDDHDEBDEICGIHBGF": ("2", "cloze"),
        }

        cleaned_content = clozes.clean_code_from_clozes(content)
        hashed_content = clozes.replace_cloze_text_with_hashes(
            cleaned_content, hashed_clozes
        )

        assert hashed_content == expected_hashed_content

    def test_variation_case(self):
        """
        Check for high numbers and uppercase/lowercase "c".
        """
        content = (
            "This is a string with 2 {{C394::cloZe}}.\n"
            + "Another line, same {{C394::cloZe}}."
        )
        expected_hashed_content = (
            "This is a string with 2 ZIAGEIHFICDIEFCECJF.\n"
            + "Another line, same ZIAGEIHFICDIEFCECJF."
        )

        hashed_clozes = {"ZIAGEIHFICDIEFCECJF": ("394", "cloZe")}
        cleaned_content = clozes.clean_code_from_clozes(content)
        hashed_content = clozes.replace_cloze_text_with_hashes(
            cleaned_content, hashed_clozes
        )

        assert hashed_content == expected_hashed_content

    def test_false_case(self):
        content = "This is a string with 2 {{c1:clozeS}}.\n" + "Another line."
        hashed_clozes = {}
        hashed_content = clozes.replace_cloze_text_with_hashes(content, hashed_clozes)

        assert hashed_content == content
