import re
from pathlib import Path
from unittest.mock import patch

import pytest

from oddsprout import __main__ as main


def test_dexit() -> None:
    with pytest.raises(SystemExit, match=re.escape("\x1b[31mERROR:\x1b[0m message")):
        main._dexit("message")


def test_parse_argv() -> None:
    with patch("sys.argv", ["script", "--config", "config.toml"]):
        assert main._parse_argv() == Path("config.toml")


def test_parse_argv_no_config() -> None:
    with patch("sys.argv", ["script"]):
        assert main._parse_argv() is None


def test_main(tmp_path: Path) -> None:
    (cfg_path := tmp_path / "config.toml").write_text('[types]\ninclude = ["string"]\n')
    with patch("sys.argv", ["script", "--config", str(cfg_path)]):
        main.main()


def test_main_recursion_error(tmp_path: Path) -> None:
    (cfg_path := tmp_path / "config.toml").write_text(
        '[bounds]\ncollection = [10000, 10000]\n\n[types]\ninclude = ["array"]\n'
    )
    with pytest.raises(
        SystemExit,
        match=re.escape(
            "\x1b[31mERROR:\x1b[0m recursion limit reached"
            " while generating JSON value\x1b[0m"
        ),
    ), patch("sys.argv", ["script", "--config", str(cfg_path)]):
        main.main()


def test_main_nonexistent_config(tmp_path: Path) -> None:
    with pytest.raises(
        SystemExit,
        match=(
            r"\x1b\[31mERROR:\x1b\[0m [A-Za-z0-9/_-]+"
            r"nonexistent\.toml does not exist\x1b\[0m"
        ),
    ), patch("sys.argv", ["script", "--config", str(tmp_path / "nonexistent.toml")]):
        main.main()


def test_main_invalid_config(tmp_path: Path) -> None:
    (cfg_path := tmp_path / "config.toml").write_text("invalid")
    with pytest.raises(
        SystemExit,
        match=(
            re.escape(
                "\x1b[31mERROR:\x1b[0m TOMLDecodeError: Expected '=' after a "
                "key in a key/value pair (at end of document)\x1b[0m"
            )
        ),
    ), patch("sys.argv", ["script", "--config", str(cfg_path)]):
        main.main()
