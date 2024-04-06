from typing import Literal

import pytest

from oddsprout.configuration import Config
from oddsprout.generators import JSONGenerator, _generate_float, _generate_int


@pytest.mark.parametrize("base_type", ["array", "object", "any"])
def test_json_generator(base_type: Literal["array", "object", "any"]) -> None:
    gen = JSONGenerator(Config(base=base_type))
    gen.generate_value()


def test_json_generator_number_alias() -> None:
    gen = JSONGenerator(Config(types=("number",)))

    assert set(gen._type_pool) & {_generate_int, _generate_float}


def test_json_generator_repr() -> None:
    gen = JSONGenerator()
    cfg = gen.config

    assert repr(gen) == f"JSONGenerator(config={cfg})"


def test_json_generator_recursion_error() -> None:
    gen = JSONGenerator(Config(base="object", collection_size=(500, 1000)))
    with pytest.raises(RecursionError):
        gen.generate_value()
