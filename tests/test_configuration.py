from __future__ import annotations

import re
from typing import TYPE_CHECKING, Any

import pytest
from dahlia import dahlia

from oddsprout.configuration import (
    OddsproutConfigurationError,
    _check_bounds_config,
    _check_types_config,
    _check_unexpected_items,
    load_config,
)

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
        ({"include": [], "exclude": []}, "can't use 'include' and 'exclude' at once")
    ],
)
def test_check_types_config_fail(config: dict[str, Any], err_msg: str) -> None:
    with pytest.raises(OddsproutConfigurationError, match=re.escape(err_msg)):
        _check_types_config(config)


def test_check_types_config_duplicate(capsys: pytest.CaptureFixture[str]) -> None:
    _check_types_config({"exclude": ["string", "string"]})
    _out, err = capsys.readouterr()
    assert err == dahlia("&eWARNING:&r duplicated type 'string' in 'exclude'") + "\n"


def test_check_types_config_pass() -> None:
    _check_types_config(
        {
            "charset": "ascii",
            "base": "any",
            "exclude": ["string"],
        }
    )
