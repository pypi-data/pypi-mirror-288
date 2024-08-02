from pathlib import Path
from typing import Any, TypeVar

from typedload.dataloader import Loader
from typedload.exceptions import TypedloadException

from dbnomics_data_model.json_utils.parsing import JsonParser

from .errors import JsonParseTypeError

__all__ = ["create_default_loader", "load_json_data", "load_json_file"]

T = TypeVar("T")


def create_default_loader() -> Loader:
    return Loader(
        basiccast=False,
        dictequivalence=False,  # for compatibility with cysimdjson.JSONObject
    )


default_loader = create_default_loader()


def load_json_data(data: Any, *, loader: Loader | None = None, type_: type[T]) -> T:
    if loader is None:
        loader = default_loader

    try:
        return loader.load(data, type_=type_)
    except TypedloadException as exc:
        raise JsonParseTypeError(data=data, expected_type=type_) from exc


def load_json_file(file: Path, *, loader: Loader | None = None, type_: type[T]) -> T:
    if loader is None:
        loader = default_loader

    parser = JsonParser.create()
    data = parser.parse_file(file)
    return load_json_data(data, loader=loader, type_=type_)
