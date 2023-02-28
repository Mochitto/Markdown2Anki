import pytest as pyt


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
