import json
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import NoReturn

from dahlia import dahlia

from oddsprout.configuration import load_config
from oddsprout.exceptions import OddsproutError
from oddsprout.generators import JSONGenerator


def _parse_argv() -> Path:
    parser = ArgumentParser()
    parser.add_argument("--config", type=Path, help="path to configuration file")
    args = parser.parse_args()
    return args.config


def _dexit(message: object) -> NoReturn:
    sys.exit(dahlia(f"&4ERROR:&r {message}"))


def main() -> None:
    config_path = _parse_argv()
    if not (config_path is None or config_path.exists()):
        _dexit(f"{config_path} does not exist")

    try:
        json_gen = JSONGenerator(load_config(config_path))
    except OddsproutError as e:
        _dexit(e)

    try:
        print(json.dumps(json_gen.generate_value(), indent=2))
    except RecursionError:
        _dexit("Failed to generate a JSON with the given collection size.")


if __name__ == "__main__":
    main()
