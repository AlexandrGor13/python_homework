"""
TODO:

Create a new type called Vector,
which is a list of float.

def foo(v: Vector):
    ...


foo([1.1, 2])

foo(1)  # expect-type-error
foo(["1"])  # expect-type-error
"""

from typing import TypeAlias

Vector: TypeAlias = list[float]

def foo(v: Vector):
    ...


foo([1.1, 2])

foo(1)  # expect-type-error
foo(["1"])  # expect-type-error
