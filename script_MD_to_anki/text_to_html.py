import html
import logging
import re
from typing import List

import mistune
import pygments
import pygments.util
import pygments.lexers
import pygments.formatters.html

import card_types as Types
from debug_tools import expressive_debug
from obsidian_link_plugin import ObsidianLinkPlugin
from obsidian_image_plugin import ObsidianImagePlugin


logger = logging.getLogger(__name__)


def tabs_to_html(tabs: List[Types.MDTab], vault, linenos=True) -> List[Types.HTMLTab]:
    html_tabs = [tab_to_html(tab, vault, linenos) for tab in tabs]
    return html_tabs


# DELME: entry point for process_card
def tab_to_html(tab: Types.MDTab, vault, linenos=True) -> Types.HTMLTab:
    """Compile the tab to html and wrap it in cards' specific wrappers"""
    html_body = markdown_to_html_with_highlight(tab["tab_body"], vault, linenos)

    return {"tab_label": tab["tab_label"], "tab_body": html_body}


def markdown_to_html_with_highlight(
    text: Types.MDString, vault: str, linenos=True
) -> Types.HTMLString:
    """
    Parse the text and compile to html;
    Code blocks are highlighted using
    a custom pygments template (see HighlightRenderer)
    """
    markdown = mistune.create_markdown(
        escape=False,
        hard_wrap=True,
        renderer=HighlightRenderer(linenos=linenos),
        plugins=[
            "strikethrough",
            "footnotes",
            "table",
            "url",
            "def_list",
        ],
    )

    obsidian_image = ObsidianImagePlugin()
    obsidian_image.plugin(markdown)

    obsidian_link = ObsidianLinkPlugin(vault=vault)
    obsidian_link.plugin(markdown)

    return markdown(text)


class HighlightRenderer(mistune.HTMLRenderer):
    def __init__(self, linenos=True, escape=True, allow_harmful_protocols=None):
        super().__init__(escape, allow_harmful_protocols)
        self.linenos = linenos

    def block_code(self, code, info=""):
        try:
            lexer = pygments.lexers.get_lexer_by_name(info)
        except pygments.util.ClassNotFound:
            lexer = pygments.lexers.guess_lexer(code)

        code_class = (
            "highlight__code highlight--linenos" if self.linenos else "highlight__code"
        )
        formatter = LineWrappingHtmlFormatter(cssclass=code_class, wrapcode=True)

        # Clozes handling # TODO optimization: some steps can be avoided if there are no clozes
        highlighted_code = pygments.highlight(code, lexer, formatter)

        section_head = '<section class="highlight highlight--linenos">'
        language_span = f'<span class="highlight__language">{lexer.name}</span>'
        complete_code = f"{section_head}{language_span}{highlighted_code.strip()}</section>"

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


class LineWrappingHtmlFormatter(pygments.formatters.html.HtmlFormatter):
    # https://pygments.org/docs/formatters/#HtmlFormatter
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
        for line_number, line_text in source:
            wrapped_line = line_text
            if line_number == 1:
                # it's a line of formatted code
                wrapped_line = f"<span class='highlight__line'>{line_text}</span>"
            yield line_number, wrapped_line  # FIXME maybe? when line_number != 1; yield line_number, line_text?
