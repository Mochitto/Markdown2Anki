from dataclasses import dataclass, field

from card_error import CardError
import card_types as Types


# Grouping, Extraction to MDstring
@dataclass(frozen=True)
class MDCard:
    front: Types.MDString
    back: Types.MDString = field(default="")

    def __post_init__(self):
        if not self.front:
            raise CardError("The front side of the card is missing.")

