import os

import pytest
from markdown2anki.config.first_config import create_link_to_config_file
from markdown2anki.config.configs_handle import get_configfile_paths

from setup import create_configs

class TestConfigHandling:
    
    @pytest.fixture(autouse=True)
    def setup_class(self, template_dir):
        self.path_to_link = template_dir / "links" / "link.ini"
        self.path_to_config = template_dir / 'configs' / "good.config.ini" 

    def test_create_link_to_config_file(self):
        """
        Test correct writing of link file.
        """
        config_directory, config_file = os.path.split(self.path_to_config) 

        create_link_to_config_file(
            path_to_link=self.path_to_link,
            path_to_config_file=self.path_to_config,
        )

        with open(self.path_to_link, "r") as link_file:
            link_file_content = link_file.read()

        expected_output = (
            "[LINKS]\n"
            f"config_dir = {config_directory}\n"
            f"config_file = {config_file}"
        )
        assert link_file_content == expected_output

    def test_get_configfile_paths(self):
        """
        Test correct retrival of the config file from link file.
        """
        config_directory, config_file = os.path.split(self.path_to_config) 

        create_configs(config_directory)

        create_link_to_config_file(
            path_to_link=self.path_to_link,
            path_to_config_file=self.path_to_config,
        )
        result_config_dir, result_config_file = get_configfile_paths(self.path_to_link)
        assert result_config_dir == config_directory and result_config_file == config_file

    def tests_get_configfile_paths_broken_link(self):
        """
        Test raising FileNotFound when config file is not present at
        the path written in the link file.
        """
        create_link_to_config_file(
            path_to_link=self.path_to_link,
            path_to_config_file=self.path_to_config,
        )

        with pytest.raises(FileNotFoundError):
            get_configfile_paths(self.path_to_link)
