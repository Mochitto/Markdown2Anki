import os
import sys
import logging
from pathlib import Path
import shutil

from .config_setup import setup_typeConfig
from markdown2anki.utils import common_types as Types
import markdown2anki.md_2_anki.utils.card_types as CardTypes

logger = logging.getLogger(__name__)


def welcome_user(
    configfile_name: str,
    path_to_link: Types.PathString,
    add_type_hints=False,
    welcome_message=True,
):
    """
    Welcome the user by printing the content of
    "welcome_message.txt", which is in the same directory as
    this module.
    Get input from the user to obtain an existing absolute path
    to the directory where they want their output data to be.
    """

    this_directory = Path(__file__).parent

    # Welcome the user
    if welcome_message:
        welcome_msg = get_welcome_message(
            os.path.join(this_directory, "welcome_message.txt")
        )
        logger.info(welcome_msg)

    configfile_directory = get_input_config_path()
    configfile_path = os.path.join(configfile_directory, configfile_name)

    create_link_to_config_file(path_to_link, configfile_path)

    fileConfig = setup_typeConfig(configfile_directory, add_type_hints)

    # Handle update or creation of config file
    if os.path.exists(configfile_path):
        # Update the existing configuration
        with open(configfile_path, "r+") as config_file:
            config_file_content = config_file.read()
            updated_config = fileConfig.heal_config(config_file_content)
            config_file.seek(0)
            config_file.write(updated_config)
            logger.info("🔧 Config file healed and location updated!")
    else:
        # Create configuration
        with open(configfile_path, "w") as config_file:
            config_file_content = fileConfig.create_config()
            config_file.write(config_file_content)
            logger.info("🔧 Config file created!")
            logger.info(
                "You should now configure it to your liking, before using the program ⭐"
            )

    # Create or overwrite the APKG file
    create_anki_package(Path(configfile_directory))


def create_link_to_config_file(
    path_to_link: Types.PathString,
    path_to_config_file: Types.PathString,
) -> None:
    """
    Create an ini file that stores the path to the config file and config folder.
    This can be accessed to check if it's the first time the app is running and
    to use as a default output folder.
    """
    config_dir, config_file = os.path.split(path_to_config_file)
    with open(path_to_link, "w") as link_to_dir:
        link_to_dir.write(
            "[LINKS]\n" f"config_dir = {config_dir}\n" f"config_file = {config_file}"
        )


def create_anki_package(path_to_config_directory: Path) -> None:
    filename = "Markdown2Anki.apkg"
    source = Path(__file__).parent / filename
    destination = path_to_config_directory / filename
    shutil.copy(str(source), str(destination))
    

def get_welcome_message(path_to_welcome_file: Types.PathString) -> str:
    """
    Retrieve the welcome message from the given path.
    """
    with open(path_to_welcome_file, "r") as welcome_file:
        welcome_msg = welcome_file.read()

    return welcome_msg


def get_input_config_path() -> Types.PathString:
    """
    Get an existing absolute path to a folder, that
    is used to store the config file.
    """
    invalid_input = True
    config_path = ""

    while invalid_input:
        config_path = input("\n📁 Absolute path to an existing folder:\n> ")

        if config_path.lower().strip() == "exit":
            sys.exit(0)

        if os.path.exists(config_path) and os.path.isdir(config_path):
            confirm = input(
                "\nThis path exists and is a folder! 🐙\n"
                f"A config file will be created in: {config_path}\n\n"
                "Continue? (Y/n): "
            )

            if confirm.lower() == "n":
                continue
            elif confirm.lower() == "exit":
                sys.exit(0)

            # Exit case
            invalid_input = False
        else:
            # Recursive case
            logger.warning(
                f"The given path doesn't exist or isn't a folder... 😳\n{config_path}"
            )

    return config_path
