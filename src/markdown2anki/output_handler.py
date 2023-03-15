import csv
import logging
import os
import shutil
from typing import Dict, List
from datetime import datetime

from markdown2anki.utils import common_types as Types
import markdown2anki.md_2_anki.utils.card_types as CardTypes
from markdown2anki.utils.debug_tools import expressive_debug

logger = logging.getLogger(__name__)


# FIXME: Could use some better error handling maybe
def copy_images_to_folder(
    images_to_copy: Dict[str, Types.PathString | None], outdir_folder: Types.PathString
) -> None:
    """
    Copy the images to the outdir folder and return (number of copied images, list of errors, if there was any).
    Raise CardError if the image to copy doesn't exist.

    Dict:
    "image.extension" : "path/to/image.extension"
    """
    logger.info("📷 Copying the images...")
    success = 0
    for image, path_to_image in images_to_copy.items():
        if not path_to_image:
            logger.warning(f'|--- ❌ Couldn\'t copy "{image}" (File not found)')
            continue

        destination_path = os.path.join(outdir_folder, image)

        if os.path.exists(destination_path):
            logger.warning(f'|--- ⏩ Skipping "{image}": it\'s already in the folder')
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
                f"|--- ❌ Failed to copy an image: '{image}' ({error.__class__.__name__})."
            )
            continue

    if success:
        logger.info(f"|--- ✅ Copied a total of {success} images!")


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


def backup_file(file_path: Types.PathString, output_folder: Types.PathString) -> None:
    """
    Create a copy of the file at file_path iin the output_folder
    with a new file name that "{now.isoformat}.md".
    """
    # It's good to make sure that the folder exists every time, in case
    # It gets deleted
    if not os.path.exists(output_folder):
        os.makedirs(output_folder, exist_ok=True)

    file_name = f"{datetime.now().isoformat()}.md"

    with open(file_path, "r") as file_to_backup:
        file_content = file_to_backup.read()

    with open(os.path.join(output_folder, file_name), "w") as backup_file:
        backup_file.write(file_content)

    logger.debug(f"✅ Backup file created correctly with the name {file_name}!")


def clear_backups(backups_folder: Types.PathString, limit_of_files: int) -> None:
    """
    Remove the oldest files from the given backup_folder if
    their number is higher than the limit of files number.
    """
    folder_content = os.scandir(backups_folder)

    files_ordered_by_creation = sorted(
        folder_content, key=lambda file: os.path.getmtime(file), reverse=True
    )

    if len(files_ordered_by_creation) > limit_of_files:
        files_to_delete = files_ordered_by_creation[limit_of_files:]

        total = 0
        for file in files_to_delete:
            os.remove(file.path)
            total += 1

        logging.debug(f"🚮 Cleaned up {total} backup files.")


def clear_file(file_to_clear: Types.PathString) -> None:
    """
    Clears (makes blank) the content of the given file.
    """
    with open(file_to_clear, "w"):
        pass

    logging.info(f"🧹 Cleared the input file!")
