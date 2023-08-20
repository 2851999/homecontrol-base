import json
from pathlib import Path
from typing import Generic, Optional, Type, TypeVar
from pydantic import RootModel

from pydantic.dataclasses import dataclass

from homecontrol_base.config.exceptions import ConfigFileNotFound

TDataclass = TypeVar("TDataclass", bound=dataclass)


class BaseConfig(Generic[TDataclass]):
    _dataclass_type: Type[TDataclass]
    _local_file_path: Path
    _loaded_file_path: Path
    _data: TDataclass

    def __init__(self, local_file_path: str, dataclass_type: TDataclass) -> None:
        """Initialises and loads a config file into memory

        Arguments
            local_file_path (str): Path of the file to look for (either in
                            current directory or the default config directory)
        """
        self._dataclass_type = dataclass_type
        self._local_file_path = Path(local_file_path)

        self.load()

    def load(self):
        """Loads config from a file (Can be used to reload)"""
        file_path = self.get_file_path()
        if file_path is None:
            raise ConfigFileNotFound(
                "Config file not found. Please ensure it is accessible at one "
                "of the following locations:\n"
                + "\n".join([str(path) for path in self._get_search_paths()])
            )

        self._loaded_file_path = file_path

        with open(file_path, "r", encoding="utf-8") as config_file:
            data = json.load(config_file)

        self._data = self._dataclass_type(**data)

    def save(self):
        """Saves config to a file (Will save to the same file config was
        loaded from)"""

        with open(self._loaded_file_path, "w", encoding="utf-8") as config_file:
            config_file.write(RootModel(self._data).model_dump_json(indent=4))

    def _get_search_paths(self) -> list[Path]:
        """Returns a list of paths to search for config (in order they would
        be used)

        First attempts to look in the current directory, then if it doesn't
        exist looks in /etc/homecontrol on Linux, or the home directory on
        Windows/Mac
        """
        return [
            # Local
            Path.cwd() / self._local_file_path,
            # Linux
            Path("/etc/homecontrol") / self._local_file_path,
            # Windows
            Path.home() / self._local_file_path,
        ]

    def get_file_path(self) -> Optional[Path]:
        """Returns the full filepath of this config file having searched
        in the order given by _get_search_paths
        """
        search_paths = self._get_search_paths()
        for search_path in search_paths:
            if search_path.exists():
                return search_path
        return None
