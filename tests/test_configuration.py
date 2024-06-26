from __future__ import annotations

import re
from typing import TYPE_CHECKING, Any

import pytest

from oddsprout.configuration import (
    Config,
    _check_bounds_config,
    _check_types_config,
    _check_unexpected_items,
    _transform_config,
    load_config,
)
from oddsprout.exceptions import OddsproutConfigurationError, OddsproutValueError

if TYPE_CHECKING:
    from pathlib import Path


def test_invalid_syntax_toml(tmp_path: Path) -> None:
    path = tmp_path / "invalid_syntax.toml"
    path.write_text("[invalid")

    with pytest.raises(OddsproutConfigurationError):
        load_config(path)


@pytest.mark.parametrize(
    ("items", "nouns", "err_msg"),
    [
        ({"unexpected"}, ("item", "items"), "invalid item 'unexpected'"),
        (
            {"unexpected", "other"},
            ("item", "items"),
            "invalid items 'other', 'unexpected'",
        ),
        (
            {"unexpected", "other", "another"},
            ("value", "values"),
            "invalid values 'another', 'other', 'unexpected'",
        ),
    ],
)
def test_unexpected_items(
    items: set[str], nouns: tuple[str, str], err_msg: str
) -> None:
    with pytest.raises(OddsproutConfigurationError, match=err_msg):
        _check_unexpected_items(items, nouns)


def test_no_unexpected_items() -> None:
    _check_unexpected_items(set(), ("", ""))


@pytest.mark.parametrize(
    ("config", "err_msg"),
    [
        ({"invalid": 1}, "invalid key 'invalid'"),
        ({"base": "invalid"}, "expected a [min, max] array for 'base'"),
        ({"base-max": "invalid"}, "expected an integer for 'base-max'"),
        ({"string": [1, "invalid"]}, "expected a [min, max] array for 'string'"),
        ({"collection": [1, 2, 3]}, "expected a [min, max] array for 'collection'"),
        ({"base": [1, 2], "base-max": 1}, "can't use 'base' and 'base-max' at once"),
    ],
)
def test_check_bounds_config_fail(config: dict[str, Any], err_msg: str) -> None:
    with pytest.raises(OddsproutConfigurationError, match=re.escape(err_msg)):
        _check_bounds_config(config)


def test_check_bounds_config_pass() -> None:
    _check_bounds_config(
        {
            "string": [1, 2],
            "collection": [1, 2],
            "base-max": 1,
        }
    )


@pytest.mark.parametrize(
    ("config", "err_msg"),
    [
        ({"invalid": 1}, "invalid key 'invalid'"),
        ({"charset": 1}, "expected a string for 'charset'"),
        ({"charset": "invalid"}, "invalid charset 'invalid'"),
        ({"base": "invalid"}, "invalid base type 'invalid'"),
        ({"exclude": 1}, "expected an array of type names for 'exclude'"),
        ({"exclude": ["invalid"]}, "invalid type 'invalid' in 'exclude'"),
        ({"include": 1}, "expected an array of type names for 'include'"),
        ({"include": ["invalid"]}, "invalid type 'invalid' in 'include'"),
        ({"include": [], "exclude": []}, "can't use 'include' and 'exclude' at once"),
    ],
)
def test_check_types_config_fail(config: dict[str, Any], err_msg: str) -> None:
    with pytest.raises(OddsproutConfigurationError, match=re.escape(err_msg)):
        _check_types_config(config)


def test_check_types_config_pass() -> None:
    _check_types_config(
        {
            "charset": "ascii",
            "base": "any",
            "exclude": ["string"],
        }
    )


@pytest.mark.parametrize(
    ("config", "transformed"),
    [
        (
            {"bounds": {"base": [1, 2]}},
            Config(base_size=(1, 2)),
        ),
        (
            {"bounds": {"base": [1, 2], "string-max": 10}},
            Config(base_size=(1, 2), string_size=(0, 10)),
        ),
    ],
)
def test_transform_config(config: dict[str, Any], transformed: Config) -> None:
    assert _transform_config(config) == transformed


@pytest.mark.parametrize(
    ("input_types", "expected_types"),
    [
        (
            'exclude = ["string", "array", "null"]',
            ("boolean", "float", "int", "number", "object"),
        ),
        ('include = ["boolean", "int", "float"]', ("boolean", "float", "int")),
    ],
)
def test_load_config_pass(
    tmp_path: Path, input_types: str, expected_types: tuple[str, ...]
) -> None:
    path = tmp_path / "config.toml"
    path.write_text(
        f"""
        [bounds]
        base = [1, 2]
        string-max = 10

        [types]
        charset = "ascii"
        {input_types}
        """
    )

    assert load_config(path) == Config(
        base_size=(1, 2),
        string_size=(0, 10),
        charset="ascii",
        types=expected_types,
    )


def test_load_config_no_file() -> None:
    assert load_config(None) == Config()


def test_config_empty_types() -> None:
    with pytest.raises(OddsproutValueError, match="'types' can't be empty"):
        Config(types=())


def test_config_from_file(tmp_path: Path) -> None:
    path = tmp_path / "oddsprout.toml"
    path.write_text(
        """
        [bounds]
        base-max = 17
        """
    )
    gen = Config.from_file(path)
    assert gen.base_size == (0, 17)


def test_config_size_incorrect_type() -> None:
    with pytest.raises(
        OddsproutValueError,
        match=re.escape("expected a (min, max) tuple for 'base_size'"),
    ):
        Config(base_size=1)  # type: ignore[arg-type]


def test_config_size_max_less_than_min() -> None:
    with pytest.raises(
        OddsproutValueError,
        match="max can't be less than min for 'base_size'",
    ):
        Config(base_size=(1, 0))


def test_config_invalid_base() -> None:
    with pytest.raises(
        OddsproutValueError,
        match="invalid base type 'invalid'",
    ):
        Config(base="invalid")  # type: ignore[arg-type]


def test_config_invalid_charset() -> None:
    with pytest.raises(
        OddsproutValueError,
        match="invalid charset 'invalid'",
    ):
        Config(charset="invalid")  # type: ignore[arg-type]


def test_config_types_invalid() -> None:
    with pytest.raises(
        OddsproutValueError,
        match="invalid types: 'invalid'",
    ):
        Config(types=("invalid", "int"))
