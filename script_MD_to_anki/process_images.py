import shutil
import os
import re
from typing import Dict, List, Set, Tuple
import logging

import card_types as Types

logger = logging.getLogger(__name__)


def find_image_path(
    image_filename: str,
    starting_dir: Types.PathString,
    directories_to_esclude: List[str] = [],
):
    """
    Finds the path to the image file with a tree walk, starting from "starting_dir" and excluding
    directories that are in "directories_to_exclude".
    Return None if the image is not found.

    More on the how directories are excluded:
    https://stackoverflow.com/questions/19859840/excluding-directories-in-os-walk
    """
    for root, dirs, files in os.walk(starting_dir, topdown=True):
        dirs[:] = [
            directory for directory in dirs if directory not in directories_to_esclude
        ]
        if image_filename in files:
            return os.path.join(root, image_filename)
    return None


def get_images_sources(text: Types.HTMLString) -> Set[Types.PathString]:
    """
    Get images' path as listed in img tags' src attribute.
    It won't match sources starting with https://

    Pattern:
    src="something.png"
    src="Awaadjklsakjd"
    Doesn't match:

    src="https://whatever"
    SRC="HTTPS://BIG"
    """
    images_regex = re.compile(r"(?i)src=\"(?!https://)(.+?)\"")
    images = images_regex.findall(text)
    return set(images)


def get_images_to_copy(
    cards: Dict[str, Types.HTMLString],
    starting_dir: Types.PathString,
    folders_to_exclude: List[str] = [],
) -> Dict[str, Types.PathString | None]:
    """
    Find images to copy from card/s, looking from "starting_dir" and excluding "folders_to_esclude".
    Return Dict:
    key: image's filename
    value: path to Image
    '"""
    # Extract images' file names from cards
    images_to_copy = set()
    for side in cards.values():
        images_to_copy.update(get_images_sources(side))

    # Match the images' file names (key) with their path (value)
    images_paths = dict()
    for image in images_to_copy:
        images_paths[image] = find_image_path(image, starting_dir, folders_to_exclude)

    return images_paths


def copy_images_to_folder(
    images_to_copy: Dict[str, Types.PathString | None], outdir_folder: Types.PathString
) -> Tuple[int, List[str]]:  # DOCS TODO: write that there is no metadata copied
    """
    Copy the images to the outdir folder and return (number of copied images, list of errors, if there was any).
    Raise CardError if the image to copy doesn't exist.

    Dict:
    "image.extension" : "path/to/image.extension"
    """
    # FIXME: could use a much better UX on the errors handling
    success = 0
    images_error_messages = []
    for image, path_to_image in images_to_copy.items():
        if not path_to_image:
            images_error_messages.append(f"Couldn't copy \"{image}\" (File not found)'")
            continue

        destination_path = os.path.join(outdir_folder, image)

        if os.path.exists(destination_path):
            continue  # There is an image already

        try:
            shutil.copyfile(path_to_image, destination_path)
            success += 1
        except (
            shutil.SameFileError,
            PermissionError,
            FileNotFoundError,
            TypeError,
            IsADirectoryError,
        ) as error:
            error_message = f'Couldn\'t copy "{image}" ({error.__class__.__name__}).'
            images_error_messages.append(error_message)
            continue
    return (success, images_error_messages)
