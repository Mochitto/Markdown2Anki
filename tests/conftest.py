import pytest as pyt
from typing import Callable


@pyt.fixture(scope="function")  # This can be function, session, module, class, package
def template_dir(tmp_path_factory):
    template_dir = tmp_path_factory.mktemp("tmp")
    configs_dir = template_dir / "configs"
    configs_dir.mkdir()
    links_dir = template_dir / "links"
    links_dir.mkdir()
    output_dir = template_dir / "output"
    output_dir.mkdir()

    return template_dir


@pyt.fixture
def tmp_configs(template_dir):
    return template_dir / ""


@pyt.fixture(scope="function")
def temp_md_file(tmp_path) -> Callable:
    """
    Return a function that can create a temporary markdown file with the provided
    content.
    """

    def _create_md_file(content: str) -> str:
        md_file = tmp_path / "temp_file.md"
        md_file.write_text(content)
        return str(md_file)

    return _create_md_file
