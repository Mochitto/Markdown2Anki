import card_types as CardTypes

class CardError(Exception):
    """Errors related to the parsing of the card."""
    def __init__(self, message, card=None):
        self.message = message
        self.card = card
    
    def __str__(self):
        error_message = ""

        if self.card:
            error_message += f"\n📔 This is the card that created the error:📔\n{self.card}\n\n(see details above)\n"

        error_message += f"❌{self.message}❌"
        return error_message

def validate_card_sides(card_sides: CardTypes.CardSides, card):
    """
    Raise an error if:
        - "front" is empty.
    """
    if not card_sides["front"]:
        raise CardError("The front side of the card is missing.")

def validate_card_data(card_data: CardTypes.CardWithSwap, card):
    """
    Raise an error if:
        - There are no left tabs in the front side of the card
        - There are no tabs to swap
    """
    if not (card_data["front"]["left_tabs"]):
        raise CardError("There are no left tabs in the front side of the card.", card)

    for side in ["left", "right"]:
        for index in card_data["front"][f"{side}_tabs_swap"]:
            try:
                card_data["back"][f"{side}_tabs"][index]
            except IndexError as error:
                raise CardError(
                    f"The {make_ordinal(index + 1)} tab on the front-{side} side has no corresponding "
                    + f"tab on the back-{side} side to be swapped with.", card) from error

def make_ordinal(n):
    ''' 
    Convert an integer into its ordinal representation::
    https://stackoverflow.com/a/50992575/19144535
    '''
    #TODO: maybe move to an helper module
    n = int(n)
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    else:
        suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    return str(n) + suffix