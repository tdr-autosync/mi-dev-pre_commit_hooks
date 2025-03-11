from pre_commit_hooks.forbid_import import main


def test_plain_import_forbidden(datadir):
    result = main(["logging", "-", str(datadir / "plain_import.py")])
    assert result == 1


def test_plain_import_allowed(datadir):
    result = main(["somemodule", "-", str(datadir / "plain_import.py")])
    assert result == 0


def test_qualified_import_forbidden(datadir):
    result = main(["logging", "-", str(datadir / "qualified_import.py")])
    assert result == 1


def test_qualified_import_allowed(datadir):
    result = main(["somemodule", "-", str(datadir / "qualified_import.py")])
    assert result == 0


def test_multi_import_forbidden(datadir):
    result = main(["logging", "-", str(datadir / "multi_import.py")])
    assert result == 1


def test_multi_import_allowed(datadir):
    result = main(["somemodule", "-", str(datadir / "multi_import.py")])
    assert result == 0


def test_multi_qualified_import_forbidden(datadir):
    result = main(["logging", "-", str(datadir / "multi_qualified_import.py")])
    assert result == 1


def test_multi_qualified_import_allowed(datadir):
    result = main(["somemodule", "-", str(datadir / "multi_qualified_import.py")])
    assert result == 0
