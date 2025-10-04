"""
TODO:

The function `add` accepts two arguments and returns a value, they all have the same type.
The type can only be str or int.

def add(a, b):
    ...


from typing import assert_type

assert_type(add(1, 2), int)
assert_type(add("1", "2"), str)

add(["1"], ["2"])  # expect-type-error
add("1", 2)  # expect-type-error
"""

from typing import TypeVar

T = TypeVar("T", str, int)


def add(a: T, b: T) -> T: return a + b
