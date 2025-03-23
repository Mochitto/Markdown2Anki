import pytest
from markdown2anki.markdown_handler import MarkdownHandler

# NOTE: In all below strings it is important that the string starts in the same line as
# the triple quotes. Otherwise, the frontmatter will not be detected due to the extra
# newline.


content_0 = """Some dummy content, no frontmatter."""


def test_given_file_with_no_frontmatter_raises_exception(temp_md_file):
    with pytest.raises(Exception):
        _ = MarkdownHandler(temp_md_file(content_0))


content_1 = """---
invalid_frontmatter
---

Some dummy content
"""


def test_given_file_with_invalid_yaml_raises_exception(temp_md_file):
    with pytest.raises(Exception):
        _ = MarkdownHandler(temp_md_file(content_1))


content_2 = """---
deck_name: deck
note_type_basic: basic
note_type_cloze: cloze
---

Some dummy content
"""


def test_given_file_with_valid_yaml_succeeds(temp_md_file):
    handle = MarkdownHandler(temp_md_file(content_2))

    assert handle.metadata["deck_name"] == "deck"
    assert handle.metadata["note_type_basic"] == "basic"
    assert handle.metadata["note_type_cloze"] == "cloze"
    assert handle.metadata["tags"] == ["md2anki"]


content_3 = """---
some_wrong_key: deck
note_type_basic: basic
note_type_cloze: cloze
---

Some dummy content
"""


def test_given_file_with_invalid_yaml_schema_raises_exception(temp_md_file):
    with pytest.raises(Exception):
        _ = MarkdownHandler(temp_md_file(content_3))


content_4 = """---
deck_name: deck
note_type_basic: basic
note_type_cloze: cloze
tags:
 - tag1
 - tag2
---

Some dummy content
"""


def test_given_file_with_optional_tags_succeeds(temp_md_file):
    handle = MarkdownHandler(temp_md_file(content_4))

    assert handle.metadata["tags"] == ["md2anki", "tag1", "tag2"]
