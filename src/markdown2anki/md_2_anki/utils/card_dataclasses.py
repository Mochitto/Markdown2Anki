from dataclasses import dataclass, field

import markdown2anki.md_2_anki.utils.common_types as Types
from markdown2anki.md_2_anki.utils.card_error import CardError


# Grouping, Extraction to MDstring
@dataclass(frozen=True)
class MDCard:
    front: Types.MDString
    back: Types.MDString = field(default="")

    def __post_init__(self):
        if not self.front:
            raise CardError("The front side of the card is missing.")
