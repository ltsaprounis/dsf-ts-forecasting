from examplepackage.badmodule import bad_function


def test_bad_function():
    assert bad_function(1) == 1
