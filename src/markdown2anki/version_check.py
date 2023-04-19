from importlib.metadata import version
import requests

def check_for_version(current_version: str, latest_version: str) -> bool:
    return current_version == latest_version if latest_version else True

def get_current_version(package_name: str) -> str:
    return version(package_name)

def get_latest_version(package_name:str) -> str:
    latest_version = ""
    try:
        response = requests.get(f"https://pypi.org/pypi/{package_name}/json", timeout=2)
        response.raise_for_status()
        package_data = response.json()
        latest_version = package_data['info']['version']
    except requests.exceptions.RequestException:
        pass
    return latest_version


if __name__ == "__main__":
    import type_config
    current = get_current_version(type_config.__name__)
    latest = get_latest_version(type_config.__name__)
    print(check_for_version(current, latest))
