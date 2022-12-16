import re

def wrap_label(label):
    return f'<span class="tab__label">{label.strip()}</span>'

def wrap_body(body):
    return f'<div class="tab__body">{body}</div>'

def wrap_tab(tab_label, tab_body):
    return f'<section class="tab">{tab_label}{tab_body}</section>'

def wrap_tab_group(text, over_sibling=False):
    if over_sibling:
        return f'<section class="tab_group u-over_sibling">{text}</section>'
    return f'<section class="tab_group">{text}</section>'

def activate_first_tab(tabs): # TODO: TAKE ME TO A LIB
    new_tabs = tabs.copy()
    
    new_tabs[0] = re.sub(r'(class="tab)"', r'\1 tab--isactive"', new_tabs[0])
    return new_tabs