from pathlib import Path

from pytest import fixture


@fixture
def grammar_path():
    return Path(Path.cwd(), "src", "wrapper", "assets", "grammar.lark")
