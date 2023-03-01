import logging
import re
import urllib.parse
from typing import Match

import mistune

import markdown2anki.md_2_anki.utils.common_types as Types
from markdown2anki.utils.debug_tools import expressive_debug

logger = logging.getLogger(__name__)


class ObsidianLinkPlugin:
    """
    Plugin to add wiki-links that point to an obsidian vault.
    This utilizes Obsidian's URI:
    https://help.obsidian.md/Advanced+topics/Using+obsidian+URI
    """

    def __init__(self, vault: Types.PathString) -> None:
        self.valut = vault

        self.OBSIDIAN_LINK_REGEX = (
            # [[Something]]
            # [[Something|This is the alias]]
            r"(?<!!)\[\["  # Match only if there is no "!", differentiate it from Obsidian images
            r"(?!\|)(.+?)"  # Match path to page
            r"(?:\|(.+?))?"  # Possible alias
            r"\]\]"
        )

    def parse_inline_obsidian_link(
        self, inline_message: Types.MDString, matches: Match[str], state
    ):
        path_to_page = matches.group(1)
        page_alias = matches.group(2)

        return "obsidian_link", path_to_page, page_alias

    def render_obsidian_link(self, path: Types.PathString, alias: str):
        encoded_path = urllib.parse.quote(path.encode("utf8"))
        encoded_vault = urllib.parse.quote(self.valut.encode("utf8"))
        if alias:
            return f'<a href="obsidian://open?vault={encoded_vault}&file={encoded_path}">{alias}</a>'
        else:
            path_slash_regex = re.compile(r"[\\\/]")  # Support for multiple OSs
            last_word = re.split(path_slash_regex, path)[-1]
            file_name = last_word.split(".")[0]
            return f'<a href="obsidian://open?vault={encoded_vault}&file={encoded_path}">{last_word}</a>'

    def plugin(self, Markdown: mistune.Markdown):
        Markdown.inline.register_rule(
            "obsidian_link", self.OBSIDIAN_LINK_REGEX, self.parse_inline_obsidian_link
        )
        Markdown.inline.rules.append("obsidian_link")
        if Markdown.renderer.NAME == "html":
            Markdown.renderer.register("obsidian_link", self.render_obsidian_link)
