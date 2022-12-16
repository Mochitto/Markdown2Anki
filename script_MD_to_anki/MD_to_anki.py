import sys
import os
import re
import pprint
import json
import logging
import time
import csv

from text_to_html import markdown_to_html_with_highlight
from cards_specific_wrappers import wrap_label, wrap_body, wrap_tab, wrap_tab_group, activate_first_tab

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

class CardError(Exception):
    """Class used for parsing errors related to the cards."""
    pass

def log_card_error(message: str, card_index: int=None) -> None:
    """Log message as error; if the card_index is present, wait 1.5 s and then log the full card text as error for user-side debugging."""
    logging.error(message)
    if card_index:
        time.sleep(1.5)
        logging.error(f"📔 This is the card that created the error:\n{CARDS[card_index]}")

def extract_cards(markdown_text: str) -> [str]: # TODO: write test for *** ---
    global CARDS
    """Extract the cards from the markdown file. The break points are "---+" and "***+". Return an array of strings (cards).
    """
    regex_pattern = r"\n(?:(?:---+?)|(?:\*\*\*+?))\n" # Match hr in markdown

    cards = re.split(regex_pattern, markdown_text)

    if cards[0]:
        logging.info(f"📦 Found {len(cards)} cards to process...")

    CARDS = cards
    return cards

def format_card(card: str, card_index: int) -> {"front": str, "back": str}:
    """Format card from markdown to html, with all of the necessary classes."""
    # FIXME: Remove the card_index from each function and just raise an error
    sides = extract_sides(card, card_index)
    
    front = prepare_side_for_formatting(sides["front"], card_index)
    back = prepare_side_for_formatting(sides["back"], card_index)

    formatted_card = format_fields(front, back, card_index)
    
    logging.debug(f"📔 Formatted card ready for import 📔\n{formatted_card}\n")

    return formatted_card

def extract_sides(card: str, card_index: int) -> {"front": str, "back": str}: # TODO: write test for optional back side 
    """Extract the text that is under the "Front side" and "Back side", return a dictionary with the two text blocks.
    "Back side" is optional.
    """
    stripped_card = card.strip()

    front_side_regex = re.compile(r"(?si)#\s*front\s*side\s*\n(.*?)(?:\#\s*back\s*side\s*\n|$)")
    back_side_regex = re.compile(r"(?si)#\s*back\s*side\s*\n(.*)")
    
    front_side_match = front_side_regex.search(card)
    back_side_match = back_side_regex.search(card)

    if not front_side_match: 
        log_card_error(f"❌ A card without front-side has been found.\nCard number: {card_index}\nCard content:{stripped_card}.", card_index)
        raise CardError()

    return {
        "front": front_side_match[1],
        "back": back_side_match[1] if back_side_match else ""
    }

def extract_tabs_sides(side_fragment: str, card_index: int) -> {"left_tabs": [], "right_tabs": []}: # TODO: write test for optional right side
    """Extract the text that is under the "left tabs" and "right tabs"."""
    stripped_fragment = side_fragment.strip()

    left_tabs_regex = re.compile(r"(?si)##\s*left\s*tabs\s*\n(.*?)(?=##\s*right\s*tabs|$)")
    right_tabs_regex = re.compile(r"(?si)##\s*right\s*tabs\s*\n(.*)")

    left_tabs_block = re.search(left_tabs_regex, stripped_fragment)
    right_tabs_block = re.search(right_tabs_regex, stripped_fragment)

    if not left_tabs_block: 
        log_card_error(f"❌ A card without left-tabs has been found.\nCard number: {card_index}\nCard side content: {stripped_fragment}.", card_index)
        raise CardError()

    return {
        "left_tabs": left_tabs_block[0],
        "right_tabs": right_tabs_block[0] if right_tabs_block else ""
        }

def extract_tabs(left_or_right_block: str) -> {
    "tabs": [{"tab_label": str, "tab_body": str}], 
    "tabs_to_switch": [int]
    }:
    """Extact the tabs, their text and the indexes of tabs to be swapped."""

    tabs_regex = re.compile(r"###\s*(-)?(.+?)\n(.+?)(?=###|##|$)", re.S)

    tabs_matches = tabs_regex.findall(left_or_right_block)

    tabs = []
    tabs_to_switch = []
    for index, match in enumerate(tabs_matches):
        switch_flag = match[0]
        if switch_flag:
            tabs_to_switch.append(index)

        tab_label = match[1]
        tab_body = match[2]

        tabs.append({"tab_label": tab_label.strip(), "tab_body": tab_body.strip()})
    
    return {"tabs": tabs, "tabs_to_switch": tabs_to_switch}

def format_fields(front: str, back: str, card_index: int) -> {"front": str, "back": str}:
    """Activate the first tab of each tabs side, wrap the tabs sides in tab_group containers and join them.
    If the back side is present, swap the the front tabs with back tabs (if needed) and repeat the first step with the back tabs."""
    # Format the front field -----------------------------------
    front_left, front_right = front["left"], front["right"]

    activated_front_left = activate_first_tab(front_left)
    activated_front_right = activate_first_tab(front_right)
    
    front_for_field = wrap_tab_group("".join(activated_front_left), True) + wrap_tab_group("".join(activated_front_right))
    
    front_for_field_without_newlines = remove_newlines(front_for_field)

    if not back: 
        return {
            "front": front_for_field_without_newlines, 
            "back":front_for_field_without_newlines
            }
    

    # FIXME: Should tabs be swapped with one of the same index or with the first tab possible?
    # If you change this, make sure yo also fix the back_left and back_right variables.

    # Swap the tabs on the front (that are scheduled to be swapped) with those of the same index in the back.
    # WET for readability and specific logging errors
    try: 
        left_to_include = [element if index not in front["left_swap"] 
                            else back["left"][index] 
                            for index, element in enumerate(front["left"])]
    except IndexError:
            tabs_to_swap = ', '.join(front['left_swap'])
            log_card_error(
            f"❌ Card number {card_index}:\n"
            + f"Supposed to swap a left tab (To swap: {tabs_to_swap}),"
            + f"but there's no counterpart in the BACK LEFT tabs.\n"
            + f"⬅ FRONT LEFT:\n{json.dumps(front['left'], indent=1)}\n"
            + f"⬅ BACK LEFT:\n{json.dumps(back['left'], indent=1)}\n", 
            card_index)
            raise CardError()

    try:
        right_to_include = [element if index not in front["right_swap"]
                             else back["right"][index] 
                             for index, element in enumerate(front["right"])]
    except IndexError:
        tabs_to_swap = ', '.join(front['right_swap'])
        log_card_error(
            f"❌ Card number {card_index}:\n" 
            + f"is supposed to swap a right tab (To swap: {tabs_to_swap})," 
            + f"but there's no counterpart in the BACK RIGHT tabs.\n" 
            + f"➡ FRONT RIGHT:\n{json.dumps(front['right'], indent=1)}\n"
            + f"➡ BACK RIGHT:\n{json.dumps(back['right'], indent=1)}\n", 
        card_index)
        raise CardError()
    
    # Format the back field -----------------------------------
    # Keep only tabs that haven't been swapped
    back_left = [element for index, element in enumerate(back["left"]) if index not in front["left_swap"]]
    back_right = [element for index, element in enumerate(back["right"]) if index not in front["right_swap"]]

    activated_back_left = activate_first_tab(left_to_include + back_left)
    activated_back_right = activate_first_tab(right_to_include + back_right)

    back_for_field = wrap_tab_group("".join(activated_back_left), True) + wrap_tab_group("".join(activated_back_right))

    back_for_field_without_newlines = remove_newlines(back_for_field)

    return {"front": front_for_field_without_newlines, "back":back_for_field_without_newlines}

def remove_newlines(text: str) -> str:
    """Remove newlines from the text.
    This is needed because all the newlines INSIDE tags will become <br>, when needed.
    The remaining newlines are linked to the markdown and become useless as block elements do not need them.
    
    TODO: This might become a useless step depending on mistune's configuration?"""
    return re.sub(r"\n", "", text)

def prepare_side_for_formatting(card_side: str, card_index: int): 
    """Extract tabs and which ones have to be swapped, from a card side."""

    if not card_side: return # Empty/missing side

    side_s_tabs = extract_tabs_sides(card_side, card_index)
    
    tabs_ready = prepare_tabs_for_formatting(side_s_tabs)

    logging.debug("🔃 Tabs ready for formatting 🔃\n" + json.dumps(tabs_ready, indent=2))
    return tabs_ready

def tab_to_html(tab: {"tab_label": str, "tab_body": str}) -> str:
    """Compile the tab to html and wrap it in cards' specific wrappers"""
    label = tab["tab_label"]
    body_html = markdown_to_html_with_highlight(tab["tab_body"])
    
    # The following steps are specific to the cards' CSS and HTML structure.
    # Please change them when applying changes to the HTML/CSS/JS.
    tab_label = wrap_label(label)
    tab_body = wrap_body(body_html)
    finished_tab = wrap_tab(tab_label, tab_body)

    return finished_tab

def prepare_tabs_for_formatting(tabs: {"left_tabs": str, "right_tabs": str}) -> {
        "left": str,
        "right": str,
        "left_swap": [int],
        "right_swap": [int]
    }:
    """Prepare tabs by extracting them form the string and compiling them to html"""
    left_tabs_list = extract_tabs(tabs["left_tabs"])
    right_tabs_list = extract_tabs(tabs["right_tabs"])
    
    # Wet for readability
    left_tabs_html = []
    for tab in left_tabs_list["tabs"]:
        finished_tab = tab_to_html(tab)
        left_tabs_html.append(finished_tab)

    right_tabs_html = []
    for tab in right_tabs_list["tabs"]:
        finished_tab = tab_to_html(tab)
        right_tabs_html.append(finished_tab)

    return {
        "left": left_tabs_html, 
        "right": right_tabs_html, 
        "left_swap": left_tabs_list["tabs_to_switch"],
        "right_swap": right_tabs_list["tabs_to_switch"]}


def main():
    # logging.basicConfig(filename='process.log', level=logging.INFO)
    formatter = "%(levelname)s: %(message)s"
    logging.basicConfig(level=logging.INFO, format=formatter)
    logging.info('Starting cards extraction')

    with open("Template for coding cards.md", "r", encoding="utf-8") as markdown_file:
        markdown_input = markdown_file.read()

    cards = extract_cards(markdown_input)
    if not cards[0]:
        logging.info('❓ No cards found... Please check input file.')
        sys.exit(0)

    success_cards = 0
    aborted_cards = 0
    cards_to_write = []

    for index, card in enumerate(cards):
        try:
            card_to_write = format_card(card, index)
        except CardError:
            if input("❌ Would you like to continue creating the cards, without this one? (y/N)\n>>> ").lower() != "y":
                logging.info("⛔ Process aborted. No file was created.")
                sys.exit(0)
            else:
                aborted_cards += 1
                continue
        success_cards += 1

        cards_to_write.append(card_to_write)
        logging.info(f"✅ Finished processing card number {index+1}...")

    if aborted_cards:
        logging.info(f"🙈 Failed to create {aborted_cards} card/s...")

    if success_cards:
        logging.info(f"🔥 Created a total of {success_cards} card/s!")

        with open("result.csv", "w") as output:
            fieldnames = ["front", "back"]
            writer = csv.DictWriter(output, fieldnames)
            # writer.writeheader() # The headers also get imported by anki
            # Which creates an extra card every time 

            for card in cards_to_write:
                writer.writerow(card)

        logging.info('🎆 File created! 🎆\nYou can now go import your file in Anki :)')

    else:
        logging.info('❓ No cards created... Please check input the file.')

    sys.exit(0)

if __name__ == "__main__":
    main()
