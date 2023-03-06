import pytest
import mistune

from markdown2anki.md_2_anki.process_card.compile.custom_plugins.obsidian_link_plugin import (
    ObsidianLinkPlugin,
)
from markdown2anki.md_2_anki.process_card.compile import HighlightRenderer


class TestObsidianImagePlugin:
    @pytest.fixture
    def markdown(self):
        markdown = mistune.create_markdown(
            escape=False,
            hard_wrap=True,
            renderer=HighlightRenderer(),
        )

        obsidian_image = ObsidianLinkPlugin("my vault")
        obsidian_image.plugin(markdown)
        return markdown

    def test_good_case(self, markdown):
        content = "[[/home/user/my vault/my note.md]]"
        expected_result = '<p><a href="obsidian://open?vault=my%20vault&file=/home/user/my%20vault/my%20note.md">my note.md</a></p>\n'

        result = markdown(content)
        assert result == expected_result

    def test_alias_case(self, markdown):
        content = "[[/home/user/my vault/my_note.md|My note]]"
        expected_result = '<p><a href="obsidian://open?vault=my%20vault&file=/home/user/my%20vault/my_note.md">My note</a></p>\n'

        result = markdown(content)
        assert result == expected_result

    def test_no_match_obsidian_img(self, markdown):
        content = "![[/home/user/my vault/my_note.md|My note]]"
        expected_result = "<p>![[/home/user/my vault/my_note.md|My note]]</p>\n"

        result = markdown(content)
        assert result == expected_result

    def test_empty_case(self, markdown):
        content = "[[]]"
        expected_result = "<p>[[]]</p>\n"

        result = markdown(content)
        assert result == expected_result

    def test_empty_with_alias_corner_case(self, markdown):
        content = "[[|my note]]"
        expected_result = "<p>[[|my note]]</p>\n"

        result = markdown(content)
        assert result == expected_result
