"""Prevent import of a module in a project."""
import argparse
import ast
import pathlib
import sys
from typing import Optional
from typing import Sequence


NO_LINT_HINT = "no-forbid-import"


def is_import(node: ast.AST) -> bool:
    """Return True if node is an import statement."""
    return isinstance(node, ast.ImportFrom) or isinstance(node, ast.Import)


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("module")
    parser.add_argument("help")
    parser.add_argument("files", nargs="*")
    args = parser.parse_args(argv)

    module_name = args.module
    files_to_check = args.files
    help_message = args.help

    if not files_to_check:
        print("Provide at least one file or exactly one directory to check.")
        sys.exit(2)

    # If provided directory, get all python files in it
    if pathlib.Path(files_to_check[0]).is_dir():
        python_files = list(pathlib.Path(files_to_check[0]).glob("**/*.py"))
    else:
        # Only Python files
        python_files = [
            pathlib.Path(file) for file in files_to_check if file.endswith(".py")
        ]

    if help_message != "":
        help_message = f"({help_message})"

    result = 0
    for file_to_check in python_files:
        with open(file_to_check) as f:
            tree = ast.parse(f.read())
            f.seek(0)
            lines = f.readlines()
            import_nodes = [node for node in ast.walk(tree) if is_import(node)]
            for node in import_nodes:
                line = node.lineno
                if NO_LINT_HINT in lines[line - 1]:
                    continue
                msg = f"{file_to_check}:{line}: {module_name} import is forbidden {help_message}"
                if isinstance(node, ast.ImportFrom) and node.module == module_name:
                    print(msg)
                    result = 1
                if isinstance(node, ast.Import) and module_name in [
                    a.name for a in node.names
                ]:
                    print(msg)
                    result = 1

    return result
