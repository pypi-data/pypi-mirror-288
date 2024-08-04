"""
Generate an __about__.py file from package metadata using importlib.metadata.
"""

import importlib.metadata as md
from typing import Any, cast

from metametameta.filesystem import write_to_file
from metametameta.general import any_metadict, merge_sections


def get_package_metadata(package_name: str) -> dict[str, Any]:
    """Get package metadata using importlib.metadata."""
    try:
        pkg_metadata: md.PackageMetadata = md.metadata(package_name)
        return {key: value for key, value in cast(dict, pkg_metadata).items()}
    except md.PackageNotFoundError:
        print(f"Package '{package_name}' not found.")
        return {}


def generate_from_importlib(name: str, source: str = "", output: str = "__about__.py") -> str:
    """Write package metadata to an __about__.py file."""
    pkg_metadata = get_package_metadata(name)
    if pkg_metadata:
        dir_path = "./"

        about_content, names = any_metadict(pkg_metadata)

        about_content = merge_sections(names, name, about_content)
        return write_to_file(dir_path, about_content, output)
    else:
        return "No [project] section found in pyproject.toml."


if __name__ == "__main__":
    generate_from_importlib("toml")
