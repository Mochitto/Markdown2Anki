import os

import pytest
from markdown2anki.config.first_config import create_link_to_config_file
from markdown2anki.config.configs_handle import get_configfile_paths

from tests.setup import create_configs


class TestConfigHandling:
    @pytest.fixture
    def tmp_paths(self, template_dir):
        return {
            "link": template_dir / "links" / "good_link.ini",
            "config": template_dir / "configs" / "good.config.ini",
        }

    def test_get_configfile_paths(self, tmp_paths, template_dir):
        """
        Test correct retrival of the config file from link file.
        """
        create_configs(template_dir)

        config_directory, config_file = os.path.split(tmp_paths["config"])

        result_config_dir, result_config_file = get_configfile_paths(tmp_paths["link"])
        assert (
            result_config_dir == config_directory and result_config_file == config_file
        )

    def tests_get_configfile_paths_broken_link(self, tmp_paths):
        """
        Test raising FileNotFound when config file is not present at
        the path written in the link file.
        """
        create_link_to_config_file(
            path_to_link=tmp_paths["link"],
            path_to_config_file=tmp_paths["config"],
        )

        with pytest.raises(FileNotFoundError):
            get_configfile_paths(tmp_paths["link"])
