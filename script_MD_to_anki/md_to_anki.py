import logging

from extract import extract_cards, extract_card_sides, extract_tabs_sides, extract_tabs
from formatters import format_tabs, format_tab_group
from tab_swapping import get_swapped_tabs
from text_to_html import tabs_to_html
from card_error import CardError, log_card_error


# NOTE: if changes are made to the cards' HTML/CSS/JS, you likely want to look into cards_specific_wrappers' functions
""" TODO: Add support for images 
    Manually moving media to anki's media folder (First enhancement):
    1. Create a list where images' src can go
    2. Modify mistune to extract the images' src when parsing
    3. At the end, copy the images from the source folder to a new folder

    Automatically send media and cards to anki using anki connect (Second enhancement):
    1. Check for connection at the start of the script
    2. Send cards to anki connect instead of creating the file (Report a success/failure message)
"""


# Errors ----------------------------------
CARDS = [] # A list of the markdown text of the cards, accessed when there is an error

def markdown_to_anki(markdown: str) -> [str]:
    cards = extract_cards(markdown)

    anki_cards = []
    for card in cards:
        card_sides = extract_card_sides(card)

        front_side = card_sides["front"]
        front_tabs_sides = extract_tabs_sides(front_side) # should throw error

        front_left_tabs_list = extract_tabs(front_tabs_sides["left_tabs"])
        html_tabs = tabs_to_html(front_left_tabs_list["tabs"])
        front_left_tabs_ready = format_tabs(html_tabs)
        front_left_swap = front_left_tabs_list["tabs_to_swap"]

        front_right_tabs_list = extract_tabs(front_tabs_sides["right_tabs"])
        html_tabs = tabs_to_html(front_right_tabs_list["tabs"])
        front_right_tabs_ready = format_tabs(html_tabs)
        front_right_swap = front_right_tabs_list["tabs_to_swap"]

        back_side = card_sides["back"]
        back_tabs_sides =  extract_tabs_sides(back_side) # could be empty

        back_left_tabs_list = extract_tabs(back_tabs_sides["left_tabs"])
        html_tabs = tabs_to_html(back_left_tabs_list["tabs"])
        back_left_tabs_ready = format_tabs(html_tabs)
        back_left_swap = back_left_tabs_list["tabs_to_swap"]

        back_right_tabs_list = extract_tabs(back_tabs_sides["right_tabs"])
        html_tabs = tabs_to_html(back_right_tabs_list["tabs"])
        back_right_tabs_ready = format_tabs(html_tabs)
        back_right_swap = back_right_tabs_list["tabs_to_swap"]

        front_ready_to_swap = {
                "left": front_left_tabs_ready,
                "right": front_right_tabs_ready,
                "left_swap": front_left_swap,
                "right_swap": front_right_swap
                }

        back_ready_to_swap = {
                "left": back_left_tabs_ready,
                "right": back_right_tabs_ready,
                "left_swap": back_left_swap,
                "right_swap": back_right_swap
                }

        card_swapped = get_swapped_tabs(front_ready_to_swap, back_ready_to_swap)

        formatted_front_left_tab_group = format_tab_group(card_swapped["front"]["left_tabs"])
        formatted_front_right_tab_group = format_tab_group(card_swapped["front"]["right_tabs"])

        formatted_back_left_tab_group = format_tab_group(card_swapped["back"]["left_tabs"])
        formatted_back_right_tab_group = format_tab_group(card_swapped["back"]["right_tabs"])

        formatted_card = {
                "front": (formatted_front_left_tab_group + formatted_front_right_tab_group), 
                "back": (formatted_back_left_tab_group + formatted_back_right_tab_group)
                }

        anki_cards.append(formatted_card)

        logging.debug(f"📔 Formatted card ready for import 📔\n{formatted_card}\n")

    return anki_cards

