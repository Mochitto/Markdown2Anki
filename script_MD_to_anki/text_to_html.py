import mistune

def markdown_to_html_with_highlight(text):
    """Parse the text and compile to html; in addition, code blocks are highlighted using a custom template (see HighlightRenderer)"""
    markdown = mistune.create_markdown(escape=False, renderer=HighlightRenderer(), plugins=['strikethrough', 'footnotes', 'table'])
    return markdown(text)


class HighlightRenderer(mistune.HTMLRenderer):
    def block_code(self, code, info=None):
        global code_highlighted_counter

        try:
            lexer = get_lexer_by_name(info, stripall=True)
        except pygments.util.ClassNotFound:
            lexer = guess_lexer(code)

        code_class = "highlight__code highlight--linenos" if linenos_true else "highlight__code"
        formatter = HtmlFormatter(lineseparator="<br>", cssclass=code_class, linespans="highlight__line", wrapcode=True)
        highlight_code = pygments.highlight(code, lexer, formatter)
        section_head = '<section class="highlight highlight--linenos">'
        language_span = f'<span class="highlight__language">{lexer.name}</span>'
        complete_code = f'{section_head}{language_span}{highlight_code.strip()}</section>'
        code_highlighted_counter += 1
        return complete_code

# This function could be useless
def highlight_code(html_text):
    """Take mistune formatted html, find code by matching <pre><code>, extract language and code and return the html_text with formatted and highlighted code."""
    global code_highlighted_counter
    code_regex = re.compile(r"(?s)<pre><code class=\"language-(.+?)\">(.+?)</code></pre>")
    code_matches = re.findall(code_regex, html_text)
    if not code_matches:
        return html_text # No code in the tag__body, continue

    split_regex = re.compile(r"(?s)<pre><code class=\"language-.+?\">.+?</code></pre>")
    broken_message = re.split(split_regex, html_text)

    code_to_inject = []
    for match in code_matches:
        language = match[0]
        code = match[1]

        try:
            lexer = get_lexer_by_name(language)
        except pygments.util.ClassNotFound:
            lexer = guess_lexer(code)
        
        code_class = "highlight__code highlight--linenos" if linenos_true else "highlight__code"
        formatter = HtmlFormatter(lineseparator="<br>", cssclass=code_class, linespans="highlight__line", wrapcode=True)
        highlight_code = pygments.highlight(code, lexer, formatter)

        section_head = '<section class="highlight highlight--linenos">'
        language_span = f'<span class="highlight__language">{language}</span>'
        complete_code = f'{section_head}{language_span}{highlight_code.strip()}</section>'
        
        
        code_to_inject.append(complete_code)
        
        code_highlighted_counter += 1

    
    # print(broken_message)
    zipped_message = list(zip_longest(broken_message, code_to_inject))

    final_message_parts = [
    x # Returning value
    for pair in zipped_message # First loop
    for x in pair # Second loop
    if x is not None # condition
    ]
    final_message_formatted_and_highlighted = "".join(final_message_parts)

    logging.debug(final_message_formatted_and_highlighted)
    return final_message_formatted_and_highlighted