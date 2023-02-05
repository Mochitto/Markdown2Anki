import csv
import logging
import os
import shutil
from typing import Dict, List

import md_2_anki.utils.card_types as Types
from md_2_anki.utils.debug_tools import expressive_debug

logger = logging.getLogger(__name__)


# FIXME: Could use some better error handling maybe
def copy_images_to_folder(
    images_to_copy: Dict[str, Types.PathString | None], outdir_folder: Types.PathString
) -> None:  # DOCS TODO: write that there is no metadata copied
    """
    Copy the images to the outdir folder and return (number of copied images, list of errors, if there was any).
    Raise CardError if the image to copy doesn't exist.

    Dict:
    "image.extension" : "path/to/image.extension"
    """
    logger.info("📷 Copying the images!")
    success = 0
    for image, path_to_image in images_to_copy.items():
        if not path_to_image:
            logger.warning(f'|--- Couldn\'t copy "{image}" (File not found)')
            continue

        destination_path = os.path.join(outdir_folder, image)

        if os.path.exists(destination_path):
            logger.warning(f'|--- Skipping "{image}": it\'s already in the folder')
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
            logger.error(
                f"|--- Failed to copy an image: '{image}' ({error.__class__.__name__})."
            )
            continue

    if success:
        logger.info(f"|--- Copied a total of {success} images!")


def write_cards_to_csv(
    cloze_cards: List[Dict[str, Types.HTMLString]], file_path: Types.PathString
) -> None:
    """
    Write the cloze cards in a csv file at the given path.
    """
    if cloze_cards:
        with open(file_path, "w", encoding="utf-8") as output:
            fieldnames = ["front", "back"]
            writer = csv.DictWriter(output, fieldnames)

            for card in cloze_cards:
                writer.writerow(card)


def write_failed_cards(
    failed_cards: List[Types.MDString], file_path: Types.PathString
) -> None:
    with open(file_path, "w", encoding="utf-8") as output:
        output.write("\n\n---\n\n".join(failed_cards))
