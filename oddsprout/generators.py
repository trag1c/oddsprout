from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import Dict, List, Literal, Union

from ixia import choice, choices, rand_bool, rand_int, uniform

from oddsprout.constants import CHARSETS

sys.setrecursionlimit(5_000)

JSONObject = Dict[str, "JSONValue"]
JSONArray = List["JSONValue"]
JSONValue = Union[JSONObject, JSONArray, str, int, float, bool, None]
NoneType = type(None)


@dataclass
class Config:
    types: list[str]
    base_size: tuple[int, int] = (0, 100)
    string_size: tuple[int, int] = (0, 50)
    collection_size: tuple[int, int] = (0, 100)
    charset: Literal["ascii", "alpha", "alnum", "digits"] = "ascii"
    base: Literal["any", "array", "object"] = "any"


class JSONGenerator:
    def __init__(self, config: Config) -> None:
        type_map = {
            "object": self._generate_object,
            "array": self._generate_array,
            "string": self._generate_string,
            "int": _generate_int,
            "float": _generate_float,
            "boolean": rand_bool,
            "null": NoneType,
        }
        types = config.types

        self._config = config
        self._string_size = config.string_size
        self._collection_size = config.collection_size
        self._type_pool = tuple(type_map[t] for t in types)
        self._weights = tuple(0.05 if t in {"object", "array"} else 1 for t in types)
        self._charset = CHARSETS[config.charset]

    def generate_value(self) -> JSONValue:
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
            for _ in range(size or rand_int(*self._collection_size))
        }

    def _generate_array(self, size: int | None = None) -> JSONArray:
        return [
            self._generate_value()
            for _ in range(size or rand_int(*self._collection_size))
        ]


def _generate_int() -> int:
    return rand_int(-1_000_000, 1_000_000)


def _generate_float() -> float:
    return uniform(-1_000_000, 1_000_000)
