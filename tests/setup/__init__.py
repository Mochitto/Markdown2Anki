import os
from typing import Dict

from type_config import TypeConfig
import markdown2anki.config.config_setup as config_setup
from markdown2anki.config.first_config import create_link_to_config_file
import markdown2anki.utils.common_types as Types

from .config_file_patch import config_patch, input_md_path, search_images_path

def create_configs(tmp_path: Types.PathString):
    config = config_setup.setup_typeConfig(tmp_path)

    create_good_config(config_patch, config, tmp_path)
    create_broken_config(config, tmp_path)
    create_default_config(config, tmp_path)

    # TODO: complete links setup, might want to make "create config" and use the names as params
    # create_link(tmp_path / "links" / "good")
    pass


def create_good_config(
    patch: Dict[str, str], config: TypeConfig, target_dir: Types.PathString
):
    config_content = config.create_config(patch)
    with open(os.path.join(target_dir, "good.config.ini"), "w") as config_file:
        config_file.write(config_content)
    pass


def create_broken_config(config: TypeConfig, target_dir: Types.PathString):
    config_content = config.create_config()
    broken_content = config_content[: len(config_content) // 2]
    with open(os.path.join(target_dir, "broken.config.ini"), "w") as config_file:
        config_file.write(broken_content)
    pass


def create_default_config(config: TypeConfig, target_dir: Types.PathString):
    config_content = config.create_config()
    with open(os.path.join(target_dir, "default.config.ini"), "w") as config_file:
        config_file.write(config_content)
    pass

def create_link(path_to_link, path_to_config):
    create_link_to_config_file(path_to_link, path_to_config)

if __name__ == "__main__":
    create_configs(".")
