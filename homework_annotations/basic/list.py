"""
TODO:

foo should accept a list argument,
whose element are string

def foo(x):
    pass


foo(["foo", "bar"])
foo(["foo", 1])   # expect-type-error
"""

def foo(x: list[str]):
    pass


foo(["foo", "bar"])
foo(["foo", 1])   # expect-type-error
