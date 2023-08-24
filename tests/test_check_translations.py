from pre_commit_hooks.check_const_translations import main


def test_passing_file(datadir):
    result = main([str(datadir / "test_passing.notpy")])
    assert result == 0


def test_invalid_variable(datadir):
    result = main([str(datadir / "invalid_variable.notpy")])
    assert result == 1


def test_invalid_month(datadir):
    result = main([str(datadir / "invalid_month.notpy")])
    assert result == 1


def test_tierless_base(datadir):
    result = main([str(datadir / "test_tieless_base.notpy")])
    assert result == 1
