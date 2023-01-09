import re
from typing import Dict, List, Literal, Tuple, TypedDict, TypeGuard

# Different kind of strings
MDString = str
HTMLString = str
PathString = str


class MDTab(TypedDict):
    tab_label: str
    tab_body: MDString


class HTMLTab(TypedDict):
    tab_label: str
    tab_body: HTMLString


class TabsWithSwap(TypedDict):
    left_tabs: List[HTMLString]
    left_tabs_swap: List[int]
    right_tabs: List[HTMLString]
    right_tabs_swap: List[int]


class CardWithSwap(TypedDict):
    front: TabsWithSwap
    back: TabsWithSwap


# Prepare for processing, post Swap
class CardSideWithTabs(TypedDict):
    left_tabs: List[HTMLString]
    right_tabs: List[HTMLString]


# See above, grouping
class CardWithTabs(TypedDict):
    front: CardSideWithTabs
    back: CardSideWithTabs


# Should be a tuple, result of findall; should be a dataclass tho
class ClozeType(TypedDict):
    number: int
    cloze_text: str



