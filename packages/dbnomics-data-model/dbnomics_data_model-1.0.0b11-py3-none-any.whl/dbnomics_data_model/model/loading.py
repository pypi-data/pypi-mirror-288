from collections.abc import Callable
from typing import Any, Protocol, Self, TypeAlias, TypeVar

from typedload.dataloader import Loader
from typedload.exceptions import TypedloadException, TypedloadTypeError

from dbnomics_data_model.json_utils import create_default_loader
from dbnomics_data_model.model import DatasetCode, DatasetId, SeriesCode
from dbnomics_data_model.model.identifiers.errors import DatasetCodeParseError, DatasetIdParseError
from dbnomics_data_model.model.identifiers.series_id import SeriesId
from dbnomics_data_model.model.identifiers.simple_code import SimpleCode

__all__ = ["create_loader"]


def create_loader() -> Loader:
    loader = create_default_loader()

    loader.strconstructed = {SeriesCode, SimpleCode}  # type: ignore[reportAttributeAccessIssue]

    loader.handlers.insert(0, build_handler_for_parsable(DatasetCode))
    loader.handlers.insert(0, build_handler_for_parsable(DatasetId))
    loader.handlers.insert(0, build_handler_for_parsable(SeriesId))

    return loader


class SupportsParse(Protocol):
    @classmethod
    def parse(cls, value: str) -> Self: ...


T = TypeVar("T", bound=SupportsParse)
TypedloadHandler: TypeAlias = tuple[Callable[[type[T]], bool], Callable[[Loader, Any, type[T]], T]]


def build_handler_for_parsable(parsable: type[T]) -> TypedloadHandler[T]:
    return is_type(parsable), load_parsable


def is_type(type1: type) -> Callable[[type], bool]:
    def _is_type(type2: type) -> bool:
        return type1 == type2

    return _is_type


def load_parsable(_loader: Loader, value: Any, type_: type[T]) -> T:
    if not isinstance(value, str):
        msg = f"Expected a str for {type.__name__}"
        raise TypedloadTypeError(msg, type_=type_, value=value)

    try:
        return type_.parse(value)
    except DatasetCodeParseError as exc:
        raise TypedloadException(str(exc), type_=type_, value=value) from exc


def load_dataset_id(_loader: Loader, value: Any, type_: type) -> DatasetId:
    if not isinstance(value, str):
        msg = "Expected a str for DatasetId"
        raise TypedloadTypeError(msg, type_=type_, value=value)

    try:
        return DatasetId.parse(value)
    except DatasetIdParseError as exc:
        raise TypedloadException(str(exc), type_=type_, value=value) from exc
