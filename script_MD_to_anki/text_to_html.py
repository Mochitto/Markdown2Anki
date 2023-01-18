import html
import logging
import re
from typing import List

import mistune
import pygments
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_by_name, guess_lexer

import card_types as Types
from config_handle import LINENOS
from debug_tools import expressive_debug
from obsidian_link_plugin import plugin_obsidian_link
from obsidian_image_plugin import plugin_obsidian_image
from process_clozes import (
    clean_code_from_clozes,
    get_clozes,
    hash_clozes,
    inject_clozes,
    replace_cloze_text_with_hashes,
)


logger = logging.getLogger(__name__)


def tabs_to_html(tabs: List[Types.MDTab]) -> List[Types.HTMLTab]:
    html_tabs = [tab_to_html(tab) for tab in tabs]
    return html_tabs


def tab_to_html(tab: Types.MDTab) -> Types.HTMLTab:
    """Compile the tab to html and wrap it in cards' specific wrappers"""
    html_body = markdown_to_html_with_highlight(tab["tab_body"])

    return {"tab_label": tab["tab_label"], "tab_body": html_body}


def markdown_to_html_with_highlight(text: Types.MDString) -> Types.HTMLString:
    """
    Parse the text and compile to html;
    Code blocks are highlighted using
    a custom pygments template (see HighlightRenderer)
    """
    markdown = mistune.create_markdown(
        escape=False,
        hard_wrap=True,
        renderer=HighlightRenderer(),
        plugins=[
            "strikethrough",
            "footnotes",
            "table",
            "url",
            "def_list",
            plugin_obsidian_link,
            plugin_obsidian_image,
        ],
    )
    return markdown(text)


class HighlightRenderer(mistune.HTMLRenderer):
    def block_code(self, code, info=""):
        try:
            lexer = get_lexer_by_name(info)
        except pygments.util.ClassNotFound:
            lexer = guess_lexer(code)

        code_class = (
            "highlight__code highlight--linenos" if LINENOS else "highlight__code"
        )
        formatter = LineWrappingHtmlFormatter(cssclass=code_class, wrapcode=True)

        # Clozes handling # TODO optimization: some steps can be avoided if there are no clozes
        clozes = get_clozes(code)
        hashed_clozes = hash_clozes(clozes)
        code_cleaned_from_clozes = clean_code_from_clozes(code)
        code_with_hashed_clozes = replace_cloze_text_with_hashes(
            code_cleaned_from_clozes, hashed_clozes
        )

        highlighted_code = pygments.highlight(code_with_hashed_clozes, lexer, formatter)
        highlighted_code_with_clozes = inject_clozes(highlighted_code, hashed_clozes)

        section_head = '<section class="highlight highlight--linenos">'
        language_span = f'<span class="highlight__language">{lexer.name}</span>'
        complete_code = f"{section_head}{language_span}{highlighted_code_with_clozes.strip()}</section>"

        return complete_code

    def image(self, src, alt="", title=None):
        # NOTE: Doesn't support title for now; can add if requested
        src = self._safe_url(src)
        alt = html.escape(alt)

        is_hyperlink = bool(re.match(r"https?://", src))

        if is_hyperlink:
            return f'<img src="{src}" alt={alt}>' if alt else f'<img src="{src}">'
        else:
            path_slash_regex = re.compile(r"[\\\/]")  # Support for multiple OSs
            last_word = re.split(path_slash_regex, src)[-1]
            return (
                f'<img src="{last_word}" alt={alt}>'
                if alt
                else f'<img src="{last_word}">'
            )


class LineWrappingHtmlFormatter(
    HtmlFormatter
):  # https://pygments.org/docs/formatters/#HtmlFormatter
    def wrap(self, source):
        """
        Wrap the ``source``, which is a generator yielding
        individual lines, in custom generators. See docstring
        for `format`. Can be overridden.
        """

        output = source
        if self.wrapcode:
            output = self._wrap_code(output)

        output = self._wrap_lines(source)
        output = self._wrap_pre(output)

        return output

    def _wrap_lines(self, source):
        """
        Wrap each line in a span with the 'highlight__line' class.
        """
        for i, t in source:
            if i == 1:
                # it's a line of formatted code
                wrapped_line = f"<span class='highlight__line'>{t}</span>"
            yield i, wrapped_line  # FIXME maybe? when i != 1; yield i, t?
