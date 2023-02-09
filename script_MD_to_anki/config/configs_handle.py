import configparser
import os
import sys
from typing import Tuple, Dict, Any
import logging

from utils import common_types as Types
import md_2_anki.utils.card_types as CardTypes
from utils.debug_tools import expressive_debug

from first_config import welcome_user
from parse_args import CommandLineArgsParser
from config_setup import setup_typeConfig

logger = logging.getLogger(__name__)


def get_configfile_paths(link_to_configfile) -> Tuple[Types.PathString, str]:
    current_folder = os.path.split(__file__)[0]
    complete_path_to_link = os.path.join(current_folder, link_to_configfile)

    if not os.path.exists(complete_path_to_link):
        raise FileNotFoundError(
            "The path to the file containing the link to the config file doesn't exist."
        )

    links = configparser.ConfigParser()
    links.read(complete_path_to_link)

    config_dir = links["LINKS"]["config_dir"]
    config_file = links["LINKS"]["config_file"]

    configfile_path = os.path.join(config_dir, config_file)

    if not os.path.exists(configfile_path):
        raise FileNotFoundError("The config file doesn't exist.")

    return (config_dir, config_file)


def get_CLI_config():
    cli_config = CommandLineArgsParser.parse_args()
    return vars(cli_config)


def get_file_config_content(path_to_config_file: Types.PathString) -> str:
    with open(path_to_config_file, "r") as config_file:
        content = config_file.read()
    return content


def write_file_config_content(
    path_to_config_file: Types.PathString, content: str
) -> None:
    with open(path_to_config_file, "w") as config_file:
        config_file.write(content)


def handle_configs() -> Dict[str, Any]:
    ADD_TYPES_TO_CONFIG = True
    CONFIG_LINK_PATH = "link_to_config_dir.ini"
    CONFIGFILE_NAME = "md2anki.config.ini"

    try:
        config_dir, config_file = get_configfile_paths(CONFIG_LINK_PATH)
    except FileNotFoundError:
        welcome_user(
            configfile_name=CONFIGFILE_NAME,
            path_to_link=CONFIG_LINK_PATH,
            add_type_hints=ADD_TYPES_TO_CONFIG,
        )
        sys.exit(0)

    fileConfig = setup_typeConfig(config_dir, ADD_TYPES_TO_CONFIG)
    file_config_content = get_file_config_content(os.path.join(config_dir, config_file))

    cli_config = get_CLI_config()
    if cli_config["Link config?"]:
        welcome_user(
            configfile_name=CONFIGFILE_NAME,
            path_to_link=CONFIG_LINK_PATH,
            add_type_hints=ADD_TYPES_TO_CONFIG,
        )
        sys.exit(0)
    elif cli_config["Heal config?"]:
        healed_config = fileConfig.heal_config(file_config_content)
        write_file_config_content(os.path.join(config_dir, config_file), healed_config)
        logger.info("🩹 File healed!")
        sys.exit(0)
    else:
        # This step is needed to prepare the options that were actually set
        # for validation.
        cli_config.pop("Link config?")
        cli_config.pop("Heal config?")
        for option, value in cli_config.items():
            if value == None:
                cli_config.pop(option)
    expressive_debug(logger, "cli config", cli_config, "pprint")

    valid_cli_config, cli_errors = fileConfig.validate_config(cli_config)
    file_config, file_errors = fileConfig.parse_config(file_config_content)

    if cli_errors or file_errors:
        if cli_errors:
            logger.error("❌ An error occurred while parsing the CLI arguments:")
        for option, error in cli_errors.items():
            logger.error(f"|--- {option}: {error}")
        if file_errors:
            logger.error("❌ An error occurred while parsing the config file:")
        for option, error in file_errors.items():
            logger.error(f"|--- {option}: {error}")
        sys.exit(1)

    expressive_debug(logger, "valid CLI config", valid_cli_config, "pprint")

    result_config = fileConfig.merge_config(valid_cli_config, file_config)

    return result_config


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    # There is a bug in type config when validating data.
    # Once that's solved, the config handle should be working and
    # Perform all the needed operations

    # The next step is making the project work again (plugging config handle in main)
    # And then writing tests for all of the parts before moving on to changing
    # The extraction step
    expressive_debug(logger, "config", handle_configs(), "pprint")
