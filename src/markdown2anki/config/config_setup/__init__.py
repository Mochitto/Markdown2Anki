import os
import logging

from type_config import TypeConfig

from markdown2anki.utils import common_types as Types
from markdown2anki.utils.debug_tools import expressive_debug

from . import validators as val
from . import casters as cas

logger = logging.getLogger(__name__)


def setup_typeConfig(base_path: Types.PathString, type_hints=False) -> TypeConfig:
    """
    Initialize a TypeConfig object with the needed types
    and options.
    """

    fileConfig = TypeConfig(type_hints)

    fileConfig.add_type(
        "ExistingPath",
        val.validate_existing_path,
        cas.cast_existing_path,
        "The given path doesn't exist.",
    )
    fileConfig.add_type(
        "AbsolutePath",
        val.validate_absolute_path,
        cas.cast_absolute_path,
        "The given path is not absolute.",
    )
    fileConfig.add_type(
        "NewFolder",
        val.validate_absolute_path,
        cas.cast_new_folder,
        "The given path to the folder is not absolute.",
    )
    fileConfig.add_type(
        "FoldersList",
        val.validate_folders_list,
        cas.cast_folders_list,
        "Folders names must not contain slashes; only the name is needed.",
    )
    fileConfig.add_type(
        "bool",
        val.validate_bool,
        cas.cast_bool,
        "Must be one of these (caps is ignored): true, t, yes, y, false, f, no, n",
    )
    fileConfig.add_type(
        "str",
        val.validate_str,
        cas.cast_str,
        "Somehow this is not a string. Write an issue to the project's github please; this shouldn't happen.",
    )
    fileConfig.add_type(
        "int", val.validate_int, cas.cast_int, "The option is not an integer."
    )

    fileConfig.add_option(
        type="str",
        option="Obsidian valut name",
        help="The name of the obsidian vault where the input file is from.",
        important_help="If left empty, Obsidian links will not work in your cards.",
        default="",
    )
    fileConfig.add_option(
        type="ExistingPath",
        option="search images folder",
        help="This is where the program will look for images when they appear in your cards.\nIt also searches inside of subfolders.",
        important_help="Necessary. Must be an absolute path to an existing folder.",
    )
    fileConfig.add_option(
        type="NewFolder",
        option="images out-folder",
        help="Where the images are copyed to when found in your cards.\nThis could be your anki's media's folder (https://docs.ankiweb.net/files.html#file-locations).",
        important_help="Must be an absolute path. If the folder is missing, it's created by the program.\nDefaults to an 'images' folder where this config file is.",
        default=os.path.join(base_path, "images"),
    )
    fileConfig.add_option(
        type="AbsolutePath",
        option="bad cards file path",
        help="The path to the file where cards will be written to, when there is an error with them.\nThis could be inside of your Obsidian vault for faster editing.",
        important_help="Must be an absolute path. Defaults to a 'bad_cards.md' file where this config file is.",
        default=os.path.join(base_path, "bad_cards.md"),
    )
    fileConfig.add_option(
        type="ExistingPath",
        option="input md file path",
        help="The path to your markdown input file. This could be inside of your Obsidian vault.",
        important_help="Necessary. Must be an absolute path.",
    )

    # Behaviour

    fileConfig.add_option(
        type="int",
        option="Number of backups",
        help=(
            "The number of backup files to keep (a backup is created every time you process your input file and is a copy of it)\n"
            'Backups can be very useful when "Clear file?" is set to True.'
        ),
        important_help="Must be an integer. Defaults to 10.",
        default="10",
    )

    fileConfig.add_option(
        type="bool",
        option="clear file?",
        help="Whether or not to clear the input markdown file upon cards creation.",
        important_help="Choices: True/False. Defaults to False. A file can't be restored once it has been cleared.",
        default="False",
    )
    fileConfig.add_option(
        type="bool",
        option="line numbers?",
        help="Whether or not to add line numbers to code blocks.",
        important_help="Choices: True/False. Defaults to True.",
        default="True",
    )
    fileConfig.add_option(
        type="bool",
        option="fast forward?",
        help="Whether or not to continue processing cards when there is an error in them.\nWhen fast forwarding, cards with errors are skipped but can still be found in the bad cards file and be fixed.\nWhen not fast forwarding, you will be showed the card and asked if you want to continue or not.",
        important_help="Choices: True/False. Defaults to True.",
        default="True",
    )
    fileConfig.add_option(
        type="FoldersList",
        option="folders to exclude",
        help="The names of the folders that will be excluded when looking for images to copy. Makes the process faster.",
        important_help="Must be a list of folders names, divided by commas. Can be left empty if you want to search in all sub-folders as well.",
        can_be_empty=True,
    )

    return fileConfig
