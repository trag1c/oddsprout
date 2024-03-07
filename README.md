# oddsprout

Oddsprout is a configurable CLI tool and a Python library for generating random JSONs
with no schemas involved. I made it because I needed to generate some JSONs but all
solutions I found online involved generating data based on templates.

See the [documentation] for usage.

## Installation
If you only intend to use it as a CLI tool:
```sh
pipx install oddsprout
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

Please open an issue before submitting a pull request (unless it's a minor change like
fixing a typo).

To get started:
1. Clone your fork of the project.
2. Set up the project with [just] (amake sure you have [poetry] installed):
```sh
just install
```

> [!Note]
> If you don't want to install `just`, simply look up the recipes
> in the project's `justfile`.

3. After you're done, use the following `just` recipes to check your changes:
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
