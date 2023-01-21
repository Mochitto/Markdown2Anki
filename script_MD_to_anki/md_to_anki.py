import logging

import card_types as Types
from card_error import CardError
from extract import extract_cards
from debug_tools import expressive_debug
from process_card import process_card
from process_clozes import are_clozes_in_card
from process_images import get_images_to_copy

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
        try:  # Handle CardErrors
            formatted_card = process_card(card, vault, linenos=linenos)

            if images_dir:
                images = get_images_to_copy(
                    formatted_card, images_dir, folders_to_exclude
                )
                images_to_copy.update(images)
                # TODO: Add check for images not found to send to debug/Find a better way to handle errors

            if are_clozes_in_card(formatted_card):
                processed_cards_with_cloze.append(formatted_card)
            else:
                processed_cards.append(formatted_card)
            successful_cards += 1

        except CardError as error:
            if fast_forward:
                logger.error(f"{error}")
                logger.info(f"❌ Failed to process the card number {index + 1}...")
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
                    logger.info(f"❌ Failed to process the card number {index + 1}...")
                    aborted_cards += 1
                    failed_cards.append(f"❌ ERROR ❌ - {error}\n{card}")
                    continue
            raise error
        logger.info(f"✅ Finished processing the card number {index + 1}!")

    return {
        "cards": processed_cards,
        "cards_with_clozes": processed_cards_with_cloze,
        "failed_cards": failed_cards,
        "number_of_successful": successful_cards,
        "number_of_failed": aborted_cards,
        "images_to_copy": images_to_copy,
    }
