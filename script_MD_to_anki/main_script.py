import csv
import logging
import sys

from card_error import CardError
from config_handle import BAD_CARDS_FILE, CLOZES_RESULT_FILE, FAST_FORWARD, MD_INPUT_FILE, RESULT_FILE, IMAGES_DIR, IMAGES_OUT_FOLDER, FOLDERS_TO_EXCLUDE
from debug_tools import expressive_debug
from md_to_anki import markdown_to_anki
from process_images import copy_images_to_folder
import logger as basicConfig


def main():
    logger = logging.getLogger(__name__)

    logger.info("Starting cards extraction")

    with open(MD_INPUT_FILE, "r", encoding="utf-8") as markdown_file:
        markdown_input = markdown_file.read()

    try:
        cards_with_info = markdown_to_anki(markdown_input, interactive=True, fast_forward=FAST_FORWARD, images_dir=IMAGES_DIR, folders_to_exclude=FOLDERS_TO_EXCLUDE)
    except CardError as error:
        logger.info("\n😯 There was an error and no file was created.\nExited with the following error:")
        logger.error(error)
        sys.exit(1)

    success_cards = cards_with_info["number_of_successful"]
    aborted_cards = cards_with_info["number_of_failed"]
    cards_to_write = cards_with_info["cards"]
    cards_to_write_with_clozes = cards_with_info["cards_with_clozes"]
    images_to_copy = cards_with_info["images_to_copy"]

    failed_cards = cards_with_info["failed_cards"]

    number_of_copied_images, images_error_messages = copy_images_to_folder(images_to_copy, IMAGES_OUT_FOLDER)

    if number_of_copied_images: #TODO: add emojis
        logger.info(f"Copied a total of {number_of_copied_images} images!")
    for message in images_error_messages:
        logger.error(f"Failed to copy an image: {message}")

    if success_cards:
        logger.info(f"🔥 Created a total of {success_cards} card/s!")
        if aborted_cards:
            logger.info(f"🙈 Failed to create {aborted_cards} card/s...")

        if cards_to_write_with_clozes:
            with open(CLOZES_RESULT_FILE, "w", encoding="utf-8") as output:
                fieldnames = ["front", "back"]
                writer = csv.DictWriter(output, fieldnames)
                # writer.writeheader() # The headers also get imported by anki
                # Which creates an extra card every time

                for card in cards_to_write_with_clozes:
                    writer.writerow(card)

        if cards_to_write:
            with open(RESULT_FILE, "w", encoding="utf-8") as output:
                fieldnames = ["front", "back"]
                writer = csv.DictWriter(output, fieldnames)
                # writer.writeheader() # The headers also get imported by anki
                # Which creates an extra card every time

                for card in cards_to_write:
                    writer.writerow(card)

        with open(BAD_CARDS_FILE, "w", encoding="utf-8") as output:
            output.write("\n\n---\n\n".join(failed_cards))

        logger.info("🎆 File/s created! 🎆\nYou can now go import your file/s to Anki :)")

    else:
        logger.info("❓ No cards created... Please check input the file.")

    sys.exit(0)


if __name__ == "__main__":
    main()
