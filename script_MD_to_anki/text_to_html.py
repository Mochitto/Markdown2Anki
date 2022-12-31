import logging
from typing import List

import pygments
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_by_name, guess_lexer

import mistune

from extract import extract_clozes
from formatters import clean_from_clozes, inject_clozes
import card_types as CardTypes
from config_handle import LINENOS
from logger import expressive_debug

logger = logging.getLogger(__name__)


def tabs_to_html(tabs: List[CardTypes.Tab]) -> List[CardTypes.Tab]:
    html_tabs = []
    for tab in tabs:
        html_tab = tab_to_html(tab)
        html_tabs.append(html_tab)
    return html_tabs

def tab_to_html(tab: CardTypes.Tab) -> CardTypes.Tab:
    """Compile the tab to html and wrap it in cards' specific wrappers"""
    label = tab["tab_label"]
    tab_body_in_html = markdown_to_html_with_highlight(tab["tab_body"])

    return {"tab_label": label, "tab_body": tab_body_in_html}

def markdown_to_html_with_highlight(text):
    """
    Parse the text and compile to html;
    in addition, code blocks are highlighted using
    a custom pygments template (see HighlightRenderer)
    """
    markdown = mistune.create_markdown(
        escape=False,
        hard_wrap=True,
        renderer=HighlightRenderer(),
        plugins=['strikethrough', 'footnotes', 'table', "url", "def_list"])
    return markdown(text)

class HighlightRenderer(mistune.HTMLRenderer):
    def block_code(self, code, info=None):
        try:
            lexer = get_lexer_by_name(info)
        except pygments.util.ClassNotFound:
            lexer = guess_lexer(code)

        code_class = "highlight__code highlight--linenos" if LINENOS else "highlight__code"
        
        clozes = extract_clozes(code)
        code_cleaned_from_clozes = clean_from_clozes(code)
        
        formatter = LineWrappingHtmlFormatter(cssclass=code_class, wrapcode=True)

        highlighted_code = pygments.highlight(code_cleaned_from_clozes, lexer, formatter)
        highlighted_code_with_clozes = inject_clozes(highlighted_code, clozes)
        
        section_head = '<section class="highlight highlight--linenos">'
        language_span = f'<span class="highlight__language">{lexer.name}</span>'
        complete_code = f'{section_head}{language_span}{highlighted_code_with_clozes.strip()}</section>'

        return complete_code

class LineWrappingHtmlFormatter(HtmlFormatter): # https://pygments.org/docs/formatters/#HtmlFormatter
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
            yield i, wrapped_line
