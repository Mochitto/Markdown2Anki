import logging

import card_types as Types
from card_error import CardError
from extract import extract_cards
from debug_tools import expressive_debug
from process_card import process_card
from process_clozes import are_clozes_in_card

# NOTE: if changes are made to the cards' HTML/CSS/JS, you also want to look into cards_specific_wrappers' functions

logger = logging.getLogger(__name__)


# TODO: turn behaviour configs to kwargs
def markdown_to_anki(markdown: Types.MDString, interactive=False, fast_forward=False):
    cards = extract_cards(markdown)

    if cards[0]:
        logger.info(f"📦 Found {len(cards)} cards to process...")
    else:
        raise CardError("No cards were found...")

    processed_cards = []
    processed_cards_with_cloze = []
    failed_cards = []
    aborted_cards = 0
    successful_cards = 0

    for index, card in enumerate(cards):
        try:  # Handle CardErrors
            formatted_card = process_card(card)

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
                logger.info(f"\n📔 This is the card that created the error:📔\n{card}\n\n(see card above)")
                logger.error(error)

                user_input = input("❓ Would you like to abort this card and continue? (y/N)\n>>> ").lower()
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
    }
