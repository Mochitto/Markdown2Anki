import os

import pytest
from markdown2anki.config.first_config import create_link_to_config_file


class TestConfigHandling:
    @pytest.fixture
    def tmp_paths(self, template_dir):
        return {
            "link": template_dir / "links" / "link.ini",
            "config": template_dir / "configs" / "good.config.ini",
        }

    def test_create_link_to_config_file(self, tmp_paths):
        """
        Test correct writing of link file.
        """
        config_directory, config_file = os.path.split(tmp_paths["config"])

        create_link_to_config_file(
            path_to_link=tmp_paths["link"],
            path_to_config_file=tmp_paths["config"],
        )

        with open(tmp_paths["link"], "r") as link_file:
            link_file_content = link_file.read()

        expected_output = (
            "[LINKS]\n"
            f"config_dir = {config_directory}\n"
            f"config_file = {config_file}"
        )
        assert link_file_content == expected_output
