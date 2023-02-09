import os
import logging
import sys

from md_2_anki.utils.card_error import CardError
from md_2_anki.md_to_anki import markdown_to_anki

from logger import setup_logging, setup_file_logging 
from output_handler import copy_images_to_folder, write_cards_to_csv, write_failed_cards
from config.configs_handle import handle_configs

from utils.debug_tools import expressive_debug

logger = logging.getLogger(__name__)


def main():
    # Basic logging config with handlers
    setup_logging()
    config = handle_configs()
    expressive_debug(logger, "Config from main", config, "pprint")

    setup_file_logging(logger, os.path.join(config["config directory"], "debug_log.txt"))

    logger.info("Starting cards extraction")

    with open(config["input md file path"], "r", encoding="utf-8") as markdown_file:
        markdown_input = markdown_file.read()
    try:
        cards_with_info = markdown_to_anki(
            markdown_input,
            config["Obsidian valut name"],
            linenos=config["line numbers?"],
            interactive=True,
            fast_forward=config["fast forward?"],
            images_dir=config["search images folder"],
            folders_to_exclude=config["folders to exclude"],
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

    # TODO: Use clear file? by writing to the input file if true
    # And saving what was in the file in a backup in the config folder

    if aborted_cards:
        logger.info(f"🙈 Failed to process {aborted_cards} card/s...")
        write_failed_cards(failed_cards, config["bad cards file path"])

    if images_to_copy:
        copy_images_to_folder(images_to_copy, config["images out-folder"])

    if success_cards:
        logger.info(f"🔥 Found a total of {success_cards} card/s!")
        write_cards_to_csv(cards_to_write, os.path.join(config["config directory"], "basic_anki_cards.csv"))
        write_cards_to_csv(cards_to_write_with_clozes, os.path.join(config["config directory"], "clozed_anki_cards.csv"))

        logger.info("🎆 File/s created! 🎆\nYou can now go import your file/s to Anki :)")
    else:
        logger.info("❓ No cards created... Please check input the file.")

    sys.exit(0)


if __name__ == "__main__":
    main()
