from pre_commit_hooks.check_enum_comparisons import main


def test_passing_file(datadir):
    result = main([str(datadir / "test_passing.notpy")])
    assert result == 0


def test_failing_file(datadir):
    result = main([str(datadir / "test_failing.notpy")])
    assert result == 1
