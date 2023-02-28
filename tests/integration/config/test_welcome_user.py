import sys
import io
import os

import pytest

from markdown2anki.config.first_config import welcome_user


class TestWelcomeUser:
    @pytest.fixture
    def tmp_dirs(self, template_dir):
        return {"link": template_dir / "links", "config": template_dir / "configs"}

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

    def one_error(self, tmp_dirs):
        return "not a path\n" + str(tmp_dirs["config"]) + "\nY"

    def exit1(self, tmp_dirs):
        return "exIT"

    def exit2(self, tmp_dirs):
        return str(tmp_dirs["config"]) + "\neXIt"

    # I don't totally understand parametrize; use_input_file is not accessed
    # directly, but called before and after the given function
    @pytest.mark.parametrize("use_input_file", [good_file], indirect=True)
    def test_welcome_user_good(self, use_input_file, tmp_dirs):
        welcome_user(
            "config.ini",
            os.path.join(tmp_dirs["link"], "link.ini"),
            welcome_message=False,
        )
        assert os.path.exists(str(tmp_dirs["config"] / "config.ini"))

    @pytest.mark.parametrize("use_input_file", [one_error], indirect=True)
    def test_welcome_user_one_error(self, use_input_file, tmp_dirs):
        welcome_user(
            "config.ini",
            os.path.join(tmp_dirs["link"], "link.ini"),
            welcome_message=False,
        )
        assert os.path.exists(str(tmp_dirs["config"] / "config.ini"))

    @pytest.mark.parametrize("use_input_file", [exit1], indirect=True)
    def test_welcome_user_exit1(self, use_input_file, tmp_dirs):
        with pytest.raises(SystemExit):
            welcome_user(
                "config.ini",
                os.path.join(tmp_dirs["link"], "link.ini"),
                welcome_message=False,
            )
        assert not os.path.exists(str(tmp_dirs["config"] / "config.ini"))

    @pytest.mark.parametrize("use_input_file", [exit2], indirect=True)
    def test_welcome_user_exit2(self, use_input_file, tmp_dirs):
        with pytest.raises(SystemExit):
            welcome_user(
                "config.ini",
                os.path.join(tmp_dirs["link"], "link.ini"),
                welcome_message=False,
            )
        assert not os.path.exists(str(tmp_dirs["config"] / "config.ini"))
