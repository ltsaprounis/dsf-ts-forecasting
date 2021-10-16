import pytest
from examplepackage.examplemodule import example_function


@pytest.mark.parametrize("test_input,expected", [(2, 4), (3, 9), (5, 25)])
def test_example_function(test_input, expected):
    assert example_function(test_input) == expected
