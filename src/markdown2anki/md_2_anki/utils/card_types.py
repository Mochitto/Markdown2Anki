from typing import List, TypedDict, Literal

from . import common_types as Types

# I had to use the Alternative syntax to have
# spaces in my dict keys...
# https://peps.python.org/pep-0589/#alternative-syntax
MDTab = TypedDict(
        "MDTab", 
        {
        "card side": Literal["front", "back"],
        "tab side": Literal["left", "right"],
        "label": str,
        "body": Types.MDString,
        "swap": bool,
        }
        )

HTMLTab = TypedDict(
        "HTMLTab", 
        {
        "card side": Literal["front", "back"],
        "tab side": Literal["left", "right"],
        "label": str,
        "body": Types.HTMLString,
        "swap": bool,
        }
        ) 

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

