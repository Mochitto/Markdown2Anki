import logging

import markdown2anki.md_2_anki.utils.common_types as Types
from markdown2anki.utils.debug_tools import expressive_debug

logger = logging.getLogger(__name__)


def wrap_tab_group(tab_content: Types.HTMLString, add_over_sibling=False) -> Types.HTMLString:
    if add_over_sibling:
        return f'<section class="tab_group u-over_sibling">{tab_content}</section>'
    return f'<section class="tab_group">{tab_content}</section>'


def wrap_tab(tab_label: str, tab_body: Types.HTMLString) -> Types.HTMLString:
    return f'<section class="tab">{tab_label}{tab_body}</section>'


def wrap_tab_label(label: str) -> Types.HTMLString:
    return f'<span class="tab__label">{label.strip()}</span>'


def wrap_tab_body(body: Types.HTMLString) -> Types.HTMLString:
    return f'<div class="tab__body">{body}</div>'
