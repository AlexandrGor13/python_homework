"""
TODO:

Make sure 'my_list' cannot be
reassigned to.

my_list = []

my_list.append(1)
my_list = []   # expect-type-error
my_list = "something else"   # expect-type-error
"""

from typing import Final

my_list: Final[list] = []


my_list.append(1)
my_list = []   # expect-type-error
my_list = "something else"   # expect-type-error
