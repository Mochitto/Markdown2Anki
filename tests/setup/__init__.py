import os
from pathlib import Path

from type_config import TypeConfig
import markdown2anki.config.config_setup as config_setup
from markdown2anki.config.first_config import create_link_to_config_file
import markdown2anki.utils.common_types as Types

from .config_file_patch import config_patch, input_md_path, search_images_path


def create_configs(tmp_path: Path):
    """
    Create the following files:
    tmp_path/
    |-configs/
    |---good.config.ini
    |---broken.config.ini
    |---default.config.ini
    |-links/
    |---good_link.ini
    |---broken_config_link.ini
    """
    config = config_setup.setup_typeConfig(str(tmp_path / "output"))

    configs_dir = tmp_path / "configs"
    good_config = str(configs_dir / "good.config.ini")
    default_config = str(configs_dir / "default.config.ini")
    broken_config = str(configs_dir / "broken.config.ini")

    create_config(good_config, config, patch=config_patch)
    create_config(default_config, config)
    create_config(broken_config, config, break_config=True)

    links_dir = tmp_path / "links"
    good_link = str(links_dir / "good_link.ini")
    broken_config_link = str(links_dir / "broken_config_link.ini")

    create_link(good_link, good_config)
    create_link(broken_config_link, broken_config)

    bad_input = str(tmp_path / "output" / "bad_cards.md")

    create_bad_input(bad_input)
    pass


def create_config(
    path_to_config: Types.PathString, config: TypeConfig, break_config=False, patch={}
):
    """
    Create config at the given path.
    If break_config: cut half of the config content
    If patch: apply patch to the TypeConfig object
    """
    config_content = config.create_config(patch)
    if break_config:
        broken_content = config_content[: len(config_content) // 2]
        with open(path_to_config, "w") as config_file:
            config_file.write(broken_content)
    else:
        with open(path_to_config, "w") as config_file:
            config_file.write(config_content)


def create_link(path_to_link, path_to_config):
    """
    Create link file at the given path, pointing at path_to_config.
    """
    create_link_to_config_file(path_to_link, path_to_config)


def create_bad_input(path_to_output_folder: Types.PathString):
    with open(path_to_output_folder, "w") as bad_file_md:
        bad_file_md.write("hello world")


if __name__ == "__main__":
    """
    Creates the links and configs in "test_assets" folder,
    under "configs" and "links".
    "test_assets" is gitignored.
    """
    this_directory = Path(__file__).parent / "test_assets"
    os.makedirs(this_directory / "configs", exist_ok=True)
    os.makedirs(this_directory / "links", exist_ok=True)
    create_configs(this_directory)
