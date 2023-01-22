import logging
import sys

import logger as basicConfig
from md_2_anki.utils.card_error import CardError
from config_handle import (
    LINENOS,
    VAULT,
    BAD_CARDS_FILE,
    CLOZES_RESULT_FILE,
    FAST_FORWARD,
    MD_INPUT_FILE,
    RESULT_FILE,
    IMAGES_DIR,
    IMAGES_OUT_FOLDER,
    FOLDERS_TO_EXCLUDE,
)
from md_2_anki.md_to_anki import markdown_to_anki
from output_handler import copy_images_to_folder, write_cards_to_csv, write_failed_cards

from md_2_anki.utils.debug_tools import expressive_debug


def main():
    logger = logging.getLogger(__name__)

    logger.info("Starting cards extraction")

    with open(MD_INPUT_FILE, "r", encoding="utf-8") as markdown_file:
        markdown_input = markdown_file.read()

    try:
        cards_with_info = markdown_to_anki(
            markdown_input,
            VAULT,
            linenos=LINENOS,
            interactive=True,
            fast_forward=FAST_FORWARD,
            images_dir=IMAGES_DIR,
            folders_to_exclude=FOLDERS_TO_EXCLUDE,
        )
    except CardError as error:
        logger.info(
            "\n😯 There was an error and no file was created.\nExited with the following error:"
        )
        logger.error(error)
        sys.exit(1)

    images_to_copy = cards_with_info["images_to_copy"]
    cards_to_write = cards_with_info["cards"]
    cards_to_write_with_clozes = cards_with_info["cards_with_clozes"]

    success_cards = cards_with_info["number_of_successful"]
    aborted_cards = cards_with_info["number_of_failed"]
    failed_cards = cards_with_info["failed_cards"]

    if aborted_cards:
        logger.info(f"🙈 Failed to process {aborted_cards} card/s...")
        write_failed_cards(failed_cards, BAD_CARDS_FILE)

    if images_to_copy:
        copy_images_to_folder(images_to_copy, IMAGES_OUT_FOLDER)

    if success_cards:
        logger.info(f"🔥 Found a total of {success_cards} card/s!")
        write_cards_to_csv(cards_to_write, RESULT_FILE)
        write_cards_to_csv(cards_to_write_with_clozes, CLOZES_RESULT_FILE)

        logger.info("🎆 File/s created! 🎆\nYou can now go import your file/s to Anki :)")
    else:
        logger.info("❓ No cards created... Please check input the file.")

    sys.exit(0)


if __name__ == "__main__":
    main()
