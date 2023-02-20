import os

from markdown2anki.utils.debug_tools import expressive_debug


def validate_existing_path(option: str) -> bool:
    try:
        is_absolute = os.path.isabs(option)
        does_exist = os.path.exists(option)
    except:
        return False
    return is_absolute and does_exist


def validate_absolute_path(option: str) -> bool:
    try:
        is_absolute = os.path.isabs(option)
    except:
        return False
    return is_absolute


def validate_folders_list(option: str) -> bool:
    try:
        are_plain_names = os.path.sep not in option
    except TypeError:  # option is None
        return True
    return are_plain_names


def validate_bool(option: str) -> bool:
    user_option = option.lower().strip()
    true_list = ["true", "yes", "t", "y"]
    false_list = ["false", "no", "f", "n"]
    return user_option in true_list or user_option in false_list


def validate_str(option: str) -> bool:
    return True


def validate_int(option: str) -> bool:
    try:
        int(option)
    except:
        return False
    return True
