"""
TODO:

The function `add` accepts two arguments and returns a value, they all have the same type.


def add(a, b):
    ...

from typing import List, assert_type

assert_type(add(1, 2), int)
assert_type(add("1", "2"), str)
assert_type(add(["1"], ["2"]), List[str])
assert_type(add(1, "2"), int)  # expect-type-error
"""

from typing import TypeVar

T = TypeVar("T")


def add[T](a: T, b: T) -> T: return a
