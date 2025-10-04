"""
TODO:

foo only accepts literal 'left' and 'right' as its argument.

def foo(direction):
    ...

foo("left")
foo("right")

a = "".join(["l", "e", "f", "t"])
foo(a)  # expect-type-error
"""

from typing import Literal

L = Literal["left", "right"]


def foo(direction: L): ...
