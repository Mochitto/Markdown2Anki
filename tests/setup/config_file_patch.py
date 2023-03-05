"""
This module exposes a patch to apply to the config
file, to create a "good" config file (valid) for testing.

It also points to an assets folder in the parent directory of
this file's directory.
"""
import os
from pathlib import Path

import tests

this_directory, _ = os.path.split(__file__)

assets_directory = Path(tests.__file__).parent / "assets"
search_images_path = str(assets_directory / "images")
input_md_path = str(assets_directory / "input.md")

if not os.path.exists(search_images_path) or not os.path.exists(input_md_path):
    """
    The structure of the assets folder should be the following:
        assets/
            images/
                nested/
                    <test_images>
                <test images>
                exclude_me/
                    <test_images>
            input.md
    And be in the tests/ folder, with the setup folder as sibling.
    """
    raise FileNotFoundError("Tests assets are missing. See this file for more.")

folders_to_exclude = ["exclude_me", "exclude_me_too"]

config_patch = {
    "Obsidian valut name": "Obsidian vault",
    "search images folder": search_images_path,
    "input md file path": input_md_path,
    "folders to exclude": ", ".join(folders_to_exclude),
}
