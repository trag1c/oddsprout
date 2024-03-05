from __future__ import annotations

from typing import Any, Dict, List, Tuple

import pytest

from oddsprout.utils import matches_type


@pytest.mark.parametrize(
    ("value", "type_", "expected"),
    [
        (1, int, True),
        (1, str, False),
        ([], List[str], True),
        ([1], List[int], True),
        ((1, 2), Tuple[int, int], True),
        ([1, 2, 3], List[int], True),
        (["a", "b", "c"], List[str], True),
        (["a", "b", "c"], List[int], False),
        (("a", 2, "c"), Tuple[str, int, str], True),
        (["a", 2, "c"], Tuple[str, int, str], False),
        (("a", "2", "c"), Tuple[str, int, str], False),
        ({"a": 1, "b": 2, "c": 3}, Dict[str, int], True),
        ({"a": 1, "b": "2", "c": 3}, Dict[str, int], False),
        ({"a": 1, "b": 2, "c": 3}, Dict[str, str], False),
    ],
)
def test_matches_type(value: object, type_: type[Any], expected: bool) -> None:
    assert matches_type(value, type_) == expected
