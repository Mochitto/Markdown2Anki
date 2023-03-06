from markdown2anki.md_2_anki.process_card.extract import extract_tabs


class TestExtractTabs:
    def test_happy_path(self):
        text = (
            "## B [label one]\n"
            "This is the first tab body\n"
            "which spans two lines\n\n"
            "## - [label two]\n"
            "# A great tab\n"
            "- has a great body\n"
            "## R [label three]\n"
            "Another tab\n\n"
            "## BR [label four]\n"
            "This tab has a body too\n\n"
        )
        expected = [
            {
                "card side": "back",
                "tab side": "left",
                "swap": False,
                "label": "label one",
                "body": "This is the first tab body\nwhich spans two lines",
            },
            {
                "card side": "front",
                "tab side": "left",
                "swap": True,
                "label": "label two",
                "body": "# A great tab\n- has a great body",
            },
            {
                "card side": "front",
                "tab side": "right",
                "swap": False,
                "label": "label three",
                "body": "Another tab",
            },
            {
                "card side": "back",
                "tab side": "right",
                "swap": False,
                "label": "label four",
                "body": "This tab has a body too",
            },
        ]

        assert extract_tabs(text) == expected

    def test_empty_text(self):
        text = ""
        expected = []

        assert extract_tabs(text) == expected

    def test_text_without_tabs(self):
        text = "This is text\nthat should be considered a comment"
        expected = []

        assert extract_tabs(text) == expected

    def test_stars_separator(self):
        text = "## B [label]\n" "****\n"
        expected = [
            {
                "card side": "back",
                "tab side": "left",
                "swap": False,
                "label": "label",
                "body": "****",
            },
        ]

        assert extract_tabs(text) == expected
