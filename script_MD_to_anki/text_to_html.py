import pygments
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_by_name, guess_lexer

import mistune

code_highlighted_counter = 0
linenos_true = True # TODO: add config file or something to turn them off

def markdown_to_html_with_highlight(text):
    """
    Parse the text and compile to html; 
    in addition, code blocks are highlighted using a custom pygments template (see HighlightRenderer)
    """
    markdown = mistune.create_markdown(escape=False, hard_wrap=True, renderer=HighlightRenderer(), plugins=['strikethrough', 'footnotes', 'table', "url", "def_list"])
    return markdown(text)

class HighlightRenderer(mistune.HTMLRenderer):
    def block_code(self, code, info=None):
        try:
            lexer = get_lexer_by_name(info)
        except pygments.util.ClassNotFound:
            lexer = guess_lexer(code)

        code_class = "highlight__code highlight--linenos" if linenos_true else "highlight__code"
        formatter = LineWrappingHtmlFormatter(cssclass=code_class, wrapcode=True)
        highlight_code = pygments.highlight(code, lexer, formatter)
        section_head = '<section class="highlight highlight--linenos">'
        language_span = f'<span class="highlight__language">{lexer.name}</span>'
        complete_code = f'{section_head}{language_span}<pre><code>{highlight_code.strip()}</code></pre></section>'
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

if __name__ == "__main__":  # TODO: Turn this into testing for line wrapping.
    test = """
## This is before!

---

```python
    def _wrap_lines(self, source):
    for i, t in source:
        if i == 1:
            # it's a line of formatted code
            wrapped_line = f"<span class='highlight__line'>{t}</span>"
        yield i, t

```

# Hello there!
    """
    
    print(markdown_to_html_with_highlight(test))

