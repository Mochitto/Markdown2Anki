import re
import logging
from typing import List

import md_2_anki.utils.card_types as Types
from md_2_anki.utils.card_error import CardError
from md_2_anki.utils.debug_tools import expressive_debug
from md_2_anki.process_card.process_card import process_card
from md_2_anki.process_clozes.process_clozes import (
    get_clozes,
    hash_clozes,
    clean_code_from_clozes,
    replace_cloze_text_with_hashes,
    inject_clozes,
    are_clozes_in_card,
)
from md_2_anki.process_images.process_images import get_images_to_copy

# NOTE: if changes are made to the cards' HTML/CSS/JS, you also want to look into cards_specific_wrappers' functions

logger = logging.getLogger(__name__)


# TODO: create type with returning values
def markdown_to_anki(markdown: Types.MDString, vault, **options):
    """
    Create anki cards from markdown.
    Return a dictionary with the processed cards and extra information.

    **options kwargs:
    linenos (Bool=False): whether or not to add line-numbers to highlighted code
    interactive (Bool=False): ask the user to continue or stop upon errors
    fast_forward (Bool=False): continue processing cards even when there's errors
    images_dir (Types.PathString=None): abs path to the directory where imges can be found
    folders_to_exclude (list[str]=[]): list of folders names to exclude when looking for images
    """

    # Unpacking kwargs
    linenos = options.get("linenos", True)
    interactive = options.get("interactive", False)
    fast_forward = options.get("fast_forward", False)
    images_dir = options.get("images_dir", None)
    folders_to_exclude = options.get("folders_to_exclude", list())

    cards = extract_cards(markdown)

    if cards[0]:
        logger.info(f"📦 Found {len(cards)} cards to process...")
    else:
        raise CardError("No cards were found...")

    processed_cards = []
    processed_cards_with_cloze = []
    failed_cards = []
    images_to_copy = {}
    aborted_cards = 0
    successful_cards = 0
    for index, card in enumerate(cards):
        # card is not immutable: it can change when clozes are found
        try:  # Handle CardErrors
            cloze_card_flag = False

            if are_clozes_in_card(card):
                cloze_card_flag = True

                clozes = get_clozes(card)
                hash_dictionary = hash_clozes(clozes)

                card_without_clozes = clean_code_from_clozes(card)
                card_with_hashes = replace_cloze_text_with_hashes(
                    card_without_clozes, hash_dictionary
                )

                formatted_card_without_clozes = process_card(
                    card_with_hashes, vault, linenos=linenos
                )

                formatted_card = inject_clozes(
                    formatted_card_without_clozes, hash_dictionary
                )
            else:
                formatted_card = process_card(card, vault, linenos=linenos)

            if images_dir:
                images = get_images_to_copy(
                    formatted_card, images_dir, folders_to_exclude
                )
                images_to_copy.update(images)
                # TODO: Add check for images not found to send to debug/Find a better way to handle errors

            if cloze_card_flag:
                processed_cards_with_cloze.append(formatted_card)
            else:
                processed_cards.append(formatted_card)

            successful_cards += 1

        except CardError as error:
            if fast_forward:
                logger.info(f"|--- ❌ Failed to process the card number {index + 1}...")
                logger.error(f"|------- ERROR: {error}")
                aborted_cards += 1
                failed_cards.append(f"❌ ERROR ❌ - {error}\n{card}")
                continue
            elif interactive:
                logger.info(
                    f"\n📔 This is the card that created the error:📔\n{card}\n\n(see card above)"
                )
                logger.error(error)

                user_input = input(
                    "❓ Would you like to abort this card and continue? (y/N)\n>>> "
                ).lower()
                if user_input == "y" or user_input == "yes":
                    logger.info(
                        f"|--- ❌ Failed to process the card number {index + 1}..."
                    )
                    aborted_cards += 1
                    failed_cards.append(f"❌ ERROR ❌ - {error}\n{card}")
                    continue
            raise error
        logger.info(f"|--- ✅ Finished processing the card number {index + 1}!")

    return {
        "cards": processed_cards,
        "cards_with_clozes": processed_cards_with_cloze,
        "failed_cards": failed_cards,
        "number_of_successful": successful_cards,
        "number_of_failed": aborted_cards,
        "images_to_copy": images_to_copy,
    }


def extract_cards(markdown_text: Types.MDString) -> List[Types.MDString]:
    """
    Extract cards from a markdown text.
    The delimiters used are markdown's hr.

    Pattern:
    ------
    ---
    ***
    ******
    """
    regex_pattern = r"(?:(?:---+?)|(?:\*\*\*+?))\n"  # Match hr in markdown

    cards = re.split(regex_pattern, markdown_text)

    # the lambda function is used to discard 'empty cards'
    filtered_cards = list(
        filter(lambda card: bool(card), cards)
    )  # filter returns an iterable

    return filtered_cards
