import os
import sys
import io

import pytest

from markdown2anki.config.configs_handle import handle_configs
from markdown2anki.config.first_config import create_link_to_config_file

class TestHandleConfigs:

    @pytest.fixture
    def tmp_dirs(self, template_dir):
        return {
            "link": template_dir / "links",
            "config": template_dir / "configs",
            "link file": template_dir / "links" / "link.ini",
            "config file": template_dir / "configs" / "config.ini",
        }

    @pytest.fixture
    def use_input_file(self, request, tmp_dirs):
        """
        Monkeypatch sys.stdin so that input returns the
        values given from the request parameter function and
        more than one value can be used.
        """
        # the request keyword is needed to use pytest mark parametrize
        original_stdin = sys.stdin
        # The functions are called indirectly
        # This way I can use the class' functions by passing self to them
        sys.stdin = io.StringIO(request.param(self, tmp_dirs))
        # Before yield is the setup
        yield  # This signals the point in which functions are run
        # What comes after yield is the teardown
        sys.stdin.close()
        sys.stdin = original_stdin

    def good_file(self, tmp_dirs):
        return str(tmp_dirs["config"]) + "\nY"

    @pytest.mark.parametrize("use_input_file", [good_file], indirect=True)
    def test_handle_configs_first_time(self, use_input_file, tmp_dirs):
        """
        Test the configs handle when there is no link file 
        (probably you run the program for the first time).

        It should:
            - Run "welcome_user" and create/fix the link file
            - Create the default config file at the given dir
            - Exit
        """
        # Main call: input calls are taken care of by "use_input_file"
        with pytest.raises(SystemExit):
            handle_configs(str(tmp_dirs["link file"]), "config.ini")

        # Checking if handle configs called welcome_user and created the config
        assert os.path.exists(str(tmp_dirs["config file"]))

        with open(tmp_dirs["link file"], "r") as link_file:
            link_file_content = link_file.read()

        expected_fixed_link = ("[LINKS]\n" +
            f"config_dir = {tmp_dirs['config']}\n"
            "config_file = config.ini")

        assert link_file_content == expected_fixed_link

    @pytest.mark.parametrize("use_input_file", [good_file], indirect=True)
    def test_handle_configs_broken_link(self, use_input_file, tmp_dirs):
        """
        Test the configs handle when there is a broken link file.
        Basically the same as testing first time, but
        the FileNotFound error is risen by the broken link.

        It should:
            - Run "welcome_user" and fix the link file (overwriting)
            - Create the default config.ini file at the given dir
            - Exit
        """
        # The config file shouldn't exist, the link should be broken
        create_link_to_config_file(str(tmp_dirs["link file"]), str(tmp_dirs["config file"]))

        # Main call: input calls are taken care of by "use_input_file"
        with pytest.raises(SystemExit):
            handle_configs(str(tmp_dirs["link file"]), "config.ini")

        # Checking if handle configs called welcome_user and created the config
        assert os.path.exists(str(tmp_dirs["config file"]))

        with open(tmp_dirs["link file"], "r") as link_file:
            link_file_content = link_file.read()

        expected_fixed_link = ("[LINKS]\n" +
            f"config_dir = {tmp_dirs['config']}\n"
            "config_file = config.ini")

        assert link_file_content == expected_fixed_link

