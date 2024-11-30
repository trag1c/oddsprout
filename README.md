[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

# oddsprout

Oddsprout is a configurable CLI tool and a Python library for generating random
JSONs with no schemas involved. I developed this tool out of necessity to test a
JSON parser but all solutions I found online involved generating data based on
templates.

See the [documentation] for usage.

## Installation
If you only intend to use it as a CLI tool:
```sh
uvx oddsprout
```

---

Otherwise, install the library from PyPI:
```sh
pip install oddsprout
```
Or from source:
```sh
pip install git+https://github.com/trag1c/oddsprout.git
```

## Contributing

Contributions are welcome!

Please open an issue before submitting a pull request (unless it's a minor
change like fixing a typo).

To get started:
1. Clone your fork of the project.
2. Install the project with [uv]:
```sh
uv sync
```
3. After you're done, use the following [`just`][just] recipes to check your
   changes (or run the commands manually):
```sh
just test      # runs pytest and mypy
just lint      # runs the ruff linter and formatter in check mode
just format    # runs the ruff formatter and isort
just coverage  # checks UT and docstring coverage
```

## License
`oddsprout` is licensed under the [MIT License].  
© [trag1c], 2024

[MIT License]: https://opensource.org/license/mit/
[trag1c]: https://github.com/trag1c/
[documentation]: https://trag1c.github.io/oddsprout
[uv]: https://docs.astral.sh/uv/
[just]: https://github.com/casey/just/
