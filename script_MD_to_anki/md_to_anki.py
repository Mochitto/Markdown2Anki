import logging
from typing import List

from extract import extract_cards, extract_card_sides, extract_tabs_sides, extract_tabs
from formatters import format_tabs, format_tab_group
from tab_swapping import get_swapped_tabs
from text_to_html import tabs_to_html
from card_error import CardError, validate_card_data, validate_card_sides

# NOTE: if changes are made to the cards' HTML/CSS/JS, you also want to look into cards_specific_wrappers' functions

def markdown_to_anki(markdown: str) -> List[str]:
    cards = extract_cards(markdown) 

    if cards:
        logging.info(f"📦 Found {len(cards)} cards to process...")
    else:
        raise CardError("No cards were found...")
        
    processed_cards = []
    for card in cards:

        card_sides = extract_card_sides(card) 

        validate_card_sides(card_sides, card)
        
        card_data = {
        "front": {
                "left_tabs": [],
                "left_tabs_swap": [],
                "right_tabs": [],
                "right_tabs_swap": []
        },
        "back": {
                "left_tabs": [],
                "left_tabs_swap": [],
                "right_tabs": [],
                "right_tabs_swap": []
        }
        }

        for side, side_content in card_sides.items():
            tabs_sides = extract_tabs_sides(side_content)

            for tab_side, tab_side_content in tabs_sides.items():
                if not tab_side_content: # Non-empty tab side
                        continue
                tabs_info = extract_tabs(tab_side_content)
                html_tabs = tabs_to_html(tabs_info["tabs"])
                formatted_tabs = format_tabs(html_tabs)
                
                card_data[side][tab_side] = formatted_tabs
                card_data[side][f"{tab_side}_swap"] = tabs_info["tabs_to_swap"]

        validate_card_data(card_data, card)

        card_with_swapped_tabs = get_swapped_tabs(card_data)

        formatted_card = {
            "front": "", 
            "back": ""
            }

        for side in card_sides.keys():
            formatted_card[side] += format_tab_group(card_with_swapped_tabs[side]["left_tabs"])
            formatted_card[side] += format_tab_group(card_with_swapped_tabs[side]["right_tabs"])

        processed_cards.append(formatted_card)

        logging.debug(f"📔 Formatted card ready for import 📔\n{formatted_card}\n")

    return processed_cards

