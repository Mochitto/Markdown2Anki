import pygments
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters.html import HtmlFormatter
# Changed line 787 
# From: "                yield 1, '<span id="%s">%s</span>' % (s, i, line)"
# To: "                yield 1, '<span class="%s">%s</span>' % (s, line)"
# To avoid iterating over the code different times to format it in a different way.

import sys
import os
import re
import pprint
import logging
from itertools import zip_longest

from text_to_html import markdown_to_html_with_highlight


# path = os.getcwd()
# source_file = sys.argv[1]

linenos_true = True # TODO: add config file or something to turn them off
code_highlighted_counter = 0

with open("Template for coding cards.md", "r") as markdown_file:
    markdown_input = markdown_file.read()

def highlight_code(markdown_code, language):
    return


def extract_cards(markdown_text: str) -> [str]: # TODO: write test for *** ---
    """Extract the cards from the markdown file. The break points are "---+" and "***+". Return an array of strings (cards).
    """
    regex_pattern = r"\n(?:(?:---+?)|(?:\*\*\*+?))\n" # Match hr in markdown

    cards = re.split(regex_pattern, markdown_text)

    logging.info(f"📦 Found {len(cards)} cards to process...")
    return cards

def extract_front_back(card, card_index): # TODO: write test for optional back side 
    """Extract the text that is under the "Front side" and "Back side", return a dictionary with the two text blocks.
    "Back side" is optional.
    """
    stripped_card = card.strip()

    front_side_regex = re.compile(r"(?si)#\s*front\s*side\s*\n(.*?)(?:\#\s*back\s*side\s*\n|$)")
    back_side_regex = re.compile(r"(?si)#\s*back\s*side\s*\n(.*)")
    
    front_side_match = front_side_regex.search(card)
    back_side_match = back_side_regex.search(card)

    if not front_side_match: logging.error(f"A card without front-side has been found.\nCard number: {card_index}\nCard content:{stripped_card}.")

    return {
        "front": front_side_match[0],
        "back": back_side_match[0] if back_side_match else ""
    }

def extract_left_right_tabs(front_or_back_fragment: str):
    """Extract the text that is under the "left tabs" and "right tabs", return a dictionary with the two text blocks.
    "right tabs" is optional.
    """
    left_tabs_regex = re.compile(r"(?si)##\s*left\s*tabs\s*\n(.+?)(?=##\s*right\s*tabs|$)")
    right_tabs_regex = re.compile(r"(?si)##\s*right\s*tabs\s*\n(.*)")

    left_tabs_block = re.search(left_tabs_regex, front_or_back_fragment)
    right_tabs_block = re.search(right_tabs_regex, front_or_back_fragment)

    if not left_tabs_block: logging.error(f"A card without front-side has been found.\nCard number: {card_index}\nCard content:{stripped_card}.")
    return {
        "left_tabs_block": left_tabs_block[0],
        "right_tabs_block": right_tabs_block[0] if right_tabs_block else ""
    }

def extract_tabs(left_or_right_block: str) -> {
    "tabs": [{"tab_label": str, "tab_body": str}], 
    "tabs_to_switch": [int]
    }:
    """Extact the tabs and their text. 
    It returns a dictionary with tabs and the index of the tabs that will be switched (when passing from front to back)."""

    tabs_regex = re.compile(r"###\s*(-)?(.+?)\n(.+?)(?=###|##|$)", re.S)
    """$1 = switch_flag, $2 = tab_label, $3 = tab_body """

    tabs_matches = tabs_regex.findall(left_or_right_block)
    tabs = []
    tabs_to_switch = []
    for index, match in enumerate(tabs_matches):
        switch_flag = match[0]
        tab_label = match[1]
        tab_body = match[2]
        if switch_flag: tabs_to_switch.append(index)
        tabs.append({"tab_label": tab_label, "tab_body": tab_body})
    
    return {"tabs": tabs, "tabs_to_switch": tabs_to_switch}

def main():
    # logging.basicConfig(filename='process.log', level=logging.INFO)
    formatter = "%(levelname)s: %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=formatter)
    logging.info('Starting cards extraction')
    
    
    cards = extract_cards(markdown_input)
    for index, card in enumerate(cards):
        back_front_sides = extract_front_back(card, index)
        left_and_right_tabs = extract_left_right_tabs(back_front_sides["front"])
        left_tabs = extract_tabs(left_and_right_tabs["left_tabs_block"])
        to_code = left_tabs["tabs"][0]["tab_body"]
        html = markdown_to_html_with_highlight(text)(to_code)


        logging.info(f"✅ Finished processing card number {index+1}...")

    logging.info(f"🔨 Highlighted a total of {code_highlighted_counter} code snippets!")

    logging.info(f"🔥 Created a total of {len(cards)} cards!")

    logging.info('🎆 File created! You can now go import your file in Anki :)')

if __name__ == "__main__":
    main()
