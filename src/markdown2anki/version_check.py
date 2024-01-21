from importlib.metadata import version
import logging

import requests

logger = logging.getLogger(__name__)


def check_for_version(current_version: str, latest_version: str) -> bool:
    return current_version == latest_version if latest_version else True


def get_current_version(package_name: str) -> str:
    return version(package_name)


def get_latest_version(package_name: str) -> str:
    latest_version = ""
    try:
        response = requests.get(f"https://pypi.org/pypi/{package_name}/json", timeout=2)
        response.raise_for_status()
        package_data = response.json()
        latest_version = package_data["info"]["version"]
    except requests.exceptions.RequestException:
        pass
    return latest_version


def check_for_updates(package_name: str, changelog_url: str):
    current_version = get_current_version(package_name)
    logger.info(f"Running {package_name} v{current_version} 🌸\n")

    logger.info(f"Checking for updates...")
    latest_version = get_latest_version(package_name)
    if not (check_for_version(current_version, latest_version)):
        logger.info(
            f"⏫ There is a new version available: v{latest_version}!\n"
            f"You can read what's new here: {changelog_url}\n\n"
        )
    else:
        logger.info("✨ Running the latest version!\n")


if __name__ == "__main__":
    import type_config

    logging.basicConfig(level=logging.INFO)
    check_for_updates(
        type_config.__name__,
        "https://github.com/Mochitto/type-config/blob/master/CHANGELOG.md",
    )
