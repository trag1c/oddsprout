from __future__ import annotations

import sys
from typing import TYPE_CHECKING, Dict, List, Union

from ixia import choice, choices, rand_bool, rand_int, uniform

from oddsprout.configuration import Config, load_config
from oddsprout.constants import CHARSETS

if TYPE_CHECKING:
    from os import PathLike

sys.setrecursionlimit(5_000)

JSONObject = Dict[str, "JSONValue"]
JSONArray = List["JSONValue"]
JSONValue = Union[JSONObject, JSONArray, str, int, float, bool, None]
NoneType = type(None)


class JSONGenerator:
    """A JSON value generator."""

    def __init__(self, config: Config | None = None) -> None:  # allow two-modal input
        if config is None:
            config = Config()

        type_map = {
            "object": self._generate_object,
            "array": self._generate_array,
            "string": self._generate_string,
            "int": _generate_int,
            "float": _generate_float,
            "boolean": rand_bool,
            "null": NoneType,
        }
        types = config.types.copy()
        if "number" in types:
            types.remove("number")
            types.extend(("int", "float"))
        self._type_pool = tuple(type_map[t] for t in types)
        self._weights = tuple(0.05 if t in {"object", "array"} else 1 for t in types)

        self._config = config
        self._string_size = config.string_size
        self._collection_size = config.collection_size
        self._charset = CHARSETS[config.charset]

    @property
    def config(self) -> Config:
        """The config used by the generator."""
        return self._config

    @classmethod
    def from_config(cls, path: PathLike[str] | str) -> JSONGenerator:
        """Create a JSONGenerator instance from a configuration file."""
        return cls(load_config(path))

    def generate_value(self) -> JSONValue:
        """Generate a random JSON value."""
        base = self._config.base
        size = rand_int(*self._config.base_size)
        if base == "any":
            base = choice(("object", "array"))
        return (
            self._generate_object(size)
            if base == "object"
            else self._generate_array(size)
        )

    def _generate_value(self) -> JSONValue:
        return choice(self._type_pool, self._weights)()

    def _generate_string(self) -> str:
        return "".join(choices(self._charset, k=rand_int(*self._string_size)))

    def _generate_object(self, size: int | None = None) -> JSONObject:
        return {
            self._generate_string(): self._generate_value()
            for _ in range(rand_int(*self._collection_size) if size is None else size)
        }

    def _generate_array(self, size: int | None = None) -> JSONArray:
        return [
            self._generate_value()
            for _ in range(rand_int(*self._collection_size) if size is None else size)
        ]


def _generate_int() -> int:
    return rand_int(-1_000_000, 1_000_000)


def _generate_float() -> float:
    return uniform(-1_000_000, 1_000_000)
