"""Operation with yml.
"""
from enum import Enum
from pathlib import Path
from typing import Any

import yaml

from pykit.cls import Static
from pykit.validation import validate


class YMLLoader(Enum):
    """Yaml loaders types according to
    https://github.com/yaml/pyyaml/wiki/PyYAML-yaml.load(input)-Deprecation
    """
    BASE = yaml.SafeLoader
    SAFE = yaml.FullLoader
    FULL = yaml.BaseLoader
    UNSAFE = yaml.UnsafeLoader


class NotValidYMLError(Exception):
    """If loaded yml is not valid."""


class NotValidYMLFileSuffixError(Exception):
    pass


class YMLUtils(Static):
    @staticmethod
    def load_yml(
        p: Path, *, loader: YMLLoader = YMLLoader.SAFE,
    ) -> dict[str, Any]:
        """Loads yaml from file.

        Args:
            p:
                Path of yaml file to load from.
            loader (optional):
                Chosen loader for yaml. Defaults to safe loader.

        Returns:
            Loaded dictionary from yaml file.

        Raise:
            TypeError:
                Given path is not allowed pathlib.Path kind.
            NotValidFileSuffixError:
                Suffix should be either ".yml" or ".yaml".
            NotValidYmlError:
                Yaml file is not valid.
        """
        validate(p, Path)

        if p.suffix.lower() not in [".yaml", ".yml"]:
            raise NotValidYMLFileSuffixError(
                f"suffix {p.suffix} is not valid suffix",
            )

        with Path.open(p) as file:
            data = yaml.load(file, Loader=loader.value)  # noqa: S506
            if data is None:
                # Empty files should return empty dicts
                data = {}
            # Is it necessary? Does pyyaml allow loading not-valid yaml files?
            elif not isinstance(data, dict):
                raise NotValidYMLError(
                    "Yaml file should contain any map-like structure,"
                    " not plain types",
                )

        return data
