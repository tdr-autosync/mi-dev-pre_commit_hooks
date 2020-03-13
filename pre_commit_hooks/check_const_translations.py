import argparse
import ast
from typing import Optional
from typing import Sequence

_REGEX = r"[^\w]_\(\)"


class _CheckTranslationsNodeVisitor(ast.NodeVisitor):
    """
    A NodeVisitor that checks each call to a translation-function. The call
    is expected to have only one constant parameter, no variables nor function
    calls.

    Use the TRANSLATION_FUNCTIONS constants to define which functions are
    checked.
    """

    TRANSLATION_FUNCTIONS = ["_"]

    def __init__(self, filename: str, lines: Sequence[str]):
        self.__filename = filename
        self.__lines = lines
        self.__count = 0

    def visit_Call(self, node: ast.Call):
        if getattr(node.func, "id", None) in self.TRANSLATION_FUNCTIONS:
            args = node.args
            if (
                len(args) != 1
                or not isinstance(args[0], ast.Constant)
                or isinstance(args[0], ast.Str)
                or isinstance(args[0], ast.Bytes)
            ):
                line = self.__lines[node.lineno - 1].lstrip()
                print(f'File "{self.__filename}", line {node.lineno}\n  {line}')
                self.__count += 1
        self.generic_visit(node)

    def report(self) -> int:
        return self.__count


def check_translations(filename: str) -> int:
    """
    :param filename:
    :return:
    Returns the number of failing entries in the given text.
    """
    result = 0
    with open(filename, "r", encoding="UTF-8") as f:
        content = f.read()
        tree = ast.parse(content, filename=filename)

        analyzer = _CheckTranslationsNodeVisitor(filename, content.split("\n"))
        analyzer.visit(tree)
        result += analyzer.report()
    return result


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*")
    args = parser.parse_args(argv)

    result = 0
    for i_filename in args.filenames:
        try:
            result += check_translations(i_filename)
        except SyntaxError:
            print(f'File: "{i_filename}"\n  INVALID SYNTAX.')
            continue
    return result


if __name__ == "__main__":
    exit(main())
