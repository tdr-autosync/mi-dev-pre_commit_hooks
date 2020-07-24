import argparse
import ast
from typing import Optional
from typing import Sequence

_REGEX = r"[^\w]_\(\)"


class _CheckEnumComparisonsVisitor(ast.NodeVisitor):
    """
    """

    def __init__(self, filename: str, lines: Sequence[str]):
        self.__filename = filename
        self.__lines = lines
        self.__count = 0

    def visit_BinOp(self, node):
        self.generic_visit(node)
        print("*" * 80)
        print(type(node.op).__name__)
        print("*" * 80)

    # def visit_BinOp(self, node):
    #     self.generic_visit(node)
    #     1/0
    #     if isinstance(right.args[0], ast.Integer):
    #         line = self.__lines[right.lineno - 1].lstrip()
    #         print(f'File "{self.__filename}", line {right.lineno}\n  {line}')
    #         self.__count += 1
    #     self.generic_visit(left, operator, right)

    def report(self) -> int:
        return self.__count


def check_enum_conparisons(filename: str) -> int:
    """
    :param filename:
    :return:
    Returns the number of failing entries in the given text.
    """
    result = 0
    with open(filename, "r", encoding="UTF-8") as f:
        content = f.read()
        tree = ast.parse(content, filename=filename)
        analyzer = _CheckEnumComparisonsVisitor(filename, content.split("\n"))
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
            result += check_enum_conparisons(i_filename)
        except SyntaxError:
            print(f'File: "{i_filename}"\n  INVALID SYNTAX.')
            continue
    return result


if __name__ == "__main__":
    exit(main())
