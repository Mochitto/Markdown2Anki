from pathlib import Path

import pytest

from markdown2anki.md_2_anki.process_images import find_image_path

import tests

# Folders to exclude is taken from the patch to reduce errors during maintainance
from tests.setup.config_file_patch import folders_to_exclude


class TestFindImagePath:
    @pytest.fixture
    def assets_images_path(self):
        assets_images_path = Path(tests.__file__).parent / "assets" / "images"
        return assets_images_path

    @pytest.fixture
    def good_images(self, assets_images_path):
        images_file_names = {
            "oiter.jpg": assets_images_path / Path("MORE", "oiter.jpg"),
            "Toing.jpg": assets_images_path / Path("MORE", "Toing.jpg"),
            "vruM.jpg": assets_images_path / Path("MORE", "vruM.jpg"),
            "WAAAA.jpeg": assets_images_path / Path("WAAAA.jpeg"),
            "2010.jpg": assets_images_path / Path("2010.jpg"),
            "i_am_a_forest_fire.jpeg": assets_images_path
            / Path("MORE", "YES_ME", "i_am_a_forest_fire.jpeg"),
            "FroW.jpeg": assets_images_path / Path("MORE", "YES_ME", "FroW.jpeg"),
        }
        return images_file_names

    @pytest.fixture
    def nooti_images(self, assets_images_path):
        images_file_names = {
            "mmmm.jpg": assets_images_path
            / Path("MORE", "exclude_me_too", "mmmm.jpeg"),
            "fkboi.jpeg": assets_images_path / Path("exclude_me", "fkboi.jpeg"),
        }
        return images_file_names

    def test_images_finding(self, assets_images_path, good_images, nooti_images):
        for good_image in list(good_images.keys()):
            good_image_path = find_image_path(good_image, assets_images_path)
            assert good_image_path == str(good_images[good_image])

        for nooti_image in list(nooti_images.keys()):
            nooti_image_path = find_image_path(
                nooti_image, assets_images_path, folders_to_exclude
            )
            assert nooti_image_path == None
