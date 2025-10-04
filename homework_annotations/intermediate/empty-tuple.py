"""
TODO:

foo should accept a empty tuple argument.


def foo(x):
    pass

foo(())
foo((1,))  # expect-type-error
"""


def foo(x: tuple[()]) -> None:
    pass
