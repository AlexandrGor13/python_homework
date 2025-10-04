"""
TODO:

foo should accept a argument that's
either a string or integer.

def foo(x):
    pass


foo("foo")
foo(1)

foo([])  # expect-type-error
"""


def foo(x: str | int) -> None:
    pass
