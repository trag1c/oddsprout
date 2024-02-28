from __future__ import annotations

import sys
from pathlib import Path
from typing import TYPE_CHECKING, Any

from oddsprout.exceptions import OddsproutConfigurationError
from oddsprout.generators import CHARSETS

if TYPE_CHECKING:
    from os import PathLike

if sys.version_info < (3, 11):
    from tomli import TOMLDecodeError, loads
else:
    from tomllib import TOMLDecodeError, loads


# TODO(trag1c): consider exporting these constants to a separate module
TYPES = frozenset(
    ("int", "float", "number", "string", "boolean", "null", "array", "object")
)
BASE_TYPES = frozenset(("any", "array", "object"))
CATEGORIES = frozenset(("bounds", "types"))
TYPES_KEYS = frozenset(("charset", "base", "exclude", "include"))
BOUNDS_KEYS = frozenset(
    ("collection", "collection-max", "base", "base-max", "string", "string-max")
)


def _check_unexpected_items(items: set[str], err_msg_nouns: tuple[str, str]) -> None:
    if not items:
        return
    singular, plural = err_msg_nouns
    if len(items) == 1:
        msg = f"invalid {singular} {items.pop()!r}"
    else:
        msg = f"invalid {plural} {', '.join(map(repr, items))}"
    raise OddsproutConfigurationError(msg)


"""[bounds]
base = [10, 100]
string = [10, 50]
collection = [5, 10]
base-max = 100
string-max = 50
collection-max = 10"""


def _check_bounds_config(config: dict[str, Any]) -> None:
    _check_unexpected_items(config.keys() - BOUNDS_KEYS, ("key", "keys"))
    for key, value in config.items():
        msg = ""
        if key.endswith("-max"):
            if not isinstance(value, int):
                msg = f"expected an integer for {key!r}"
            # TODO(trag1c): add a continue here?
        else:
            if f"{key}-max" in config:
                msg = f"can't use {key!r} and '{key}-max' at once"
            if not (
                isinstance(value, list)
                and len(value) == 2
                and isinstance(value[0], int)
                and isinstance(value[1], int)
            ):
                msg = f"expected a [min, max] array for {key}"
        if msg:
            raise OddsproutConfigurationError(msg)


def _check_types_config(config: dict[str, Any]) -> None:
    _check_unexpected_items(config.keys() - TYPES_KEYS, ("key", "keys"))

    # TODO(trag1c): fix this (will cause a TypeError if someone makes charset a list)
    if (charset := config["charset"]) not in CHARSETS:
        msg = (
            f"invalid charset {charset!r} "
            "(valid options: 'ascii', 'alpha', 'alnum', 'digits')"
        )
        raise OddsproutConfigurationError(msg)

    if (base := config["base"]) not in BASE_TYPES:
        msg = f"invalid base type {base!r} (valid options: 'any', 'array', 'object')"
        raise OddsproutConfigurationError(msg)

    for key in ("exclude", "include"):
        value = config[key]
        if not (
            isinstance(value, list) and all(isinstance(item, str) for item in value)
        ):  # TODO(trag1c): make a util for this^^^?
            msg = f"expected an array of type names for {key!r}"
            raise OddsproutConfigurationError(msg)
        for item in value:
            if item not in TYPES:
                msg = f"invalid type {item!r} in {key!r}"
                raise OddsproutConfigurationError(msg)

    if conflicting_types := set(config["exclude"]) & set(config["include"]):
        template = "can't include and exclude type{} at once"
        if len(conflicting_types) == 1:
            msg = template.format(f" {conflicting_types.pop()!r}")
        else:
            msg = template.format("s " + ", ".join(map(repr, conflicting_types)))
        raise OddsproutConfigurationError(msg)


def load_config(path: PathLike[str] | str) -> dict[str, int]:
    try:
        config = loads(Path(path).read_text())
    except TOMLDecodeError as e:
        raise OddsproutConfigurationError(str(e)) from None
        # TODO(trag1c): reconsider the above line (maybe add a prefix saying
        # it's a TOML error or maybe just use the original exception)

    found_categories = set(config)
    _check_unexpected_items(found_categories - CATEGORIES, ("category", "categories"))
    if "bounds" in found_categories:
        _check_bounds_config(config["bounds"])
    if "types" in found_categories:
        _check_types_config(config["types"])
    return config


if __name__ == "__main__":
    load_config("../oddsprout.toml")
