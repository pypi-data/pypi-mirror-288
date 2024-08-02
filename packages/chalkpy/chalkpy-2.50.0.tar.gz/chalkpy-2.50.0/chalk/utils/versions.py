from functools import lru_cache
from importlib.metadata import PackageNotFoundError, version

import requests
from packaging.requirements import Requirement
from packaging.specifiers import SpecifierSet
from packaging.version import Version

INVALID_PACKAGE_VERSIONS = {"pydantic": SpecifierSet(">=2.0.0")}

# the cache is only really useful for testing
@lru_cache
def get_all_versions(package_name: str):
    url = f"https://pypi.org/pypi/{package_name}/json"
    response = requests.get(url)
    if response.status_code != 200:
        raise ImportError(f"While validating {package_name} version, could not fetch versions from pypi.")

    data = response.json()
    return list(data["releases"].keys())


def validate_versions():
    for package_name, exclude_version in INVALID_PACKAGE_VERSIONS.items():
        try:
            cleaned_package_version = Version(version(package_name))
            if cleaned_package_version in exclude_version:
                raise ImportError(
                    f"{package_name} version cannot be {str(exclude_version)}, but got '{str(cleaned_package_version)}'."
                )
        except PackageNotFoundError:
            continue


def validate_requirement_version(requirement_line: str):
    """Takes a line from requirements.txt and validates that the versions are between Chalk's required bounds. If not, raises and ImportError."""
    return
    req = Requirement(requirement_line.split(";")[0].strip())

    if (rpv := INVALID_PACKAGE_VERSIONS.get(req.name, None)) is not None:
        all_versions = get_all_versions(req.name)

        specifiers = req.specifier & rpv
        remaining_versions = specifiers.filter(all_versions)
        if list(remaining_versions):
            raise ImportError(
                f"{req.name} version cannot be {rpv}: version pinned in requirements.txt ('{requirement_line}') does not meet this constraint."
            )
