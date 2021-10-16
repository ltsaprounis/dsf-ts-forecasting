"""A module that fails the tests"""

long_string = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"


def bad_function(a: int) -> int:
    """Return input + 2

    Parameters
    ----------
    a : int
        input integer

    Returns
    -------
    int
        input + 2
    """
    return a + 2
