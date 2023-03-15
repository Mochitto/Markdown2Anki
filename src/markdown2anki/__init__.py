import os
import logging
import sys
from pathlib import Path

from markdown2anki.md_2_anki.utils.card_error import CardError
from markdown2anki.md_2_anki import markdown_to_anki

import markdown2anki
import markdown2anki.logger as log
import markdown2anki.output_handler as out
import markdown2anki.version_check as ver
import markdown2anki.config.configs_handle as config_handle

from markdown2anki.utils.debug_tools import expressive_debug

logger = logging.getLogger(__name__)

# DEV CONFIG
CONFIG_LINK_PATH = str(Path(__file__).parent / "link_to_config_dir.ini")
CONFIGFILE_NAME = "md2anki.config.ini"
ADD_TYPES_TO_CONFIG = False
CONSOLE_DEBUG = False


def main():
    # Basic logging config with handlers
    log.setup_logging(CONSOLE_DEBUG)

    config = config_handle.handle_configs(
        CONFIG_LINK_PATH, CONFIGFILE_NAME, ADD_TYPES_TO_CONFIG
    )
    log.setup_file_logging(
        logger, os.path.join(config["config directory"], "debug_log.txt")
    )

    current_version = ver.get_current_version(markdown2anki.__name__)
    logger.info(f"Running Markdown2Anki v{current_version} 🌸")

    latest_version = ver.get_latest_version(markdown2anki.__name__)
    if not (ver.check_for_version(current_version, latest_version)):
        logger.info(f"⏫ There is a new version available: v{latest_version}!\n"
                    "You can read what's new here: https://github.com/Mochitto/Markdown2Anki/blob/master/CHANGELOG.md\n\n")


    expressive_debug(logger, "Processed config from main", config, "pprint")
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

    if aborted_cards:
        logger.info(f"🙈 Failed to process {aborted_cards} card/s...")
        out.write_failed_cards(failed_cards, config["bad cards file path"])

    if images_to_copy:
        out.copy_images_to_folder(images_to_copy, config["images out-folder"])

    if success_cards:
        logger.info(f"🔥 Successfully created a total of {success_cards} card/s!")
        out.write_cards_to_csv(
            cards_to_write,
            os.path.join(config["config directory"], "basic_anki_cards.csv"),
        )
        out.write_cards_to_csv(
            cards_to_write_with_clozes,
            os.path.join(config["config directory"], "clozed_anki_cards.csv"),
        )

        # Handle backups
        out.backup_file(
            config["input md file path"],
            os.path.join(config["config directory"], "backups"),
        )

        out.clear_backups(
            os.path.join(config["config directory"], "backups"),
            config["Number of backups"],
        )

        if config["clear file?"]:
            out.clear_file(config["input md file path"])

        logger.info("🎆 File/s created! 🎆\nYou can now go import your file/s to Anki :)")
    else:
        logger.info("❓ No cards created... Please check input the file.")

    sys.exit(0)


if __name__ == "__main__":
    main()
