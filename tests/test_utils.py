from __future__ import annotations

from typing import Any

import pytest

from oddsprout.utils import matches_type


@pytest.mark.parametrize(
    ("value", "type_", "expected"),
    [
        (1, int, True),
        (1, str, False),
        ([], list[str], True),
        ([1], list[int], True),
        ((1, 2), tuple[int, int], True),
        ([1, 2, 3], list[int], True),
        (["a", "b", "c"], list[str], True),
        (["a", "b", "c"], list[int], False),
        (("a", 2, "c"), tuple[str, int, str], True),
        (["a", 2, "c"], tuple[str, int, str], False),
        (("a", "2", "c"), tuple[str, int, str], False),
        ({"a": 1, "b": 2, "c": 3}, dict[str, int], True),
        ({"a": 1, "b": "2", "c": 3}, dict[str, int], False),
        ({"a": 1, "b": 2, "c": 3}, dict[str, str], False),
        ([1], list, True),
        ({1: 2}, dict, True),
    ],
)
def test_matches_type(value: object, type_: type[Any], expected: bool) -> None:
    assert matches_type(value, type_) == expected
