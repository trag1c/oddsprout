from __future__ import annotations

import sys
from pathlib import Path
from typing import TYPE_CHECKING, Any, cast

from dahlia import dprint

from oddsprout.constants import (
    BASE_TYPES,
    BOUNDS_KEYS,
    CATEGORIES,
    CHARSETS,
    TYPES,
    TYPES_KEYS,
)
from oddsprout.exceptions import OddsproutConfigurationError
from oddsprout.generators import Config

if TYPE_CHECKING:
    from os import PathLike

if sys.version_info < (3, 11):
    import tomli as toml
else:
    import tomllib as toml


def _check_unexpected_items(items: set[str], err_msg_nouns: tuple[str, str]) -> None:
    if not items:
        return
    singular, plural = err_msg_nouns
    if len(items) == 1:
        msg = f"invalid {singular} {items.pop()!r}"
    else:
        msg = f"invalid {plural} {', '.join(map(repr, sorted(items)))}"
    raise OddsproutConfigurationError(msg)


def _check_bounds_config(config: dict[str, Any]) -> None:
    _check_unexpected_items(config.keys() - BOUNDS_KEYS, ("key", "keys"))
    for key, value in config.items():
        if key.endswith("-max"):
            if not isinstance(value, int):
                msg = f"expected an integer for {key!r}"
                raise OddsproutConfigurationError(msg)
            # NOTE: Disabling coverage for 'continue' since CPython's peephole optimizer
            # never executes it. See: https://github.com/nedbat/coveragepy/issues/198
            continue  # pragma: no cover
        if f"{key}-max" in config:
            msg = f"can't use {key!r} and '{key}-max' at once"
            raise OddsproutConfigurationError(msg)
        if not (
            isinstance(value, list)
            and len(value) == 2
            and isinstance(value[0], int)
            and isinstance(value[1], int)
        ):
            msg = f"expected a [min, max] array for {key!r}"
            raise OddsproutConfigurationError(msg)
    # TODO(trag1c): check what collection sizes could be too large and drop a warning


def _check_types_config(config: dict[str, Any]) -> None:
    _check_unexpected_items(config.keys() - TYPES_KEYS, ("key", "keys"))

    if not isinstance(charset := config.get("charset", "ascii"), str):
        msg = (
            "expected a string for 'charset' "
            f"(one of {', '.join(map(repr, CHARSETS))})"
        )
        raise OddsproutConfigurationError(msg)
    if charset not in CHARSETS:
        msg = (
            f"invalid charset {charset!r} "
            "(valid options: 'ascii', 'alpha', 'alnum', 'digits')"
        )
        raise OddsproutConfigurationError(msg)

    if (base := config.get("base", "any")) not in BASE_TYPES:
        msg = f"invalid base type {base!r} (valid options: 'any', 'array', 'object')"
        raise OddsproutConfigurationError(msg)

    for key in ("exclude", "include"):
        if (value := config.get(key)) is None:
            continue
        if not (
            isinstance(value, list) and all(isinstance(item, str) for item in value)
        ):  # TODO(trag1c): make a util for this^^^?
            msg = f"expected an array of type names for {key!r}"
            raise OddsproutConfigurationError(msg)
        for item in set(value):
            if item not in TYPES:
                msg = f"invalid type {item!r} in {key!r}"
                raise OddsproutConfigurationError(msg)
            if value.count(item) > 1:
                dprint(
                    f"&eWARNING:&r duplicated type {item!r} in {key!r}", file=sys.stderr
                )

    if set(config) >= {"include", "exclude"}:
        msg = "can't use 'include' and 'exclude' at once"
        raise OddsproutConfigurationError(msg)


def _transform_config(config: dict[str, Any]) -> Config:
    transformed = {}
    for key, value in config.get("bounds", {}).items():
        new_key = (key[:-4] if key.endswith("-max") else key) + "_size"
        transformed[new_key] = (0, value) if key.endswith("-max") else tuple(value)
    types_config = config.get("types", {})
    if included_types := types_config.pop("include", []):
        transformed["types"] = included_types
    if excluded_types := types_config.pop("exclude", []):
        # assuming "include" is not defined based on prior checks
        transformed["types"] = sorted(set(TYPES) - set(excluded_types))
    transformed.update(types_config)
    return cast(Config, transformed)


def load_config(path: PathLike[str] | str) -> Config:
    try:
        config = toml.loads(Path(path).read_text())
    except toml.TOMLDecodeError as e:
        raise OddsproutConfigurationError(str(e)) from None
        # TODO(trag1c): reconsider the above line (maybe add a prefix saying
        # it's a TOML error or maybe just use the original exception)

    found_categories = set(config)
    _check_unexpected_items(found_categories - CATEGORIES, ("category", "categories"))
    if "bounds" in found_categories:
        _check_bounds_config(config["bounds"])
    if "types" in found_categories:
        _check_types_config(config["types"])
    return _transform_config(config)
