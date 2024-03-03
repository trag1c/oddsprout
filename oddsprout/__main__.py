import json
import sys
from argparse import ArgumentParser
from pathlib import Path

from dahlia import dahlia, dprint

from oddsprout.configuration import load_config
from oddsprout.exceptions import OddsproutError
from oddsprout.generators import config, generate_value

if __name__ == "__main__":
    try:
        parser = ArgumentParser()
        parser.add_argument("--config", type=Path, help="path to configuration file")
        args = parser.parse_args()
        config.update(load_config(args.config))
        try:
            print(json.dumps(generate_value(initial=True), indent=2))
        except RecursionError:
            dprint(
                "&4ERROR:&r Failed to generate a JSON with the given collection size.",
                file=sys.stderr,
            )
    except OddsproutError as e:
        sys.exit(dahlia(f"&4ERROR:&r {e}"))
