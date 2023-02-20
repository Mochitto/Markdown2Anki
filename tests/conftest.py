import pytest as pyt

import setup

@pyt.fixture(scope="session")
def template_dir(tmp_path_factory):
    template_dir = tmp_path_factory.mktemp("tmp")
    configs_dir = template_dir / "configs"
    configs_dir.mkdir()
    links_dir = template_dir / "links"
    links_dir.mkdir()

    

    
    return template_dir




