import os
import sys
import io
import filecmp
from pathlib import Path

import pytest

from markdown2anki.config.configs_handle import handle_configs
from markdown2anki.config.first_config import create_link_to_config_file

from tests.setup import create_configs
import tests


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

    @pytest.fixture
    def change_sys_argv(self, request):
        """
        Change sys argv to what is given.
        """
        original_sys_argvs = sys.argv
        sys.argv = request.param
        yield
        sys.argv = original_sys_argvs

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

        expected_fixed_link = (
            "[LINKS]\n" + f"config_dir = {tmp_dirs['config']}\n"
            "config_file = config.ini"
        )

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
        create_link_to_config_file(
            str(tmp_dirs["link file"]), str(tmp_dirs["config file"])
        )

        # Main call: input calls are taken care of by "use_input_file"
        with pytest.raises(SystemExit):
            handle_configs(str(tmp_dirs["link file"]), "config.ini")

        # Checking if handle configs called welcome_user and created the config
        assert os.path.exists(str(tmp_dirs["config file"]))

        with open(tmp_dirs["link file"], "r") as link_file:
            link_file_content = link_file.read()

        expected_fixed_link = (
            "[LINKS]\n" + f"config_dir = {tmp_dirs['config']}\n"
            "config_file = config.ini"
        )

        assert link_file_content == expected_fixed_link

    @pytest.mark.parametrize(
        "use_input_file,change_sys_argv",
        [(good_file, ["md2anki", "-lc"])],
        indirect=True,
    )
    def test_handle_configs_link_config(
        self, use_input_file, tmp_dirs, template_dir, change_sys_argv
    ):
        """
        Test the configs handle when using "-lc".

        It should:
            - Run "welcome user":
                Since the config already exists, it should get healed!
            - Exit
        """
        create_configs(template_dir)

        with pytest.raises(SystemExit):
            handle_configs(
                str(tmp_dirs["link"] / "broken_config_link.ini"), "broken.config.ini"
            )

        assert filecmp.cmp(
            str(tmp_dirs["config"] / "broken.config.ini"),
            str(tmp_dirs["config"] / "default.config.ini"),
        )

    @pytest.mark.parametrize(
        "use_input_file,change_sys_argv",
        [(good_file, ["md2anki", "-hc"])],
        indirect=True,
    )
    def test_handle_configs_heal_config(
        self, use_input_file, tmp_dirs, template_dir, change_sys_argv
    ):
        """
        Test the configs handle when using "-hc".

        It should:
            - Heal the given config
            - Exit
        """
        create_configs(template_dir)

        with pytest.raises(SystemExit):
            handle_configs(
                str(tmp_dirs["link"] / "broken_config_link.ini"), "broken.config.ini"
            )

        assert filecmp.cmp(
            str(tmp_dirs["config"] / "broken.config.ini"),
            str(tmp_dirs["config"] / "default.config.ini"),
        )

    @pytest.mark.parametrize("change_sys_argv", [["md2anki"]], indirect=True)
    def test_handle_configs_error(self, tmp_dirs, template_dir, change_sys_argv):
        """
        Test that configs handle exits with
        a code 1 when there are problems with
        the config file.
        """
        create_configs(template_dir)

        with pytest.raises(SystemExit) as pytest_wrapped_exit:
            handle_configs(
                str(tmp_dirs["link"] / "broken_config_link.ini"), "broken.config.ini"
            )
        assert pytest_wrapped_exit.value.code == 1

    @pytest.mark.parametrize(
        "change_sys_argv", [["md2anki", "-ln", "false"]], indirect=True
    )
    def test_handle_configs_good_path(self, tmp_dirs, template_dir, change_sys_argv):
        """
        Test that configs handle works correctly.

        Notice: it's also testing CLI - config file merging
        since there is the "-ln false" flag.
        """
        create_configs(template_dir)
        good_configs = handle_configs(
            str(tmp_dirs["link"] / "good_link.ini"), "good.config.ini"
        )

        # Notice: this can fail also when the
        # tests/setup/config_file_patch changes. (or when new options are added)
        # TODO: There could be a way to use the patch
        # To reduce errors and maintainance
        # Optimally, I'd want only one file to handle all of this (the patch file)
        # Would be nice to have a function that fills in the options dependant on
        # the tmp folder and return the config that I should get from this function.

        # tests refers to the tests folder. This is done
        # to avoid using relative paths starting from this file.
        expected_config = {
            "Obsidian valut name": "Obsidian vault",
            "line numbers?": False,
            "search images folder": str(
                Path(tests.__file__).parent / "assets" / "images"
            ),
            "folders to exclude": ["exclude_me", "exclude_me_too"],
            "Number of backups": 10,
            "clear file?": False,
            "images out-folder": f'{template_dir / "output" / "images"}',
            "bad cards file path": f'{template_dir / "output" / "bad_cards.md"}',
            "fast forward?": True,
            "input md file path": str(
                Path(tests.__file__).parent / "assets" / "input.md"
            ),
            "config directory": f'{tmp_dirs["config"]}',
        }
        assert good_configs == expected_config

    @pytest.mark.parametrize("change_sys_argv", [["md2anki", "-bf"]], indirect=True)
    def test_handle_configs_bad_file_as_input(
        self, tmp_dirs, template_dir, change_sys_argv
    ):
        """
        Test that configs handle uses bad cards as input
        when the "-bf" flag is used.
        """
        create_configs(template_dir)
        good_configs = handle_configs(
            str(tmp_dirs["link"] / "good_link.ini"), "good.config.ini"
        )

        assert good_configs["bad cards file path"] == good_configs["input md file path"]
