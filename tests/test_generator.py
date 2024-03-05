from typing import Literal

import pytest

from oddsprout.generators import Config, JSONGenerator


@pytest.mark.parametrize(
    "base_type",
    ["array", "object", "any"]
)
def test_json_generator(base_type: Literal["array", "object", "any"]) -> None:
    gen = JSONGenerator(Config(base=base_type))
    gen.generate_value()
