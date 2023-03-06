from pathlib import Path

import pytest

from markdown2anki.md_2_anki.process_images import get_images_to_copy

import tests

# Folders to exclude is taken from the patch to reduce errors during maintainance
from tests.setup.config_file_patch import folders_to_exclude


class TestGetImagesToCopy:
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
    def nooti_images(self):
        images_file_names = {
            "mmmm.jpg": None,
            "fkboi.jpeg": None,
        }
        return images_file_names

    def test_images_finding(self, assets_images_path, good_images, nooti_images):
        card1 = {"front": "", "back": ""}

        all_images_list = list(good_images.keys()) + list(nooti_images.keys())
        half_of_images_len = len(all_images_list) // 2

        for image in all_images_list[:half_of_images_len]:
            card1["front"] += f'<img src="{image}">'

        for image in all_images_list[half_of_images_len:]:
            card1["back"] += f'<img src="{image}">'

        all_images_dict = good_images | nooti_images
        found_images = get_images_to_copy(card1, assets_images_path, folders_to_exclude)
        for image in list(found_images.keys()):
            assert found_images[image] == (
                str(all_images_dict[image]) if all_images_dict[image] else None
            )
