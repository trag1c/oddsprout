from __future__ import annotations

import json
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import TYPE_CHECKING, cast

from dahlia import dahlia

from oddsprout.configuration import load_config
from oddsprout.exceptions import OddsproutError
from oddsprout.generators import JSONGenerator

if TYPE_CHECKING:
    from typing_extensions import Never


def _parse_argv() -> Path | None:
    parser = ArgumentParser()
    parser.add_argument("--config", type=Path, help="path to configuration file")
    args = parser.parse_args()
    return cast("Path | None", args.config)


def _dexit(message: object) -> Never:
    sys.exit(dahlia(f"&4ERROR:&r {message}"))


def main() -> None:
    config_path = _parse_argv()
    if not (config_path is None or config_path.exists()):
        _dexit(f"{config_path} does not exist")

    try:
        json_gen = JSONGenerator(load_config(config_path))
        print(json.dumps(json_gen.generate_value(), indent=2))
    except OddsproutError as e:
        _dexit(e)


if __name__ == "__main__":
    main()
