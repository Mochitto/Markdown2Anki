import logging

CARDS = []

class CardError(Exception):
    """Class used for parsing errors related to the cards."""

def log_card_error(message: str, card_index: int=None) -> None:
    """
    Log message as error;
    if the card_index is present, wait 1.5 s
    and then log the full card text as error for user-side debugging.
    """
    global CARDS
    logging.error(f"❌ {message} ❌")
    if card_index is not None: # Index could be 0, so it's not possible to use a falsy statement
        input("Enter anything to continue and see the cards' text...")
        logging.error(f"📔 This is the card that created the error:\n{CARDS[card_index]}")
