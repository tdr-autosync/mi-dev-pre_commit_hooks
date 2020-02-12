import argparse
import ast
from typing import Optional
from typing import Sequence

_REGEX = r"[^\w]_\(\)"


class _CheckTranslationsNodeVisitor(ast.NodeVisitor):

    TRANSLATION_FUNCTIONS = ["_"]

    def __init__(self, filename: str):
        self._filename = filename
        self._invalid_calls = []

    def visit_Call(self, node):
        if getattr(node.func, "id", None) in self.TRANSLATION_FUNCTIONS:
            if len(node.args) != 1:
                self._invalid_calls.append(node)
            elif not isinstance(node.args[0], ast.Constant):
                self._invalid_calls.append(node)
            else:
                pass  # Valid call.
        self.generic_visit(node)

    def report(self) -> int:
        for i_node in self._invalid_calls:
            msg = "Translation function called with non-constant:"
            print(f"{self._filename}:{i_node.lineno}: {msg}")
        return len(self._invalid_calls)


def check_translations(filename: str) -> int:
    """
    :param filename:
    :return:
    Returns the number of failing entries in the given text.
    """
    result = 0
    with open(filename, "r", encoding="UTF-8") as f:
        tree = ast.parse(f.read(), filename=filename)

        analyzer = _CheckTranslationsNodeVisitor(filename)
        analyzer.visit(tree)
        result += analyzer.report()
    return result


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*")
    args = parser.parse_args(argv)

    result = 0
    for filename in args.filenames:
        result += check_translations(filename)
    return result


if __name__ == "__main__":
    exit(main())
