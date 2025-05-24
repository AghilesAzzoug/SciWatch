from pathlib import Path

from pytest import fixture


@fixture
def unit_test_scrapping_config_path():
    return Path(Path.cwd(), "tests", "resources", "unit_test_scrapping_config.toml").absolute()
