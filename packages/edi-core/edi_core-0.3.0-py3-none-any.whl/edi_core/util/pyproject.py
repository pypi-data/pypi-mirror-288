from typing import Dict, Any

from edi_core.parser.toml_parser import parse_toml_file


class PyProject:
    _root: str
    _config: Dict[str, Any]
    _config_file_name = "pyproject.toml"

    def __init__(self, path: str):
        self.path = path
        self._config = parse_toml_file(f'{path}/{self._config_file_name}')
