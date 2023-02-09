from typing import List, TypedDict

from . import common_types as Types

class MDTab(TypedDict):
    tab_label: str
    tab_body: Types.MDString


class HTMLTab(TypedDict):
    tab_label: str
    tab_body: Types.HTMLString


class TabsWithSwap(TypedDict):
    left_tabs: List[Types.HTMLString]
    left_tabs_swap: List[int]
    right_tabs: List[Types.HTMLString]
    right_tabs_swap: List[int]


class CardWithSwap(TypedDict):
    front: TabsWithSwap
    back: TabsWithSwap


# Prepare for processing, post Swap
class CardSideWithTabs(TypedDict):
    left_tabs: List[Types.HTMLString]
    right_tabs: List[Types.HTMLString]


# See above, grouping
class CardWithTabs(TypedDict):
    front: CardSideWithTabs
    back: CardSideWithTabs
