import logging
import re
from typing import Match

import mistune

import markdown2anki.md_2_anki.utils.common_types as Types
from markdown2anki.utils.debug_tools import expressive_debug

logger = logging.getLogger(__name__)


class ObsidianImagePlugin:
    """
    Plugin to add support for the embedding syntax used in obsidian.
    Notice: this doesn't embedd notes but, as the name suggests, only images.
    """

    def __init__(self) -> None:

        self.OBSIDIAN_IMAGE_REGEX = (
            # ![[Something]]
            # ![[Something|300]]
            # DO NOT MATCH:
            # ![[|300]]
            # ![[]]
            r"!\[\["
            r"(?!\|)(.+?)"  # Match path to image (doesn't match if the first char is a pipe)
            r"(?:\|(.+?))?"  # Possible width; not strictly digits to allow for bad formatting
            r"\]\]"
        )

    def parse_inline_obsidian_image(
        self, inline_message: Types.MDString, matches: Match[str], state
    ):
        path_to_image = matches.group(1)
        image_width = matches.group(2)

        return "obsidian_image", path_to_image, image_width

    def render_obsidian_image(
        self, path_to_image: Types.PathString, width_or_alias: str
    ):
        path_to_image = path_to_image.strip()
        is_hyperlink = bool(re.match(r"https?://", path_to_image))

        # Check if it's a number of an alias
        try:
            image_width = int(width_or_alias)
        except (TypeError, ValueError):
            image_width = None

        if is_hyperlink:
            return (
                f'<img src="{path_to_image}" style="width:{image_width}px">'
                if image_width
                else f'<img src="{path_to_image}">'
            )
        else:
            path_slash_regex = re.compile(r"[\\\/]")  # Support for multiple OSs
            last_word = re.split(path_slash_regex, path_to_image)[-1]
            return (
                f'<img src="{last_word}" style="width:{image_width}px">'
                if image_width
                else f'<img src="{last_word}">'
            )

    def plugin(self, Markdown: mistune.Markdown):
        Markdown.inline.register_rule(
            "obsidian_image",
            self.OBSIDIAN_IMAGE_REGEX,
            self.parse_inline_obsidian_image,
        )
        Markdown.inline.rules.append("obsidian_image")
        if Markdown.renderer.NAME == "html":
            Markdown.renderer.register("obsidian_image", self.render_obsidian_image)
