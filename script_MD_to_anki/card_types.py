from typing import Dict, List, TypedDict

class CardSides(TypedDict):
    front: str
    back: str

class TabsSides(TypedDict):
    left_tabs: str
    right_tabs: str

class Tab(TypedDict):
    tab_label: str
    tab_body: str

class TabsList(TypedDict):
    tabs: List[Tab]
    tabs_to_swap: List[int]

class CardSideWithSwap(TypedDict):
    left_tabs: str
    left_tabs_to_swap: str
    right_tabs: str
    right_tabs_to_swap: str

class CardWithSwap(TypedDict):
    front: CardSideWithSwap
    back: CardSideWithSwap

class CardSideWithTabs(TypedDict):
    left_tabs: List[str]
    right_tabs: List[str]

class CardWithTabs(TypedDict):
    front: CardSideWithTabs
    back: CardSideWithTabs