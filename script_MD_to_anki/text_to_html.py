import pygments
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_by_name, guess_lexer

import mistune

code_highlighted_counter = 0
linenos_true = True # TODO: add config file or something to turn them off

def markdown_to_html_with_highlight(text):
    """Parse the text and compile to html; in addition, code blocks are highlighted using a custom template (see HighlightRenderer)"""
    markdown = mistune.create_markdown(escape=False, hard_wrap=True, renderer=HighlightRenderer(), plugins=['strikethrough', 'footnotes', 'table', "url", "def_list"])
    return markdown(text)

class HighlightRenderer(mistune.HTMLRenderer):
    def block_code(self, code, info=None):
        try:
            lexer = get_lexer_by_name(info, stripall=True)
        except pygments.util.ClassNotFound:
            lexer = guess_lexer(code)

        code_class = "highlight__code highlight--linenos" if linenos_true else "highlight__code"
        formatter = HtmlFormatter(cssclass=code_class, linespans="highlight__line", wrapcode=True)
        highlight_code = pygments.highlight(code, lexer, formatter)
        section_head = '<section class="highlight highlight--linenos">'
        language_span = f'<span class="highlight__language">{lexer.name}</span>'
        complete_code = f'{section_head}{language_span}{highlight_code.strip()}</section>'
        return complete_code