import logging
logger = logging.getLogger(__name__)

def wrap_tab_group(text, add_over_sibling=False):
    if add_over_sibling:
        return f'<section class="tab_group u-over_sibling">{text}</section>'
    return f'<section class="tab_group">{text}</section>'

def wrap_tab(tab_label, tab_body):
    return f'<section class="tab">{tab_label}{tab_body}</section>'

def wrap_tab_label(label):
    return f'<span class="tab__label">{label.strip()}</span>'

def wrap_tab_body(body):
    return f'<div class="tab__body">{body}</div>'
