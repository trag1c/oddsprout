from __future__ import annotations

import string
import sys
from typing import Dict, List, Union

from ixia import choice, choices, rand_bool, rand_int, uniform

sys.setrecursionlimit(5_000)

JSONObject = Dict[str, "JSONValue"]
JSONArray = List["JSONValue"]
JSONValue = Union[JSONObject, JSONArray, str, int, float, bool, None]
NoneType = type(None)

CHARSETS = {
    "ascii": "".join(map(chr, range(128))),
    "alpha": string.ascii_letters,
    "alnum": string.ascii_letters + string.digits,
    "digits": string.digits,
}

config = {
    "base_size": 100,
    "base_type": "any",
    "string_size": 50,
    "collection_size": 10,
    "charset": "ascii",
}

# TODO(trag1c): refactor this to use a class


def generate_string() -> str:
    return "".join(
        choices(CHARSETS[config["charset"]], k=rand_int(0, config["string_size"]))
    )


def generate_int() -> int:
    return rand_int(-1_000_000, 1_000_000)


def generate_float() -> float:
    return uniform(-1_000_000, 1_000_000)


def generate_object(size: int | None = None) -> JSONObject:
    return {
        generate_string(): generate_value()
        for _ in range(size or rand_int(0, config["collection_size"]))
    }


def generate_array(size: int | None = None) -> JSONArray:
    return [
        generate_value() for _ in range(size or rand_int(0, config["collection_size"]))
    ]


TYPE_POOL = (
    generate_int,
    generate_float,
    rand_bool,
    generate_string,
    generate_object,
    generate_array,
    NoneType,
)
CONTAINER_TYPE_POOL = (generate_object, generate_array)
TYPE_POOL_WEIGHTS = (1, 1, 1, 1, 0.05, 0.05, 1)


def generate_value(*, initial: bool = False) -> JSONValue:
    if not initial:
        return choice(TYPE_POOL, TYPE_POOL_WEIGHTS)()
    size = rand_int(0, config["base_size"])
    if config["base_type"] == "any":
        config["base_type"] = choice(("object", "array"))
    return (
        generate_object(size)
        if config["base_type"] == "object"
        else generate_array(size)
    )
