import pytest

from markdown2anki.config.config_setup import setup_typeConfig


class TestTypeConfig:
    """
    The objective of this test is to
    keep track of changes in options and types of
    the main config file (built with typeconfig).
    """

    @pytest.fixture
    def tmp_dirs(self, template_dir):
        return {"link": template_dir / "links", "config": template_dir / "configs"}

    def test_options_and_types(self, tmp_dirs):
        config = setup_typeConfig(tmp_dirs["config"])

        config_options = [
            "Obsidian valut name",
            "search images folder",
            "images out-folder",
            "bad cards file path",
            "input md file path",
            "Number of backups",
            "clear file?",
            "line numbers?",
            "fast forward?",
            "folders to exclude",
        ]
        actual_options = config.get_options().keys()
        lacking_options = set(actual_options) - set(config_options)
        extra_options = set(config_options) - set(actual_options)
        options_message = (
            f"Config lacks option/s {lacking_options} " if lacking_options else ""
        )
        options_message += (
            f"Config has extra option/s {extra_options}" if extra_options else ""
        )
        assert not options_message

    def test_types(self, tmp_dirs):
        config = setup_typeConfig(tmp_dirs["config"])

        config_types = [
            "ExistingPath",
            "AbsolutePath",
            "NewFolder",
            "FoldersList",
            "bool",
            "str",
            "int",
        ]
        actual_types = config.get_types().keys()
        extra_types = set(config_types) - set(actual_types)
        lacking_types = set(actual_types) - set(config_types)
        types_message = f"Config lacks type/s {lacking_types} " if lacking_types else ""
        types_message += f"Config has extra type/s {extra_types}" if extra_types else ""
        assert not types_message
