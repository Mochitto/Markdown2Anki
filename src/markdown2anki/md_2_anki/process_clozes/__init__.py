import logging
import re
from typing import Dict, List, Tuple

import markdown2anki.md_2_anki.utils.common_types as Types
from markdown2anki.md_2_anki.utils.card_error import CardError
from markdown2anki.utils.debug_tools import expressive_debug

logger = logging.getLogger(__name__)


class HandleClozes:
    """
    This class takes care of hashing and unhashing clozes.
    This is necessary to make sure code-highlighting won't break clozes.
    """

    def __init__(self, card: Types.MDString) -> None:
        self.card = card
        self._clozes = self._get_clozes(card)
        self._hash_dictionary = self._create_hash_dictionary(self._clozes)
        self.hashed_markdown = self._hash_clozes()

    def _get_clozes(self, text: Types.MDString) -> List[str]:
        """
        Extract clozes from text.

        Pattern:
        {{c1::something}}
        {{C9::something}}
        """
        clozes_regex = re.compile(r"(?i)({{c\d+::.+?}})")

        clozes_matches = clozes_regex.findall(text)

        return clozes_matches

    def _create_hash_dictionary(self, clozes: List[str]) -> Dict[str, str]:
        """
        Transform matched clozes into a dictionary that has:
        keys: hashed match
        values: cloze
        """

        # A dictionary built to use with translate()
        # {key: ord(number), value: letter} + "-" : Z
        number_to_letter_translation = {
            48: "A",
            49: "B",
            50: "C",
            51: "D",
            52: "E",
            53: "F",
            54: "G",
            55: "H",
            56: "I",
            57: "J",
            45: "Z",
        }

        result = dict()
        for cloze in clozes:
            hash_number = str(hash(cloze))

            hash_in_letters = hash_number.translate(number_to_letter_translation)
            result[hash_in_letters] = cloze

        return result

    def _replace_clozes_with_hashes(
        self, markdown_text: Types.MDString, hashed_clozes: Dict[str, str]
    ) -> Types.MDString:
        """
        Replace the text of clozes ({{c1::This part}}) with the corresponding hash.
        """
        if not hashed_clozes:
            return markdown_text

        markdown_with_hashes = markdown_text

        for hash_key, cloze in hashed_clozes.items():
            cloze_regex = re.compile(re.escape(cloze))
            markdown_with_hashes, number_of_substitutions = re.subn(
                cloze_regex,
                hash_key,
                markdown_with_hashes,
            )
            if number_of_substitutions < 1:
                raise CardError(
                    "Bad formatting in code's cloze; make sure you are not using nested clozes."
                )
        expressive_debug(logger, "Markdown with hash", markdown_with_hashes, "json")

        return markdown_with_hashes

    def _hash_clozes(self) -> Types.MDString:
        """
        Replace clozes that are part of the card with string hashes.
        """
        hashed_markdown = self._replace_clozes_with_hashes(
            self.card, self._hash_dictionary
        )
        return hashed_markdown

    def inject_clozes(
        self, card: Dict[str, Types.MDString]
    ) -> Dict[str, Types.MDString]:
        """
        Replace the hashes in the text with the corresponding cloze:
        HSJDKASKHDAKS -> {{c1::my cloze}}
        And normalize clozes (make sure the "c" is lowercase).
        """
        front = card["front"]
        back = card["back"]

        for hashed_cloze, cloze in self._hash_dictionary.items():
            normalized_cloze = "{{c" + cloze[3:]
            hash_regex = re.compile(re.escape(hashed_cloze))

            front = re.sub(hash_regex, normalized_cloze, front)
            back = re.sub(hash_regex, normalized_cloze, back)

        return {"front": front, "back": back}


def are_clozes_in_card(card: Types.MDString) -> bool:
    """
    Check if in the front of the card there is at least one cloze

    Pattern:
    {{c1::something}}
    {{C5::something else}}
    """
    clozes_regex = re.compile(r"{{c(\d+)::(.+?)}}", re.IGNORECASE)

    return bool(clozes_regex.search(card))
