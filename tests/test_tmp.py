import os
import io
import sys
from pathlib import Path

import pytest
from markdown2anki.config.first_config import create_link_to_config_file, welcome_user
from markdown2anki.config.configs_handle import get_configfile_paths
import markdown2anki.utils.common_types as Types

from setup import create_configs

THIS_DIR = Path(__file__).parent

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

class TestWelcomeUser:

    @pytest.fixture(autouse=True)
    def setup_class(self, template_dir):
        self.links_directory = template_dir / "links"
        self.config_directory = template_dir / "configs"

    @pytest.fixture
    def use_input_file(self, request):
        """
        Monkeypatch sys.stdin so that input returns the
        values given from the request parameter function and
        more than one value can be used.
        """
        # the request keyword is needed to use pytest mark parametrize
        original_stdin = sys.stdin
        # This way I can use the class' functions by passing self to them
        sys.stdin = io.StringIO(request.param(self))
        # Before yield is the setup
        yield # This signals the point in which functions are run
        # What comes after yield is the teardown
        sys.stdin.close()
        sys.stdin = original_stdin

    def good_file(self):
        return (
            str(self.config_directory) +
            "\nY"
            ) 

    def one_error(self):
        return (
            "not a path\n" +
            str(self.config_directory) +
            "\nY"
            )

    def exit1(self):
        return (
            "exIT"
            ) 

    def exit2(self):
        return (
            str(self.config_directory) +
            "\neXIt"
            ) 

    # I don't totally understand parametrize
    @pytest.mark.parametrize("use_input_file", [good_file], indirect=True)
    def test_welcome_user_good(self, use_input_file):
        welcome_user("config.ini", os.path.join(self.links_directory, "link.ini"), welcome_message=False)
        assert os.path.exists(str(self.config_directory / "config.ini"))

    @pytest.mark.parametrize("use_input_file", [one_error], indirect=True)
    def test_welcome_user_one_error(self, use_input_file):
        welcome_user("config.ini", os.path.join(self.links_directory, "link.ini"), welcome_message=False)
        assert os.path.exists(str(self.config_directory / "config.ini"))
        
    @pytest.mark.parametrize("use_input_file", [exit1], indirect=True)
    def test_welcome_user_exit1(self, use_input_file):
        with pytest.raises(SystemExit):
            welcome_user("config.ini", os.path.join(self.links_directory, "link.ini"), welcome_message=False)
        assert not os.path.exists(str(self.config_directory / "config.ini"))

    @pytest.mark.parametrize("use_input_file", [exit2], indirect=True)
    def test_welcome_user_exit2(self, use_input_file):
        with pytest.raises(SystemExit):
            welcome_user("config.ini", os.path.join(self.links_directory, "link.ini"), welcome_message=False)
        assert not os.path.exists(str(self.config_directory / "config.ini"))
