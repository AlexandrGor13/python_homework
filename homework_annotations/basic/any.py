"""
TODO:

Modify 'foo' so it takes an argument
of arbitrary type.

def foo():
    pass

foo(1)
foo("10")
foo(1, 2)   # expect-type-error
"""

from typing import Any

def foo(_: Any):
    pass


foo(1)
foo("10")
foo(1, 2)   # expect-type-error
