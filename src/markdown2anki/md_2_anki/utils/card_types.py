from typing import List, TypedDict, Literal, Tuple

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
    },
)

HTMLTab = TypedDict(
    "HTMLTab",
    {
        "card side": Literal["front", "back"],
        "tab side": Literal["left", "right"],
        "label": str,
        "body": Types.HTMLString,
        "swap": bool,
    },
)

FormattedTab = TypedDict(
    "FormattedTab",
    {
        "card side": Literal["front", "back"],
        "tab side": Literal["left", "right"],
        "text": Types.HTMLString,
        "swap": bool,
    },
)


class SwapMappings(TypedDict):
    restore: List[int]
    remove: List[int]
    replace: List[Tuple[int, int]]


# Prepare for processing, post Swap
class TabSides(TypedDict):
    left: List[Types.HTMLString]
    right: List[Types.HTMLString]


# See above, grouping
class CardWithTabs(TypedDict):
    front: TabSides
    back: TabSides
