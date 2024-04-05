from pathlib import Path
from typing import Literal

import pytest

from oddsprout.configuration import Config
from oddsprout.generators import JSONGenerator


@pytest.mark.parametrize("base_type", ["array", "object", "any"])
def test_json_generator(base_type: Literal["array", "object", "any"]) -> None:
    gen = JSONGenerator(Config(base=base_type))
    gen.generate_value()


def test_json_generator_no_config() -> None:
    JSONGenerator()


def test_json_generator_from_file(tmp_path: Path) -> None:
    path = tmp_path / "oddsprout.toml"
    path.write_text(
        """
        [bounds]
        base-max = 17
        """
    )
    gen = JSONGenerator.from_config_file(path)
    assert gen.config.base_size == (0, 17)
