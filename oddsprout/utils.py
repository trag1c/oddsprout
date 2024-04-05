from __future__ import annotations

from itertools import starmap
from typing import TYPE_CHECKING, Any, cast, get_args, get_origin

if TYPE_CHECKING:
    from collections.abc import Collection


def matches_type(value: object, type_: Any) -> bool:
    """
    Check if a value matches a given type.
    Made for recursive type checking.

    Examples:
    * `matches_type(1, int) -> True`
    * `matches_type([1, 2, 3], List[int]) -> True`
    * `matches_type([1, 2, '3'], List[int]) -> False`
    * `matches_type({'a': 1, 'b': 2}, Dict[str, int]) -> True`
    """
    if (origin := get_origin(type_)) is None:
        return isinstance(value, type_)
    if not isinstance(value, origin):
        return False
    if not (args := get_args(type_)):
        return True
    if origin is dict:
        key_type, value_type = args
        value = cast("dict[Any, Any]", value)
        return all(
            matches_type(key, key_type) and matches_type(value, value_type)
            for key, value in value.items()
        )
    value = cast("Collection[Any]", value)
    if len(args) == 1:
        return all(matches_type(item, args[0]) for item in value)
    if len(args) != len(value):
        return False
    return all(starmap(matches_type, zip(value, args)))
