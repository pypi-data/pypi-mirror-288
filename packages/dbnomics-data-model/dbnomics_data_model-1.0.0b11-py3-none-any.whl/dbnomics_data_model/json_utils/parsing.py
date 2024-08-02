from abc import ABC, abstractmethod
from pathlib import Path
from typing import TypeGuard, cast

import cysimdjson
from jsonalias import Json

from dbnomics_data_model.json_utils.types import JsonObject

from .errors import (
    JsonBytesParseError,
    JsonFileParseError,
    JsonStringParseError,
)

__all__ = ["CysimdJsonParser", "JsonParser"]


class JsonParser(ABC):
    @classmethod
    def create(cls) -> "JsonParser":
        return CysimdJsonParser()

    @abstractmethod
    def is_object(self, data: Json) -> TypeGuard[JsonObject]: ...

    @abstractmethod
    def parse_bytes(self, value: bytes) -> Json: ...

    @abstractmethod
    def parse_file(self, file: Path) -> Json: ...

    @abstractmethod
    def parse_string(self, value: str) -> Json: ...


class CysimdJsonParser(JsonParser):
    def __init__(self) -> None:
        self._parser = cysimdjson.JSONParser()

    def is_object(self, data: Json) -> TypeGuard[JsonObject]:
        return isinstance(data, cysimdjson.JSONObject)

    def parse_bytes(self, value: bytes) -> Json:
        try:
            return cast(Json, self._parser.parse(value))
        except ValueError as exc:
            raise JsonBytesParseError(value=value) from exc

    def parse_file(self, file: Path) -> Json:
        try:
            return cast(Json, self._parser.load(str(file)))
        except OSError as exc:
            # cysimdjson does not raise a FileNotFoundError
            if not file.is_file():
                raise FileNotFoundError(file) from exc
        except ValueError as exc:
            raise JsonFileParseError(file_path=file) from exc

    def parse_string(self, value: str) -> Json:
        try:
            return cast(Json, self._parser.parse_string(value))
        except ValueError as exc:
            raise JsonStringParseError(value=value) from exc
