import logging
import sys

from logger import setup_logging, setup_file_logging 
from md_2_anki.utils.card_error import CardError
from md_2_anki.md_to_anki import markdown_to_anki
from output_handler import copy_images_to_folder, write_cards_to_csv, write_failed_cards

from md_2_anki.utils.debug_tools import expressive_debug

logger = logging.getLogger(__name__)


def main():
    # Basic logging config with handlers
    setup_logging()
    # I should check for the config value here at line 24 instead than doin it in the file
    # Check for config file
    #   If exists:
    #       continue the program
    #   If doesn't exist:
    #       run creation


    cli_args = CommandLineArgsParser.parse_args(sys.argv[1:])
    file_config = get_config_file()
    config = MergeConfigs(
        command_line_args=cli_args, config_from_file=file_config
    ).merged_config

    # setup_logging(config["log_file"])

    logger.info("Starting cards extraction")

    with open(config["md_input_file"], "r", encoding="utf-8") as markdown_file:
        markdown_input = markdown_file.read()

    try:
        cards_with_info = markdown_to_anki(
            markdown_input,
            config["vault_name"],
            linenos=config["linenos"],
            interactive=True,
            fast_forward=config["fast_forward"],
            images_dir=config["images_dir"],
            folders_to_exclude=config["folders_to_exclude"],
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
        write_failed_cards(failed_cards, config["failed_cards_file"])

    if images_to_copy:
        copy_images_to_folder(images_to_copy, config["images_out_folder"])

    if success_cards:
        logger.info(f"🔥 Found a total of {success_cards} card/s!")
        write_cards_to_csv(cards_to_write, config["anki_csv_file"])
        write_cards_to_csv(cards_to_write_with_clozes, config["clozes_anki_csv_file"])

        logger.info("🎆 File/s created! 🎆\nYou can now go import your file/s to Anki :)")
    else:
        logger.info("❓ No cards created... Please check input the file.")

    sys.exit(0)


if __name__ == "__main__":
    main()
