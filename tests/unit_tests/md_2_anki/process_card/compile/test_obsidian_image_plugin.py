import pytest
import mistune

from markdown2anki.md_2_anki.process_card.compile.custom_plugins.obsidian_image_plugin import (
    ObsidianImagePlugin,
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

        obsidian_image = ObsidianImagePlugin()
        obsidian_image.plugin(markdown)
        return markdown

    def test_good_case(self, markdown):
        content = "![[https://i.redd.it/vgzilxklh5991.jpg|300]]"
        expected_result = '<p><img src="https://i.redd.it/vgzilxklh5991.jpg" style="width:300px"></p>\n'

        result = markdown(content)
        assert result == expected_result

    def test_alias_case(self, markdown):
        content = "![[https://i.redd.it/vgzilxklh5991.jpg|This is a comment]]"
        expected_result = '<p><img src="https://i.redd.it/vgzilxklh5991.jpg"></p>\n'

        result = markdown(content)
        assert result == expected_result

    def test_no_width_case(self, markdown):
        content = "![[https://i.redd.it/vgzilxklh5991.jpg]]"
        expected_result = '<p><img src="https://i.redd.it/vgzilxklh5991.jpg"></p>\n'

        result = markdown(content)
        assert result == expected_result

    def test_no_match_wikilink(self, markdown):
        content = "[[https://i.redd.it/vgzilxklh5991.jpg]]"
        expected_result = "<p>[[https://i.redd.it/vgzilxklh5991.jpg]]</p>\n"

        result = markdown(content)
        assert result == expected_result

    def test_empty_case(self, markdown):
        content = "![[]]"
        expected_result = "<p>![[]]</p>\n"

        result = markdown(content)
        assert result == expected_result

    def test_empty_with_alias_corner_case(self, markdown):
        content = "![[|300]]"
        expected_result = "<p>![[|300]]</p>\n"

        result = markdown(content)
        assert result == expected_result

    # Corner cases very unlikely to come up (not even Obsidian supports them):
    # def test_pipe_corner_case(self, markdown):
    #     content = "![[something|called/weirdly|with|pipes.md]]"
    #     expected_result = '<p><img src="something|called/weirdly|with|pipes.md" style="width:300px"></p>\n'

    #     result = markdown(content)
    #     assert result == expected_result

    # def test_pipe_alias_corner_case(self, markdown):
    #     content = "![[something|called/weirdly|with|pipes.md|300]]"
    #     expected_result = '<p><img src="something|called/weirdly|with|pipes.md" style="width:300px"></p>\n'

    #     result = markdown(content)
    #     assert result == expected_result
