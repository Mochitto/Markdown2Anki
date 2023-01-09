import logging
from typing import List

import mistune
import pygments

import card_types as Types
from config_handle import LINENOS
from extract import extract_clozes
from formatters import clean_from_clozes, inject_clozes
from debug_tools import expressive_debug
from obsidian_link_plugin import plugin_obsidian_link
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_by_name, guess_lexer

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
        plugins=['strikethrough', 'footnotes', 'table', "url", "def_list", plugin_obsidian_link])
    return markdown(text)

class HighlightRenderer(mistune.HTMLRenderer):
    def block_code(self, code, info=None):
        try:
            lexer = get_lexer_by_name(info)
        except pygments.util.ClassNotFound:
            lexer = guess_lexer(code)

        code_class = "highlight__code highlight--linenos" if LINENOS else "highlight__code"
        
        # step 1: get matches
        # step 2: clean from clozes
        # step 3: make a dict with key: hash, value: cloze tuple
        # step 4: sub each cloze text (\btext\b) with the corresponding hash (iterate over the dict to get the text and hash)
        # step 5: replace hash with text, once highlighted

        # # The hash is transformed to a sequence of letters so that it can be picked up as a var token by pygments, putting it in a single span
        # hash_clozed_text = lambda match: str(hash(match[1]))
        # number_to_letter = "ABCDEFGHIL"
        # hash_clozed_text_word = lambda match: "".join([number_to_letter[int(number)] if number != "-" else "M" for number in hash_clozed_text(match)])

        clozes = extract_clozes(code)
        
        expressive_debug(logger, "These are the clozes", clozes, "pprint")

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
