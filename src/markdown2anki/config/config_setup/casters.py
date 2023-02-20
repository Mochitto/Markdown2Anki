from typing import List
import os

from markdown2anki.utils import common_types as Types
import markdown2anki.md_2_anki.utils.card_types as CardTypes
from markdown2anki.utils.debug_tools import expressive_debug


def cast_existing_path(option: str) -> Types.PathString:
    return option


def cast_absolute_path(option: str) -> Types.PathString:
    return option


def cast_new_folder(option: str) -> Types.PathString:
    """
    Creates folder if missing.
    """
    os.makedirs(option, exist_ok=True)
    return option


def cast_folders_list(option: str) -> List[str]:
    if option is None:
        return []
    folders = option.split(",")
    cleaned_folders = [folder.strip() for folder in folders]
    return cleaned_folders


def cast_bool(option: str) -> bool:
    user_option = option.lower().strip()
    true_list = ["true", "yes", "t", "y"]
    return True if user_option in true_list else False


def cast_str(option: str) -> str:
    return option


def cast_int(option: str) -> int:
    return int(option)
