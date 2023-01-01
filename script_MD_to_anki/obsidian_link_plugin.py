import re
import mistune
import logging
import urllib

from config_handle import VAULT
from logger import expressive_debug

logger = logging.getLogger(__name__)

OBSIDIAN_LINK_REGEX = (
    # [[Something]]
    # [[Something|This is the alias]]
    r'\[\['
    r'(.+?)' # Match path to page
    r'(?:\|(.+?))?' # Possible alias 
    r'\]\]')

def parse_inline_obsidian_link(inline_message, matches, state):
    path_to_page = matches.group(1)
    page_alias = matches.group(2) 

    return "obsidian_link", path_to_page, page_alias

def render_obsidian_link(path, alias):
    encoded_path = urllib.parse.quote(path.encode("utf8"))
    encoded_vault = urllib.parse.quote(VAULT.encode("utf8")) 
    if alias:
        return f'<a href="obsidian://open?vault={encoded_vault}&file={encoded_path}">{alias}</a>'
    else:
        path_slash_regex = re.compile(r"[\\\/]") # Support for multiple OSs
        last_word = re.split(path_slash_regex, path)[-1]
        return f'<a href="obsidian://open?vault={encoded_vault}&file={encoded_path}">{last_word}</a>'

def plugin_obsidian_link(Markdown):
    Markdown.inline.register_rule("obsidian_link", OBSIDIAN_LINK_REGEX, parse_inline_obsidian_link)
    Markdown.inline.rules.append('obsidian_link')
    if Markdown.renderer.NAME == 'html':
         Markdown.renderer.register('obsidian_link', render_obsidian_link)
