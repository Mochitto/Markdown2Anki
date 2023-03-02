import os
import re
from typing import Dict, List, Set
import logging

import markdown2anki.md_2_anki.utils.common_types as Types

logger = logging.getLogger(__name__)


def find_image_path(
    image_filename: str,
    starting_dir: Types.PathString,
    directories_to_esclude: List[str] = [],
) -> Types.PathString | None:
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
    It will match whatever else that is put as src.

    Pattern:
    <img src="something.png">
    <ImG class="a-class" SRC="ASDJHASKDJaSLKDJj">

    Doesn't match:
    <img src="https://whatever">
    <img SRC="HTTPS://BIG">
    """
    images_regex = re.compile(r"(?i)\<img.*?src=\"(?!https://)(.+?)\".*?\>")
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
