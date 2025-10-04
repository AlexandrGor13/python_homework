"""
TODO:

'foo' takes keyword arguments of
type integer or string.

def foo(**kwargs):
    ...


foo(a=1, b="2")
foo(a=[1])   # expect-type-error
"""

def foo(**kwargs: int | str):
    ...


foo(a=1, b="2")
foo(a=[1])   # expect-type-error
