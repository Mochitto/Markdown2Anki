import configparser
import os
import sys
from typing import Tuple, Dict, Any
import logging
from pathlib import Path

from markdown2anki.utils import common_types as Types
import markdown2anki.md_2_anki.utils.card_types as CardTypes
from markdown2anki.utils.debug_tools import expressive_debug

from .first_config import welcome_user, create_anki_package
from .parse_args import CommandLineArgsParser
from .config_setup import setup_typeConfig

logger = logging.getLogger(__name__)


def get_configfile_paths(
    link_to_configfile: Types.PathString,
) -> Tuple[Types.PathString, str]:
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


def handle_configs(
    config_link_path: Types.PathString,
    configfile_name: Types.PathString,
    add_types_to_config: bool = False,
) -> Dict[str, Any]:
    """
    Handle both arguments from the CLI and from the config file.
    If there are special CLI commands, the operations linked to them
    are carried out, often resulting in exiting the program.
    If there are errors in the parsing, the errors are printed to
    using logging and exit the program.
    If there are no errors during parssing, return the config dictionary with
    the validated data.
    """
    try:
        config_dir, config_file = get_configfile_paths(config_link_path)
    except FileNotFoundError:
        welcome_user(
            configfile_name=configfile_name,
            path_to_link=config_link_path,
            add_type_hints=add_types_to_config,
        )
        sys.exit(0)

    fileConfig = setup_typeConfig(config_dir, add_types_to_config)
    file_config_content = get_file_config_content(os.path.join(config_dir, config_file))

    cli_config = get_CLI_config()
    if cli_config["Anki package?"]:
        create_anki_package(Path(config_dir))
        logger.info("✨ Anki file created in your config folder!")
        sys.exit(0)
    elif cli_config["Link config?"]:
        welcome_user(
            configfile_name=configfile_name,
            path_to_link=config_link_path,
            add_type_hints=add_types_to_config,
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
        cli_config.pop("Anki package?")
        cli_config.pop("Link config?")
        cli_config.pop("Heal config?")
        for option, value in cli_config.items():
            if value == None:
                cli_config.pop(option)

    file_config, file_errors = fileConfig.parse_config(file_config_content)
    # expressive_debug(logger, "File config Parsed", file_config, "pprint")
    validated_file_config, file_validation_errors = fileConfig.validate_config(
        file_config
    )
    # expressive_debug(logger, "Validated file config", validated_file_config, "pprint")

    # Pop is used so that this extra option doesn't break the validation
    if cli_config.pop("Bad file as input?"):
        # None will let the user know the value is unset with an error
        bad_file_path = file_config.get("bad cards file path", None)
        cli_config["input md file path"] = bad_file_path

    validated_cli_config, cli_errors = fileConfig.validate_config(cli_config)

    if cli_errors or file_errors or file_validation_errors:
        if cli_errors:
            logger.error("❌ An error occurred while parsing the CLI arguments:")
            for option, error in cli_errors.items():
                logger.error(f"|--- {option}: {error}")
        if file_errors:
            logger.error("❌ An error occurred while parsing the config file:")
            for option, error in file_errors.items():
                logger.error(f"|--- {option}: {error}")
        if file_validation_errors:
            logger.error("❌ An error occurred while validating the config file:")
            for option, error in file_validation_errors.items():
                logger.error(f"|--- {option}: {error}")
        sys.exit(1)

    result_config = fileConfig.merge_config(validated_cli_config, validated_file_config)
    result_config["config directory"] = config_dir

    return result_config
