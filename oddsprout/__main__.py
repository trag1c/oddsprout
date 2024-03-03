import json
import sys
from argparse import ArgumentParser
from pathlib import Path

from oddsprout.exceptions import OddsproutError
from oddsprout.generators import generate_value

if __name__ == "__main__":
    try:
        parser = ArgumentParser()
        parser.add_argument("--config", type=Path, help="path to configuration file")
        try:
            print(json.dumps(generate_value(initial=True), indent=2))
        except RecursionError:
            print(
                "ERROR: Failed to generate a JSON with the given collection size.",
                file=sys.stderr,
            )
    except OddsproutError as e:
        sys.exit(f"ERROR: {e}")
